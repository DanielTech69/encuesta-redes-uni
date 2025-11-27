# encuesta_universitaria_final.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# ========================================
# CONFIGURACIÓN + REINICIAR SOLO SI TÚ QUIERES
# ========================================
st.set_page_config(page_title="Redes vs Rendimiento Uni", layout="wide")
st.title("¿Cuánto tiempo pasas en redes sociales y juegos?")
st.markdown("**Encuesta anónima universitaria** – Ayúdanos a mejorar la experiencia estudiantil")

ARCHIVO = "datos_encuesta_universitaria.csv"

# BOTÓN SECRETO (solo tú lo puedes usar)
if st.sidebar.button("REINICIAR TODOS LOS DATOS (solo admin)", type="primary"):
    if os.path.exists(ARCHIVO):
        os.remove(ARCHIVO)
        st.success("Datos borrados. Encuesta reiniciada desde cero.")
        st.rerun()

# Session state
if 'redes' not in st.session_state:
    st.session_state.redes = []
if 'enviado' not in st.session_state:
    st.session_state.enviado = False

tab1, tab2 = st.tabs(["Encuesta", "Estadísticas y Resultados"])

# ========================================
# PESTAÑA 1: ENCUESTA
# ========================================
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
            numero = st.text_input("Tu WhatsApp", placeholder="71234567")

    st.subheader("Tiempo diario en redes y juegos")
    redes_sociales = ["TikTok", "Instagram", "WhatsApp", "YouTube", "Facebook", "Twitter/X", "Snapchat", "Pinterest", "Telegram", "LinkedIn", "Reddit", "Discord", "BeReal", "Kwai", "Threads"]
    juegos = ["Free Fire", "Call of Duty Mobile", "PUBG Mobile", "Roblox", "Minecraft", "Mobile Legends", "Among Us", "Genshin Impact", "Clash Royale", "Brawl Stars"]
    opciones_todo = [""] + ["Redes: " + r for r in redes_sociales] + ["Juegos: " + j for j in juegos]

    col1, col2, col3, col4 = st.columns([3.5, 1.2, 1.2, 1])
    with col1:
        seleccion = st.selectbox("Elige plataforma", opciones_todo)
    with col2:
        horas = st.selectbox("Horas", list(range(0, 11)), index=1)
    with col3:
        minutos = st.selectbox("Minutos", [0, 15, 30, 45])
    with col4:
        if st.button("Agregar", use_container_width=True):
            if not seleccion:
                st.error("Elige una plataforma")
            elif horas == 0 and minutos == 0:
                st.error("Agrega al menos 15 min")
            else:
                nombre_limpio = seleccion.split(": ", 1)[1]
                total_horas = horas + (minutos / 60)
                st.session_state.redes.append({"plataforma": nombre_limpio, "horas": round(total_horas, 2)})
                st.success(f"Agregado: {nombre_limpio}")
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

    st.subheader("¿Qué tipo de contenido consumes más?")
    contenidos = {
        "Retos y tendencias": "Desafíos virales", "Comedia": "Videos graciosos", "Tutoriales": "Aprender algo",
        "Contenido tops": "Rankings y listas", "ASMR": "Sonidos relajantes", "Animales": "Mascotas tiernas",
        "Sincronización de labios": "Lip sync", "Proceso vs. resultado": "Antes y después",
        "Carruseles de contenido": "Comparaciones", "Contenido sobrio": "Info directa",
        "Recreación de diálogos": "Actuaciones virales", "Hashtag trends": "Tendencias del momento",
        "Consejos de expertos": "Tips profesionales", "Vlog de un día": "Mi rutina",
        "Detrás de cámaras": "Cómo lo hago", "Mini-documentales": "Historias cortas",
        "Curiosidades": "Datos interesantes", "Mi opinión sobre...": "Reviews",
        "Videos interactivos": "Pregunto a la audiencia"
    }
    contenido_fav = st.multiselect("Elige hasta 3", list(contenidos.keys()), max_selections=3)
    for c in contenido_fav:
        st.caption(f"_{contenidos[c]}_")

    st.subheader("¿Qué actividad te gustaría que organicemos?")
    actividad = st.text_area("", placeholder="Torneo, taller, cine, fiesta...", height=100)

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
        st.markdown("<h1 style='text-align: center; color:#e74c3c;'>¡GRACIAS POR PARTICIPAR!</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>Tus respuestas ya están guardadas</h2>", unsafe_allow_html=True)
        if st.button("Llenar otra encuesta"):
            st.session_state.redes = []
            st.session_state.enviado = False
            st.rerun()

