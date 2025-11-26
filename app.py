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
