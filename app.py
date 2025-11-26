# app.py
# cuestionario_bolivia.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Cuestionario: Historia de Bolivia", layout="centered")
st.title("¿Cuánto sabes de la Historia de Bolivia?")
st.markdown("### 10 preguntas de opción múltiple • Responde y ve las estadísticas en tiempo real")

# Archivo donde se guardan todas las respuestas
ARCHIVO = "resultados_historia_bolivia.csv"

# ==================== LAS 10 PREGUNTAS ====================
preguntas = [
    {
        "pregunta": "¿En qué año se fundó la República de Bolivia?",
        "opciones": ["1825", "1826", "1830", "1809"],
        "correcta": "1825",
        "idx_correcta": 0
    },
    {
        "pregunta": "¿Quién fue el primer presidente de Bolivia?",
        "opciones": ["Andrés de Santa Cruz", "Antonio José de Sucre", "Simón Bolívar", "José Ballivián"],
        "correcta": "Antonio José de Sucre",
        "idx_correcta": 1
    },
    {
        "pregunta": "¿Cómo se llamó originalmente Bolivia cuando se independizó?",
        "opciones": ["República Bolívar", "Alto Perú", "República de Charcas", "República de Sucre"],
        "correcta": "República Bolívar",
        "idx_correcta": 0
    },
    {
        "pregunta": "¿En qué guerra Bolivia perdió su salida al mar?",
        "opciones": ["Guerra del Acre", "Guerra del Chaco", "Guerra del Pacífico", "Guerra de la Independencia"],
        "correcta": "Guerra del Pacífico",
        "idx_correcta": 2
    },
    {
        "pregunta": "¿Qué país invadió Bolivia en la Guerra del Pacífico (1879)?",
        "opciones": ["Perú", "Argentina", "Chile", "Brasil"],
        "correcta": "Chile",
        "idx_correcta": 2
    },
    {
        "pregunta": "¿Quién fue conocido como el 'Mariscal de Zepita'?",
        "opciones": ["Andrés de Santa Cruz", "Antonio José de Sucre", "José de San Martín", "Manuel Isidoro Belzu"],
        "correcta": "Antonio José de Sucre",
        "idx_correcta": 1
    },
    {
        "pregunta": "¿En qué año ocurrió la Revolución del 52 liderada por el MNR?",
        "opciones": ["1945", "1952", "1932", "1964"],
        "correcta": "1952",
        "idx_correcta": 1
    },
    {
        "pregunta": "¿Qué presidente boliviano nacionalizó los hidrocarburos en 1937?",
        "opciones": ["Gualberto Villarroel", "David Toro", "Germán Busch", "Hernando Siles"],
        "correcta": "Germán Busch",
        "idx_correcta": 2
    },
    {
        "pregunta": "¿Cuál es el nombre del héroe indígena que lideró la rebelión de 1781?",
        "opciones": ["Andrés Tupac Amaru", "Túpac Katari", "Bartolina Sisa", "Zárate Willka"],
        "correcta": "Túpac Katari",
        "idx_correcta": 1
    },
    {
        "pregunta": "¿En qué ciudad se firmó el Acta de Independencia de Bolivia el 6 de agosto de 1825?",
        "opciones": ["Sucre (Chuquisaca)", "La Paz", "Cochabamba", "Potosi"],
        "correcta": "Sucre (Chuquisaca)",
        "idx_correcta": 0
    }
]

# Inicializar estado
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = [None] * len(preguntas)
if 'enviado' not in st.session_state:
    st.session_state.enviado = False
if 'nombre' not in st.session_state:
    st.session_state.nombre = ""

# === FORMULARIO ===
with st.form(key="cuestionario"):
    st.text_input("Tu nombre (opcional)", key="nombre")
    
    for i, p in enumerate(preguntas):
        st.subheader(f"Pregunta {i+1}/10")
        st.write(p["pregunta"])
        st.session_state.respuestas[i] = st.radio(
            "Selecciona tu respuesta:",
            options=p["opciones"],
            index=None,
            key=f"preg{i}"
        )
    
    submit = st.form_submit_button("¡Enviar mis respuestas!", type="primary")

