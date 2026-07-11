import streamlit as st
import random
from database import guardar_registro_juego

def inicializar_estado():
    if "d1_juego_score" not in st.session_state:
        st.session_state.d1_juego_score = 0
    if "d1_juego_intentos" not in st.session_state:
        st.session_state.d1_juego_intentos = 0
    if "d1_quiz_enviado" not in st.session_state:
        st.session_state.d1_quiz_enviado = False
    if "d1_juego_actual_p" not in st.session_state:
        st.session_state.d1_juego_actual_p = random.randint(8, 20)
        st.session_state.d1_juego_actual_e = st.session_state.d1_juego_actual_p + random.choice([-2, -1, 0, 1, 2])

def app():
    st.title("🧬 Día 1: Bioelementos e Ionización")
    st.markdown("La base de la fisiología animal y celular radica en el equilibrio de cargas atómicas.")
    
    inicializar_estado()
    enfoque = st.radio("Selecciona tu enfoque de análisis:", ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], horizontal=True)
    tab1, tab2, tab3 = st.tabs(["🔬 Teoría y Laboratorio", "🎮 Juego: Carga Cuántica", "📝 Quiz de Certificación"])

    with tab1:
        st.header("Fundamentos: El Balance Iónico")
        st.markdown("En los líquidos corporales los bioelementos casi nunca se encuentran en estado neutro. La pérdida o ganancia de electrones modifica su carga neta.")
        
        col_t1, col_t2 = st.columns(2)
        col_t1.info("**Catión (+)**\nPierde electrones. Predomina la carga de los protones. Ejemplo: Ca²⁺, Na⁺, K⁺.")
        col_t2.error("**Anión (-)**\nGana electrones. Predomina la carga negativa. Ejemplo: Cl⁻, HCO₃⁻.")

        st.markdown("---")
        st.subheader("🔬 Espectrómetro de Masas: Simulador de Ionización")
        col_p, col_e = st.columns(2)
        protones = col_p.slider("🔴 Protones (Carga Positiva)", min_value=1, max_value=20, value=11)
        electrones = col_e.slider("🔵 Electrones (Carga Negativa)", min_value=1, max_value=20, value=10)

        carga_neta = protones - electrones
        identidad = "Desconocido"
        if protones == 11 and carga_neta == 1: identidad = "Ión Sodio (Na+) - Principal catión extracelular"
        elif protones == 20 and carga_neta == 2: identidad = "Ión Calcio (Ca2+) - Clave en contracción muscular"
        elif protones == 17 and carga_neta == -1: identidad = "Ión Cloruro (Cl-) - Principal anión extracelular"
        elif carga_neta == 0: identidad = "Átomo Neutro (Inestable en solución acuosa)"
        else: identidad = f"Ión con carga neta de {carga_neta}"

        st.success(f"**Identidad Clínica:** {identidad}")
        
        html_protones = "<div class='particula proton'></div>" * protones
        html_electrones = "<div class='particula electron'></div>" * electrones
        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;">
            <div style="margin-bottom: 10px;"><strong>Núcleo (Protones):</strong><br>{html_protones}</div>
            <div><strong>Nube (Electrones):</strong><br>{html_electrones}</div>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.header("🎮 Carga Cuántica: Semáforo Estático")
        st.metric("Puntaje Acumulado", st.session_state.d1_juego_score)
        
        p_actual = st.session_state.d1_juego_actual_p
        e_actual = st.session_state.d1_juego_actual_e
        carga_real = p_actual - e_actual
        st.subheader(f"🔴 Protones: {p_actual}  |  🔵 Electrones: {e_actual}")
        
        col_b1, col_b2, col_b3 = st.columns(3)
        def verificar_respuesta(res_usr):
            st.session_state.d1_juego_intentos += 1
            if (res_usr == "Catión" and carga_real > 0) or (res_usr == "Anión" and carga_real < 0) or (res_usr == "Neutro" and carga_real == 0):
                st.session_state.d1_juego_score += 10
                st.toast("¡Correcto!", icon="✅")
            else:
                st.session_state.d1_juego_score -= 5
                st.toast("Error.", icon="❌")
            st.session_state.d1_juego_actual_p = random.randint(8, 20)
            st.session_state.d1_juego_actual_e = st.session_state.d1_juego_actual_p + random.choice([-2, -1, 0, 1, 2])

        if col_b1.button("Catión (+)", use_container_width=True): verificar_respuesta("Catión"); st.rerun()
        if col_b2.button("Neutro (0)", use_container_width=True): verificar_respuesta("Neutro"); st.rerun()
        if col_b3.button("Anión (-)", use_container_width=True): verificar_respuesta("Anión"); st.rerun()

    with tab3:
        st.header("📝 Quiz de Certificación")
        deshabilitar = st.session_state.d1_quiz_enviado

        q1 = st.radio("1. En medicina veterinaria, una deficiencia sérica de Ca²⁺ causa tetania. ¿Qué estructura atómica define al calcio ionizado?", ["A) Tiene 2 protones más que electrones.", "B) Tiene 2 electrones más que protones.", "C) Perdió 2 neutrones en el plasma."], disabled=deshabilitar, key="d1_q1")
        q2 = st.radio("2. ¿Por qué el Cloro (Cl⁻) es considerado el principal anión del líquido extracelular?", ["A) Porque cede su electrón para unirse al Sodio.", "B) Porque ha ganado un electrón para completar su octeto.", "C) Porque expulsa protones del núcleo."], disabled=deshabilitar, key="d1_q2")
        q3 = st.radio("3. En un paciente deshidratado, el Sodio (Na⁺) se concentra. ¿Cuál es el mecanismo físico que formó este ion?", ["A) Aumento de temperatura corporal.", "B) Síntesis de protones in mitocondria.", "C) Pérdida de un electrón de valencia."], disabled=deshabilitar, key="d1_q3")
        q4 = st.number_input("4. Un átomo en una muestra de sangre tiene 12 protones y 10 electrones. Escribe el valor de su carga neta:", value=0, step=1, disabled=deshabilitar, key="d1_q4")

        if st.button("Enviar Respuestas y Guardar", type="primary", disabled=deshabilitar, use_container_width=True):
            aciertos = sum([q1.startswith("A"), q2.startswith("B"), q3.startswith("C"), q4 == 2])
            precision = (aciertos / 4) * 100
            
            guardar_registro_juego(
                st.session_state.get("token_actual", "DEMO"), 1, st.session_state.d1_juego_score, int(precision),
                {"quiz_respuestas": [q1[0], q2[0], q3[0], q4], "enfoque": enfoque}
            )
            st.session_state.d1_quiz_enviado = True
            st.success(f"¡Resultados procesados! Precisión: {precision}%")
            st.rerun()
