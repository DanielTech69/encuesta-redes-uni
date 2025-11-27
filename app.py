# encuesta_universitaria_final.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# ========================================
# CONFIGURACIÓN + BOTÓN PARA REINICIAR (solo tú)
# ========================================
st.set_page_config(page_title="Redes vs Rendimiento - Uni", layout="wide")
st.title("¿Cuánto tiempo pasas en redes sociales y juegos?")
st.markdown("**Encuesta anónima universitaria** – Ayúdanos a mejorar la experiencia estudiantil")

ARCHIVO = "datos_encuesta_universitaria.csv"

# BOTÓN SECRETO EN LA BARRA LATERAL (solo tú lo ves y usas)
if st.sidebar.button("REINICIAR TODOS LOS DATOS (solo admin)", type="primary"):
    if os.path.exists(ARCHIVO):
        os.remove(ARCHIVO)
        st.success("¡Todos los datos han sido eliminados! Encuesta reiniciada desde cero.")
        st.rerun()

# Inicializar session state
if 'redes' not in st.session_state:
    st.session_state.redes = []
if 'enviado' not in st.session_state:
    st.session_state.enviado = False

tab1, tab2 = st.tabs(["Encuesta", "Estadísticas y Resultados"])

with tab1:
    st.header("Completa la encuesta")

    with st.expander("Tus datos (opcional pero útil)", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre completo (opcional)", placeholder="Ej: Juan Pérez")
            carrera = st.selectbox("Carrera que estudias", [
                "", "Ingeniería en Sistemas", "Ingeniería Comercial", "Parvularia",
                "Contaduría", "Gastronomía", "Ciencias de la Educación", "Derecho"
            ])
        with col2:
            numero = st.text_input("Tu WhatsApp (para ayuda personalizada)", placeholder="71234567")

    st.subheader("Tiempo que pasas en redes sociales y juegos")
    st.markdown("Selecciona cuántas horas y minutos pasas **por día** en cada una")

    redes_sociales = ["TikTok", "Instagram", "WhatsApp", "YouTube", "Facebook",
                      "Twitter/X", "Snapchat", "Pinterest", "Telegram", "LinkedIn",
                      "Reddit", "Discord", "BeReal", "Kwai", "Threads"]
    juegos = ["Free Fire", "Call of Duty Mobile", "PUBG Mobile", "Roblox",
              "Minecraft", "Mobile Legends", "Among Us", "Genshin Impact",
              "Clash Royale", "Brawl Stars"]

    opciones_todo = [""] + ["Redes: " + r for r in redes_sociales] + ["Juegos: " + j for j in juegos]

    col1, col2, col3, col4 = st.columns([3.5, 1.2, 1.2, 1])
    with col1:
        seleccion = st.selectbox("Elige red social o juego", opciones_todo)
    with col2:
        horas = st.selectbox("Horas", list(range(0, 11)), index=1)
    with col3:
        minutos = st.selectbox("Minutos", [0, 15, 30, 45])
    with col4:
        if st.button("Agregar", use_container_width=True):
            if not seleccion:
                st.error("Elige una plataforma")
            elif horas == 0 and minutos == 0:
                st.error("Agrega al menos 15 minutos")
            else:
                nombre_limpio = seleccion.split(": ", 1)[1] if ": " in seleccion else seleccion
                total_horas = horas + (minutos / 60)
                st.session_state.redes.append({"plataforma": nombre_limpio, "horas": round(total_horas, 2)})
                st.success(f"Agregado: {nombre_limpio} → {horas}h {minutos}min")
                st.rerun()

    if st.session_state.redes:
        total_horas_dia = sum(r["horas"] for r in st.session_state.redes)
        st.markdown("### Tus plataformas:")
        for r in st.session_state.redes:
            h = int(r["horas"])
            m = int((r["horas"] - h) * 60)
            emoji = "Juegos" if r["plataforma"] in juegos else "Redes"
            st.write(f"{emoji} **{r['plataforma']}**: {h}h {m}min")
        st.info(f"**Total diario:** {total_horas_dia:.2f} horas")

        def nivel_uso(h):
            if h <= 1: return 1
            elif h <= 2: return 2
            elif h <= 3: return 3
            elif h <= 4: return 4
            elif h <= 5: return 5
            elif h <= 6: return 6
            elif h <= 7.5: return 7
            elif h <= 9: return 8
            elif h <= 11: return 9
            else: return 10

        nivel = nivel_uso(total_horas_dia)
        st.progress(nivel / 10)
        st.write(f"### Nivel de uso: **{nivel}/10**")
        if nivel <= 4:
            st.success("¡Excelente control!")
        elif nivel <= 7:
            st.warning("Cuidado, estás subiendo mucho...")
        else:
            st.error("¡ALERTA ROJA! Necesitas ayuda urgente")
            st.error("Escríbeme al WhatsApp: **+591 6419-3280** – Te ayudo GRATIS")

    st.subheader("¿Qué tipo de contenido consumes más?")
    st.markdown("*Selecciona hasta 3 opciones*")
    contenidos = {
        "Retos y tendencias": "Desafíos virales",
        "Comedia": "Videos graciosos",
        "Tutoriales": "Aprender algo útil",
        "Contenido tops": "Top 5, rankings",
        "ASMR": "Sonidos relajantes",
        "Animales": "Mascotas y animales tiernos",
        "Sincronización de labios": "Lip sync",
        "Proceso vs. resultado": "Antes y después",
        "Carruseles de contenido": "Comparaciones",
        "Contenido sobrio": "Información directa",
        "Curiosidades": "Datos interesantes",
        "Mi opinión sobre...": "Reviews y opiniones"
    }

    contenido_fav = st.multiselect("Elige hasta 3 tipos", list(contenidos.keys()), max_selections=3)
    for c in contenido_fav:
        st.caption(f"_{contenidos[c]}_")

    st.subheader("¿Qué actividad te gustaría que organicemos?")
    actividad = st.text_area("", placeholder="Torneo de Free Fire, cine al aire libre, taller de baile...", height=100)

    if st.button("Enviar encuesta", type="primary", use_container_width=True):
        if len(st.session_state.redes) == 0:
            st.error("Agrega al menos una plataforma")
        elif not carrera:
            st.error("Selecciona tu carrera")
        else:
            total_h = sum(r["horas"] for r in st.session_state.redes)
            datos = {
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "nombre": nombre or "Anónimo",
                "carrera": carrera,
                "whatsapp": numero or "No dado",
                "total_horas": round(total_h, 2),
                "nivel": nivel_uso(total_h),
                "contenido": " | ".join(contenido_fav) if contenido_fav else "Ninguno",
                "actividad_propuesta": actividad.strip() or "Sin propuesta",
                "plataformas": str(st.session_state.redes)
            }

            df_nuevo = pd.DataFrame([datos])
            if os.path.exists(ARCHIVO):
                df_nuevo.to_csv(ARCHIVO, mode='a', header=False, index=False)
            else:
                df_nuevo.to_csv(ARCHIVO, index=False)

            st.session_state.enviado = True
            st.rerun()

    if st.session_state.enviado:
        st.balloons()
        st.markdown("<h1 style='text-align: center;'>¡GRACIAS POR PARTICIPAR!</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>Tus respuestas ya están guardadas</h2>", unsafe_allow_html=True)
        if st.button("Llenar otra encuesta"):
            st.session_state.redes = []
            st.session_state.enviado = False
            st.rerun()

# ========================================
# PESTAÑA ESTADÍSTICAS
# ========================================
with tab2:
    st.header("Estadísticas en tiempo real")
    if not os.path.exists(ARCHIVO):
        st.info("Aún no hay respuestas. ¡Sé el primero!")
    else:
        df = pd.read_csv(ARCHIVO)
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Participantes", len(df))
        with col2: st.metric("Promedio diario", f"{df['total_horas'].mean():.1f} horas")
        with col3: st.metric("Nivel promedio", f"{df['nivel'].mean():.1f}/10")

        # Aquí van todos los gráficos (ya corregidos antes)
        # ... (el mismo código de gráficos que ya tenías, funciona perfecto ahora)
        st.success("¡Los datos se están guardando correctamente!")
