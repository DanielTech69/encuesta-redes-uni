# encuesta_universitaria_final.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Configuración
st.set_page_config(page_title="Redes vs Rendimiento - Uni", layout="wide")
st.title("¿Cuánto tiempo pasas en redes sociales y juegos?")
st.markdown("**Encuesta anónima universitaria** – Ayúdanos a mejorar la experiencia estudiantil")

ARCHIVO = "datos_encuesta_universitaria.csv"

# Inicializar session state
if 'redes' not in st.session_state:
    st.session_state.redes = []
if 'enviado' not in st.session_state:
    st.session_state.enviado = False

# --- Pestañas ---
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

    # === SEPARADAS: REDES SOCIALES ===
    redes_sociales = [
        "TikTok", "Instagram", "WhatsApp", "YouTube", "Facebook",
        "Twitter/X", "Snapchat", "Pinterest", "Telegram", "LinkedIn",
        "Reddit", "Discord", "BeReal", "Kwai", "Threads"
    ]

    # === SEPARADAS: JUEGOS ===
    juegos = [
        "Free Fire", "Call of Duty Mobile", "PUBG Mobile", "Roblox",
        "Minecraft", "Mobile Legends", "Among Us", "Genshin Impact",
        "Clash Royale", "Brawl Stars"
    ]

    # Unimos pero manteniendo orden visual
    opciones_todo = [""] + ["📱 " + r for r in redes_sociales] + ["🎮 " + j for j in juegos]

    col1, col2, col3, col4 = st.columns([3.5, 1.2, 1.2, 1])
    with col1:
        seleccion = st.selectbox("Elige red social o juego", opciones_todo, key="select_plataforma")
    with col2:
        horas = st.selectbox("Horas", list(range(0, 11)), index=1, key="h")
    with col3:
        minutos = st.selectbox("Minutos", [0, 15, 30, 45], key="m")
    with col4:
        if st.button("➕ Agregar", use_container_width=True):
            if not seleccion:
                st.error("Elige una plataforma")
            elif horas == 0 and minutos == 0:
                st.error("Agrega al menos 15 minutos")
            else:
                nombre_limpio = seleccion.replace("📱 ", "").replace("🎮 ", "")
                total_horas = horas + (minutos / 60)
                st.session_state.redes.append({"plataforma": nombre_limpio, "horas": round(total_horas, 2)})
                st.success(f"Agregado: {nombre_limpio} → {horas}h {minutos}min")
                st.rerun()

    # Mostrar lista agregada
    if st.session_state.redes:
        total_horas_dia = sum(r["horas"] for r in st.session_state.redes)
        st.markdown("### Tus plataformas:")
        for r in st.session_state.redes:
            h = int(r["horas"])
            m = int((r["horas"] - h) * 60)
            emoji = "🎮" if r["plataforma"] in juegos else "📱"
            st.write(f"{emoji} **{r['plataforma']}**: {h}h {m}min")
        st.info(f"**Total diario: {total_horas_dia:.2f} horas → {int(total_horas_dia)}h {int((total_horas_dia % 1)*60)}min**")

        # Nivel de adicción
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
            st.success(["¡Genial!", "Muy bien", "Controlado", "Saludable"][nivel-1])
        elif nivel <= 6:
            st.warning("Cuidado, estás cerca del límite")
        else:
            st.error("¡ALERTA! Uso muy alto. Necesitas ayuda urgente")
            st.error("Escríbeme al WhatsApp: **+591 6419-3280** – Te ayudo GRATIS")

    # === TIPOS DE CONTENIDO CON DESCRIPCIONES VISIBLES ===
    st.subheader("¿Qué tipo de contenido consumes más?")
    st.markdown("*Selecciona hasta 3 opciones*")

    contenidos = {
        "Retos y tendencias": "Participa en desafíos virales que están de moda.",
        "Comedia": "Sketches graciosos o videos de humor.",
        "Tutoriales": "Enseña algo útil: habilidades, productos o consejos rápidos.",
        "Contenido tops": "Listas como 'Top 5 cosas que no sabías sobre...'.",
        "ASMR": "Videos relajantes con sonidos suaves para calmar.",
        "Animales": "Mascotas, animales lindos o situaciones divertidas.",
        "Sincronización de labios": "Lip sync con audios populares o diálogos graciosos.",
        "Proceso vs. resultado": "Antes y después: maquillaje, remodelaciones, proyectos.",
        "Carruseles de contenido": "Comparaciones, 'lo bueno vs lo malo', mensajes impactantes.",
        "Contenido sobrio": "Información directa y clara, sin filtros.",
        "Recreación de diálogos": "Escenas de películas o series con audios virales.",
        "Hashtag trends": "Videos que siguen tendencias del momento.",
        "Consejos de expertos": "Trucos y tips de tu área de especialización.",
        "Vlog de un día": "Un día en tu vida o actividad interesante.",
        "Detrás de cámaras": "Cómo haces tus cosas o un día normal.",
        "Mini-documentales": "Historias cortas contadas de forma entretenida.",
        "Curiosidades": "Datos interesantes sobre cualquier tema.",
        "Mi opinión sobre...": "Opiniones respetuosas sobre productos, películas, temas.",
        "Videos interactivos": "Preguntas a la audiencia para que comenten."
    }

    # Mostrar todas las opciones con descripción en letra pequeña
    contenido_fav = st.multiselect(
        "Elige hasta 3 tipos de contenido que más ves",
        options=list(contenidos.keys()),
        max_selections=3
    )

    # Mostrar descripciones debajo
    for opcion in contenidos:
        if opcion in contenido_fav:
            st.caption(f"_{contenidos[opcion]}_")

    # === ACTIVIDAD EXTRACURRICULAR ===
    st.subheader("¿Qué actividad o evento te gustaría que organicemos en la universidad?")
    st.caption("_Ejemplos: Torneo de Free Fire, evento de anime, taller de cocina, cine al aire libre, feria de emprendedores, charlas motivacionales..._")
    actividad = st.text_area("", placeholder="Escribe tu propuesta aquí...", height=100)

    # === ENVIAR ===
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
            st.success("¡Encuesta enviada! Gracias por participar")
            st.balloons()
            st.session_state.redes = []
            st.rerun()

