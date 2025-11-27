# encuesta_universitaria.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Configuración
st.set_page_config(page_title="Redes vs Rendimiento - U", layout="wide")
st.title("¿Cuánto tiempo pasas realmente en redes sociales?")
st.markdown("**Encuesta anónima universitaria** – Ayúdanos a mejorar tu experiencia y la publicidad de la universidad")

ARCHIVO = "datos_encuesta_universitaria.csv"

# Inicializar session state
if 'redes' not in st.session_state:
    st.session_state.redes = []
if 'enviado' not in st.session_state:
    st.session_state.enviado = False

# --- Pestañas ---
tab1, tab2 = st.tabs(["Encuesta", "Estadísticas y Recomendaciones"])

with tab1:
    st.header("Completa la encuesta")

    with st.expander("Tus datos (para ayuda personalizada y estadísticas)", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre completo (opcional pero recomendado)")
            carrera = st.selectbox("Carrera que estudias", [
                "", "Ingeniería en Sistemas", "Medicina", "Derecho", "Psicología", "Administración",
                "Arquitectura", "Diseño Gráfico", "Contaduría", "Enfermería", "Otro"
            ])
        with col2:
            numero = st.text_input("Tu WhatsApp (si necesitas ayuda para reducir el uso)")

    st.subheader("Redes sociales que usas y horas diarias")
    st.markdown("*Puedes agregar todas las que uses*")

    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        nueva_red = st.text_input("Nombre de la red social", key="input_red")
    with col2:
        nuevas_horas = st.number_input("Horas diarias (ej: 3.5)", min_value=0.0, step=0.5, key="input_horas")
    with col3:
        if st.button("➕ Agregar", use_container_width=True):
            if nueva_red and nuevas_horas > 0:
                st.session_state.redes.append({"red": nueva_red.strip().title(), "horas": nuevas_horas})
                st.success(f"Agregado: {nueva_red} – {nuevas_horas}h")
                st.rerun()
            else:
                st.error("Completa ambos campos")

    # Mostrar redes agregadas
    if st.session_state.redes:
        total_horas = sum(r["horas"] for r in st.session_state.redes)
        st.write("### Tus redes:")
        for r in st.session_state.redes:
            st.write(f"• **{r['red']}**: {r['horas']} horas/día")
        st.info(f"**Total diario: {total_horas:.2f} horas**")

        # Nivel de uso (1 a 10)
        def nivel_uso(horas):
            if horas <= 0.33: return 1
            elif horas <= 1: return 2
            elif horas <= 2: return 3
            elif horas <= 3: return 4
            elif horas <= 4: return 5
            elif horas <= 5: return 6
            elif horas <= 6: return 7
            elif horas <= 7: return 8
            elif horas <= 8: return 9
            else: return 10

        nivel = nivel_uso(total_horas)
        st.progress(nivel / 10)
        st.write(f"### Tu nivel de uso: **{nivel}/10**")

        mensajes = {
            1: "¡Excelente! Uso muy saludable",
            2: "Muy bien, tienes control total",
            3: "Bien, pero puedes mejorar",
            4: "Moderado, empieza a poner límites",
            5: "Cuidado, estás en zona amarilla",
            6: "Alerta: uso alto detectado",
            7: "Peligro: estás en zona roja",
            8: "Muy elevado: afecta tu productividad",
            9: "Adicción severa detectada",
            10: "¡ADICCIÓN CRÍTICA! Necesitas ayuda urgente"
        }
        if nivel <= 4:
            st.success(mensajes[nivel])
        elif nivel <= 6:
            st.warning(mensajes[nivel])
        else:
            st.error(mensajes[nivel])
            st.error(f"""
            Si sientes que no puedes controlar tu tiempo en redes, 
            escríbeme al WhatsApp: **+591 6419-3280**  
            Te ayudo **GRATIS** a reducir el uso y recuperar tu tiempo
            """)

    # Contenido más visto
    st.subheader("¿Qué tipo de contenido consumes más?")
    contenidos = [
        "Memes y humor", "Reels/TikToks de baile", "Tutoriales educativos", "Gaming/Streams",
        "Noticias", "Deportes", "Belle ferritin/moda", "Fitness/gimnasio", "Comida/recetas",
        "Viajes", "Música", "Anime", "Política", "Cripto/Inversiones", "Motivación",
        "ASMR", "Reviews de productos", "Vlogs diarios", "Contenido religioso", "Otros"
    ]
    contenido_fav = st.multiselect("Selecciona hasta 3 tipos que más ves", contenidos, max_selections=3)

    # Hora pico
    st.subheader("¿A qué hora del día usas más las redes?")
    hora_pico = st.slider("Hora donde más te conectas", 0, 23, 20)

    # Enviar
    if st.button("Enviar mi encuesta", type="primary", use_container_width=True):
        if len(st.session_state.redes) == 0:
            st.error("Agrega al menos una red social")
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
                "hora_pico": hora_pico,
                "contenido": " | ".join(contenido_fav) if contenido_fav else "Ninguno",
                "redes": str(st.session_state.redes)
            }

            df_nuevo = pd.DataFrame([datos])
            if os.path.exists(ARCHIVO):
                df_nuevo.to_csv(ARCHIVO, mode='a', header=False, index=False)
            else:
                df_nuevo.to_csv(ARCHIVO, index=False)

            st.success("¡Encuesta enviada con éxito! Gracias por ayudarnos a mejorar")
            st.balloons()
            st.session_state.enviado = True
            st.session_state.redes = []

