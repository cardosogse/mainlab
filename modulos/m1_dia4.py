import streamlit as st
import database as db

def mostrar_dia4():
    st.subheader("Día 4: Equilibrio Ácido-Base")
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🌡️ Cámara de Perfusión")
    solucion = st.radio("Muestra:", ["Plasma (pH 7.4)", "Agua Destilada (pH 7.0)"])
    
    if st.button("Inyectar 10 mL de HCl", use_container_width=True):
        token = st.session_state['token_actual']
        if "Agua" in solucion:
            if not st.session_state["advertencia_ph"]:
                st.warning("💡 ALERTA: El agua carece de sistemas amortiguadores. Presiona otra vez para desnaturalizar.")
                st.session_state["advertencia_ph"] = True
            else:
                st.error("🚨 CHOQUE DE ACIDOSIS. Proteínas desnaturalizadas. -1 Vida.")
                db.descontar_vida_db(token)
                st.session_state["vidas"] = max(0, st.session_state["vidas"] - 1)
                st.session_state["advertencia_ph"] = False
                st.rerun()
        else:
            st.success("🛡️ TAMPÓN EXITOSO: El bicarbonato absorbió los protones.")
            st.session_state["advertencia_ph"] = False
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🚑 Cuestionario Fisiológico")
    Q1 = st.radio("1. Selección de D-Glucosa:", ["A) Desvía luz derecha.", "B) Modelo llave-cerradura."], index=None)
    Q2 = st.radio("2. Glucosa y Galactosa:", ["A) Isótopos", "B) Epímeros"], index=None)
    
    if st.button("Evaluar Módulo", use_container_width=True):
        token = st.session_state['token_actual']
        errores = 0
        if Q1 and "B)" not in Q1: errores += 1
        if Q2 and "B)" not in Q2: errores += 1
        
        if not Q1 or not Q2: st.warning("Examen incompleto.")
        elif errores == 0:
            st.balloons()
            st.success("🏆 ¡Récord perfecto!")
            st.session_state["puntos_acumulados"] += 200
            db.sincronizar_progreso_db(token, st.session_state["puntos_acumulados"], "2")
            st.rerun()
        else:
            st.session_state["errores_quiz"] += 1
            if st.session_state["errores_quiz"] == 1:
                st.warning("💡 Tienes un error. Corrige sin penalización.")
            else:
                db.descontar_vida_db(token)
                st.session_state["vidas"] = max(0, st.session_state["vidas"] - 1)
                st.error("❌ Fallo Clínico. -1 Vida.")
                st.session_state["errores_quiz"] = 0
                st.rerun()
