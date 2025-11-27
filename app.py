# app.py - ENCUESTA PÚBLICA COMPLETA CON GRÁFICOS Y TABLA FINAL
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Encuesta Redes Sociales UNI", layout="centered")
st.title("¿Cuánto tiempo usas redes sociales? + ¿Qué evento quieres en la UNI?")
st.markdown("**Encuesta pública y anónima opcional** | Al final verás los resultados en vivo")

CSV_FILE = "datos_encuestas_publicas.csv"

# Crear archivo si no existe
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Nombre", "Carrera", "Número", "Redes_Horas", "Horas_Totales", 
                               "Contenido_Favorito", "Actividad_Sugerida", "Nivel", "Fecha"])
    df.to_csv(CSV_FILE, index=False)

contenidos = ["Memes", "Reels/TikTok", "Stories", "Fotos de amigos", "Tutoriales", "Deportes", 
              "Música", "Influencers", "Juegos", "Noticias", "Moda", "Comida", "Fitness", "Anime", "Otros"]

with st.form("encuesta"):
    st.subheader("Tus datos")
    nombre = st.text_input("Nombre completo (se mostrará públicamente)")
    carrera = st.selectbox("Carrera", ["Ingeniería de Sistemas", "Ingeniería Comercial", "Psicología", 
                                       "Derecho", "Arquitectura", "Medicina", "Otra"])
    numero = st.text_input("Tu número (opcional, se mostrará si lo pones)")

    st.subheader("Redes sociales + horas diarias")
    redes_input = st.text_area("Escribe tus redes y horas (una por línea)\nEjemplo:\nInstagram - 4 horas\nTikTok - 3 horas\nYouTube - 2 horas")
    
    st.subheader("Contenido que más ves")
    contenido = st.multiselect("Selecciona hasta 5", contenidos)

    st.subheader("¡Haz la UNI más divertida!")
    actividad = st.text_area("¿Qué actividad o evento te gustaría que organice la universidad? (fiesta, taller, torneo, cine, etc.)")

    enviado = st.form_submit_button("¡ENVIAR Y VER RESULTADOS EN VIVO!")

    if enviado:
        if not nombre or not redes_input:
            st.error("Nombre y redes+horas son obligatorios")
        else:
            # Procesar redes y horas
            lineas = [l.strip() for l in redes_input.split("\n") if l.strip()]
            horas_total = 0
            redes_lista = []
            for linea in lineas:
                if "-" in linea:
                    red = linea.split("-", 1)[0].strip()
                    try:
                        hora = float(linea.split("-")[1].strip().replace("horas", "").replace("h", ""))
                        horas_total += hora
                        redes_lista.append(f"{red}: {hora}h")
                    except:
                        pass
            redes_str = " | ".join(redes_lista) if redes_lista else "Ninguna"

            # Calcular nivel
            if horas_total <= 1: nivel = 1
            elif horas_total <= 2: nivel = 2
            elif horas_total <= 3: nivel = 3
            elif horas_total <= 4: nivel = 4
            elif horas_total <= 5: nivel = 5
            elif horas_total <= 7: nivel = 6
            elif horas_total <= 9: nivel = 7
            elif horas_total <= 11: nivel = 8
            elif horas_total <= 14: nivel = 9
            else: nivel = 10

            # Guardar
            nuevo = {
                "Nombre": nombre,
                "Carrera": carrera,
                "Número": numero if numero else "No dio",
                "Redes_Horas": redes_str,
                "Horas_Totales": round(horas_total, 1),
                "Contenido_Favorito": " | ".join(contenido),
                "Actividad_Sugerida": actividad.strip(),
                "Nivel": nivel,
                "Fecha": pd.Timestamp.now().strftime("%d/%m/%Y")
            }
            df = pd.read_csv(CSV_FILE)
            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            df.to_csv(CSV_FILE, index=False)

            st.success("¡Gracias por participar!")
            st.balloons()

            st.subheader(f"Tu nivel de uso: **{nivel}/10** → {horas_total:.1f} horas diarias")
            if nivel >= 7:
                st.error("¡Cuidado! Tu uso es alto. Si quieres ayuda: +591 64143280 (Daniel)")

            # =================== GRÁFICOS Y TABLA PÚBLICA ===================
            st.markdown("---")
            st.header("RESULTADOS EN VIVO DE TODA LA UNIVERSIDAD")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total estudiantes", len(df))
            with col2:
                st.metric("Horas promedio diarias", round(df["Horas_Totales"].mean(), 1))

            # Gráfico 1: Participación por carrera
            carrera_count = df["Carrera"].value_counts()
            fig1 = px.bar(x=carrera_count.index, y=carrera_count.values, 
                          title="Participación por carrera", labels={"x": "Carrera", "y": "Estudiantes"})
            st.plotly_chart(fig1, use_container_width=True)

            # Gráfico 2: Niveles de adicción
            nivel_count = df["Nivel"].value_counts().sort_index()
            fig2 = px.bar(x=nivel_count.index, y=nivel_count.values, 
                          title="¿Cuántos estudiantes están en cada nivel?", 
                          labels={"x": "Nivel (1-10)", "y": "Cantidad"})
            st.plotly_chart(fig2, use_container_width=True)

            # Gráfico 3: Contenido favorito
            contenido_flat = df["Contenido_Favorito"].str.split(" | ", expand=True).stack()
            top_contenido = contenido_flat.value_counts().head(10)
            fig3 = px.pie(values=top_contenido.values, names=top_contenido.index, 
                          title="Contenido que más ven los estudiantes")
            st.plotly_chart(fig3, use_container_width=True)

            # Tabla pública completa
            st.subheader("Todos los que participaron (público)")
            df_display = df[["Nombre", "Carrera", "Número", "Nivel", "Actividad_Sugerida"]].copy()
            df_display["Nivel"] = df_display["Nivel"].astype(int)
            st.dataframe(df_display, use_container_width=True)

            st.info("¡Estos datos se actualizan SOLO con cada nueva respuesta! Comparte el link para que todos vean cómo estamos como universidad.")
