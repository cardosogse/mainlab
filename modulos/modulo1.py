import streamlit as st

# Importamos los módulos que ya tienes
from modulos import m1_dia1, m1_dia2, m1_dia3, m1_dia4

# Importación segura para los nuevos módulos que vamos a crear (Días 5 y 6)
try:
    from modulos import m1_dia5
    dia5_listo = True
except ImportError:
    dia5_listo = False

try:
    from modulos import m1_dia6
    dia6_listo = True
except ImportError:
    dia6_listo = False


def app():
    """
    Función orquestadora de la Unidad 1.
    Controla el menú lateral y enruta el tráfico hacia el día correspondiente.
    """
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧬 U1: Agua y Equilibrio Ácido-Base")
    
    # El nuevo menú alineado al 100% con la FMVZ UNAM
    menu_unidad1 = [
        "Día 1: Bioelementos e Ionización",
        "Día 2: Enlaces Químicos y Polaridad",
        "Día 3: Estructura del Agua y Fuerzas",
        "Día 4: Solubilidad y Micelas",
        "Día 5: pH y Amortiguadores",
        "Día 6: Fluidoterapia Clínica"
    ]
    
    eleccion = st.sidebar.radio("Selecciona tu sesión:", menu_unidad1)
    
    st.sidebar.markdown("---")
    st.sidebar.caption("🔬 FMVZ UNAM - Bioquímica Celular")

    # Enrutador de Módulos
    if eleccion == "Día 1: Bioelementos e Ionización":
        m1_dia1.app()
        
    elif eleccion == "Día 2: Enlaces Químicos y Polaridad":
        m1_dia2.app()
        
    elif eleccion == "Día 3: Estructura del Agua y Fuerzas":
        m1_dia3.app()
        
    elif eleccion == "Día 4: Solubilidad y Micelas":
        m1_dia4.app()
        
    elif eleccion == "Día 5: pH y Amortiguadores":
        if dia5_listo:
            m1_dia5.app()
        else:
            st.warning("🚧 El módulo del Día 5 (pH y Amortiguadores) está en construcción. ¡Pronto estará disponible!")
            
    elif eleccion == "Día 6: Fluidoterapia Clínica":
        if dia6_listo:
            m1_dia6.app()
        else:
            st.warning("🚧 El módulo del Día 6 (Fluidoterapia Clínica) está en construcción. ¡Pronto estará disponible!")
