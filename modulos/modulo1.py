import streamlit as st

def mostrar_modulo1():
    """
    Orquesta la navegación de la Unidad 1 mediante un sistema responsivo de pestañas,
    optimizando la visualización en dispositivos móviles y aislando fallos de renderizado.
    """
    # Encabezado estilizado de la Unidad
    st.markdown("<h2 style='color:#ffffff; margin-top:0;'>Unidad 1: Fundamentos de Química Biológica</h2>", unsafe_allow_html=True)
    
    # Declaración de pestañas responsivas (Reemplaza a st.radio horizontal)
    tab_dia1, tab_dia2, tab_dia3, tab_dia4 = st.tabs([
        "📅 Día 1: Fases y Modelos",
        "📅 Día 2: Estructura y Bioelementos",
        "📅 Día 3: Fusión e Interacciones",
        "📅 Día 4: Homeostasis y pH"
    ])
    
    # ==========================================
    # CARGA ENCAPSULADA DE CONTENIDOS DIARIOS
    # ==========================================
    
    with tab_dia1:
        try:
            from modulos.m1_dia1 import mostrar_dia1
            mostrar_dia1()
        except Exception as e:
            st.error(f"⚠️ No se pudo cargar el contenido del Día 1: {e}")
            
    with tab_dia2:
        try:
            from modulos.m1_dia2 import mostrar_dia2
            mostrar_dia2()
        except Exception as e:
            st.error(f"⚠️ No se pudo cargar el contenido del Día 2: {e}")
            
    with tab_dia3:
        try:
            from modulos.m1_dia3 import mostrar_dia3
            mostrar_dia3()
        except Exception as e:
            st.error(f"⚠️ No se pudo cargar el contenido del Día 3: {e}")
            
    with tab_dia4:
        try:
            from modulos.m1_dia4 import mostrar_dia4
            mostrar_dia4()
        except Exception as e:
            st.error(f"⚠️ No se pudo cargar el contenido del Día 4: {e}")
