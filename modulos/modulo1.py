import streamlit as st
import database as db

# Importación dinámica de las aplicaciones diarias del laboratorio
import modulos.m1_dia1 as m1_dia1
import modulos.m1_dia2 as m1_dia2
import modulos.m1_dia3 as m1_dia3
import modulos.m1_dia4 as m1_dia4
import modulos.m1_dia5 as m1_dia5
import modulos.m1_dia6 as m1_dia6

def inyectar_universo_y_neon_rapido():
    """
    Inyecta un fondo espacial dinámico de estrellas centelleantes y acelera
    la frecuencia del pulso de neón cian del logo principal para evitar retrasos visuales.
    """
    css_universo = """
    <style>
    /* --- FONDO DEL UNIVERSO Y ESTRELLAS EN MOVIMIENTO --- */
    .stApp {
        background: radial-gradient(circle at center, #0a0e17 0%, #030508 100%) !important;
        background-attachment: fixed;
        position: relative;
        overflow-x: hidden;
    }
    
    /* Simulación de polvo cósmico y estrellas mediante gradientes repetitivos traslúcidos */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 40px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 30px),
            radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 40px);
        background-size: 550px 550px, 350px 350px, 250px 250px;
        background-position: 0 0, 40px 60px, 130px 270px;
        opacity: 0.3;
        z-index: 0;
        pointer-events: none;
    }

    /* --- OPTIMIZACIÓN DEL PULSO DE NEÓN (MÁS RÁPIDO E INTENSO) --- */
    .main-title-suffix {
        color: #00f2fe !important;
        text-shadow: 0 0 8px #00f2fe, 
                     0 0 15px #00f2fe, 
                     0 0 30px #4facfe !important;
        animation: pulsarRapido 1.2s infinite alternate ease-in-out !important;
    }
    
    @keyframes pulsarRapido {
        0% { text-shadow: 0 0 6px #00f2fe, 0 0 12px #00f2fe, 0 0 20px #4facfe; filter: brightness(1); }
        100% { text-shadow: 0 0 15px #00f2fe, 0 0 25px #00f2fe, 0 0 45px #00f2fe, 0 0 70px #00c6ff; filter: brightness(1.3); }
    }

    /* --- CONTENEDORES DEL SELECTOR DE DÍAS --- */
    .selector-dias-container {
        background: rgba(22, 27, 34, 0.75);
        border: 1px solid #30363d;
        backdrop-filter: blur(8px);
        padding: 15px;
        border-radius: 14px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }
    </style>
    """
    st.markdown(css_universo, unsafe_allow_html=True)

def mostrar_modulo1():
    """
    Orquestador principal de la Unidad 1.
    Renderiza el menú de control estelar e intercomunica los días académicos.
    """
    # 1. Reparar apariencia visual inyectando el espacio exterior y el pulso óptimo
    inyectar_universo_y_neon_rapido()
    
    # 2. Inicializar el tracking del día si no existe en el estado de sesión
    if "dia_seleccionado" not in st.session_state:
        st.session_state["dia_seleccionado"] = 1

    st.markdown("### 🗺️ Panel de Control del Analizador: Módulo 1")
    st.markdown("Selecciona el día del itinerario científico que deseas ejecutar en este ciclo:")

    # 3. INTERFAZ DE NAVEGACIÓN EN LÍNEA (EVITA MENÚS COLAPSADOS)
    st.markdown("<div class='selector-dias-container'>", unsafe_allow_html=True)
    
    # Renderizado en columnas equidistantes para soporte móvil responsivo
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    
    dias_config = [
        (c1, 1, "Día 1", "🧬 Ionización"),
        (c2, 2, "Día 2", "💥 Enlaces"),
        (c3, 3, "Día 3", "🧊 Agua"),
        (c4, 4, "Día 4", "🛡️ Micelas"),
        (c5, 5, "Día 5", "🩸 pH & Buffers"),
        (c6, 6, "Día 6", "💧 Fluidos")
    ]
    
    for col, num_dia, label, sub in dias_config:
        with col:
            # Resaltar visualmente el día activo
            es_activo = st.session_state["dia_seleccionado"] == num_dia
            tipo_boton = "primary" if es_activo else "secondary"
            
            if st.button(
                f"{label}\n{sub}", 
                key=f"btn_nav_dia_{num_dia}", 
                use_container_width=True, 
                type=tipo_boton,
                disabled=st.session_state.get("procesando", False)
            ):
                st.session_state["dia_seleccionado"] = num_dia
                st.session_state["dia_actual_traker"] = num_dia
                # Registrar telemetría de navegación entre hitos del embudo
                db.registrar_evento_telemetria(
                    st.session_state.get("token_actual", "DEMO"), 
                    num_dia, 
                    f"navegacion_hacia_dia_{num_dia}"
                )
                st.rerun()
                
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")

    # 4. ENRUTADOR DE FLUJO DE EJECUCIÓN (ROUTING DISPATCHER)
    dia_actual = st.session_state["dia_seleccionado"]
    
    try:
        if dia_actual == 1:
            m1_dia1.app()
        elif dia_actual == 2:
            m1_dia2.app()
        elif dia_actual == 3:
            m1_dia3.app()
        elif dia_actual == 4:
            m1_dia4.app()
        elif dia_actual == 5:
            m1_dia5.app()
        elif dia_actual == 6:
            m1_dia6.app()
    except Exception as e:
        st.error(
            f"🚨 **Error de acoplamiento en el analizador diario:** No se pudo inicializar la interfaz del Día {dia_actual}. "
            f"Verifica la integridad de los archivos del módulo fuente."
        )
        st.caption(f"*Detalle técnico del error:* {str(e)}")
