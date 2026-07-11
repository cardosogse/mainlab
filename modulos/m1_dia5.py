import streamlit as st
import random
from database import guardar_registro_juego

CASOS_CLINICOS_pH = [
    {"cuadro": "Perro con cetoacidosis diabética (exceso de H⁺).", "accion_correcta": "El Bicarbonato (HCO₃⁻) absorbe los protones.", "accion_incorrecta": "El ácido carbónico libera más protones."},
    {"cuadro": "Gato con vómitos crónicos severos (déficit de H⁺).", "accion_correcta": "El sistema libera protones desde ácidos débiles.", "accion_incorrecta": "El paciente hiperventila."},
    {"cuadro": "Caballo con asfixia temporal. Acumulación de CO₂.", "accion_correcta": "El CO₂ reacciona con agua aumentando protones.", "accion_incorrecta": "El CO₂ reacciona con OH⁻."}
]

def inicializar_estado():
    if "d5_juego_score" not in st.session_state:
        st.session_state.d5_juego_score = 0
    if "d5_juego_intentos" not in st.session_state:
        st.session_state.d5_juego_intentos = 0
    if "d5_quiz_enviado" not in st.session_state:
        st.session_state.d5_quiz_enviado = False
    if "d5_caso_actual" not in st.session_state:
        st.session_state.d5_caso_actual = random.choice(CASOS_CLINICOS_pH)

def app():
    st.title("🩸 Día 5: pH y Amortiguadores")
    inicializar_estado()
    enfoque = st.radio("Selecciona tu enfoque de análisis:", ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], horizontal=True, key="d5_enfoque")
    tab1, tab2, tab3 = st.tabs(["🔬 Curva de Titulación", "⚖️ Balanza de Protones", "📝 Quiz de Certificación"])

    with tab1:
        st.header("Fundamentos: Buffers")
        estres = st.slider("Inyección de Equivalentes Ácidos (-) o Básicos (+)", min_value=-15, max_value=15, value=0)
        ph_base = 7.40
        if -5 <= estres <= 5:
            ph_act, est, col = ph_base + (estres * 0.02), "🟢 Homeostasis", "green"
        elif estres < -5:
            ph_act, est, col = (ph_base - 0.1) - (abs(estres) - 5) * 0.15, "🔴 Acidosis Grave", "red"
        else:
            ph_act, est, col = (ph_base + 0.1) + (estres - 5) * 0.15, "🔵 Alcalosis Grave", "blue"

        st.metric("pH Sanguíneo del Paciente", f"{ph_act:.2f}")
        st.subheader(est)
        st.progress(max(0.0, min(1.0, (ph_act - 6.0) / 3.0)))

    with tab2:
        st.header("⚖️ Balanza de Protones (Triage Rápido)")
        st.metric("Puntaje Acumulado", st.session_state.d5_juego_score)
        caso = st.session_state.d5_caso_actual
        st.error(f"🚨 **Cuadro Paciente:** {caso['cuadro']}")

        def verificar_accion(es_corr):
            st.session_state.d5_juego_intentos += 1
            if es_corr:
                st.session_state.d5_juego_score += 20
                st.toast("¡Equilibrio químico restaurado!", icon="✅")
                st.session_state.d5_caso_actual = random.choice(CASOS_CLINICOS_pH)
            else:
                st.session_state.d5_juego_score -= 10
                st.toast("Descompensación del paciente.", icon="❌")

        col1, col2 = st.columns(2)
        if col1.button(caso["accion_correcta"], use_container_width=True, key="d5_c1"): verificar_accion(True); st.rerun()
        if col2.button(caso["accion_incorrecta"], use_container_width=True, key="d5_c2"): verificar_accion(False); st.rerun()

    with tab3:
        st.header("📝 Quiz de Certificación")
        deshabilitar = st.session_state.d5_quiz_enviado

        q1 = st.radio("1. Si el pH pasa de 7.0 a 6.0, la concentración de protones (H⁺):", ["A) Aumentó al doble.", "B) Disminuyó.", "C) Aumentó diez veces (x10)."], disabled=deshabilitar, key="d5_q1")
        q2 = st.radio("2. Buffer plasmático principal contra ácidos metabólicos:", ["A) Sistema Bicarbonato.", "B) Fosfato.", "C) Colesterol."], disabled=deshabilitar, key="d5_q2")
        q3 = st.radio("3. Un buffer alcanza su máxima capacidad de amortiguación cuando:", ["A) Se evapora.", "B) pH es igual al pKa.", "C) Agua supera solutos."], disabled=deshabilitar, key="d5_q3")
        q4 = st.number_input("4. Límite inferior del pH fisiológico normal en mamíferos:", value=7.00, step=0.01, format="%.2f", disabled=deshabilitar, key="d5_q4")

        if st.button("Enviar Respuestas y Guardar", type="primary", disabled=deshabilitar, use_container_width=True, key="d5_submit"):
            aciertos = sum([q1.startswith("C"), q2.startswith("A"), q3.startswith("B"), round(q4, 2) == 7.35])
            precision = (aciertos / 4) * 100
            guardar_registro_juego(st.session_state.get("token_actual", "DEMO"), 5, st.session_state.d5_juego_score, int(precision), {"enfoque": enfoque})
            st.session_state.d5_quiz_enviado = True
            st.success(f"Finalizado. Precisión: {precision}%")
            st.rerun()
