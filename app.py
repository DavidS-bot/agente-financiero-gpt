

import streamlit as st
import pandas as pd
from openai import OpenAI

# Cargar la API Key desde los secretos de Streamlit
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Configurar la página
st.set_page_config(page_title="Agente Financiero GPT", page_icon="📊")
st.title("📈 Asistente de Inversión Inmobiliaria con GPT")

# Subida del archivo Excel
uploaded_file = st.file_uploader("📂 Sube tu Excel con propiedades", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.dataframe(df)

    # Validación de columnas necesarias
    columnas_requeridas = [
        "Precio Compra (€)",
        "Alquiler Mensual (€)",
        "Gastos Anuales (€)",
        "Tipo Interés (%)",
        "Años Hipoteca",
        "Porcentaje Equity (%)"
    ]

    if not all(col in df.columns for col in columnas_requeridas):
        st.error("❌ El archivo Excel no contiene todas las columnas requeridas.")
    else:
        # Función para analizar propiedad con GPT
        def analizar_propiedad(row):
            prompt = f"""
Eres un asesor financiero experto. Evalúa esta propiedad:
- Precio compra: {row['Precio Compra (€)']}€
- Alquiler mensual: {row['Alquiler Mensual (€)']}€
- Gastos anuales: {row['Gastos Anuales (€)']}€
- Tipo de interés: {row['Tipo Interés (%)']}%
- Años hipoteca: {row['Años Hipoteca']}
- Equity aportado: {row['Porcentaje Equity (%)']}%

El objetivo es lograr al menos un 10% de rentabilidad sobre el equity. Da una recomendación breve y profesional.
"""

            respuesta = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asesor experto en inversiones inmobiliarias."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            return respuesta.choices[0].message.content

        # Aplicar el análisis fila por fila
        with st.spinner("🧠 Analizando con GPT..."):
            df["Recomendación GPT"] = df.apply(analizar_propiedad, axis=1)

        st.success("✅ Análisis completado")
        st.dataframe(df)

        # Botón para descargar el Excel con recomendaciones
        st.download_button(
            label="📥 Descargar Excel con análisis",
            data=df.to_excel(index=False, engine="openpyxl"),
            file_name="Analisis_GPT.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

