import streamlit as st
from modulos import m1_dia1, m1_dia2, m1_dia3, m1_dia4, m1_dia5, m1_dia6

def app():
    # Mapeo de navegación estructurado
    menu_sesiones = {
        "Día 1: Bioelementos e Ionización": m1_dia1,
        "Día 2: Enlaces Químicos y Polaridad": m1_dia2,
        "Día 3: Estructura del Agua y Fuerzas": m1_dia3,
        "Día 4: Solubilidad y Micelas": m1_dia4,
        "Día 5: pH y Amortiguadores": m1_dia5,
        "Día 6: Fluidoterapia Clínica": m1_dia6
    }
    
    st.sidebar.markdown("### 🗺️ Itinerario Científico")
    
    # Navegación nativa vertical: Cero st.rerun() bruscos al hacer clic
    seleccion = st.sidebar.radio("Ir a la sesión:", list(menu_sesiones.keys()))
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state['auth'] = None
        st.session_state['token_actual'] = None
        st.query_params.clear()
        st.rerun()
        
    # Renderizado directo e inmediato del área central
    modulo_activo = menu_sesiones[seleccion]
    modulo_activo.app()
