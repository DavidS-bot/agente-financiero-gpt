import openai
import pandas as pd
import streamlit as st
from io import BytesIO

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Agente Financiero GPT", page_icon="📊")
st.title("📈 Asistente de Inversión Inmobiliaria con GPT")

uploaded_file = st.file_uploader("📂 Sube tu Excel con propiedades", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.dataframe(df)

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
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asesor experto en inversiones inmobiliarias."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            return response["choices"][0]["message"]["content"]

        with st.spinner("Analizando con GPT..."):
            df["Recomendación GPT"] = df.apply(analizar_propiedad, axis=1)

        st.success("✅ Análisis completado")
        st.dataframe(df)

        output = BytesIO()
        df.to_excel(output, index=False, engine="openpyxl")
        output.seek(0)

        st.download_button(
            label="📥 Descargar Excel con análisis",
            data=output,
            file_name="Analisis_GPT.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
