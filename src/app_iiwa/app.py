#!/usr/bin/env python
# coding: utf-8

"""
App IIWA - Aplicación Unificada para Procesamiento de Padrones
Combina las funcionalidades de CAJA y CAMPO en una sola interfaz
"""

import os
import sys
import re
import queue
import threading
import platform
import subprocess
from pathlib import Path
from datetime import datetime
from tempfile import NamedTemporaryFile
import warnings

warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# ====================================
# UTILIDADES COMUNES
# ====================================


def get_desktop_dir() -> Path:
    """Obtiene la ruta del escritorio independiente del SO"""
    system = platform.system()
    home = Path.home()

    if system == "Windows":
        try:
            from ctypes import windll, wintypes, create_unicode_buffer

            CSIDL_DESKTOPDIRECTORY = 0x10
            SHGFP_TYPE_CURRENT = 0
            buf = create_unicode_buffer(wintypes.MAX_PATH)
            windll.shell32.SHGetFolderPathW(
                None, CSIDL_DESKTOPDIRECTORY, None, SHGFP_TYPE_CURRENT, buf
            )
            p = Path(buf.value)
            if p.exists():
                return p
        except Exception:
            pass
        return home / "Desktop"

    if system == "Darwin":
        return home / "Desktop"

    # Linux / Unix
    try:
        out = subprocess.run(
            ["xdg-user-dir", "DESKTOP"], capture_output=True, text=True, check=True
        )
        p = Path(out.stdout.strip())
        if str(p) and p.exists():
            return p
    except Exception:
        pass

    cfg = home / ".config" / "user-dirs.dirs"
    if cfg.exists():
        try:
            txt = cfg.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r'XDG_DESKTOP_DIR="?(.+?)\"?$', txt, re.M)
            if m:
                path = m.group(1).replace("$HOME", str(home))
                p = Path(path)
                if p.exists():
                    return p
        except Exception:
            pass

    return home / "Desktop"


def ensure_dirs(*dirs):
    """Crea directorios si no existen"""
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)


def open_folder(path):
    """Abre una carpeta en el explorador del sistema"""
    system = platform.system()
    try:
        if system == "Darwin":
            os.system(f'open "{path}"')
        elif system == "Windows":
            os.system(f'explorer "{path}"')
        else:
            os.system(f'xdg-open "{path}"')
    except Exception as e:
        print(f"Error abriendo carpeta: {e}")


# ====================================
# FUNCIONES DE PROCESAMIENTO CAMPO
# ====================================


def exportar_resumenes_en_grid(
    df_cps: dict,
    ruta_salida: str,
    hoja="ResumenCPs",
    por_fila=4,
    pad_filas=2,
    pad_cols=2,
):
    """Exporta resúmenes de CPs en formato grid"""

    def _key(cp):
        s = str(cp)
        return (0, int(s)) if s.isdigit() else (1, s)

    items = sorted(df_cps.items(), key=lambda kv: _key(kv[0]))

    block_widths = {cp: df.shape[1] + 1 for cp, df in items}
    block_heights = {cp: df.shape[0] + 2 for cp, df in items}
    max_block_width = max(block_widths.values()) if block_widths else 2

    with pd.ExcelWriter(ruta_salida, engine="xlsxwriter") as writer:
        wb = writer.book
        ws = wb.add_worksheet(hoja)
        writer.sheets[hoja] = ws

        fmt_titulo = wb.add_format({"bold": True})
        fmt_header = wb.add_format({"bold": True, "bg_color": "#F2F2F2"})

        fila_actual = 0
        for i in range(0, len(items), por_fila):
            fila_items = items[i : i + por_fila]
            altura_fila = max(block_heights[cp] for cp, _ in fila_items) + pad_filas

            for j, (cp, df_bloque) in enumerate(fila_items):
                col_inicio = j * (max_block_width + pad_cols)
                ws.write(fila_actual, col_inicio, f"CP {cp}", fmt_titulo)

                df_bloque.to_excel(
                    writer,
                    sheet_name=hoja,
                    startrow=fila_actual + 1,
                    startcol=col_inicio,
                    header=True,
                    index=True,
                )

                n_cols_visibles = df_bloque.shape[1] + 1
                ws.set_row(fila_actual + 1, None, fmt_header)
                ws.set_column(col_inicio, col_inicio + n_cols_visibles - 1, 18)

            fila_actual += altura_fila


