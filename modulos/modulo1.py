import streamlit as st
from typing import Dict, Callable, Final, Optional

# Importaciones seguras con manejo de errores centralizado
from modulos import m1_dia1, m1_dia2, m1_dia3, m1_dia4

# Mapeo de módulos cargables para evitar lógica if-elif redundante
MODULOS_DISPONIBLES: Dict[str, Any] = {
    "Día 1: Bioelementos e Ionización": m1_dia1,
    "Día 2: Enlaces Químicos y Polaridad": m1_dia2,
    "Día 3: Estructura del Agua y Fuerzas": m1_dia3,
    "Día 4: Solubilidad y Micelas": m1_dia4,
}

try:
    from modulos import m1_dia5
    MODULOS_DISPONIBLES["Día 5: pH y Amortiguadores"] = m1_dia5
except ImportError:
    pass

try:
    from modulos import m1_dia6
    MODULOS_DISPONIBLES["Día 6: Fluidoterapia Clínica"] = m1_dia6
except ImportError:
    pass

def app() -> None:
    """
    Función orquestadora refactorizada para la Unidad 1.
    Utiliza el patrón de mapeo de comandos para enrutamiento determinista.
    """
    # Validación de seguridad: Acceso restringido a usuarios autenticados
    if st.session_state.get('auth') is None:
        st.error("Acceso no autorizado. Por favor, inicia sesión.")
        return

    st.sidebar.markdown("---")
    st.sidebar.subheader("🧬 U1: Agua y Equilibrio Ácido-Base")
    
    opciones: list[str] = list(MODULOS_DISPONIBLES.keys())
    eleccion: str = st.sidebar.radio("Selecciona tu sesión:", opciones)
    
    st.sidebar.markdown("---")
    st.sidebar.caption("🔬 FMVZ UNAM - Bioquímica Celular")

    # Ejecución del módulo seleccionado mediante acceso directo al mapa
    modulo = MODULOS_DISPONIBLES.get(eleccion)
    
    if hasattr(modulo, 'app'):
        modulo.app()
    else:
        st.warning(f"🚧 El módulo '{eleccion}' se encuentra en fase de construcción.")
