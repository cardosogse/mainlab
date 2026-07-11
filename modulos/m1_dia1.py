import streamlit as st
import random
from typing import Dict, Any, Final
from database import guardar_registro_juego

# Constantes de control
MAX_VIDAS: Final[int] = 3
PUNTOS_CORRECTO: Final[int] = 10
PUNTOS_ERROR: Final[int] = 5

def inicializar_estado() -> None:
    """Inicializa de forma tipada y segura el estado del Día 1."""
    defaults: Dict[str, Any] = {
        "d1_juego_score": 0,
        "d1_juego_intentos": 0,
        "d1_quiz_enviado": False,
        "d1_juego_actual_p": random.randint(8, 20)
    }
    defaults["d1_juego_actual_e"] = defaults["d1_juego_actual_p"] + random.choice([-2, -1, 0, 1, 2])
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def app() -> None:
    """Orquestador del módulo Día 1 con validación de estado."""
    st.title("🧬 Día 1: Bioelementos e Ionización")
    inicializar_estado()

    enfoque: str = st.radio("Selecciona enfoque:", ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], horizontal=True)
    tab1, tab2, tab3 = st.tabs(["🔬 Teoría", "🎮 Juego", "📝 Quiz"])

    # --- PESTAÑA 1: TEORÍA ---
    with tab1:
        # (Lógica de visualización mantenida, optimizada con componentes de layout)
        protones = st.slider("Protones", 1, 20, 11)
        electrones = st.slider("Electrones", 1, 20, 10)
        carga_neta = protones - electrones
        st.success(f"Carga neta detectada: {carga_neta}")

    # --- PESTAÑA 2: JUEGO ---
    with tab2:
        def verificar_respuesta(respuesta: str) -> None:
            carga_real = st.session_state.d1_juego_actual_p - st.session_state.d1_juego_actual_e
            es_correcta = (respuesta == "Catión" and carga_real > 0) or \
                          (respuesta == "Anión" and carga_real < 0) or \
                          (respuesta == "Neutro" and carga_real == 0)
            
            if es_correcta:
                st.session_state.d1_juego_score += PUNTOS_CORRECTO
                st.toast("Correcto", icon="✅")
            else:
                st.session_state.d1_juego_score -= PUNTOS_ERROR
                st.toast("Error", icon="❌")
            
            st.session_state.d1_juego_actual_p = random.randint(8, 20)
            st.session_state.d1_juego_actual_e = st.session_state.d1_juego_actual_p + random.choice([-2, -1, 0, 1, 2])
            st.rerun()

        if st.button("Catión (+)"): verificar_respuesta("Catión")
        # ... (Botones restantes)

    # --- PESTAÑA 3: QUIZ ---
    with tab3:
        if st.button("Enviar Respuestas", disabled=st.session_state.d1_quiz_enviado):
            # Lógica de persistencia Failsafe centralizada
            metadata = {"score": st.session_state.d1_juego_score, "enfoque": enfoque}
            exito = guardar_registro_juego(
                alumno_id=st.session_state.get("usuario_correo", "invitado@unam.mx"),
                dia_modulo=1,
                puntaje=st.session_state.d1_juego_score,
                precision=80, # Placeholder para cálculo dinámico
                meta=metadata
            )
            st.session_state.d1_quiz_enviado = True
            st.rerun()
