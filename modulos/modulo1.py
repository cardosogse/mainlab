import streamlit as st

# Importaciones directas y seguras de los submódulos de trabajo
from modulos import m1_dia1, m1_dia2, m1_dia3, m1_dia4, m1_dia5, m1_dia6

def mostrar_modulo1():
    """
    Función orquestadora de la Unidad 1.
    Controla el menú lateral y enruta el tráfico hacia el día correspondiente.
    """
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧬 U1: Agua y Equilibrio Ácido-Base")
    
    # Menú unificado alineado al plan de estudios FMVZ UNAM
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

    # Enrutamiento lógico exacto
    if eleccion == "Día 1: Bioelementos e Ionización":
        m1_dia1.app()
    elif eleccion == "Día 2: Enlaces Químicos y Polaridad":
        m1_dia2.app()
    elif eleccion == "Día 3: Estructura del Agua y Fuerzas":
        m1_dia3.app()
    elif eleccion == "Día 4: Solubilidad y Micelas":
        m1_dia4.app()
    elif eleccion == "Día 5: pH y Amortiguadores":
        m1_dia5.app()
    elif eleccion == "Día 6: Fluidoterapia Clínica":
        m1_dia6.app()