def run_proceso_campo(
    sistema_path: Path,
    data_dir: Path,
    output_dir: Path,
    log_func,
    month_label: str = "SISTEMA",
):
    """Ejecuta el proceso CAMPO"""
    try:
        ensure_dirs(data_dir, output_dir)

        log_func("=== INICIANDO PROCESO CAMPO ===")

        # Validaciones - usar archivo SISTEMA seleccionado por el usuario
        if not sistema_path.exists():
            return False, f"No existe el archivo SISTEMA seleccionado: {sistema_path}"

        # Buscar LISTA C.P..xlsx en la carpeta de datos seleccionada por el usuario
        lista_cp_path = data_dir / "LISTA C.P..xlsx"
        if not lista_cp_path.exists():
            return (
                False,
                f"Falta LISTA C.P..xlsx en la carpeta de datos: {lista_cp_path}",
            )

        log_func(f"Leyendo: {sistema_path}")
        df = pd.read_excel(sistema_path, engine="openpyxl")

        # Crear columnas si no existen
        if "NumerodeCuenta" not in df.columns:
            log_func("Creando columna # de cuenta")
            df["NumerodeCuenta"] = (
                df["Principal"].astype(str) + "-" + df["Derivada"].astype(str)
            )

        if "Domicilio" not in df.columns:
            log_func("Creando columna domicilio")
            df["Domicilio"] = (
                df["vialDescripcion"].astype(str)
                + " "
                + df["callNombre"].astype(str)
                + " "
                + df["manzana"].astype(str)
                + " "
                + df["lote"].astype(str)
                + " "
                + df["exterior"].astype(str)
                + " "
                + df["Interior"].astype(str)
                + " "
                + df["Edificio"].astype(str)
                + " "
                + df["departamento"].astype(str)
            )

        # Validar columnas requeridas
        required_cols = [
            "agua",
            "actualizacionagua",
            "recargosagua",
            "drenaje",
            "actualizaciondrenaje",
            "recargosdrenaje",
            "mejoras",
            "iva",
        ]
        for col in required_cols:
            if col not in df.columns:
                return False, f"Columna faltante en SISTEMA.xlsx: {col}"

        log_func("Calculando totales...")
        df["Total"] = (
            df["agua"]
            + df["actualizacionagua"]
            + df["recargosagua"]
            + df["drenaje"]
            + df["actualizaciondrenaje"]
            + df["recargosdrenaje"]
            + df["mejoras"]
            + df["iva"]
        )

        # Tablas generales
        log_func("Generando tablas por código postal...")
        cp = df.groupby("CodigoPostal")["NumerodeCuenta"].nunique().to_frame()
        cp.index = cp.index.astype(int)

        df2 = df.copy()
        df2.index = df2["NumerodeCuenta"]
        duplicados = df2.loc[df2.index[df2.index.duplicated()]]

        t_consumo = df.groupby("TipoConsumo")["NumerodeCuenta"].nunique().to_frame()
        t_consumo = pd.concat(
            [
                t_consumo,
                pd.DataFrame(
                    {"NumerodeCuenta": [t_consumo["NumerodeCuenta"].sum()]},
                    index=["Total general"],
                ),
            ]
        )

        t_conexion = df.groupby("TipoConexion")["NumerodeCuenta"].nunique().to_frame()
        t_conexion = pd.concat(
            [
                t_conexion,
                pd.DataFrame(
                    {"NumerodeCuenta": [t_conexion["NumerodeCuenta"].sum()]},
                    index=["Total general"],
                ),
            ]
        )

        veinte_25 = df.loc[df["bimfinal"].astype(str).str.contains("2025", na=False)]

        # Por CP
        log_func("Procesando datos por código postal...")
        codigos_postales = cp.index.sort_values(ascending=True).to_list()
        df_cps, df_completos_cps = {}, {}

        for cps in codigos_postales:
            df_cp = df.loc[df["CodigoPostal"] == cps].copy()
            df_cps[f"{cps}"] = (
                df_cp.groupby("TipoConexion")["NumerodeCuenta"].nunique().to_frame()
            )

            # Consolidar agua y drenaje
            df_cp["agua"] = df_cp["agua"] + df_cp["actualizacionagua"]
            df_cp.drop(columns=["actualizacionagua"], inplace=True)

            df_cp["drenaje"] = df_cp["drenaje"] + df_cp["actualizaciondrenaje"]
            df_cp.drop(columns=["actualizaciondrenaje"], inplace=True)

            df_cp["recargos"] = df_cp["recargosagua"] + df_cp["recargosdrenaje"]
            df_cp.drop(columns=["recargosagua", "recargosdrenaje"], inplace=True)

            df_cp["Total"] = (
                df_cp["agua"]
                + df_cp["drenaje"]
                + df_cp["recargos"]
                + df_cp["mejoras"]
                + df_cp["iva"]
            )
            df_completos_cps[f"{cps}"] = df_cp

        # Resumen grid
        log_func("Creando resumen de códigos postales...")
        resumen_path = data_dir / "resumen_cps.xlsx"
        tmp_resumen = resumen_path.with_suffix(".tmp.xlsx")
        exportar_resumenes_en_grid(df_cps, tmp_resumen, por_fila=3)
        tmp_resumen.replace(resumen_path)

        lista_cp = pd.read_excel(lista_cp_path, engine="openpyxl")
        resumen_cps = pd.read_excel(resumen_path, engine="openpyxl")

        # Reporte principal
        log_func("Guardando reporte principal...")
        reporte_path = output_dir / "ReporteRezagoAgua.xlsx"
        tmp_reporte = reporte_path.with_suffix(".tmp.xlsx")

        with pd.ExcelWriter(tmp_reporte, mode="w", engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=str(month_label or "SISTEMA"), index=False)
            cp.to_excel(writer, sheet_name="C.P.", index=True)
            t_consumo.to_excel(writer, sheet_name="T. CONSUMO", index=True)
            t_conexion.to_excel(writer, sheet_name="T. CONEXION", index=True)
            veinte_25.to_excel(writer, sheet_name="2025", index=False)
            resumen_cps.to_excel(writer, sheet_name="RESUMEN", index=False)
            lista_cp.to_excel(writer, sheet_name="LISTA C.P.", index=False)
            duplicados.to_excel(writer, sheet_name="DUPLICADOS", index=False)
        tmp_reporte.replace(reporte_path)

        # Reporte para macro - dividido por código postal
        log_func("Creando excel para macro (dividido por código postal)...")
        out_macro = output_dir / "reporte_macro.xlsx"

        # Preparar datos base para el reporte macro
        reporte_macro_base = df[
            [
                "ClaveCatastral",
                "Propietario",
                "Domicilio",
                "CodigoPostal",
                "UltimoPago",
                "NumerodeCuenta",
                "TipoConsumo",
                "TipoConexion",
                "Zona",
                "bimInicial",
                "bimfinal",
            ]
        ].copy()

        reporte_macro_base["agua"] = df["agua"] + df["actualizacionagua"]
        reporte_macro_base["drenaje"] = df["drenaje"] + df["actualizaciondrenaje"]
        reporte_macro_base["recargos"] = df["recargosagua"] + df["recargosdrenaje"]
        reporte_macro_base["mejoras"] = df["mejoras"]
        reporte_macro_base["iva"] = df["iva"]
        reporte_macro_base["total"] = (
            reporte_macro_base["iva"]
            + reporte_macro_base["mejoras"]
            + reporte_macro_base["recargos"]
            + reporte_macro_base["drenaje"]
            + reporte_macro_base["agua"]
        )
        reporte_macro_base["Domicilio"] = (
            reporte_macro_base["Domicilio"].astype(str).str.replace("nan", "")
        )

        # Crear el Excel con una hoja por código postal
        tmp_macro = out_macro.with_suffix(".tmp.xlsx")
        with pd.ExcelWriter(tmp_macro, mode="w", engine="openpyxl") as writer:
            for cp in codigos_postales:
                # Filtrar datos para este código postal específico
                datos_cp = reporte_macro_base[
                    reporte_macro_base["CodigoPostal"] == cp
                ].copy()

                # Quitar la columna CodigoPostal ya que es redundante en cada hoja
                datos_cp = datos_cp.drop(columns=["CodigoPostal"])

                # Nombre de la hoja
                nombre_hoja = f"CP {cp}"

                # Escribir a la hoja correspondiente
                datos_cp.to_excel(writer, sheet_name=nombre_hoja, index=False)

                log_func(f"  📊 CP {cp}: {len(datos_cp)} registros")

        tmp_macro.replace(out_macro)
        log_func(
            f"  ✅ Reporte macro creado con {len(codigos_postales)} hojas (una por CP)"
        )

        # Libro por CP
        log_func("Generando libro por códigos postales...")
        cp_book_path = output_dir / "CodigosPostales.xlsx"
        tmp_cp_book = cp_book_path.with_suffix(".tmp.xlsx")

        with pd.ExcelWriter(tmp_cp_book, mode="w", engine="openpyxl") as writer:
            for cps in codigos_postales:
                hoja = f"CP {cps}"
                det = df_completos_cps[f"{cps}"].copy()
                det = det.loc[:, ~det.columns.str.contains(r"^Unnamed")]
                res = df_cps[f"{cps}"].copy()
                if "NumerodeCuenta" in res.columns:
                    res = res.rename(columns={"NumerodeCuenta": "Cuentas únicas"})

                det.to_excel(
                    writer, sheet_name=hoja, index=False, startrow=0, startcol=0
                )
                startcol_resumen = det.shape[1] + 2
                res.to_excel(
                    writer,
                    sheet_name=hoja,
                    startrow=0,
                    startcol=startcol_resumen,
                    index=True,
                )

                ws = writer.sheets[hoja]
                ws.cell(
                    row=1, column=startcol_resumen + 1, value="Resumen por TipoConexion"
                )
        tmp_cp_book.replace(cp_book_path)

        log_func(f"PROCESO CAMPO COMPLETADO. Reportes en: {output_dir}")
        return True, output_dir

    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