# === PROCESAR ENVÍO ===
if submit:
    if None in st.session_state.respuestas:
        st.error("Por favor responde todas las preguntas")
    else:
        # Calcular puntaje
        correctas = sum(1 for i, resp in enumerate(st.session_state.respuestas)
                       if resp == preguntas[i]["correcta"])
        
        st.session_state.enviado = True
        st.success(f"¡Listo {st.session_state.nombre or 'amigo'}! Acertaste {correctas} de 10")

        # Guardar respuesta en CSV
        registro = {"fecha": datetime.now().strftime("%Y-%m-%d %H:%M")}
        registro["nombre"] = st.session_state.nombre or "Anónimo"
        registro["puntaje"] = correctas
        
        for i in range(10):
            registro[f"pregunta_{i+1}"] = st.session_state.respuestas[i]
            registro[f"correcta_{i+1}"] = (st.session_state.respuestas[i] == preguntas[i]["correcta"])
        
        df_nuevo = pd.DataFrame([registro])
        if ARCHIVO in os.listdir():
            df_nuevo.to_csv(ARCHIVO, mode='a', header=False, index=False)
        else:
            df_nuevo.to_csv(ARCHIVO, index=False)
        
        st.balloons()

# === ESTADÍSTICAS (solo después de enviar o si ya hay datos) ===
if st.session_state.enviado or ARCHIVO in os.listdir():
    st.markdown("---")
    st.header("Estadísticas generales (todos los participantes)")
    
    if ARCHIVO not in os.listdir():
        st.info("Aún no hay respuestas guardadas.")
    else:
        df = pd.read_csv(ARCHIVO)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total participantes", len(df))
        with col2:
            st.metric("Promedio de aciertos", f"{df['puntaje'].mean():.1f}/10")
        
        # Gráficos por pregunta
        for i in range(10):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(f"Pregunta {i+1}")
                st.write(preguntas[i]["pregunta"][:80] + "...")
                
                # Conteo de respuestas
                respuestas_col = df[f"pregunta_{i+1}"]
                conteo = respuestas_col.value_counts()
                
                # Gráfico de tarta (pie chart)
                fig_pie, ax_pie = plt.subplots(figsize=(5,5))
                colores = ["#ff9999" if opt != preguntas[i]["correcta"] else "#66b3ff" 
                          for opt in conteo.index]
                wedges, texts, autotexts = ax_pie.pie(
                    conteo.values, labels=conteo.index, autopct='%1.0f%%',
                    colors=colores, startangle=90
                )
                # Resaltar la correcta
                wedges[preguntas[i]["idx_correcta"]].set_edgecolor('darkblue')
                wedges[preguntas[i]["idx_correcta"]].set_linewidth(3)
                ax_pie.set_title(f"Respuestas pregunta {i+1}")
                st.pyplot(fig_pie)
            
            with col2:
                st.write(" ")  # espacio
                st.write(" ")  # espacio
                # Barra de aciertos
                aciertos = df[f"correcta_{i+1}"].sum()
                errores = len(df) - aciertos
                fig_bar, ax_bar = plt.subplots(figsize=(5,4))
                ax_bar.bar(["Correctas", "Incorrectas"], [aciertos, errores], 
                          color=["#66b3ff", "#ff9999"])
                ax_bar.set_title(f"Aciertos pregunta {i+1}")
                ax_bar.set_ylabel("Personas")
                for j, v in enumerate([aciertos, errores]):
                    ax_bar.text(j, v + 0.5, str(v), ha='center', fontweight='bold')
                st.pyplot(fig_bar)

        # Puntaje general
        st.markdown("---")
        st.subheader("Distribución general de puntajes")
        fig_final, ax_final = plt.subplots()
        df['puntaje'].value_counts().sort_index().plot(kind='bar', ax=ax_final, color="#9966ff")
        ax_final.set_xlabel("Número de aciertos")
        ax_final.set_ylabel("Cantidad de personas")
        ax_final.set_title("¿Cuántos saben de Historia de Bolivia?")
        st.pyplot(fig_final)
