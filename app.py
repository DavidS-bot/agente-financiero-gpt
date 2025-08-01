
import openai
import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Agente Financiero GPT", page_icon="📊")
st.title("📈 Asistente de Inversión Inmobiliaria con GPT")

uploaded_file = st.file_uploader("📂 Sube tu Excel con propiedades", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.dataframe(df)

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
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un asesor experto en inversiones inmobiliarias."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content

    with st.spinner("Analizando con GPT..."):
        df["Recomendación GPT"] = df.apply(analizar_propiedad, axis=1)

    st.success("✅ Análisis completado")
    st.dataframe(df)

    st.download_button(
        label="📥 Descargar Excel con análisis",
        data=df.to_excel(index=False),
        file_name="Analisis_GPT.xlsx"
    )