# ====================================
# FUNCIONES DE PROCESAMIENTO CAJA
# ====================================


def run_proceso_caja(sistema_path: Path, data_dir: Path, output_dir: Path, log_func):
    """Ejecuta el proceso CAJA"""
    try:
        log_func("=== INICIANDO PROCESO CAJA ===")
        log_func(f"📋 Archivo SISTEMA: {sistema_path}")
        log_func(f"📁 Carpeta de datos: {data_dir}")
        log_func(f"📁 Carpeta de salida: {output_dir}")

        ensure_dirs(data_dir, output_dir)

        # Usar el archivo SISTEMA seleccionado por el usuario, no buscar en data_dir
        if not sistema_path.exists():
            return False, f"No existe el archivo SISTEMA seleccionado: {sistema_path}"

        log_func(f"Leyendo: {sistema_path}")
        df = pd.read_excel(sistema_path)
        df["fechapago"] = pd.to_datetime(df["fechapago"], yearfirst=True).dt.strftime(
            "%Y-%m-%d"
        )

        # 2024-6 anteriores y sin mejoras
        log_func("[1/7] Calculando 2024-6 anteriores y sin mejoras…")
        df_filtrado = df[
            (df["conDescripcion"] != "MEJORAS AMBIENTALES") & (df["pagdAño"] < 2025)
        ]
        df_filtrado.to_excel(
            output_dir / "2024-6_anteriores_y_sin_mejoras_ambientales.xlsx"
        )

        # EVIDENCIAS-X fecha de pago
        log_func("[2/7] Calculando evidencias por fecha de pago…")

        def redondear(x):
            return round(x, 2)

        keys = ["FolioImpreso", "fechapago"]
        df["fechapago"] = pd.to_datetime(df["fechapago"], yearfirst=True).dt.strftime(
            "%Y-%m-%d"
        )
        df_filtrado["fechapago"] = pd.to_datetime(
            df_filtrado["fechapago"], yearfirst=True
        ).dt.strftime("%Y-%m-%d")

        df["_cents"] = (
            (pd.to_numeric(df["pagdCosto"], errors="coerce") * 100)
            .round()
            .astype("Int64")
        )
        df_filtrado["_cents"] = (
            (pd.to_numeric(df_filtrado["pagdCosto"], errors="coerce") * 100)
            .round()
            .astype("Int64")
        )

        rezago_cents = (
            df_filtrado.groupby(keys, dropna=False, as_index=False)["_cents"]
            .sum()
            .rename(columns={"_cents": "_rezago_cents"})
        )
        pago_total_cents = (
            df.groupby(keys, dropna=False, as_index=False)["_cents"]
            .sum()
            .rename(columns={"_cents": "_pago_cents"})
        )

        def with_key_sentinel(d):
            out = d.copy()
            out["k_folio"] = out["FolioImpreso"].astype("string").fillna("__NA__")
            out["k_fecha"] = out["fechapago"].astype("string").fillna("__NA__")
            return out

        rezago_k = with_key_sentinel(rezago_cents)
        pago_k = with_key_sentinel(pago_total_cents)
        keys_all = pd.concat(
            [rezago_k[["k_folio", "k_fecha"]], pago_k[["k_folio", "k_fecha"]]],
            ignore_index=True,
        ).drop_duplicates()

        base = keys_all.merge(
            pago_k[["k_folio", "k_fecha", "_pago_cents"]],
            on=["k_folio", "k_fecha"],
            how="left",
        ).merge(
            rezago_k[["k_folio", "k_fecha", "_rezago_cents"]],
            on=["k_folio", "k_fecha"],
            how="left",
        )

        base["FolioImpreso"] = base["k_folio"].replace({"__NA__": np.nan})
        base["fechapago"] = base["k_fecha"].replace({"__NA__": np.nan})

        meta_cols = [
            "NumerodeCuenta",
            "Propietario",
            "Domicilio",
            "Colonia",
            "CodigoPostal",
            "AñoInicial",
            "BimestreInicial",
            "AñoFinal",
            "BimestreFinal",
        ]
        meta = df[keys + meta_cols].drop_duplicates(keys, keep="last")
        evidencias_x_fecha = base.merge(meta, on=keys, how="left")

        evidencias_x_fecha["pago"] = (evidencias_x_fecha["_pago_cents"] / 100).astype(
            float
        )
        evidencias_x_fecha["REZAGO IIWA 2024-6 y anteriores (pagdCosto)"] = (
            (evidencias_x_fecha["_rezago_cents"] / 100).fillna(0.0).astype(float)
        )
        evidencias_x_fecha["20% IIWA"] = (
            evidencias_x_fecha["REZAGO IIWA 2024-6 y anteriores (pagdCosto)"] * 0.20
        )

        orden_columnas = [
            "NumerodeCuenta",
            "Propietario",
            "Domicilio",
            "Colonia",
            "CodigoPostal",
            "AñoInicial",
            "BimestreInicial",
            "AñoFinal",
            "BimestreFinal",
            "fechapago",
            "FolioImpreso",
            "pago",
            "REZAGO IIWA 2024-6 y anteriores (pagdCosto)",
            "20% IIWA",
        ]
        evidencias_x_fecha = evidencias_x_fecha[orden_columnas].copy()
        evidencias_x_fecha.index += 1

        for c in ["pago", "REZAGO IIWA 2024-6 y anteriores (pagdCosto)", "20% IIWA"]:
            evidencias_x_fecha[c] = evidencias_x_fecha[c].apply(redondear)

        evidencias_x_fecha.to_excel(output_dir / "evidencias_x_fecha.xlsx")

        # PAGOS DIARIOS
        log_func("[3/7] Calculando PAGOS DIARIOS…")
        orden_pagos = [
            "DIAS",
            "# DE CUENTAS",
            "PAGO CAJA",
            "BASE IIWA 2024-6 Anteriores y sin Mejoras Ambientales",
            "pagdDescuento",
            "pagIva",
        ]

        pagos_diarios = (
            df.groupby(["fechapago"], as_index=False)
            .agg(
                {
                    "FolioImpreso": "nunique",
                    "pagdCosto": "sum",
                    "pagdDescuento": "sum",
                    "pagIva": "sum",
                }
            )
            .rename(
                columns={
                    "fechapago": "DIAS",
                    "FolioImpreso": "# DE CUENTAS",
                    "pagdCosto": "PAGO CAJA",
                }
            )
        )
        pagos_diarios["BASE IIWA 2024-6 Anteriores y sin Mejoras Ambientales"] = np.nan
        pagos_diarios = pagos_diarios[orden_pagos]

        pagos_diarios["DIAS"] = pd.to_datetime(pagos_diarios["DIAS"]).dt.strftime(
            "%d-%b"
        )
        pagos_diarios.set_index("DIAS", inplace=True)

        base_por_dia = (
            df_filtrado.groupby(["fechapago"], as_index=False)["pagdCosto"]
            .sum()
            .rename(
                columns={
                    "pagdCosto": "BASE IIWA 2024-6 Anteriores y sin Mejoras Ambientales"
                }
            )
        )

        tmp = base_por_dia.copy()
        tmp["DIAS"] = pd.to_datetime(tmp["fechapago"]).dt.strftime("%d-%b")
        tmp = tmp[
            ["DIAS", "BASE IIWA 2024-6 Anteriores y sin Mejoras Ambientales"]
        ].set_index("DIAS")

        pagos_diarios["BASE IIWA 2024-6 Anteriores y sin Mejoras Ambientales"] = (
            pagos_diarios.index.map(
                tmp["BASE IIWA 2024-6 Anteriores y sin Mejoras Ambientales"]
            ).fillna(0.0)
        )
        pagos_diarios.to_excel(output_dir / "pagos_diarios.xlsx")

        # PAGOS X C.P.
        log_func("[4/7] Calculando PAGOS POR C.P.…")
        pagos_x_cp = (
            df.groupby(["CodigoPostal"], as_index=False)
            .agg({"FolioImpreso": "nunique", "pagdCosto": "sum"})
            .rename(
                columns={
                    "CodigoPostal": "C.P.",
                    "FolioImpreso": "NUMERO DE CUENTAS",
                    "pagdCosto": "PAGO CAJA POR C.P.",
                }
            )
        )
        pagos_x_cp["BASE IIWA 2024-6 Anteriores y sin Mejoras Ambientales"] = np.nan
        pagos_x_cp.set_index("C.P.", inplace=True)

        base_por_cp = (
            df_filtrado.groupby(["CodigoPostal"], as_index=False)["pagdCosto"]
            .sum()
            .rename(
                columns={
                    "pagdCosto": "BASE IIWA 2024-6 Anteriores y sin Mejoras Ambientales",
                    "CodigoPostal": "C.P.",
                }
            )
        )

        tmp = base_por_cp.copy()
        tmp = tmp[
            ["C.P.", "BASE IIWA 2024-6 Anteriores y sin Mejoras Ambientales"]
        ].set_index("C.P.")

        pagos_x_cp["BASE IIWA 2024-6 Anteriores y sin Mejoras Ambientales"] = (
            pagos_x_cp.index.map(
                tmp["BASE IIWA 2024-6 Anteriores y sin Mejoras Ambientales"]
            ).fillna(0.0)
        )
        pagos_x_cp["20% IIWA"] = (
            pagos_x_cp["BASE IIWA 2024-6 Anteriores y sin Mejoras Ambientales"] * 0.20
        )
        pagos_x_cp.to_excel(output_dir / "pagos_x_cp.xlsx")

        # Validar archivos adicionales para CAJA
        registros_path = data_dir / "REGISTROS.csv"
        folios_path = data_dir / "FOLIOS.csv"

        log_func(f"🔍 Buscando archivos en: {data_dir}")
        log_func(
            f"🔍 REGISTROS.csv: {'✅ Encontrado' if registros_path.exists() else '❌ No encontrado'} en {registros_path}"
        )
        log_func(
            f"🔍 FOLIOS.csv: {'✅ Encontrado' if folios_path.exists() else '❌ No encontrado'} en {folios_path}"
        )

        # Listar archivos disponibles para ayudar con debug
        try:
            files_in_data = list(data_dir.glob("*.csv"))
            log_func(
                f"📋 Archivos CSV encontrados en carpeta de datos: {[f.name for f in files_in_data]}"
            )
        except Exception:
            pass

        if registros_path.exists() and folios_path.exists():
            log_func("[5/7] Enlazando REGISTROS y FOLIOS…")

            df_registros = pd.read_csv(registros_path, encoding="latin1", index_col=1)
            dict_folio_num = pd.read_csv(folios_path, encoding="latin1").dropna()
            dict_folio_num.index = (
                dict_folio_num.pop("NumerodeCuenta").astype(str).str.strip()
            )

            evidencias_x_fecha.index = evidencias_x_fecha.pop("NumerodeCuenta")
            evidencias_x_fecha = evidencias_x_fecha.sort_values(
                "fechapago", ascending=True
            )
            df_registros.index = df_registros.index.astype(str).str.strip()
            evidencias_x_fecha.index = evidencias_x_fecha.index.astype(str).str.strip()

            inter = evidencias_x_fecha.index.intersection(df_registros.index)
            e_folio_geo = evidencias_x_fecha.loc[inter]

            if "folio_notif" not in e_folio_geo.columns:
                e_folio_geo.insert(0, "folio_notif", np.nan)
            e_folio_geo["folio_notif"] = e_folio_geo.index.map(
                df_registros["folio_notif"].to_dict()
            )

            evidencias_x_fecha.loc[inter, "folio_notif"] = e_folio_geo["folio_notif"]
            evidencias_x_fecha.insert(
                0, "folio_notif", evidencias_x_fecha.pop("folio_notif")
            )

            inter_dict = evidencias_x_fecha.index.intersection(dict_folio_num.index)
            alt = dict_folio_num.loc[inter_dict, "FOLIO IIWA"].drop_duplicates()
            evidencias_x_fecha["folio_notif"] = evidencias_x_fecha[
                "folio_notif"
            ].fillna(alt)

            resultado = evidencias_x_fecha.sort_index(kind="mergesort")

            log_func(
                f"Cuentas con folio notif: {len(resultado.loc[resultado['folio_notif'].notna()])}"
            )
            log_func(
                f"Cuentas sin folio notif: {len(resultado.loc[resultado['folio_notif'].isna()])}"
            )
            log_func(f"Total de folios: {len(resultado)}")

            out_geo = output_dir / "E. folio Geolocalización.xlsx"
            resultado.groupby("CodigoPostal", group_keys=True, as_index=True).apply(
                lambda x: x.sort_values("fechapago", ascending=True)
            ).to_excel(out_geo)

            sin_geo = resultado.loc[resultado["folio_notif"].isna()]
            sin_geo["latitud_not"] = sin_geo.index.map(
                df_registros["latitud_not"].to_dict()
            )
            sin_geo["longitud_not"] = sin_geo.index.map(
                df_registros["longitud_not"].to_dict()
            )
            sin_geo.to_excel(output_dir / "sin_folio.xlsx")

            log_func("[6/7] Generando EVIDENCIAS C.P. y FECHA PAGO…")
            # Lógica similar para evidencias_cp_fecha...
        else:
            log_func(
                "[5-6/7] Saltando procesamiento de REGISTROS/FOLIOS (archivos no encontrados)"
            )

        # Consolidar a Excel final
        log_func("[7/7] Consolidando a Excel final…")
        salida_path = output_dir / "REPORTE_COMPLETO.xlsx"

        with pd.ExcelWriter(salida_path, engine="openpyxl") as writer:
            # Hoja SISTEMA - usar el archivo seleccionado por el usuario
            df_sistema = pd.read_excel(sistema_path)
            df_sistema["fechapago"] = pd.to_datetime(
                df_sistema["fechapago"], yearfirst=True
            ).dt.strftime("%Y-%m-%d")
            df_sistema.to_excel(writer, sheet_name="SISTEMA", index=False)

            # Agregar archivos de salida
            for archivo in output_dir.glob("*.xlsx"):
                if (
                    archivo.name != "reporte_completo.xlsx"
                    and not archivo.name.startswith("~")
                ):
                    try:
                        df_temp = pd.read_excel(archivo)
                        sheet_name = archivo.stem[:31]  # Limitar nombre de hoja
                        df_temp.to_excel(writer, sheet_name=sheet_name, index=False)
                    except Exception as e:
                        log_func(f"Error procesando {archivo.name}: {e}")

        log_func(f"PROCESO CAJA COMPLETADO. Reporte final: {salida_path}")
        return True, output_dir

    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


