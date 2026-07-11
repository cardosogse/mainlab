import streamlit as st
import random
from database import guardar_registro_juego

ESCENARIOS_D3 = [
    {"caso": "Unión intermolecular entre dos moléculas de agua (H₂O - H₂O).", "fuerza": "Puentes de Hidrógeno", "razon": "El H positivo atrae al par libre del Oxígeno."},
    {"caso": "Colas de ácidos grasos interactuando en el centro de la membrana celular.", "fuerza": "Van der Waals", "razon": "Regiones apolares unidas por dispersión débil."},
    {"caso": "Un ión de Sodio (Na⁺) rodeado por moléculas de agua en el plasma.", "fuerza": "Ion-Dipolo", "razon": "La carga total del ión atrae a los polos parciales del agua."}
]

def inicializar_estado():
    if "d3_juego_score" not in st.session_state:
        st.session_state.d3_juego_score = 0
    if "d3_juego_intentos" not in st.session_state:
        st.session_state.d3_juego_intentos = 0
    if "d3_quiz_enviado" not in st.session_state:
        st.session_state.d3_quiz_enviado = False
    if "d3_escenario_actual" not in st.session_state:
        st.session_state.d3_escenario_actual = random.choice(ESCENARIOS_D3)

def app():
    st.title("🧊 Día 3: Fuerzas y Red del Agua")
    inicializar_estado()
    enfoque = st.radio("Selecciona tu enfoque de análisis:", ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], horizontal=True, key="d3_enfoque")
    tab1, tab2, tab3 = st.tabs(["🔬 Red Térmica del Agua", "🎮 Juego: Fuerzas Cruzadas", "📝 Quiz de Certificación"])

    with tab1:
        st.header("Fundamentos: El Dipolo")
        st.info("Puente de Hidrógeno: Interacción electrostática crucial para la alta tensión superficial y calor específico del agua.")
        temp = st.slider("Temperatura (°C)", min_value=-10, max_value=120, value=25)

        if temp < 0:
            estado, color, css = "Sólido (Hielo)", "#a0c4ff", "display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; padding: 20px;"
        elif temp < 100:
            estado, color, css = "Líquido (Agua)", "#4facfe", "display: flex; flex-wrap: wrap; gap: 5px; justify-content: center; padding: 20px;"
        else:
            estado, color, css = "Gas (Vapor)", "#e5e5e5", "display: flex; flex-wrap: wrap; gap: 40px; justify-content: space-around; padding: 50px;"

        st.success(f"**Estado Físico:** {estado}")
        matriz = f"<div style='width: 30px; height: 30px; background-color: {color}; border-radius: 50%;'></div>" * 16
        st.markdown(f"<div style='background-color: #f8f9fa; border-radius: 10px; {css}'>{matriz}</div>", unsafe_allow_html=True)

    with tab2:
        st.header("🎮 Fuerzas Cruzadas")
        st.metric("Puntaje Acumulado", st.session_state.d3_juego_score)
        escenario = st.session_state.d3_escenario_actual
        st.info(f"**{escenario['caso']}**")
        
        def verificar_fuerza(sel):
            st.session_state.d3_juego_intentos += 1
            if sel == escenario["fuerza"]:
                st.session_state.d3_juego_score += 10
                st.toast("¡Correcto!", icon="✅")
                st.session_state.d3_escenario_actual = random.choice(ESCENARIOS_D3)
            else:
                st.session_state.d3_juego_score -= 5
                st.toast("Incorrecto.", icon="❌")

        col1, col2, col3 = st.columns(3)
        if col1.button("Puentes de Hidrógeno", use_container_width=True): verificar_fuerza("Puentes de Hidrógeno"); st.rerun()
        if col2.button("Van der Waals", use_container_width=True): verificar_fuerza("Van der Waals"); st.rerun()
        if col3.button("Ion-Dipolo", use_container_width=True): verificar_fuerza("Ion-Dipolo"); st.rerun()

    with tab3:
        st.header("📝 Quiz de Certificación")
        deshabilitar = st.session_state.d3_quiz_enviado

        q1 = st.radio("1. ¿Qué fuerza intermolecular rompe el surfactante pulmonar para evitar el colapso alveolar?", ["A) Van der Waals.", "B) Puentes de hidrógeno moleculares.", "C) Enlaces iónicos."], disabled=deshabilitar, key="d3_q1")
        q2 = st.radio("2. ¿Por qué el congelamiento tisular causa necrosis celular?", ["A) El agua se comprime.", "B) Desnaturaliza lípidos.", "C) Los puentes de H forman una red cristalina que expande el volumen."], disabled=deshabilitar, key="d3_q2")
        q3 = st.radio("3. Al inyectar solución salina, los iones se estabilizan por:", ["A) Interacciones ion-dipolo.", "B) Enlaces covalentes.", "C) Evaporación."], disabled=deshabilitar, key="d3_q3")
        q4 = st.number_input("4. Máximo teórico de puentes de hidrógeno de una molécula de agua:", value=0, step=1, disabled=deshabilitar, key="d3_q4")

        if st.button("Enviar Respuestas y Guardar", type="primary", disabled=deshabilitar, use_container_width=True, key="d3_submit"):
            aciertos = sum([q1.startswith("B"), q2.startswith("C"), q3.startswith("A"), q4 == 4])
            precision = (aciertos / 4) * 100
            guardar_registro_juego(st.session_state.get("token_actual", "DEMO"), 3, st.session_state.d3_juego_score, int(precision), {"enfoque": enfoque})
            st.session_state.d3_quiz_enviado = True
            st.success(f"Finalizado. Precisión: {precision}%")
            st.rerun()
