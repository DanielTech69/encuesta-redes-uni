# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Encuesta Uso de Redes Sociales - Universidad", layout="centered")
st.title("Cuantos tiempo pasas realmente en redes sociales?")

st.markdown("""
Por favor responde con sinceridad. Esta encuesta es anonima pero nos ayuda a mejorar 
la experiencia universitaria y detectar casos de uso excesivo.
""")

# --- Datos personales ---
with st.expander("Tus datos (solo si quieres ayuda personalizada)", expanded=True):
    nombre = st.text_input("Nombre completo (opcional pero recomendado)")
    carrera = st.selectbox("Carrera que estudias", [
        "", "Ingenieria en Sistemas", "Medicina", "Derecho", "Psicologia", 
        "Administracion", "Arquitectura", "Diseno Grafico", "Otro"
    ])
    numero = st.text_input("Numero de WhatsApp (si necesitas ayuda para reducir el uso)")

# --- Redes sociales (ilimitadas) ---
st.subheader("Redes sociales que usas y tiempo diario")
if 'redes_temp' not in st.session_state:
    st.session_state.redes_temp = []

def agregar_red():
    red = st.session_state.nueva_red
    hora = st.session_state.nueva_hora
    if red and hora > 0:
        st.session_state.redes_temp.append({"red": red, "horas": hora})
        st.session_state.nueva_red = ""
        st.session_state.nueva_hora = 0

st.text_input("Nombre de la red social", key="nueva_red")
st.number_input("Horas diarias aproximadas (puedes usar decimales)", min_value=0.0, step=0.5, key="nueva_hora")
st.button("Agregar red social", on_click=agregar_red)

if st.session_state.redes_temp:
    st.write("### Tus redes agregadas:")
    total_horas = 0
    for item in st.session_state.redes_temp:
        st.write(f"- {item['red']}: {item['horas']} horas/dia")
        total_horas += item['horas']
    st.write(f"Total diario estimado: {total_horas:.2f} horas")

# --- Nivel de uso (10 niveles) ---
def calcular_nivel(horas_totales):
    if horas_totales <= 0.33: return 1   # 0-20 min
    elif horas_totales <= 1: return 2     # hasta 1h
    elif horas_totales <= 2: return 3
    elif horas_totales <= 3: return 4
    elif horas_totales <= 4: return 5
    elif horas_totales <= 5: return 6
    elif horas_totales <= 6: return 7
    elif horas_totales <= 7: return 8
    elif horas_totales <= 8: return 9
    else: return 10

if st.session_state.redes_temp:
    total_horas = sum(item['horas'] for item in st.session_state.redes_temp)
    nivel = calcular_nivel(total_horas)
    st.progress(nivel / 10)
    st.write(f"Nivel de uso actual: {nivel}/10")

    mensajes = {
        1: "Excelente! Tienes un uso muy saludable",
        2: "Muy bien, uso moderado y controlado",
        3: "Bien, pero podrias reducir un poco mas",
        4: "Uso moderado, empieza a poner limites",
        5: "Cuidado, estas en zona amarilla",
        6: "Alerta! Tu uso ya es alto",
        7: "Peligro: estas en zona roja",
        8: "Uso muy elevado, te afecta la productividad",
        9: "Adiccion severa detectada",
        10: "ADICCION CRITICA! Necesitas ayuda urgente"
    }
    st.warning(mensajes[nivel])

    if nivel >= 7:
        st.error(f"""
        Si sientes que no puedes controlar tu tiempo en redes, 
        escribeme al WhatsApp: 64193280 
        Te ayudo gratis a reducir el uso!
        """)

# --- Contenido mas visto ---
st.subheader("Que tipo de contenido consumes mas?")
opciones_contenido = [
    "Memes y humor", "Reels/TikToks bailes", "Tutoriales educativos", "Gaming/streams",
    "Noticias", "Deportes", "Belleza/moda", "Fitness/gimnasio", "Comida/recetas",
    "Viajes", "Musica", "Anime", "Politica", "Criptomonedas/inversiones",
    "Motivacion/superacion", "ASMR", "Reviews de productos", "Vlogs diarios",
    "Contenido religioso", "Otros"
]

contenido_fav = st.multiselect("Selecciona hasta 3 tipos de contenido que mas ves", opciones_contenido)

# --- Horario de mayor uso ---
st.subheader("En que horario usas mas las redes?")
hora_pico = st.slider("Hora del dia donde mas te conectas", 0, 23, 20)

