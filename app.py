# encuesta_universitaria_v2.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Redes vs Rendimiento - Universidad", layout="wide")
st.title("¿Cuánto tiempo pasas realmente en redes sociales?")
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
    
    with st.expander("Tus datos (para estadísticas y ayuda personalizada)", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre completo (opcional pero recomendado para reconocerte)", value="")
            carrera = st.selectbox("Carrera que estudias", [
                "", 
                "Ingeniería en Sistemas", 
                "Ingeniería Comercial", 
                "Parvularia", 
                "Contaduría", 
                "Gastronomía", 
                "Ciencias de la Educación", 
                "Derecho"
            ])
        with col2:
            numero = st.text_input("Tu WhatsApp (si necesitas ayuda para reducir el uso)", placeholder="Ej: 76543210")

    st.subheader("Redes sociales y juegos que usas diariamente")
    st.markdown("*Selecciona las que usas y cuántas horas + minutos pasas en cada una*")

    # Lista de 20 redes/juegos más populares en Bolivia y Latam (2025)
    redes_populares = [
        "TikTok", "Instagram", "WhatsApp", "YouTube", "Facebook", 
        "Free Fire", "Facebook Gaming", "Twitch", "Discord", "Twitter/X",
        "Pinterest", "Snapchat", "Reddit", "Telegram", "LinkedIn",
        "Roblox", "Minecraft", "Call of Duty Mobile", "PUBG Mobile", "Kwai"
    ]

    col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 1])
    with col1:
        red_seleccionada = st.selectbox("Elige la red social o juego", [""] + redes_populares, key="select_red")
    with col2:
        horas = st.selectbox("Horas", list(range(0, 11)), key="select_horas")
    with col3:
        minutos = st.selectbox("Minutos", [0, 15, 30, 45], key="select_minutos")
    with col4:
        if st.button("➕ Agregar", use_container_width=True):
            if red_seleccionada and (horas > 0 or minutos > 0):
                total_horas = horas + (minutos / 60)
                st.session_state.redes.append({
                    "red": red_seleccionada,
                    "horas": round(total_horas, 2)
                })
                st.success(f"Agregado: {red_seleccionada} – {horas}h {minutos}min")
                st.rerun()
            else:
                st.error("Selecciona una red y al menos algo de tiempo")

    # Mostrar redes agregadas
    if st.session_state.redes:
        total_horas = sum(r["horas"] for r in st.session_state.redes)
        st.write("### Tus redes agregadas:")
        for r in st.session_state.redes:
            h = int(r["horas"])
            m = int((r["horas"] - h) * 60)
            st.write(f"• **{r['red']}**: {h}h {m}min")
        
        st.info(f"**Total diario: {total_horas:.2f} horas ({int(total_horas)}h {int((total_horas - int(total_horas)) * 60)}min)**")

        # Nivel de uso (1 a 10)
        def nivel_uso(horas):
            if horas <= 1: return 1
            elif horas <= 2: return 2
            elif horas <= 3: return 3
            elif horas <= 4: return 4
            elif horas <= 5: return 5
            elif horas <= 6: return 6
            elif horas <= 7.5: return 7
            elif horas <= 9: return 8
            elif horas <= 11: return 9
            else: return 10

        nivel = nivel_uso(total_horas)
        st.progress(nivel / 10)
        st.write(f"### Tu nivel de uso: **{nivel}/10**")

        mensajes = {
            1: "¡Excelente! Uso muy saludable",
            2: "Muy bien, tienes control total",
            3: "Bien, puedes mejorar un poco",
            4: "Moderado, empieza a poner límites",
            5: "Cuidado, zona amarilla",
            6: "Alerta: uso alto detectado",
            7: "Peligro: estás en zona roja",
            8: "Muy elevado: afecta tu productividad",
            9: "Adicción severa detectada",
            10: "¡ADICCIÓN CRÍTICA! Necesitas ayuda urgente"
        }
        color = "success" if nivel <= 4 else "warning" if nivel <= 6 else "error"
        st.markdown(f"<p style='color:{'green' if nivel<=4 else 'orange' if nivel<=6 else 'red'}; font-size:18px'><b>{mensajes[nivel]}</b></p>", unsafe_allow_html=True)

        if nivel >= 7:
            st.error(f"""
            Si sientes que no puedes controlar tu tiempo en redes,
            escríbeme al WhatsApp: **+591 6419-3280**
            Te ayudo **GRATIS** a recuperar tu tiempo y mejorar tu rendimiento
            """)

    # Contenido más consumido (con descripciones pequeñas)
    st.subheader("¿Qué tipo de contenido consumes más en redes?")
    st.markdown("*Selecciona hasta 3 que más veas*")

    contenidos = {
        "Retos y tendencias": "Participa en desafíos virales que están de moda.",
        "Comedia": "Sketches graciosos o videos de humor.",
        "Tutoriales": "Enseña algo útil: habilidades, productos o consejos rápidos.",
        "Contenido tops": "Listas como 'Top 5 cosas que no sabías sobre...'",
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

    contenido_fav = st.multiselect(
        "Elige hasta 3 tipos de contenido",
        options=list(contenidos.keys()),
        max_selections=3,
        help="Pasa el mouse sobre cada opción para ver su descripción"
    )

    # Mostrar descripción al seleccionar
    for c in contenido_fav:
        st.caption(f"*{c}: {contenidos[c]}*")

    # Nueva pregunta: Actividad extracurricular
    st.subheader("¿Qué actividad extracurricular o evento te gustaría que organice la universidad?")
    st.caption("*Ej examples: Evento de anime, torneo de Free Fire, taller de cocina, feria de emprendedores, cine al aire libre, etc.*")
    actividad_propuesta = st.text_area("", placeholder="Escribe tu idea aquí...", height=100)

    # Enviar encuesta
    if st.button("Enviar mi encuesta", type="primary", use_container_width=True):
        if len(st.session_state.redes) == 0:
            st.error("Agrega al menos una red social o juego")
        elif not carrera:
            st.error("Selecciona tu carrera")
        else:
            total_horas = sum(r["horas"] for r in st.session_state.redes)
            nivel = nivel_uso(total_horas)
            datos = {
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "nombre": nombre or "Anónimo",
                "carrera": carrera,
                "whatsapp": numero or "No dado",
                "total_horas": round(total_horas, 2),
                "nivel": nivel,
                "contenido": " | ".join(contenido_fav) if contenido_fav else "Ninguno",
                "actividad_propuesta": actividad_propuesta.strip() or "Ninguna sugerencia",
                "redes": str(st.session_state.redes)
            }
            df_nuevo = pd.DataFrame([datos])
            if os.path.exists(ARCHIVO):
                df_nuevo.to_csv(ARCHIVO, mode='a', header=False, index=False)
            else:
                df_nuevo.to_csv(ARCHIVO, index=False)
            
            st.success("¡Encuesta enviada con éxito! Gracias por participar 🎉")
            st.balloons()
            st.session_state.enviado = True
            st.session_state.redes = []
            st.rerun()

# =============================================
# PESTAÑA DE ESTADÍSTICAS
# =============================================
with tab2:
    st.header("Estadísticas Generales de la Universidad")
    
    if not os.path.exists(ARCHIVO):
        st.info("Aún no hay respuestas. ¡Comparte el enlace para empezar!")
    else:
        df = pd.read_csv(ARCHIVO)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total participantes", len(df))
        with col2:
            avg_h = df['total_horas'].mean()
            avg_h_entero = int(avg_h)
            avg_min = int((avg_h - avg_h_entero) * 60)
            st.metric("Promedio diario", f"{avg_h_entero}h {avg_min}min")
        with col3:
            st.metric("Nivel promedio de adicción", f"{df['nivel'].mean():.1f}/10")

        st.markdown("---")

        # 1. Carreras con más participación
        st.subheader("1. Participación por carrera")
        carrera_counts = df['carrera'].value_counts()
        fig, ax = plt.subplots()
        sns.barplot(x=carrera_counts.values, y=carrera_counts.index, palette="viridis")
        ax.set_title("¿Qué carrera participó más?")
        st.pyplot(fig)

        # 2. Promedio de horas totales
        st.subheader("2. Horas promedio en redes sociales")
        fig2, ax2 = plt.subplots()
        ax2.hist(df['total_horas'], bins=15, color="#ff6b6b", edgecolor='black')
        ax2.axvline(avg_h, color='red', linestyle='--', label=f'Promedio: {avg_h:.2f}h')
        ax2.legend()
        ax2.set_xlabel("Horas por día")
        ax2.set_title("Distribución del uso de redes")
        st.pyplot(fig2)

        # 3. Contenido más visto
        st.subheader("3. Contenido más consumido")
        contenido_lista = []
        for c in df['contenido']:
            if c != "Ninguno":
                contenido_lista.extend([x.strip() for x in c.split("|")])
        if contenido_lista:
            top_cont = pd.Series(contenido_lista).value_counts().head(8)
            fig3, ax3 = plt.subplots()
            ax3.pie(top_cont.values, labels=top_cont.index, autopct='%1.0f%%', startangle=90)
            ax3.set_title("Top 8 contenidos más populares")
            st.pyplot(fig3)

        # 4. Carrera más adicta
        st.subheader("4. ¿Qué carrera es la más adicta a las redes?")
        adiccion_por_carrera = df.groupby('carrera')['nivel'].mean().sort_values(ascending=False)
        fig4, ax4 = plt.subplots()
        sns.barplot(x=adiccion_por_carrera.values, y=adiccion_por_carrera.index, palette="rocket")
        ax4.set_title("Nivel promedio de adicción por carrera")
        st.pyplot(fig4)

        # 5. Redes más usadas
        st.subheader("5. Redes sociales más usadas en la universidad")
        redes_lista = []
        for redes_str in df['redes']:
            try:
                redes = eval(redes_str)
                for r in redes:
                    redes_lista.append(r['red'])
            except:
                pass
        if redes_lista:
            top_redes = pd.Series(redes_lista).value_counts().head(10)
            fig5, ax5 = plt.subplots()
            sns.barplot(x=top_redes.values, y=top_redes.index, palette="mako")
            ax5.set_title("Top 10 redes/juegos más usados")
            st.pyplot(fig5)

        st.markdown("---")
        st.subheader("Tabla completa de participantes")
        df_display = df[['nombre', 'carrera', 'whatsapp', 'total_horas', 'nivel', 'actividad_propuesta']].copy()
        df_display['total_horas'] = df_display['total_horas'].apply(lambda x: f"{int(x)}h {int((x - int(x))*60)}min")
        df_display.rename(columns={
            'nombre': 'Nombre',
            'carrera': 'Carrera',
            'whatsapp': 'WhatsApp',
            'total_horas': 'Tiempo diario',
            'nivel': 'Nivel adicción (/10)',
            'actividad_propuesta': 'Actividad propuesta'
        }, inplace=True)
        st.dataframe(df_display, use_container_width=True)

        # Botón de descarga
        st.download_button(
            "📥 Descargar todos los datos (CSV)",
            df.to_csv(index=False).encode('utf-8'),
            "encuesta_universitaria_completa.csv",
            "text/csv"
        )
