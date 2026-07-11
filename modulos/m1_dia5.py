import streamlit as st
import random
import database as db

CASOS_CLINICOS_pH = [
    {
        "id": "cetoacidosis",
        "cuadro_vet": "Paciente canino con cetoacidosis diabética severa (acumulación crítica de cuerpos cetónicos y protones $H^+$).",
        "cuadro_med": "Paciente humano con cetoacidosis diabética en terapia intensiva (acumulación de acetoacetato y protones $H^+$).",
        "cuadro_bio": "Sistema de cultivo celular expuesto a una carga metabólica ácida extrema por acumulación de protones $H^+$.",
        "accion_correcta": "El Bicarbonato ($HCO_3^-$) plasmático capta los protones libres para formar ácido carbónico ($H_2CO_3$).", 
        "accion_incorrecta": "El ácido carbónico plasmático se disocia liberando una mayor cantidad de protones libres al medio.",
        "fundamento": "Ante una carga de ácidos, el amortiguador bicarbonato actúa como base conjugada, atrapando protones libres para mitigar la caída del pH."
    }
]

def inicializar_estado_dia5():
    if "d5_juego_score" not in st.session_state: st.session_state.d5_juego_score = 0
    if "d5_juego_intentos" not in st.session_state: st.session_state.d5_juego_intentos = 0
    if "d5_quiz_enviado" not in st.session_state: st.session_state.d5_quiz_enviado = False
    if "d5_caso_actual" not in st.session_state:
        st.session_state.d5_caso_actual = random.choice(CASOS_CLINICOS_pH)
        caso = st.session_state.d5_caso_actual
        opciones = [
            {"texto": caso["accion_correcta"], "es_correcta": True},
            {"texto": caso["accion_incorrecta"], "es_correcta": False}
        ]
        random.shuffle(opciones)
        st.session_state.d5_opciones_fijadas = opciones
    if "d5_retroalimentacion" not in st.session_state: st.session_state.d5_retroalimentacion = None

def calcular_logica_triage(es_correcta: bool, token_alumno: str, enfoque: str):
    """Procesa de forma aislada la puntuación sin colisionar con el renderizado."""
    st.session_state.d5_juego_intentos += 1
    caso = st.session_state.d5_caso_actual
    
    if es_correcta:
        st.session_state.d5_juego_score += 20
        st.toast(f"¡Estabilizado! {caso['fundamento']}", icon="✅")
    else:
        st.session_state.d5_juego_score = max(0, st.session_state.d5_juego_score - 10)
        st.toast("Fallo en la compensación molecular.", icon="❌")
        
    # Transición limpia al siguiente estado
    st.session_state.d5_caso_actual = random.choice(CASOS_CLINICOS_pH)
    nuevo_caso = st.session_state.d5_caso_actual
    nuevas_opciones = [
        {"texto": nuevo_caso["accion_correcta"], "es_correcta": True},
        {"texto": nuevo_caso["accion_incorrecta"], "es_correcta": False}
    ]
    random.shuffle(nuevas_opciones)
    st.session_state.d5_opciones_fijadas = nuevas_opciones

def app():
    inicializar_estado_dia5()
    token_alumno = st.session_state.get("token_actual", "DEMO")
    
    enfoque = st.radio(
        "🔬 Ajustar la Sensibilidad del Transductor:", 
        ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], 
        horizontal=True,
        key="d5_enfoque_radio"
    )
    
    tab_curva, tab_juego, tab_quiz = st.tabs(["🔬 Curva de Titulación", "⚖️ Triage Ácido-Base", "📝 Cuestionario"])

    with tab_curva:
        st.markdown("### Autoionización del Agua")
        st.latex(r"H_2O + H_2O \rightleftharpoons H_3O^+ + OH^-")
        estres = st.slider("Equivalentes H+ / OH-:", -15, 15, 0, key="d5_slider_estres")
        st.metric("pH Calculado", f"{(7.40 + (estres * 0.02)):.2f}")

    with tab_juego:
        caso = st.session_state.d5_caso_actual
        cuadro = caso["cuadro_vet"] if enfoque == "🐾 Veterinaria" else caso["cuadro_med"] if enfoque == "🩺 Medicina" else caso["cuadro_bio"]
        st.error(f"📋 **Evaluación de Emergencia:** {cuadro}")
        
        opc = st.session_state.d5_opciones_fijadas
        col1, col2 = st.columns(2)
        
        # Invocación limpia delegada a controladores puros externos
        if col1.button(opc[0]["texto"], use_container_width=True, key="d5_btn_x1"):
            calcular_logica_triage(opc[0]["es_correcta"], token_alumno, enfoque)
            st.rerun()
            
        if col2.button(opc[1]["texto"], use_container_width=True, key="d5_btn_x2"):
            calcular_logica_triage(opc[1]["es_correcta"], token_alumno, enfoque)
            st.rerun()

    with tab_quiz:
        st.markdown("🔒 *Zona de evaluación formateada y protegida contra escritura.*")