# ========================================
# PESTAÑA 2: ESTADÍSTICAS (TODOS LOS Gráficos Y TABLA)
# ========================================
with tab2:
    st.header("Estadísticas en tiempo real")

    if not os.path.exists(ARCHIVO):
        st.info("Aún no hay respuestas. ¡Sé el primero!")
    else:
        df = pd.read_csv(ARCHIVO)

        # Asegurar columnas
        for col in ["fecha","nombre","carrera","whatsapp","total_horas","nivel","contenido","actividad_propuesta","plataformas"]:
            if col not in df.columns:
                df[col] = "Dato no registrado"

        # Métricas
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Participantes", len(df))
        with col2:
            avg = df['total_horas'].mean()
            st.metric("Promedio diario", f"{int(avg)}h {int((avg%1)*60)}min")
        with col3: st.metric("Nivel promedio", f"{df['nivel'].mean():.1f}/10")

        st.markdown("---")

        # 1. Participación por carrera
        st.subheader("1. Participación por carrera")
        fig, ax = plt.subplots(figsize=(10,6))
        sns.countplot(y='carrera', data=df, order=df['carrera'].value_counts().index, palette="viridis", ax=ax)
        ax.set_title("Carreras con más respuestas")
        st.pyplot(fig)
        plt.clf()

        # 2. Distribución de horas
        st.subheader("2. Horas diarias")
        fig2, ax2 = plt.subplots(figsize=(10,6))
        ax2.hist(df['total_horas'], bins=15, color="#e74c3c", edgecolor="black")
        ax2.axvline(avg, color="red", linestyle="--", label=f"Promedio: {avg:.1f}h")
        ax2.set_xlabel("Horas por día")
        ax2.legend()
        st.pyplot(fig2)
        plt.clf()

        # 3. Contenido más consumido (CORRECTO)
        st.subheader("3. Contenido más consumido")
        cont_list = []
        for c in df['contenido']:
            if pd.notna(c) and c not in ["Ninguno", "Dato no registrado"]:
                cont_list.extend([x.strip() for x in str(c).split("|")])
        if cont_list:
            top = pd.Series(cont_list).value_counts().head(8)
            fig3, ax3 = plt.subplots(figsize=(8,8))
            ax3.pie(top.values, labels=top.index, autopct="%1.1f%%", startangle=90)
            ax3.set_title("Top 8 tipos de contenido")
            st.pyplot(fig3)
            plt.clf()

        # 4. Carrera más adicta
        st.subheader("4. Carrera más adicta")
        adic = df.groupby('carrera')['nivel'].mean().sort_values(ascending=False)
        fig4, ax4 = plt.subplots(figsize=(10,6))
        sns.barplot(x=adic.values, y=adic.index, palette="rocket", ax=ax4)
        ax4.set_title("Nivel promedio por carrera")
        st.pyplot(fig4)
        plt.clf()

        # 5. Plataformas más usadas
        st.subheader("5. Plataformas más usadas")
        plat_list = []
        for p in df['plataformas']:
            try:
                items = eval(p)
                for item in items:
                    plat_list.append(item['plataforma'])
            except: pass
        if plat_list:
            top_plat = pd.Series(plat_list).value_counts().head(10)
            fig5, ax5 = plt.subplots(figsize=(10,6))
            sns.barplot(x=top_plat.values, y=top_plat.index, palette="mako", ax=ax5)
            ax5.set_title("Top 10 plataformas")
            st.pyplot(fig5)
            plt.clf()

        # Tabla completa
        st.markdown("---")
        st.subheader("Tabla completa de participantes")
        display = df[['nombre','carrera','whatsapp','total_horas','nivel','actividad_propuesta']].copy()
        display['total_horas'] = display['total_horas'].apply(lambda x: f"{int(x)}h {int((x%1)*60)}min")
        display.rename(columns={
            'nombre':'Nombre','carrera':'Carrera','whatsapp':'WhatsApp',
            'total_horas':'Tiempo diario','nivel':'Nivel (1-10)','actividad_propuesta':'Propuesta'
        }, inplace=True)
        st.dataframe(display, use_container_width=True)

        st.download_button("Descargar datos (CSV)", 
                          df.to_csv(index=False).encode('utf-8'),
                          "encuesta_completa.csv", "text/csv")
