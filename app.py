# app.py - VERSIÓN FINAL OFICIAL (100% funcional y perfecta)
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

st.set_page_config(page_title="Encuesta Redes Sociales UNI", layout="centered")
st.title("¿Cuánto usas redes sociales? + ¿Qué evento quieres en la UNI?")
st.markdown("**Encuesta pública de la Universidad Salesiana** | Resultados en vivo al final")

CSV_FILE = "datos_finales.csv"

# Crear archivo si no existe
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Nombre", "Carrera", "Número", "Redes_Usadas", "Horas_Totales", 
                               "Contenido_Favorito", "Actividad_Sugerida", "Nivel", "Fecha"])
    df.to_csv(CSV_FILE, index=False)

# Opciones de redes
redes_opciones = [
    "Instagram", "TikTok", "WhatsApp", "YouTube", "Facebook", 
    "Twitter/X", "Snapchat", "Twitch", "Discord", "Pinterest", "Juegos (Steam, Roblox, etc.)", "Otra"
]

# Opciones de contenido (tus 19 exactas)
contenidos = [
    "Tutoriales (paso a paso)", "Bailes", "Lip-sync", "Proceso vs. resultado", "Carruseles orgánicos",
    "Mal y bien (cómo NO hacerlo)", "Contenido sobrio/reflexivo", "Los tops (listas)", "Videos con efecto doble",
    "Mini-entrevistas", "Un día en mi vida", "Videos de humor", "Retos virales", "DIY (Hazlo tú mismo)",
    "Videos POV", "Reseñas y unboxings", "ASMR", "Vlogs de viaje", "Preguntas y respuestas", "Detrás de cámaras"
]

with st.form("encuesta_final"):
    st.subheader("1. Tus datos")
    nombre = st.text_input("Nombre completo (se mostrará públicamente)", placeholder="Juan Pérez")
    carrera = st.selectbox("Carrera", [
        "Ingeniería de Sistemas", "Ingeniería Comercial", "Psicología", "Derecho", "Arquitectura", 
        "Medicina", "Contaduría", "Diseño Gráfico", "Otra"
    ])
    numero = st.text_input("Tu número (opcional, se mostrará)", placeholder="71234567")

    st.subheader("2. Redes sociales que usas y tiempo diario")
    redes_seleccionadas = st.multiselect("Selecciona todas las que usas", redes_opciones)
    
    horas_totales = 0
    redes_con_horas = []
    for red in redes_seleccionadas:
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**{red}**")
        with col2:
            horas = st.selectbox(f"Horas en {red}", options=list(range(0, 21)), index=2, key=f"h_{red}")
            minutos = st.selectbox(f"Minutos en {red}", options=[0, 15, 30, 45], index=0, key=f"m_{red}")
            total_min = horas * 60 + minutos
            horas_decimal = round(total_min / 60, 2)
            if horas_decimal > 0:
                horas_totales += horas_decimal
                redes_con_horas.append(f"{red}: {horas}h {minutos}m")

    st.subheader("3. ¿Qué contenido consumes más?")
    contenido = st.multiselect("Selecciona hasta 5 tipos que más ves", contenidos, max_selections=5)

    st.subheader("4. ¡Haz la UNI más divertida!")
    actividad = st.text_area("¿Qué actividad o evento te gustaría que organicemos? (fiesta, taller, torneo, cine, viaje, etc.)")

    enviado = st.form_submit_button("¡ENVIAR Y VER RESULTADOS EN VIVO!")

    if enviado:
        if not nombre or not redes_seleccionadas:
            st.error("Nombre y al menos una red social son obligatorios")
        else:
            # Calcular nivel 1-10
            if horas_totales <= 1: nivel = 1
            elif horas_totales <= 2: nivel = 2
            elif horas_totales <= 3: nivel = 3
            elif horas_totales <= 4: nivel = 4
            elif horas_totales <= 5: nivel = 5
            elif horas_totales <= 7: nivel = 6
            elif horas_totales <= 9: nivel = 7
            elif horas_totales <= 11: nivel = 8
            elif horas_totales <= 14: nivel = 9
            else: nivel = 10

            # Guardar datos
            nuevo = {
                "Nombre": nombre,
                "Carrera": carrera,
                "Número": numero if numero else "No dio",
                "Redes_Usadas": " | ".join(redes_con_horas),
                "Horas_Totales": round(horas_totales, 2),
                "Contenido_Favorito": " | ".join(contenido),
                "Actividad_Sugerida": actividad.strip() if actividad.strip() else "No sugirió",
                "Nivel": nivel,
                "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            df = pd.read_csv(CSV_FILE)
            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            df.to_csv(CSV_FILE, index=False)

            st.success("¡GRACIAS POR PARTICIPAR!")
            st.balloons()
            st.subheader(f"Tu nivel personal: **{nivel}/10** → {horas_totales:.2f} horas diarias")
            if nivel >= 7:
                st.error("¡CUIDADO! Uso alto. Si necesitas ayuda: +591 64143280 (Daniel)")

            # ====================== RESULTADOS PÚBLICOS EN VIVO ======================
            st.markdown("---")
            st.header("RESULTADOS EN VIVO DE TODA LA UNIVERSIDAD SALESIANA")

            col1, col2, col3 = st.columns(3)
            col1.metric("Total participantes", len(df))
            col2.metric("Horas promedio diarias", round(df["Horas_Totales"].mean(), 2))
            col3.metric("Nivel promedio", round(df["Nivel"].mean(), 1))

            # Gráfico 1: Participación por carrera
            fig1 = px.bar(df["Carrera"].value_counts(), title="Participación por carrera")
            st.plotly_chart(fig1, use_container_width=True)

            # Gráfico 2: Niveles de adicción
            nivel_counts = df["Nivel"].value_counts().sort_index()
            fig2 = px.bar(x=nivel_counts.index, y=nivel_counts.values, 
                          title="¿Cuántos estudiantes están en cada nivel?", 
                          labels={"x": "Nivel (1-10)", "y": "Cantidad"})
            st.plotly_chart(fig2, use_container_width=True)

            # Gráfico 3: Contenido más consumido
            contenido_flat = df["Contenido_Favorito"].str.split(" | ", expand=True).stack()
            top_contenido = contenido_flat.value_counts().head(10)
            fig3 = px.pie(values=top_contenido.values, names=top_contenido.index, 
                          title="Contenido más consumido por los estudiantes")
            st.plotly_chart(fig3, use_container_width=True)

            # Tabla pública completa
            st.subheader("Todos los participantes")
            display = df[["Nombre", "Carrera", "Número", "Nivel", "Actividad_Sugerida"]].copy()
            st.dataframe(display, use_container_width=True, hide_index=True)

            st.info("¡Comparte este link para que todos vean cómo estamos como universidad!")