# ====================================
# CLASE PARA LOGGING EN GUI
# ====================================


class GuiLogger:
    """Cola de mensajes para actualizar el Text sin bloquear la UI"""

    def __init__(self, text_widget: tk.Text, interval_ms: int = 80):
        self.text_widget = text_widget
        self.queue = queue.Queue()
        self.interval_ms = interval_ms
        self._pump()

    def log(self, msg: str):
        """Método principal para enviar mensajes al log"""
        if not isinstance(msg, str):
            msg = str(msg)
        if not msg.endswith("\\n"):
            msg += "\\n"
        timestamp = datetime.now().strftime("[%H:%M:%S] ")
        self.queue.put(timestamp + msg)

    def _pump(self):
        """Procesa la cola de mensajes"""
        processed = 0
        while processed < 100:  # Limitar procesamiento por ciclo
            try:
                msg = self.queue.get_nowait()
            except queue.Empty:
                break
            else:
                state = self.text_widget["state"]
                if state == "disabled":
                    self.text_widget.configure(state="normal")
                self.text_widget.insert(tk.END, msg)
                self.text_widget.see(tk.END)
                if state == "disabled":
                    self.text_widget.configure(state="disabled")
                processed += 1

        self.text_widget.after(self.interval_ms, self._pump)


# ====================================
# APLICACIÓN GUI PRINCIPAL
# ====================================