# =============================================
# ESTADÍSTICAS Y RECOMENDACIONES
# =============================================
with tab2:
    st.header("Estadísticas Generales y Recomendaciones de Publicidad")

    if not os.path.exists(ARCHIVO):
        st.info("Aún no hay datos. Comparte el enlace para empezar a recolectar respuestas.")
    else:
        df = pd.read_csv(ARCHIVO)

        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Total estudiantes", len(df))
        with col2: st.metric("Promedio horas/día", f"{df['total_horas'].mean():.2f}")
        with col3: st.metric("Nivel promedio", f"{df['nivel'].mean():.1f}/10")
        with col4: st.metric("Hora pico", f"{int(df['hora_pico'].mode()[0])}:00 h")

        # Gráficos
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Redes sociales más usadas")
            redes_lista = []
            for redes_str in df['redes']:
                try:
                    redes = eval(redes_str)
                    for r in redes:
                        redes_lista.append(r['red'])
                except:
                    pass
            if redes_lista:
                top_redes = pd.Series(redes_lista).value_counts().head(8)
                fig, ax = plt.subplots()
                sns.barplot(x=top_redes.values, y=top_redes.index, palette="rocket", ax=ax)
                ax.set_title("Top 8 redes más usadas")
                st.pyplot(fig)

            st.subheader("Contenido más consumido")
            contenido_lista = []
            for c in df['contenido']:
                if c != "Ninguno":
                    contenido_lista.extend([x.strip() for x in c.split("|")])
            if contenido_lista:
                top_contenido = pd.Series(contenido_lista).value_counts().head(10)
                fig2, ax2 = plt.subplots()
                ax2.pie(top_contenido.values, labels=top_contenido.index, autopct='%1.0f%%', startangle=90)
                ax2.set_title("Top 10 contenidos más vistos")
                st.pyplot(fig2)

        with c2:
            st.subheader("Distribución de horas diarias")
            fig3, ax3 = plt.subplots()
            ax3.hist(df['total_horas'], bins=15, color="#ff6b6b", edgecolor='black')
            ax3.set_xlabel("Horas por día")
            ax3.set_ylabel("Estudiantes")
            ax3.set_title("¿Cuántas horas pasan en redes?")
            st.pyplot(fig3)

            st.subheader("Hora pico de conexión")
            hora_counts = df['hora_pico'].value_counts().sort_index()
            fig4, ax4 = plt.subplots()
            ax4.bar(hora_counts.index, hora_counts.values, color="#4ecdc4")
            ax4.set_xticks(range(0, 24, 2))
            ax4.set_xlabel("Hora del día")
            ax4.set_title("Mejor hora para publicar")
            st.pyplot(fig4)

        # RECOMENDACIONES AUTOMÁTICAS
        st.markdown("---")
        st.subheader("Recomendaciones de Publicidad para la Universidad")
        st.success("""
        **Basado en los datos recolectados:**
        - **Mejor hora para publicar**: entre las **{0} y {1} horas**
        - **Formato ideal**: Reels/TikToks cortos de **15-30 segundos** (contenido #{2})
        - **Frecuencia recomendada**: 4-6 publicaciones por semana (3 videos + 3 fotos)
        - **Temas que más enganchan**: {3}, {4}, {5}
        - **Red principal para invertir publicidad**: **{6}**
        """.format(
            int(df['hora_pico'].mode()[0])-1,
            int(df['hora_pico'].mode()[0])+1,
            pd.Series(contenido_lista).value_counts().index[0],
            pd.Series(contenido_lista).value_counts().index[0],
            pd.Series(contenido_lista).value_counts().index[1] if len(pd.Series(contenido_lista).value_counts()) > 1 else "N/A",
            pd.Series(contenido_lista).value_counts().index[2] if len(pd.Series(contenido_lista).value_counts()) > 2 else "N/A",
            pd.Series(redes_lista).value_counts().index[0]
        ))

        if st.button("Descargar todos los datos (CSV)"):
            st.download_button("Descargar CSV completo", df.to_csv(index=False), "datos_encuesta.csv", "text/csv")