# ==========================================
# PESTAÑA ESTADÍSTICAS (CORREGIDA Y ROBUSTA)
# ==========================================
with tab2:
    st.header("Estadísticas Generales")

    if not os.path.exists(ARCHIVO):
        st.info("Aún no hay datos. ¡Comparte el enlace!")
    else:
        df = pd.read_csv(ARCHIVO)

        # === CORREGIR COLUMNAS FALTANTES (compatibilidad con archivos viejos) ===
        columnas_esperadas = ["fecha","nombre","carrera","whatsapp","total_horas","nivel","contenido","actividad_propuesta","plataformas"]
        for col in columnas_esperadas:
            if col not in df.columns:
                df[col] = "Dato no registrado"

        # Métricas principales
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Participantes", len(df))
        with col2:
            avg = df['total_horas'].mean()
            st.metric("Promedio diario", f"{int(avg)}h {int((avg%1)*60)}min")
        with col3: st.metric("Nivel promedio", f"{df['nivel'].mean():.1f}/10")

        st.markdown("---")

        # 1. Participación por carrera
        st.subheader("1. Participación por carrera")
        fig, ax = plt.subplots()
        sns.countplot(y='carrera', data=df, order=df['carrera'].value_counts().index, palette="viridis", ax=ax)
        ax.set_title("Carreras con más respuestas")
        st.pyplot(fig)

        # 2. Distribución de horas
        st.subheader("2. Horas diarias en redes y juegos")
        fig2, ax2 = plt.subplots()
        ax2.hist(df['total_horas'], bins=15, color="#e74c3c", edgecolor="black")
        ax2.axvline(avg, color="red", linestyle="--", label=f"Promedio: {avg:.2f}h")
        ax2.legend()
        st.pyplot(fig2)

        # 3. Contenido favorito
        st.subheader("3. Contenido más consumido")
        cont_list = []
        for c in df['contenido']:
            if c and c != "Ninguno" and c != "Dato no registrado":
                cont_list.extend([x.strip() for x in c.split("|")])
        if cont_list:
            top = pd.Series(cont_list).value_counts().head(8)
            fig3, ax3 = plt.subplots()
            ax3.pie(top.values, labels=top.index, autopct="%1.0f%%")
            ax3.set_title("Top 8 tipos de contenido")
            st.pyplot(fig3)

        # 4. Carrera más adicta
        st.subheader("4. Carrera más adicta a redes/juegos")
        adic = df.groupby('carrera')['nivel'].mean().sort_values(ascending=False)
        fig4, ax4 = plt.subplots()
        sns.barplot(x=adic.values, y=adic.index, palette="rocket", ax=ax4)
        ax4.set_title("Nivel promedio de adicción por carrera")
        st.pyplot(fig4)

        # 5. Plataformas más usadas
        st.subheader("5. Plataformas más usadas")
        plat_list = []
        for p in df['plataformas']:
            try:
                items = eval(p)
                for item in items:
                    plat_list.append(item['plataforma'])
            except:
                pass
        if plat_list:
            top_plat = pd.Series(plat_list).value_counts().head(10)
            fig5, ax5 = plt.subplots()
            sns.barplot(x=top_plat.values, y=top_plat.index, palette="mako", ax=ax5)
            ax5.set_title("Top 10 plataformas más usadas")
            st.pyplot(fig5)

        # Tabla final
        st.markdown("---")
        st.subheader("Tabla completa de participantes")
        display = df[['nombre', 'carrera', 'whatsapp', 'total_horas', 'nivel', 'actividad_propuesta']].copy()
        display['total_horas'] = display['total_horas'].apply(lambda x: f"{int(x)}h {int((x%1)*60)}min")
        display.rename(columns={
            'nombre': 'Nombre',
            'carrera': 'Carrera',
            'whatsapp': 'WhatsApp',
            'total_horas': 'Tiempo diario',
            'nivel': 'Nivel (1-10)',
            'actividad_propuesta': 'Actividad propuesta'
        }, inplace=True)
        st.dataframe(display, use_container_width=True)

        st.download_button("Descargar datos completos (CSV)", 
                         df.to_csv(index=False).encode('utf-8'),
                         "encuesta_completa.csv", "text/csv")
