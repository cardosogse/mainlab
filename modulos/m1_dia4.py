import streamlit as st
import database as db

def mostrar_dia4():
    st.subheader("Día 4: Equilibrio Ácido-Base y Sistemas Amortiguadores Celulares")
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### Estructura de los Grupos Funcionales Secundarios")
    grupo = st.selectbox("Grupo Funcional a Inspeccionar:", ["Carbonilo (C=O)", "Metilo (CH3)", "Hidroxilo (-OH)", "Tiol / Disulfuro (-SH)"])
    if "Carbonilo" in grupo: st.warning("**Carbonilo:** Centro neurálgico del metabolismo de glúcidos.")
    elif "Metilo" in grupo: st.warning("**Metilo:** Crítico en empaquetamiento estructural y marcas epigenéticas.")
    elif "Tiol" in grupo: st.warning("**Tiol/Disulfuro:** Brindan rigidez mecánica a pezuñas y cuernos por la queratina.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🌡️ Cámara de Perfusión y Desnaturalización Proteica")
    solucion = st.radio("Cámara de Perfusión Sanguínea:", ["Plasma con Amortiguador Bicarbonato (pH 7.4)", "Agua Destilada Pura (pH 7.0)"])
    
    if st.button("Inyectar 10 mL de HCl", use_container_width=True):
        token = st.session_state['token_actual']
        if "Agua" in solucion:
            if not st.session_state["advertencia_ph"]:
                st.markdown("<div class='card-hint'>💡 <b>ALERTA DE SEGURIDAD:</b> El agua carece de sistemas amortiguadores. Presiona una vez más si deseas desnaturalizar las proteínas de la muestra.</div>", unsafe_allow_html=True)
                st.session_state["advertencia_ph"] = True
            else:
                st.session_state["vidas"] = max(0, st.session_state["vidas"] - 1)
                db.sincronizar_progreso_db(token, st.session_state["puntos_acumulados"], "1", st.session_state["vidas"])
                st.markdown("<div class='card-error'>🚨 <b>CHOQUE DE ACIDOSIS:</b> pH cayó a 2.0. Proteínas desnaturalizadas. <b>-1 Vida.</b></div>", unsafe_allow_html=True)
                st.session_state["advertencia_ph"] = False
                st.rerun()
        else:
            st.markdown("<div class='card-success'>🛡️ <b>TAMPÓN EXITOSO:</b> El bicarbonato absorbió los protones ($H^+$), derivándolos a CO2 exhalable pulmonar.</div>", unsafe_allow_html=True)
            st.session_state["advertencia_ph"] = False
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🚑 Cuestionario de Certificación Fisiológica")
    Q1 = st.radio("1. ¿Por qué la evolución orgánica seleccionó la D-Glucosa sobre la L-Glucosa?", ["A) Desvía la luz a la derecha.", "B) Modelo estereoquímico llave-cerradura en los sitios activos enzimáticos."], index=None)
    Q2 = st.radio("2. Glucosa y Galactosa difieren únicamente en la orientación espacial del carbono asimétrico 4 (C-4), son:", ["A) Isótopos", "B) Epímeros"], index=None)
    
    if st.button("Firmar y Evaluar Módulo", use_container_width=True):
        token = st.session_state['token_actual']
        errores = 0
        if Q1 and "B)" not in Q1: errores += 1
        if Q2 and "B)" not in Q2: errores += 1
        
        if not Q1 or not Q2: 
            st.warning("Examen incompleto.")
        elif errores == 0:
            st.balloons()
            st.session_state["puntos_acumulados"] += 200
            db.sincronizar_progreso_db(token, st.session_state["puntos_acumulados"], "2", st.session_state["vidas"])
            st.success("🏆 ¡Felicidades! Récord perfecto.")
            st.rerun()
        else:
            st.session_state["errores_quiz"] += 1
            if st.session_state["errores_quiz"] == 1:
                st.markdown(f"<div class='card-hint'>💡 Tienes {errores} error(es). Recuerda que la variación en un único centro quiral define un epímero. Corrige sin penalización.</div>", unsafe_allow_html=True)
            else:
                st.session_state["vidas"] = max(0, st.session_state["vidas"] - 1)
                db.registrar_intento_quiz(token, st.session_state["vidas"], st.session_state["errores_quiz"])
                st.error("❌ Fallo Clínico Severo. Se ha descontado 1 Vida.")
                st.session_state["errores_quiz"] = 0
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
