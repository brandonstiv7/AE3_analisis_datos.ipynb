from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
DATA = BASE / "datos" / "dataset_ae2.csv"
OUT = BASE / "resultados"
OUT.mkdir(exist_ok=True)

def preparar_y_enriquecer(df):
    original = df.copy()
    final = df.copy()
    for c in final.select_dtypes(include=["object", "string"]).columns:
        final[c] = final[c].astype("string").str.strip()
    if "municipio" in final.columns:
        mapa = {"medellin":"Medellín", "medellín":"Medellín",
                "envigado":"Envigado", "santa elena":"Santa Elena", "sabaneta":"Sabaneta"}
        final["municipio"] = final["municipio"].str.lower().map(mapa).fillna(final["municipio"])
    # No se eliminan filas ni se imputan faltantes: se conservan y se identifican.
    final["tiene_respuesta_incompleta"] = final.isna().any(axis=1)
    if "interes_compra_plantas" in final:
        final["indicador_interes_plantas"] = final["interes_compra_plantas"].astype("string").str.lower().eq("sí")
    if "interes_talleres" in final:
        final["indicador_interes_talleres"] = final["interes_talleres"].astype("string").str.lower().eq("sí")
    return original, final

def tabla_frecuencias(df, columna, archivo):
    t = df.groupby(columna, dropna=False).size().reset_index(name="respuestas")
    t["participacion_pct"] = (t["respuestas"] / len(df) * 100).round(2)
    t = t.sort_values("respuestas", ascending=False)
    t.to_csv(OUT / archivo, index=False, encoding="utf-8-sig")
    return t

def exportar(df):
    df.to_csv(OUT/"dataset_preparado.csv", index=False, encoding="utf-8-sig")
    if "municipio" in df: tabla_frecuencias(df,"municipio","01_respuestas_por_municipio.csv")
    if "producto_interes" in df: tabla_frecuencias(df,"producto_interes","02_interes_por_producto.csv")
    if "canal_preferido" in df: tabla_frecuencias(df,"canal_preferido","03_canales_preferidos.csv")
    indicadores=[c for c in ["indicador_interes_plantas","indicador_interes_talleres"] if c in df]
    if indicadores:
        filas=[]
        for c in indicadores:
            validos=int(df[c].notna().sum()); si=int(df[c].sum())
            filas.append({"indicador":c,"respuestas_si":si,"respuestas_validas":validos,
                          "participacion_si_pct":round(si/validos*100,2) if validos else None})
        pd.DataFrame(filas).to_csv(OUT/"04_interes_plantas_talleres.csv",index=False,encoding="utf-8-sig")

def generar_resumen(df):
    L=["RESUMEN DESCRIPTIVO DEL DATAFRAME AE3","="*55,
       f"Filas: {df.shape[0]}",f"Columnas: {df.shape[1]}","","COLUMNAS Y TIPOS","-"*55]
    L += [f"- {c}: {df[c].dtype}" for c in df.columns]
    L += ["","VALORES NULOS POR COLUMNA","-"*55]
    L += [f"- {c}: {int(v)}" for c,v in df.isna().sum().items()]
    L += ["","ESTADÍSTICAS DESCRIPTIVAS","-"*55]
    num=df.select_dtypes(include="number")
    L += [num.describe().round(2).to_string() if not num.empty else "No hay columnas numéricas."]
    L += ["","MUESTRA","-"*55,df.head().to_string(index=False)]
    (OUT/"resumen_dataset.txt").write_text("\\n".join(L),encoding="utf-8")
