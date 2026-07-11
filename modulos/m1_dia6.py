import streamlit as st
import random
from database import guardar_registro_juego

# Base de datos de casos para el "Triage Clínico"
CASOS_TRIAGE = [
    {
        "paciente": "Canino con deshidratación severa y shock hipovolémico.",
        "fluidos": ["Solución Salina Isotónica", "Agua destilada"],
        "correcta": "Solución Salina Isotónica",
        "razon": "Restaurar volumen intravascular sin causar lisis celular."
    },
    {
        "paciente": "Felino con edema cerebral por traumatismo craneoencefálico.",
        "fluidos": ["Solución Hipertónica", "Solución Hipotónica"],
        "correcta": "Solución Hipertónica",
        "razon": "Extrae el exceso de líquido del cerebro hacia el torrente sanguíneo."
    },
    {
        "paciente": "Paciente con hipernatremia severa (exceso de sodio en sangre).",
        "fluidos": ["Solución Hipotónica (Dextrosa 5%)", "Solución Salina al 0.9%"],
        "correcta": "Solución Hipotónica (Dextrosa 5%)",
        "razon": "Ayuda a diluir el sodio plasmático gradualmente."
    }
]

def inicializar_estado():
    """Blindaje de variables de sesión para el Día 6."""
    if "d6_juego_score" not in st.session_state:
        st.session_state.d6_juego_score = 0
    if "d6_quiz_enviado" not in st.session_state:
        st.session_state.d6_quiz_enviado = False
    if "d6_caso_actual" not in st.session_state:
        st.session_state.d6_caso_actual = random.choice(CASOS_TRIAGE)

def app():
    st.title("💧 Día 6: Fluidoterapia Clínica")
    st.markdown("La administración de fluidos no es azar; es una manipulación precisa de la tonicidad celular.")
    
    inicializar_estado()

    enfoque = st.radio("Selecciona tu enfoque de análisis:", ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], horizontal=True)

    tab1, tab2, tab3 = st.tabs(["🔬 Consola de Fluidoterapia", "🎮 Juego: Triage Clínico", "📝 Quiz de Certificación"])

    # ==========================================
    # PESTAÑA 1: TEORÍA Y SIMULADOR
    # ==========================================
    with tab1:
        st.header("Fundamentos: Tonicidad y Ósmosis")
        st.markdown(
            "La **tonicidad** mide la capacidad de una solución externa para mover agua dentro o fuera de la célula. "
            "Si el plasma es hipertónico respecto al eritrocito, este se arruga. Si es hipotónico, se hincha y puede explotar (lisis)."
        )
        
        st.subheader("🔬 Simulador de Tonicidad Celular")
        tonicidad = st.slider("Tonicidad del Fluido (0.5x a 1.5x)", min_value=0.5, max_value=1.5, value=1.0, step=0.1)

        if tonicidad < 0.9:
            estado_visual = "eritrocito-hipotonico"
            mensaje = "🔴 ¡HIPOTÓNICO! La célula se hincha (Riesgo de Lisis)."
        elif tonicidad <= 1.1:
            estado_visual = "eritrocito-isotonico"
            mensaje = "🟢 ¡ISOTÓNICO! Equilibrio hídrico perfecto."
        else:
            estado_visual = "eritrocito-hipertonico"
            mensaje = "🔵 ¡HIPERTÓNICO! La célula se crenó (deshidratación celular)."

        st.info(mensaje)
        st.markdown(f"""
        <div class='plasma-sanguineo'>
            <div class='{estado_visual}'></div>
        </div>
        """, unsafe_allow_html=True)
        
        st.caption("Nota: La consola ajusta el volumen celular en tiempo real según la tonicidad inyectada.")

    # ==========================================
    # PESTAÑA 2: JUEGO - TRIAGE CLÍNICO
    # ==========================================
    with tab2:
        st.header("🎮 Triage Clínico")
        st.markdown("Elige el fluido correcto antes de que el paciente se descompense.")
        
        st.metric("Puntaje Acumulado", st.session_state.d6_juego_score)
        st.markdown("---")
        
        caso = st.session_state.d6_caso_actual
        st.warning(f"**Paciente:** {caso['paciente']}")
        
        def verificar_triage(seleccion):
            if seleccion == caso["correcta"]:
                st.session_state.d6_juego_score += 25
                st.toast(f"¡Correcto! {caso['razon']}", icon="✅")
                st.session_state.d6_caso_actual = random.choice(CASOS_TRIAGE)
            else:
                st.session_state.d6_juego_score -= 15
                st.toast("Fluido incorrecto. La célula sufrió estrés osmótico.", icon="❌")

        for opcion in caso["fluidos"]:
            if st.button(opcion, use_container_width=True):
                verificar_triage(opcion)
                st.rerun()

    # ==========================================
    # PESTAÑA 3: QUIZ DE CERTIFICACIÓN
    # ==========================================
    with tab3:
        st.header("📝 Quiz de Certificación")
        st.markdown("Demuestra tu dominio sobre la terapia hídrica.")
        
        deshabilitar = st.session_state.d6_quiz_enviado

        q1 = st.radio(
            "1. ¿Qué le sucede a un eritrocito si lo colocamos en una solución de agua destilada (hipotónica pura)?",
            ["A) Se mantiene igual.", "B) Se crenó (se arruga).", "C) Se lisa (explota) al entrar agua por ósmosis."],
            disabled=deshabilitar, key="d6_q1"
        )
        
        q2 = st.radio(
            "2. ¿Por qué no debemos inyectar agua pura (hipotónica) directamente al torrente sanguíneo de un paciente?",
            ["A) Porque causaría lisis masiva de eritrocitos y toxicidad renal.", "B) Porque es demasiado cara.", "C) Porque es un excelente buffer de pH."],
            disabled=deshabilitar, key="d6_q2"
        )
        
        q3 = st.radio(
            "3. En un estado de choque hemorrágico, ¿cuál es el objetivo principal de la fluidoterapia?",
            ["A) Cambiar el color de la sangre.", "B) Restaurar el volumen intravascular y mantener la perfusión tisular.", "C) Aumentar la concentración de urea en sangre."],
            disabled=deshabilitar, key="d6_q3"
        )
        
        q4 = st.number_input(
            "¿Cuál es el valor aproximado de la osmolaridad plasmática normal en mamíferos (mOsm/L)?",
            value=290, min_value=0, step=1, disabled=deshabilitar, key="d6_q4"
        )

        if st.button("Enviar Respuestas Finales", type="primary", disabled=deshabilitar, use_container_width=True):
            aciertos = 0
            if q1.startswith("C"): aciertos += 1
            if q2.startswith("A"): aciertos += 1
            if q3.startswith("B"): aciertos += 1
            if 280 <= q4 <= 300: aciertos += 1
            
            precision = (aciertos / 4) * 100
            
            metadata = {
                "juego_score_final": st.session_state.d6_juego_score,
                "quiz_respuestas": [q1[0], q2[0], q3[0], q4],
                "enfoque_seleccionado": enfoque
            }
            
            # Ajuste de consistencia de la llave identificadora del alumno
            id_investigador = st.session_state.get("token_actual", "TOKEN-DEMO-MVZ")
            
            exito = guardar_registro_juego(id_investigador, 6, st.session_state.d6_juego_score, int(precision), metadata)
            
            st.session_state.d6_quiz_enviado = True
            if exito: st.success(f"¡Unidad 1 Finalizada! Precisión: {precision}%")
            else: st.warning(f"Evaluación completada con éxito. Precisión: {precision}%")
            
            st.rerun()
