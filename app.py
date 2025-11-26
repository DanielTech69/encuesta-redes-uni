# app.py - VERSIÓN FINAL OFICIAL CON "AÑADIR OTRA RED"
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

st.set_page_config(page_title="Encuesta Redes Sociales UNI", layout="centered")
st.title("¿Cuánto usas las redes? + ¿Qué evento quieres en la UNI?")
st.markdown("**Universidad Salesiana de Bolivia** | Resultados en vivo al final")

CSV_FILE = "datos_definitivos.csv"

# Crear archivo si no existe
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Nombre", "Carrera", "Número", "Redes_Usadas", "Horas_Totales", 
                               "Contenido_Favorito", "Actividad_Sugerida", "Nivel", "Fecha"])
    df.to_csv(CSV_FILE, index=False)

# Lista inicial de redes
redes_base = [
    "Instagram", "TikTok", "WhatsApp", "YouTube", "Facebook", "Twitter/X", 
    "Snapchat", "Twitch", "Discord", "Pinterest", "Juegos (Steam, Roblox, etc.)", "BeReal"
]

# 19 tipos de contenido que me diste
contenidos = [
    "Tutoriales (paso a paso)", "Bailes", "Lip-sync", "Proceso vs. resultado", "Carruseles orgánicos",
    "Mal y bien (cómo NO hacerlo)", "Contenido sobrio/reflexivo", "Los tops (listas)", "Videos con efecto doble",
    "Mini-entrevistas", "Un día en mi vida", "Videos de humor", "Retos virales", "DIY (Hazlo tú mismo)",
    "Videos POV", "Reseñas y unboxings", "ASMR", "Vlogs de viaje", "Preguntas y respuestas", "Detrás de cámaras"
]

with st.form("encuesta_final"):
    st.subheader("1. Tus datos")
    nombre = st.text_input("Nombre completo (se verá públicamente)")
    carrera = st.selectbox("Carrera", [
        "Ingeniería de Sistemas", "Ingeniería Comercial", "Psicología", "Derecho", "Arquitectura", 
        "Medicina", "Contaduría", "Diseño Gráfico", "Otra"
    ])
    numero = st.text_input("Tu número (opcional)")

    st.subheader("2. Redes sociales y tiempo diario")
    
    # Estado para guardar las redes seleccionadas
    if "redes_lista" not in st.session_state:
        st.session_state.redes_lista = []

    # Añadir red predefinida
    red_pre = st.selectbox("Selecciona una red", [""] + redes_base + ["Otra (escribir)"])
    if red_pre and red_pre not in st.session_state.redes_lista:
        if st.button(f"Añadir {red_pre}"):
            if red_pre == "Otra (escribir)":
                otra = st.text_input("Escribe el nombre de la red", key="otra_input")
                if otra and st.button("Confirmar y añadir"):
                    st.session_state.redes_lista.append(otra)
                    st.success(f"{otra} añadida")
                    st.rerun()
            else:
                st.session_state.redes_lista.append(red_pre)
                st.rerun()

    # Mostrar redes añadidas con horas/minutos
    horas_totales = 0
    redes_con_horas = []
    for i, red in enumerate(st.session_state.redes_lista):
        st.markdown(f"**{i + 1}. {red}**")
        col1, col2 = st.columns(2)
        with col1:
            horas = st.selectbox(f"Horas en {red}", options=list(range(0, 21)), key=f"h_{i}")
        with col2:
            minutos = st.selectbox(f"Minutos", options=[0, 15, 30, 45], key=f"m_{i}")
        total_min = horas * 60 + minutos
        if total_min > 0:
            horas_decimal = round(total_min / 60, 2)
            horas_totales += horas_decimal
            redes_con_horas.append(f"{red}: {horas}h {minutos}m")

    # Botón para eliminar red
    if st.session_state.redes_lista:
        eliminar = st.selectbox("¿Quitar alguna red?", [""] + st.session_state.redes_lista)
        if eliminar and st.button("Eliminar red"):
            st.session_state.redes_lista.remove(eliminar)
            st.rerun()

    st.subheader("3. ¿Qué contenido consumes más?")
    contenido = st.multiselect("Selecciona hasta 5", contenidos, max_selections=5)

    st.subheader("4. ¡Haz la UNI más divertida!")
    actividad = st.text_area("¿Qué actividad o evento te gustaría? (fiesta, taller, torneo, viaje, cine, etc.)")

    enviado = st.form_submit_button("¡ENVIAR Y VER RESULTADOS EN VIVO!")

    if enviado:
        if not nombre or len(st.session_state.redes_lista) == 0:
            st.error("Nombre y al menos una red son obligatorios")
        else:
            # Calcular nivel
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

            # Guardar
            nuevo = {
                "Nombre": nombre,
                "Carrera": carrera,
                "Número": numero if numero else "No dio",
                "Redes_Usadas": " | ".join(redes_con_horas),
                "Horas_Totales": round(horas_totales, 2),
                "Contenido_Favorito": " | ".join(contenido),
                "Actividad_Sugerida": actividad.strip() if actividad.strip() else "Sin sugerencia",
                "Nivel": nivel,
                "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            df = pd.read_csv(CSV_FILE)
            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            df.to_csv(CSV_FILE, index=False)

            st.success("¡GRACIAS!")
            st.balloons()
            st.subheader(f"Tu nivel: **{nivel}/10** → {horas_totales:.2f} horas diarias")
            if nivel >= 7:
                st.error("¡Alto consumo! Ayuda: +591 64143280")

            # ================= RESULTADOS PÚBLICOS =================
            st.markdown("---")
            st.header("RESULTADOS EN VIVO - UNIVERSIDAD SALESIANA")

            col1, col2, col3 = st.columns(3)
            col1.metric("Participantes", len(df))
            col2.metric("Horas promedio", round(df["Horas_Totales"].mean(), 2))
            col3.metric("Nivel promedio", round(df["Nivel"].mean(), 1))

            # Gráfico 1: Por carrera
            fig1 = px.bar(df["Carrera"].value_counts(), title="Participación por carrera")
            st.plotly_chart(fig1, use_container_width=True)

            # Gráfico 2: Niveles
            fig2 = px.bar(df["Nivel"].value_counts().sort_index(), title="Estudiantes por nivel de uso")
            st.plotly_chart(fig2, use_container_width=True)

            # Gráfico 3: Contenido
            cont_flat = df["Contenido_Favorito"].str.split(" | ", expand=True).stack()
            top_cont = cont_flat.value_counts().head(10)
            fig3 = px.pie(values=top_cont.values, names=top_cont.index, title="Contenido más visto")
            st.plotly_chart(fig3, use_container_width=True)

            # Tabla final
            st.subheader("Todos los participantes")
            st.dataframe(df[["Nombre", "Carrera", "Número", "Nivel", "Actividad_Sugerida"]], 
                        use_container_width=True, hide_index=True)

            st.info("¡Comparte este link y todos verán los resultados en vivo!")
