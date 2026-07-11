import streamlit as st

def cargar_css() -> None:
    """Inyecta estilos CSS optimizados con uso de clamp() para responsividad."""
    estilos: str = """
    <style>
    /* Reset visual para inmersión pedagógica */
    #MainMenu, footer, header { visibility: hidden; }
    
    /* Simulador de Partículas: Uso de unidades relativas */
    .particula {
        display: inline-block;
        border-radius: 50%;
        margin: clamp(2px, 0.5vw, 5px);
        box-shadow: inset -2px -2px 4px rgba(0,0,0,0.4);
    }
    
    /* Simulador Hemodinámico: Ajuste dinámico de dimensiones */
    .eritrocito-isotonico {
        width: clamp(60px, 10vw, 120px);
        height: clamp(60px, 10vw, 120px);
        border-radius: 50%;
        background: radial-gradient(circle at center, #ff7b7b 30%, #cc0000 80%);
        transition: all 0.6s ease;
    }
    </style>
    """
    st.markdown(estilos, unsafe_allow_html=True)