# --- Enviar encuesta ---
if st.button("Enviar mi encuesta", type="primary"):
    if len(st.session_state.redes_temp) == 0:
        st.error("Agrega al menos una red social")
    else:
        total_horas = sum(item['horas'] for item in st.session_state.redes_temp)
        nivel = calcular_nivel(total_horas)
        datos = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "nombre": nombre or "Anonimo",
            "carrera": carrera,
            "numero": numero or "No proporcionado",
            "total_horas": round(total_horas, 2),
            "nivel": nivel,
            "hora_pico": hora_pico,
            "contenido_favorito": " | ".join(contenido_fav) if contenido_fav else "Ninguno",
            "redes_detalle": str(st.session_state.redes_temp)
        }
        
        # Guardar en CSV
        archivo = "datos_encuestas.csv"
        df_nuevo = pd.DataFrame([datos])
        if os.path.exists(archivo):
            df_nuevo.to_csv(archivo, mode='a', header=False, index=False)
        else:
            df_nuevo.to_csv(archivo, index=False)
        
        st.success("Encuesta enviada con exito! Gracias por participar")
        st.balloons()

        st.session_state.redes_temp = []

# === AÑADE ESTO AL FINAL DEL ARCHIVO (después del botón de enviar) ===

import matplotlib.pyplot as plt
import seaborn as sns

# Pestañas: Encuesta | Resultados
tab1, tab2 = st.tabs(["📊 Hacer la encuesta", "📈 Resultados generales"])

with tab1:
    # === TODO EL CÓDIGO QUE YA TENÍAS (hasta el final) ===
    # (pega aquí todo tu código original desde st.title hasta el final)
    pass  # (aquí va tu código original)

with tab2:
    st.header("Estadísticas generales de todas las encuestas")
    
    if not os.path.exists("datos_encuestas.csv"):
        st.warning("Aún no hay datos. Sé el primero en responder la encuesta!")
    else:
        df = pd.read_csv("datos_encuestas.csv")
        
        if len(df) == 0:
            st.warning("No hay datos todavía.")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Distribución por carrera")
                carrera_counts = df['carrera'].value_counts()
                fig1, ax1 = plt.subplots()
                sns.barplot(x=carrera_counts.values, y=carrera_counts.index, palette="viridis", ax=ax1)
                ax1.set_title("Número de respuestas por carrera")
                ax1.set_xlabel("Cantidad de estudiantes")
                st.pyplot(fig1)
                
                st.subheader("Nivel de uso (1-10)")
                nivel_counts = df['nivel'].value_counts().sort_index()
                fig2, ax2 = plt.subplots()
                bars = ax2.bar(nivel_counts.index, nivel_counts.values, color="#ff4444")
                ax2.set_xticks(range(1,11))
                ax2.set_title("Distribución del nivel de adicción")
                ax2.set_xlabel("Nivel (1 = muy bajo, 10 = crítico)")
                ax2.set_ylabel("Número de personas")
                # Colorear barras peligrosas
                for i in range(6,10):
                    bars[i].set_color('#ff0000')
                st.pyplot(fig2)

            with col2:
                st.subheader("Horas totales diarias promedio")
                avg_horas = df['total_horas'].mean()
                st.metric("Promedio de horas diarias", f"{avg_horas:.2f} h")
                
                st.subheader("Distribución de horas diarias")
                fig3, ax3 = plt.subplots()
                ax3.hist(df['total_horas'], bins=20, color="#6666ff", edgecolor='black')
                ax3.set_title("Histograma de horas diarias en redes sociales")
                ax3.set_xlabel("Horas por día")
                ax3.set_ylabel("Número de estudiantes")
                st.pyplot(fig3)
                
                st.subheader("Hora pico de uso")
                hora_counts = df['hora_pico'].value_counts().sort_index()
                fig4, ax4 = plt.subplots()
                ax4.bar(hora_counts.index, hora_counts.values, color="#00aa00")
                ax4.set_xticks(range(0,24,2))
                ax4.set_title("Hora del día con más uso")
                ax4.set_xlabel("Hora (formato 24h)")
                ax4.set_ylabel("Cantidad de personas")
                st.pyplot(fig4)

            # Contenido más visto
            st.subheader("Tipos de contenido más consumidos")
            contenido_lista = []
            for texto in df['contenido_favorito']:
                if texto != "Ninguno" and pd.notna(texto):
                    contenido_lista.extend([x.strip() for x in texto.split("|")])
            
            if contenido_lista:
                contenido_df = pd.Series(contenido_lista).value_counts().head(10)
                fig5, ax5 = plt.subplots()
                sns.barplot(x=contenido_df.values, y=contenido_df.index, palette="magma", ax=ax5)
                ax5.set_title("Top 10 tipos de contenido más vistos")
                st.pyplot(fig5)
            
            st.success(f"Total de encuestas recolectadas: {len(df)}")