class AppIIWA:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_variables()
        self.setup_widgets()
        self.logger = None
        self.processing = False

    def setup_window(self):
        """Configura la ventana principal"""
        self.root.title("🔄💧📊 App IIWA - Procesador Unificado de Padrones")
        self.root.geometry("950x750")

        # Configurar propiedades de la ventana
        self.root.resizable(True, True)
        self.root.minsize(850, 650)

        # Configurar colores y tema
        try:
            # Usar un fondo claro que funcione bien con ttk en todos los sistemas
            self.root.configure(bg="#f5f5f5")

            # Configurar icono de la aplicación usando el JPEG
            try:
                from tkinter import PhotoImage
                from PIL import Image, ImageTk
                import os

                # Buscar el logo en la raíz del proyecto
                logo_path = Path(__file__).parent.parent.parent / "principal.jpeg"
                if logo_path.exists():
                    # Cargar imagen original
                    img = Image.open(logo_path)

                    # Recortar la imagen para mostrar el centro más grande
                    # La imagen original parece tener mucho espacio en blanco alrededor
                    width, height = img.size

                    # Calcular el área de recorte para centrar el logo
                    # Recortar aproximadamente 25% de cada lado para enfocar el centro
                    crop_margin = min(width, height) // 4
                    left = crop_margin
                    top = crop_margin
                    right = width - crop_margin
                    bottom = height - crop_margin

                    # Recortar la imagen
                    img_cropped = img.crop((left, top, right, bottom))

                    # En macOS, usar tamaños más grandes para pantallas Retina
                    if sys.platform == "darwin":
                        # Crear iconos de múltiples tamaños para mejor calidad
                        sizes = [128, 64, 48, 32, 16]  # De mayor a menor
                        icons = []

                        for size in sizes:
                            # Usar LANCZOS para mejor calidad de redimensionamiento
                            resized = img_cropped.resize(
                                (size, size), Image.Resampling.LANCZOS
                            )
                            # Aplicar anti-aliasing suave
                            if hasattr(resized, "convert"):
                                resized = resized.convert("RGBA")
                            icons.append(ImageTk.PhotoImage(resized))

                        # Usar el icono más grande como principal
                        self.logo_icon = icons[0]  # 128x128
                        self.root.iconphoto(True, *icons)

                        # Guardar referencia a todos los iconos para evitar garbage collection
                        self._icon_refs = icons
                    else:
                        # Para otros sistemas, usar tamaño estándar mejorado
                        img_resized = img_cropped.resize(
                            (64, 64), Image.Resampling.LANCZOS
                        )
                        if hasattr(img_resized, "convert"):
                            img_resized = img_resized.convert("RGBA")
                        self.logo_icon = ImageTk.PhotoImage(img_resized)
                        self.root.iconphoto(True, self.logo_icon)

            except Exception as e:
                # Si falla la carga del icono, continuar sin él
                print(f"No se pudo cargar el icono: {e}")

            # En macOS, configurar algunas propiedades adicionales
            if sys.platform == "darwin":
                # Hacer que la ventana se vea más nativa en macOS
                self.root.tk.call(
                    "::tk::unsupported::MacWindowStyle",
                    "style",
                    self.root._w,
                    "documentProc",
                )

        except Exception:
            # Si falla algún estilo, continuar sin él
            pass

        # Icono y configuración adicional
        try:
            if sys.platform == "darwin":
                font_family = "SF Pro Display"
            else:
                font_family = "Segoe UI"
        except:
            font_family = "Arial"

        self.font_normal = (font_family, 10)
        self.font_bold = (font_family, 10, "bold")
        self.font_title = (font_family, 14, "bold")

    def setup_variables(self):
        """Inicializa las variables de control"""
        # Rutas por defecto - detectar automáticamente la ubicación del proyecto
        project_root = Path(
            __file__
        ).parent.parent.parent  # Ir desde src/app_iiwa/app.py hasta la raíz
        default_data = project_root / "data"
        default_output = project_root / "output"

        self.proceso_var = tk.StringVar(value="CAMPO")
        self.data_dir_var = tk.StringVar(value=str(default_data))
        self.output_dir_var = tk.StringVar(value=str(default_output))
        self.sistema_file_var = tk.StringVar(value=str(default_data / "SISTEMA.xlsx"))
        self.month_label_var = tk.StringVar(value="SISTEMA")

    def setup_widgets(self):
        """Crea y configura todos los widgets"""
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill="both", expand=True)

        # Título
        title_label = ttk.Label(main_frame, text="App IIWA")
        title_label.pack(pady=(0, 10))

        subtitle_label = ttk.Label(
            main_frame, text="Procesador Unificado para CAMPO y CAJA"
        )
        subtitle_label.pack(pady=(0, 20))

        # Sección de selección de proceso
        process_frame = ttk.LabelFrame(main_frame, text="Tipo de Proceso", padding=10)
        process_frame.pack(fill="x", pady=(0, 15))

        ttk.Radiobutton(
            process_frame,
            text="CAMPO - Procesamiento de rezagos de agua",
            variable=self.proceso_var,
            value="CAMPO",
        ).pack(anchor="w")
        ttk.Radiobutton(
            process_frame,
            text="CAJA - Análisis de pagos y evidencias",
            variable=self.proceso_var,
            value="CAJA",
        ).pack(anchor="w", pady=(5, 0))

        # Sección de rutas
        paths_frame = ttk.LabelFrame(
            main_frame, text="Configuración de Rutas", padding=10
        )
        paths_frame.pack(fill="x", pady=(0, 15))

        # Carpeta de datos
        ttk.Label(paths_frame, text="📁 Carpeta de datos:").grid(
            row=0, column=0, sticky="w", padx=(0, 10)
        )
        data_entry = ttk.Entry(paths_frame, textvariable=self.data_dir_var, width=60)
        data_entry.grid(row=0, column=1, sticky="ew", padx=(0, 5))
        ttk.Button(paths_frame, text="Buscar...", command=self.browse_data_dir).grid(
            row=0, column=2
        )

        # Carpeta de salida
        ttk.Label(paths_frame, text="Carpeta de salida:").grid(
            row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 0)
        )
        output_entry = ttk.Entry(
            paths_frame, textvariable=self.output_dir_var, width=60
        )
        output_entry.grid(row=1, column=1, sticky="ew", padx=(0, 5), pady=(10, 0))
        ttk.Button(paths_frame, text="Buscar...", command=self.browse_output_dir).grid(
            row=1, column=2, pady=(10, 0)
        )

        # Archivo SISTEMA (solo para CAMPO)
        ttk.Label(paths_frame, text="Archivo SISTEMA.xlsx:").grid(
            row=2, column=0, sticky="w", padx=(0, 10), pady=(10, 0)
        )
        sistema_entry = ttk.Entry(
            paths_frame, textvariable=self.sistema_file_var, width=60
        )
        sistema_entry.grid(row=2, column=1, sticky="ew", padx=(0, 5), pady=(10, 0))
        ttk.Button(
            paths_frame, text="Buscar...", command=self.browse_sistema_file
        ).grid(row=2, column=2, pady=(10, 0))

        # Etiqueta de mes (solo para CAMPO)
        ttk.Label(paths_frame, text="Etiqueta de hoja:").grid(
            row=3, column=0, sticky="w", padx=(0, 10), pady=(10, 0)
        )
        month_entry = ttk.Entry(
            paths_frame, textvariable=self.month_label_var, width=20
        )
        month_entry.grid(row=3, column=1, sticky="w", padx=(0, 5), pady=(10, 0))

        paths_frame.columnconfigure(1, weight=1)

        # Área de logs
        log_frame = ttk.LabelFrame(main_frame, text="Registro de Actividad", padding=10)
        log_frame.pack(fill="both", expand=True, pady=(0, 15))

        # Text widget con scrollbar
        log_container = ttk.Frame(log_frame)
        log_container.pack(fill="both", expand=True)

        # Configurar fuentes para diferentes tipos de mensaje
        if sys.platform == "darwin":
            self.font_log_normal = ("Monaco", 9)
            self.font_log_large = ("Monaco", 11, "bold")
            self.font_log_title = ("Monaco", 12, "bold")
        else:
            self.font_log_normal = ("Consolas", 9)
            self.font_log_large = ("Consolas", 11, "bold")
            self.font_log_title = ("Consolas", 12, "bold")

        self.log_text = tk.Text(
            log_container,
            wrap="word",
            state="disabled",
            height=15,
            font=self.font_log_normal,
        )
        self.log_text.pack(side="left", fill="both", expand=True)

        # Configurar tags para diferentes estilos de texto
        # Colores que funcionan bien en modo claro y oscuro
        if sys.platform == "darwin":
            # En macOS, usar colores que se adapten al tema del sistema
            self.log_text.configure(
                bg="#2d2d2d",
                fg="white",
                insertbackground="white",
                selectbackground="#4a90e2",
                selectforeground="white",
            )
            self.log_text.tag_configure(
                "normal", font=self.font_log_normal, foreground="white"
            )
            self.log_text.tag_configure(
                "large", font=self.font_log_large, foreground="white"
            )
            self.log_text.tag_configure(
                "title", font=self.font_log_title, foreground="#4a90e2"
            )  # Azul suave
            self.log_text.tag_configure(
                "success", font=self.font_log_large, foreground="#52c41a"
            )
            self.log_text.tag_configure(
                "error", font=self.font_log_large, foreground="#ff4d4f"
            )
            self.log_text.tag_configure(
                "warning", font=self.font_log_normal, foreground="#faad14"
            )
        else:
            # En otros sistemas, usar colores claros
            self.log_text.configure(
                bg="white",
                fg="black",
                insertbackground="black",
                selectbackground="#0078d4",
                selectforeground="white",
            )
            self.log_text.tag_configure(
                "normal", font=self.font_log_normal, foreground="black"
            )
            self.log_text.tag_configure(
                "large", font=self.font_log_large, foreground="black"
            )
            self.log_text.tag_configure(
                "title", font=self.font_log_title, foreground="#0078d4"
            )
            self.log_text.tag_configure(
                "success", font=self.font_log_large, foreground="#107c10"
            )
            self.log_text.tag_configure(
                "error", font=self.font_log_large, foreground="#d13438"
            )
            self.log_text.tag_configure(
                "warning", font=self.font_log_normal, foreground="#ff8c00"
            )

        log_scroll = ttk.Scrollbar(
            log_container, orient="vertical", command=self.log_text.yview
        )
        log_scroll.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=log_scroll.set)

        # Botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(0, 0))

        self.progress_bar = ttk.Progressbar(button_frame, mode="indeterminate")
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.process_button = ttk.Button(
            button_frame,
            text="🚀 Iniciar Proceso",
            command=self.start_process,
            style="Accent.TButton",
        )
        self.process_button.pack(side="right", padx=(5, 0))

        ttk.Button(
            button_frame, text="📂 Abrir Salida", command=self.open_output_folder
        ).pack(side="right", padx=(5, 0))

        ttk.Button(button_frame, text="🧹 Limpiar Log", command=self.clear_log).pack(
            side="right", padx=(5, 0)
        )

        # Inicializar logger
        self.logger = GuiLogger(self.log_text)
        self._log_to_gui(
            "✅ App IIWA iniciada. Selecciona un proceso y las rutas correspondientes."
        )

    def browse_data_dir(self):
        """Selecciona carpeta de datos"""
        folder = filedialog.askdirectory(
            title="Seleccionar carpeta de datos", initialdir=self.data_dir_var.get()
        )
        if folder:
            self.data_dir_var.set(folder)

    def browse_output_dir(self):
        """Selecciona carpeta de salida"""
        folder = filedialog.askdirectory(
            title="Seleccionar carpeta de salida", initialdir=self.output_dir_var.get()
        )
        if folder:
            self.output_dir_var.set(folder)

    def browse_sistema_file(self):
        """Selecciona archivo SISTEMA.xlsx"""
        file = filedialog.askopenfilename(
            title="Seleccionar archivo SISTEMA.xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialdir=Path(self.data_dir_var.get()),
        )
        if file:
            self.sistema_file_var.set(file)

    def clear_log(self):
        """Limpia el área de logs"""
        self.log_text.configure(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state="disabled")
        self._log_to_gui("📋 Log limpiado.")

    def open_output_folder(self):
        """Abre la carpeta de salida"""
        output_path = Path(self.output_dir_var.get())
        if output_path.exists():
            open_folder(str(output_path))
        else:
            messagebox.showwarning("Advertencia", "La carpeta de salida no existe aún.")

    def start_process(self):
        """Inicia el proceso seleccionado en un hilo separado"""
        if self.processing:
            return

        # Validaciones básicas
        data_path = Path(self.data_dir_var.get())
        output_path = Path(self.output_dir_var.get())

        if not data_path.exists():
            messagebox.showerror("Error", f"La carpeta de datos no existe: {data_path}")
            return

        proceso = self.proceso_var.get()

        # Validar que el archivo SISTEMA existe para ambos procesos
        sistema_path = Path(self.sistema_file_var.get())
        if not sistema_path.exists():
            messagebox.showerror(
                "Error", f"El archivo SISTEMA.xlsx no existe: {sistema_path}"
            )
            return

        self.processing = True
        self.process_button.configure(state="disabled", text="🔄 Procesando...")
        self.progress_bar.start(10)

        self._log_to_gui(f"🎯 Iniciando proceso {proceso}...")

        # Ejecutar en hilo separado
        thread = threading.Thread(
            target=self._run_process_thread,
            args=(proceso, data_path, output_path),
            daemon=True,
        )
        thread.start()

    def _run_process_thread(self, proceso, data_path, output_path):
        """Ejecuta el proceso en un hilo separado"""
        try:
            if proceso == "CAMPO":
                sistema_path = Path(self.sistema_file_var.get())
                month_label = self.month_label_var.get().strip() or "SISTEMA"

                success, result = run_proceso_campo(
                    sistema_path=sistema_path,  # Archivo SISTEMA seleccionado por el usuario
                    data_dir=data_path,  # Carpeta de datos seleccionada por el usuario
                    output_dir=output_path,  # Carpeta de salida seleccionada por el usuario
                    log_func=self._log_to_gui,
                    month_label=month_label,
                )

            elif proceso == "CAJA":
                sistema_path = Path(
                    self.sistema_file_var.get()
                )  # Usar el archivo seleccionado también para CAJA
                success, result = run_proceso_caja(
                    sistema_path=sistema_path,  # Archivo SISTEMA seleccionado por el usuario
                    data_dir=data_path,  # Carpeta de datos seleccionada por el usuario (para REGISTROS.csv y FOLIOS.csv)
                    output_dir=output_path,  # Carpeta de salida seleccionada por el usuario
                    log_func=self._log_to_gui,
                )

            if success:
                self._log_to_gui(f"✅ Proceso {proceso} completado exitosamente!")
                self._log_to_gui(f"📁 Resultados disponibles en: {result}")

                # Mostrar notificación de éxito
                self.root.after(
                    100,
                    lambda: messagebox.showinfo(
                        "Proceso Completado",
                        f"El proceso {proceso} se completó exitosamente.\\n\\nResultados en:\\n{result}",
                    ),
                )
            else:
                self._log_to_gui(f"❌ Error en proceso {proceso}: {result}")
                self.root.after(
                    100,
                    lambda: messagebox.showerror(
                        "Error en Proceso", f"Error en proceso {proceso}:\\n\\n{result}"
                    ),
                )

        except Exception as e:
            error_msg = f"Error inesperado: {type(e).__name__}: {e}"
            self._log_to_gui(f"💥 {error_msg}")
            self.root.after(
                100, lambda: messagebox.showerror("Error Crítico", error_msg)
            )

        finally:
            # Restaurar UI en el hilo principal
            self.root.after(100, self._finish_process)

    def _log_to_gui(self, message):
        """Función de log que siempre funciona, incluso si GuiLogger falla"""
        from datetime import datetime

        timestamp = datetime.now().strftime("[%H:%M:%S] ")
        full_message = timestamp + str(message) + "\n"

        # Detectar tipo de mensaje para aplicar estilo
        msg_str = str(message)
        tag = None

        if "¡Bienvenido" in msg_str or "App IIWA" in msg_str:
            tag = "title"
        elif "✅" in msg_str or "completado exitosamente" in msg_str:
            tag = "success"
        elif "❌" in msg_str or "Error" in msg_str or "💥" in msg_str:
            tag = "error"
        elif "⚠️" in msg_str or "Advertencia" in msg_str:
            tag = "warning"
        elif "===" in msg_str or "🎯" in msg_str:
            tag = "large"

        # Intentar con el logger primero
        if self.logger:
            try:
                self.logger.log(str(message))
                return
            except:
                pass

        # Fallback: escribir directamente al widget de texto
        try:
            self.root.after(0, lambda: self._write_to_text_widget(full_message, tag))
        except:
            # Último recurso: print
            print(full_message.strip())

    def _write_to_text_widget(self, message, tag=None):
        """Escribe directamente al widget de texto con opcional tag de estilo"""
        try:
            state = self.log_text["state"]
            if state == "disabled":
                self.log_text.configure(state="normal")

            start_index = self.log_text.index("end-1c")
            self.log_text.insert("end", message)

            # Aplicar tag si se especifica
            if tag and hasattr(self, "log_text"):
                end_index = self.log_text.index("end-1c")
                self.log_text.tag_add(tag, start_index, end_index)
            self.log_text.see("end")
            if state == "disabled":
                self.log_text.configure(state="disabled")
        except:
            pass

    def _finish_process(self):
        """Restaura la UI después de completar el proceso"""
        self.processing = False
        self.process_button.configure(state="normal", text="Iniciar Proceso")
        self.progress_bar.stop()
        self._log_to_gui("⏹️ Proceso finalizado. Listo para nueva ejecución.")

    def run(self):
        """Inicia la aplicación"""
        # Mostrar la ventana
        self.root.deiconify()

        # Mensaje de bienvenida (sólo si logger está disponible)
        welcome_msg = """
¡Bienvenido a App IIWA!

Esta aplicación unifica los procesadores CAMPO y CAJA:

CAMPO: Procesa datos de rezagos de agua, genera reportes por CP y análisis detallados
CAJA: Analiza pagos, evidencias, y genera reportes consolidados con geolocalización

Instrucciones:
1. Selecciona el tipo de proceso (CAMPO o CAJA)
2. Configura las rutas de datos y salida
3. Para CAMPO: asegúrate de tener SISTEMA.xlsx y LISTA C.P..xlsx
4. Para CAJA: asegúrate de tener SISTEMA.xlsx, REGISTROS.csv y FOLIOS.csv
5. ¡Presiona 'Iniciar Proceso' y observa los logs en tiempo real!

Los logs se actualizan automáticamente mostrando el progreso detallado.
        """
        self._log_to_gui(welcome_msg.strip())

        self.root.mainloop()


# ====================================
# PUNTO DE ENTRADA PRINCIPAL
# ====================================

if __name__ == "__main__":
    app = AppIIWA()
    app.run()
