import streamlit as st
import importlib

def app():
    # --- ARQUITECTURA DINÁMICA DE INVESTIGACIÓN ---
    configuracion_sesiones = {
        "⚛️ Día 1: Bioelementos e Ionización": {"modulo": "modulos.m1_dia1"},
        "💥 Día 2: Enlaces Químicos y Polaridad": {"modulo": "modulos.m1_dia2"},
        "🧊 Día 3: Estructura del Agua y Fuerzas": {"modulo": "modulos.m1_dia3"},
        "🧱 Día 4: Solubilidad y Micelas": {"modulo": "modulos.m1_dia4"},
        "⚖️ Día 5: pH y Amortiguadores": {"modulo": "modulos.m1_dia5"},
        "🩸 Día 6: Fluidoterapia Clínica": {"modulo": "modulos.m1_dia6"},
        "🧬 Día 7: Grupos Funcionales y Estereoquímica": {"modulo": "modulos.m1_dia7"}
    }
    
    # CONTENEDOR VISUAL PRINCIPAL (Inmediatamente visible en computadoras y celulares)
    st.markdown(
        "<div style='border-left: 4px solid #00f2fe; padding-left: 15px; margin-bottom: 5px;'>"
        "<h3 style='color:#00f2fe; font-family:monospace; margin:0;'>🗺️ ITINERARIO DE INVESTIGACIÓN</h3>"
        "</div>", 
        unsafe_allow_html=True
    )
    st.caption("Selecciona la sesión de laboratorio programada para desbloquear los simuladores cuánticos:")
    
    # Selector de alta visibilidad en el flujo principal del DOM
    seleccion_sesion = st.selectbox(
        "Estación de trabajo activa:", 
        list(configuracion_sesiones.keys()),
        key="selector_itinerario_principal"
    )
    
    st.markdown("---")
    
    # El botón de salida se queda seguro en la barra lateral para no estorbar el flujo
    if st.sidebar.button("🚪 Finalizar Práctica", use_container_width=True, key="btn_logout_sidebar"):
        st.session_state['auth'] = None
        st.session_state['token_actual'] = None
        st.query_params.clear()
        st.rerun()
        
    # --- CARGA BAJO DEMANDA (Lazy Loading Seguro) ---
    meta_modulo = configuracion_sesiones[seleccion_sesion]
    try:
        modulo_instanciado = importlib.import_module(meta_modulo["modulo"])
        modulo_instanciado.app()
    except ModuleNotFoundError:
        st.error(f"🚨 Estación curricular no encontrada. Verifica el archivo '{meta_modulo['modulo']}' en tu repositorio.")
    except Exception as e:
        st.error(f"🚨 Error de ejecución en la sesión activa: {str(e)}")
