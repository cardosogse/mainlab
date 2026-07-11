import streamlit as st
import importlib

def app():
    # --- ARQUITECTURA DINÁMICA DE CRECIMIENTO SIN ACOPLAMIENTO ---
    configuracion_sesiones = {
        "Día 1: Bioelementos e Ionización": {"modulo": "modulos.m1_dia1", "icono": "⚛️"},
        "Día 2: Enlaces Químicos y Polaridad": {"modulo": "modulos.m1_dia2", "icono": "💥"},
        "Día 3: Estructura del Agua y Fuerzas": {"modulo": "modulos.m1_dia3", "icono": "🧊"},
        "Día 4: Solubilidad y Micelas": {"modulo": "modulos.m1_dia4", "icono": "🧱"},
        "Día 5: pH y Amortiguadores": {"modulo": "modulos.m1_dia5", "icono": "⚖️"},
        "Día 6: Fluidoterapia Clínica": {"modulo": "modulos.m1_dia6", "icono": "🩸"}
    }
    
    st.sidebar.markdown("### 🗺️ Itinerario de Investigación")
    seleccion_sesion = st.sidebar.radio("Ir a la sesión:", list(configuracion_sesiones.keys()))
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Finalizar Práctica"):
        st.session_state['auth'] = None
        st.session_state['token_actual'] = None
        st.query_params.clear()
        st.rerun()
        
    # --- CARGA BAJO DEMANDA (Lazy Loading & Dynamic Import) ---
    meta_modulo = configuracion_sesiones[seleccion_sesion]
    try:
        # Importación dinámica del archivo de forma aislada
        modulo_instanciado = importlib.import_module(meta_modulo["modulo"])
        modulo_instanciado.app()
    except ModuleNotFoundError:
        st.error(f"Falta el archivo ejecutor del {seleccion_sesion}. Verifica tu repositorio.")
    except Exception as e:
        st.error(f"Error de ejecución interna en el módulo: {str(e)}")
