# AE3 – La Esmeralda Café y Vivero

**Aviso:** `datos/dataset_demo_simulado.csv` contiene 50 respuestas simuladas solo para probar el código. No es el dataset real de AE2 ni debe presentarse como tal.

## Estructura
- `notebooks/AE3_analisis_datos.ipynb`: flujo de carga, diagnóstico, transformación, enriquecimiento, tablas y exportación.
- `datos/dataset_demo_simulado.csv`: dataset sintético de demostración.
- `datos/dataset_ae2.csv`: ubicación esperada para el dataset auténtico de AE2.
- `analisis_ae3.py`: funciones reutilizables.
- `resultados/`: dataset preparado, tablas CSV y resumen TXT de demostración.
- `Documento_Avance_AE3.docx`: documento Word que debe actualizarse con los resultados reales.
- `requirements.txt`: dependencias.

## Preguntas provisionales
1. Distribución por municipio.
2. Interés por producto/experiencia.
3. Canales preferidos.
4. Interés en plantas y talleres.
Ajustar a las preguntas originales de AE2.

## Transformaciones y enriquecimiento
- Recorte de espacios en texto.
- Estandarización de municipios conocidos.
- Conservación de nulos y filas; no se imputan datos.
- Marca `tiene_respuesta_incompleta`.
- Indicadores booleanos de interés en plantas y talleres.

## Ejecución
1. `python -m pip install -r requirements.txt`
2. Copiar el dataset real como `datos/dataset_ae2.csv`.
3. Abrir el notebook y cambiar `ruta = ruta_demo` por `ruta = ruta_ae2`.
4. Ejecutar todas las celdas y guardar el notebook con salidas visibles.
5. Actualizar el Word con las cifras reales.

## Exportaciones
`resultados/dataset_preparado.csv`, tablas `01` a `04` y `resultados/resumen_dataset.txt`. Se regeneran al ejecutar el notebook.
