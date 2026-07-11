import streamlit as st
import random
from database import guardar_registro_juego

ESCENARIOS_D4 = [
    {"entorno": "Gotas de grasa rodeadas de jugo digestivo acuoso.", "solucion": "Micela Clásica", "desc": "Cabezas hidrofílicas al exterior, colas al centro."},
    {"entorno": "Líquidos extra e intracelulares separados por una barrera.", "solucion": "Bicapa Lipídica", "desc": "Dos capas con colas enfrentadas al centro."},
    {"entorno": "Pequeña gota de agua atrapada en tejido adiposo puro.", "solucion": "Micela Inversa", "desc": "Colas al exterior, cabezas al centro."}
]

def inicializar_estado():
    if "d4_juego_score" not in st.session_state:
        st.session_state.d4_juego_score = 0
    if "d4_juego_intentos" not in st.session_state:
        st.session_state.d4_juego_intentos = 0
    if "d4_quiz_enviado" not in st.session_state:
        st.session_state.d4_quiz_enviado = False
    if "d4_escenario_actual" not in st.session_state:
        st.session_state.d4_escenario_actual = random.choice(ESCENARIOS_D4)

def app():
    st.title("🛡️ Día 4: Solubilidad y Micelas")
    inicializar_estado()
    enfoque = st.radio("Selecciona tu enfoque de análisis:", ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], horizontal=True, key="d4_enfoque")
    tab1, tab2, tab3 = st.tabs(["🔬 Cámara de Exclusión", "🎮 Ensamblador de Micelas", "📝 Quiz de Certificación"])

    with tab1:
        st.header("Fundamentos: El Efecto Hidrofóbico")
        inyeccion = st.selectbox("Selecciona la biomolécula a inyectar:", ["Glucosa (Altamente Polar)", "Ácido Graso (Altamente Apolar)", "Fosfolípido (Anfipático)"])

        if inyeccion == "Glucosa (Altamente Polar)":
            est, desc, html = "Solvatación Completa", "Capa de solvatación estable.", "<div style='background-color:#e3f2fd; padding:30px; text-align:center;'>💧💠💧</div>"
        elif inyeccion == "Ácido Graso (Altamente Apolar)":
            est, desc, html = "Exclusión Hidrofóbica", "El agua expulsa los lípidos.", "<div style='background-color:#e3f2fd; padding:30px; text-align:center;'><div style='background-color:#fff59d; width:60px; height:60px; display:inline-block; border-radius:50%;'></div></div>"
        else:
            est, desc, html = "Auto-ensamblaje", "Formación espontánea de micelas.", "<div style='background-color:#e3f2fd; padding:30px; text-align:center;'><div style='border:5px dashed #ffab91; width:80px; height:80px; display:inline-block; border-radius:50%;'></div></div>"
        st.success(f"Reacción: {est}")
        st.markdown(desc)
        st.markdown(html, unsafe_allow_html=True)

    with tab2:
        st.header("🎮 Ensamblador de Micelas")
        st.metric("Puntaje Acumulado", st.session_state.d4_juego_score)
        escenario = st.session_state.d4_escenario_actual
        st.info(f"🧬 **Entorno:** {escenario['entorno']}")
        
        def verificar_ensamblaje(sel):
            st.session_state.d4_juego_intentos += 1
            if sel == escenario["solucion"]:
                st.session_state.d4_juego_score += 15
                st.toast("¡Correcto!", icon="✅")
                st.session_state.d4_escenario_actual = random.choice(ESCENARIOS_D4)
            else:
                st.session_state.d4_juego_score -= 5
                st.toast("Error de orientación.", icon="❌")

        if st.button("🔵 Micela Clásica", use_container_width=True): verificar_ensamblaje("Micela Clásica"); st.rerun()
        if st.button("🍔 Micela Inversa", use_container_width=True): verificar_ensamblaje("Micela Inversa"); st.rerun()
        if st.button("🧱 Bicapa Lipídica", use_container_width=True): verificar_ensamblaje("Bicapa Lipídica"); st.rerun()

    with tab3:
        st.header("📝 Quiz de Certificación")
        deshabilitar = st.session_state.d4_quiz_enviado

        q1 = st.radio("1. Las sales biliares emulsionan grasas porque son:", ["A) Apolar.", "B) Anfipáticas.", "C) Enzimas."], disabled=deshabilitar, key="d4_q1")
        q2 = st.radio("2. El efecto hidrofóbico ocurre fundamentalmente porque:", ["A) El agua busca maximizar la entropía de sus puentes de H.", "B) Repulsión magnética.", "C) Enlaces iónicos."], disabled=deshabilitar, key="d4_q2")
        q3 = st.radio("3. Al inyectar Calcio (Ca²⁺) el agua forma:", ["A) Micelas.", "B) Puentes disulfuro.", "C) Capa de solvatación orientando oxígenos negativos."], disabled=deshabilitar, key="d4_q3")
        q4 = st.number_input("4. ¿Cuántas colas hidrofóbicas posee un fosfolípido estándar?", value=0, step=1, disabled=deshabilitar, key="d4_q4")

        if st.button("Enviar Respuestas y Guardar", type="primary", disabled=deshabilitar, use_container_width=True, key="d4_submit"):
            aciertos = sum([q1.startswith("B"), q2.startswith("A"), q3.startswith("C"), q4 == 2])
            precision = (aciertos / 4) * 100
            guardar_registro_juego(st.session_state.get("token_actual", "DEMO"), 4, st.session_state.d4_juego_score, int(precision), {"enfoque": enfoque})
            st.session_state.d4_quiz_enviado = True
            st.success(f"Guardado. Precisión: {precision}%")
            st.rerun()
