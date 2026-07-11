import streamlit as st
import random
from database import guardar_registro_juego

CASOS_TRIAGE = [
    {"paciente": "Canino con deshidratación severa y shock hipovolémico.", "fluidos": ["Solución Salina Isotónica", "Agua destilada"], "correcta": "Solución Salina Isotónica", "razon": "Restaurar volumen intravascular sin causar lisis."},
    {"paciente": "Felino con edema cerebral por traumatismo.", "fluidos": ["Solución Hipertónica", "Solución Hipotónica"], "correcta": "Solución Hipertónica", "razon": "Extrae exceso de líquido cerebral al torrente sanguíneo."},
    {"paciente": "Paciente con hipernatremia severa (exceso de sodio).", "fluidos": ["Solución Hipotónica (Dextrosa 5%)", "Solución Salina al 0.9%"], "correcta": "Solución Hipotónica (Dextrosa 5%)", "razon": "Diluye el sodio plasmático gradualmente."}
]

def inicializar_estado():
    if "d6_juego_score" not in st.session_state:
        st.session_state.d6_juego_score = 0
    if "d6_quiz_enviado" not in st.session_state:
        st.session_state.d6_quiz_enviado = False
    if "d6_caso_actual" not in st.session_state:
        st.session_state.d6_caso_actual = random.choice(CASOS_TRIAGE)

def app():
    st.title("💧 Día 6: Fluidoterapia Clínica")
    inicializar_estado()
    enfoque = st.radio("Selecciona tu enfoque de análisis:", ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], horizontal=True, key="d6_enfoque")
    tab1, tab2, tab3 = st.tabs(["🔬 Consola de Fluidoterapia", "🎮 Juego: Triage Clínico", "📝 Quiz de Certificación"])

    with tab1:
        st.header("Fundamentos: Tonicidad y Ósmosis")
        st.markdown("La tonicidad regula la dinámica de fluidos celulares.")
        tonicidad = st.slider("Tonicidad del Fluido (0.5x a 1.5x)", min_value=0.5, max_value=1.5, value=1.0, step=0.1)

        if tonicidad < 0.9:
            est_vis, msg = "eritrocito-hipotonico", "🔴 ¡HIPOTÓNICO! Riesgo de Lisis."
        elif tonicidad <= 1.1:
            est_vis, msg = "eritrocito-isotonico", "🟢 ¡ISOTÓNICO! Equilibrio perfecto."
        else:
            est_vis, msg = "eritrocito-hipertonico", "🔵 ¡HIPERTÓNICO! La célula se crenó."

        st.info(msg)
        st.markdown(f"<div class='plasma-sanguineo'><div class='{est_vis}'></div></div>", unsafe_allow_html=True)

    with tab2:
        st.header("🎮 Triage Clínico")
        st.metric("Puntaje Acumulado", st.session_state.d6_juego_score)
        caso = st.session_state.d6_caso_actual
        st.warning(f"**Paciente:** {caso['paciente']}")
        
        def verificar_triage(sel):
            if sel == caso["correcta"]:
                st.session_state.d6_juego_score += 25
                st.toast(f"¡Correcto! {caso['razon']}", icon="✅")
                st.session_state.d6_caso_actual = random.choice(CASOS_TRIAGE)
            else:
                st.session_state.d6_juego_score -= 15
                st.toast("Fluido incorrecto.", icon="❌")

        for opcion in caso["fluidos"]:
            if st.button(opcion, use_container_width=True, key=f"d6_btn_{opcion}"):
                verificar_triage(opcion)
                st.rerun()

    with tab3:
        st.header("📝 Quiz de Certificación")
        deshabilitar = st.session_state.d6_quiz_enviado

        q1 = st.radio("1. ¿Qué le sucede a un eritrocito en una solución de agua destilada?", ["A) Se mantiene igual.", "B) Se crenó.", "C) Se lisa (explota) por ósmosis."], disabled=deshabilitar, key="d6_q1")
        q2 = st.radio("2. ¿Por qué no se debe inyectar agua pura intravenosa?", ["A) Causa lisis masiva de eritrocitos y daño renal.", "B) Costo elevado.", "C) Excelente buffer."], disabled=deshabilitar, key="d6_q2")
        q3 = st.radio("3. Objetivo primario de fluidoterapia en choque hemorrágico:", ["A) Cambiar color.", "B) Restaurar volumen intravascular y perfusión tisular.", "C) Aumentar urea."], disabled=deshabilitar, key="d6_q3")
        q4 = st.number_input("4. Valor aproximado de la osmolaridad plasmática normal (mOsm/L):", value=290, min_value=0, step=1, disabled=deshabilitar, key="d6_q4")

        if st.button("Enviar Respuestas Finales", type="primary", disabled=deshabilitar, use_container_width=True, key="d6_submit"):
            # Corrección lógica de validación de fin de módulo
            aciertos = sum([q1.startswith("C"), q2.startswith("A"), q3.startswith("B"), 280 <= q4 <= 300])
            precision = (aciertos / 4) * 100
            
            id_investigador = st.session_state.get("token_actual", "TOKEN-DEMO-MVZ")
            guardar_registro_juego(id_investigador, 6, st.session_state.d6_juego_score, int(precision), {"enfoque": enfoque})
            
            st.session_state.d6_quiz_enviado = True
            st.success(f"¡Unidad 1 Finalizada! Precisión: {precision}%")
            st.rerun()
