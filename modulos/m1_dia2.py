import streamlit as st
import random
from database import guardar_registro_juego

BIOELEMENTOS = {
    "Oxígeno (O)": {"simbolo": "O", "chi": 3.44},
    "Nitrógeno (N)": {"simbolo": "N", "chi": 3.04},
    "Carbono (C)": {"simbolo": "C", "chi": 2.55},
    "Hidrógeno (H)": {"simbolo": "H", "chi": 2.20},
    "Sodio (Na)": {"simbolo": "Na", "chi": 0.93},
    "Cloro (Cl)": {"simbolo": "Cl", "chi": 3.16},
    "Calcio (Ca)": {"simbolo": "Ca", "chi": 1.00},
    "Fósforo (P)": {"simbolo": "P", "chi": 2.19}
}

INTRUSOS_DB = [
    {"opciones": ["O-O (O₂)", "C-H (Metano)", "N-N (N₂)", "Na-Cl (Sal)"], "intruso": "Na-Cl (Sal)", "razon": "El NaCl es Iónico, los demás son Covalentes Apolares."},
    {"opciones": ["O-H (Agua)", "N-H (Amoníaco)", "C-O (Carbonilo)", "O-O (O₂)"], "intruso": "O-O (O₂)", "razon": "El O₂ es Apolar puro, los demás son Covalentes Polares."},
    {"opciones": ["Ca-Cl (Cloruro de Calcio)", "K-Cl (Cloruro de Potasio)", "Na-Cl (Cloruro de Sodio)", "C-H (Metano)"], "intruso": "C-H (Metano)", "razon": "El enlace C-H es Apolar, los demás son Iónicos clásicos."}
]

def inicializar_estado():
    if "d2_juego_score" not in st.session_state:
        st.session_state.d2_juego_score = 0
    if "d2_juego_intentos" not in st.session_state:
        st.session_state.d2_juego_intentos = 0
    if "d2_quiz_enviado" not in st.session_state:
        st.session_state.d2_quiz_enviado = False
    if "d2_ronda_actual" not in st.session_state:
        st.session_state.d2_ronda_actual = random.choice(INTRUSOS_DB)

def app():
    st.title("💥 Día 2: Enlaces y Polaridad")
    inicializar_estado()
    
    enfoque = st.radio("Selecciona tu enfoque de análisis:", ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], horizontal=True, key="d2_enfoque")
    tab1, tab2, tab3 = st.tabs(["🔬 Reactor de Fusión", "🎮 Juego: El Intruso Químico", "📝 Quiz de Certificación"])

    with tab1:
        st.header("Fundamentos: La Escala de Pauling")
        st.info("**Δχ < 0.4 : Covalente Apolar** | **Δχ [0.4 - 1.7] : Covalente Polar** | **Δχ > 1.7 : Iónico**")
        
        col_a, col_b = st.columns(2)
        atomo_a = col_a.selectbox("Átomo A:", list(BIOELEMENTOS.keys()), index=3)
        atomo_b = col_b.selectbox("Átomo B:", list(BIOELEMENTOS.keys()), index=0)

        if st.button("💥 ¡COLISIONAR!", use_container_width=True, type="primary"):
            datos_a, datos_b = BIOELEMENTOS[atomo_a], BIOELEMENTOS[atomo_b]
            delta_chi = round(abs(datos_a["chi"] - datos_b["chi"]), 2)
            
            cat = datos_a["simbolo"] if datos_a["chi"] < datos_b["chi"] else datos_b["simbolo"]
            an = datos_b["simbolo"] if datos_a["chi"] < datos_b["chi"] else datos_a["simbolo"]

            st.markdown(f"### Δχ = {delta_chi}")
            if delta_chi < 0.4:
                st.success("Enlace Covalente Apolar.")
                html = f"<div class='nube-apolar'><span>{datos_a['simbolo']}</span><span>{datos_b['simbolo']}</span></div>"
            elif delta_chi <= 1.7:
                st.warning("Enlace Covalente Polar.")
                html = f"<div class='nube-polar'><span>{datos_a['simbolo']}</span><span>{datos_b['simbolo']}</span></div>"
            else:
                st.error("Enlace Iónico.")
                html = f"<div class='ruptura-ionica'><div class='ion-cat'>{cat}⁺</div><div class='ion-an'>{an}⁻</div></div>"
            st.markdown(html, unsafe_allow_html=True)

    with tab2:
        st.header("🎮 El Intruso Químico")
        st.metric("Puntaje Acumulado", st.session_state.d2_juego_score)
        
        ronda = st.session_state.d2_ronda_actual
        def verificar_intruso(sel):
            st.session_state.d2_juego_intentos += 1
            if sel == ronda["intruso"]:
                st.session_state.d2_juego_score += 15
                st.toast(f"¡Correcto! {ronda['razon']}", icon="✅")
                st.session_state.d2_ronda_actual = random.choice(INTRUSOS_DB)
            else:
                st.session_state.d2_juego_score -= 5
                st.toast("Incorrecto.", icon="❌")

        for op in ronda["opciones"]:
            if st.button(op, use_container_width=True, key=f"btn_{op}"):
                verificar_intruso(op)
                st.rerun()

    with tab3:
        st.header("📝 Quiz de Certificación")
        deshabilitar = st.session_state.d2_quiz_enviado

        q1 = st.radio("1. ¿Qué fármacos atraviesan con mayor facilidad la barrera hematoencefálica?", ["A) Iónicos.", "B) Covalentes apolares (lipofílicos).", "C) Alta polaridad."], disabled=deshabilitar, key="d2_q1")
        q2 = st.radio("2. En el agua (H₂O), la alta electronegatividad del oxígeno genera un:", ["A) Enlace covalente apolar.", "B) Enlace covalente polar con cargas parciales.", "C) Enlace iónico."], disabled=deshabilitar, key="d2_q2")
        q3 = st.radio("3. En el suero fisiológico, el Sodio y Cloro están:", ["A) Compartiendo electrones.", "B) Enlace polar fuerte.", "C) Disociados como iones libres (Na⁺ y Cl⁻)."], disabled=deshabilitar, key="d2_q3")
        q4 = st.number_input("4. Delta Chi para Cloro (3.16) y Carbono (2.55):", value=0.00, step=0.01, format="%.2f", disabled=deshabilitar, key="d2_q4")

        if st.button("Enviar Respuestas y Guardar", type="primary", disabled=deshabilitar, use_container_width=True, key="d2_submit"):
            aciertos = sum([q1.startswith("B"), q2.startswith("B"), q3.startswith("C"), round(q4, 2) == 0.61])
            precision = (aciertos / 4) * 100
            guardar_registro_juego(st.session_state.get("token_actual", "DEMO"), 2, st.session_state.d2_juego_score, int(precision), {"enfoque": enfoque})
            st.session_state.d2_quiz_enviado = True
            st.success(f"Guardado. Precisión: {precision}%")
            st.rerun()
