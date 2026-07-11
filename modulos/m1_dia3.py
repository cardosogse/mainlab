import streamlit as st
import random
from database import guardar_registro_juego

# Base de datos de escenarios para el juego "Fuerzas Cruzadas"
ESCENARIOS_D3 = [
    {"caso": "Unión intermolecular entre dos moléculas de agua (H₂O - H₂O).", "fuerza": "Puentes de Hidrógeno", "razon": "El H parcialmente positivo es atraído por el par libre del Oxígeno."},
    {"caso": "Colas de ácidos grasos interactuando en el centro de la membrana celular.", "fuerza": "Van der Waals", "razon": "Son regiones apolares que se mantienen unidas por fuerzas de dispersión débiles."},
    {"caso": "Un ión de Sodio (Na⁺) rodeado por moléculas de agua en el plasma.", "fuerza": "Ion-Dipolo", "razon": "La carga total del ión atrae a los polos parciales opuestos del agua."},
    {"caso": "Unión entre las bases nitrogenadas (Adenina y Timina) en la doble hélice de ADN.", "fuerza": "Puentes de Hidrógeno", "razon": "Otorgan estabilidad temporal que permite la replicación del ADN."},
    {"caso": "Interacción entre moléculas de oxígeno (O₂) disueltas en la sangre antes de unirse a la hemoglobina.", "fuerza": "Van der Waals", "razon": "El O₂ es apolar, su interacción es débil y momentánea."}
]

def inicializar_estado():
    """Blindaje de variables de sesión para el Día 3."""
    if "d3_juego_score" not in st.session_state:
        st.session_state.d3_juego_score = 0
    if "d3_juego_intentos" not in st.session_state:
        st.session_state.d3_juego_intentos = 0
    if "d3_quiz_enviado" not in st.session_state:
        st.session_state.d3_quiz_enviado = False
    if "d3_escenario_actual" not in st.session_state:
        st.session_state.d3_escenario_actual = random.choice(ESCENARIOS_D3)

def app():
    st.title("🧊 Día 3: Fuerzas y Red del Agua")
    st.markdown("Los enlaces covalentes construyen la molécula, pero son las fuerzas intermoleculares las que construyen la vida.")
    
    inicializar_estado()

    # Selector de Enfoque Clínico
    enfoque = st.radio("Selecciona tu enfoque de análisis:", ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], horizontal=True)

    tab1, tab2, tab3 = st.tabs(["🔬 Red Térmica del Agua", "🎮 Juego: Fuerzas Cruzadas", "📝 Quiz de Certificación"])

    # ==========================================
    # PESTAÑA 1: TEORÍA Y SIMULADOR
    # ==========================================
    with tab1:
        st.header("Fundamentos: El Dipolo y sus Fuerzas")
        st.markdown(
            "Debido a que el agua es un **dipolo** (tiene un polo negativo en el oxígeno y polos positivos en los hidrógenos), "
            "actúa como un imán diminuto. Esta asimetría da lugar a la fuerza intermolecular biológica por excelencia:"
        )
        
        st.info("**Puente de Hidrógeno:** Interacción electrostática entre el H (δ+) de una molécula y el par de electrones libres de O, N o F de otra. "
                "Aunque es 20 veces más débil que un enlace covalente, su multiplicidad otorga al agua su alta tensión superficial y calor específico.")

        st.markdown("---")
        st.subheader("🔬 Simulador Térmico: Densidad y Puentes de H.")
        st.markdown("Desliza la temperatura para observar el efecto de la energía cinética sobre los puentes de hidrógeno.")

        temp = st.slider("Temperatura (°C)", min_value=-10, max_value=120, value=25)

        # Lógica del motor térmico y CSS dinámico
        if temp < 0:
            estado = "Sólido (Hielo)"
            explicacion = "Máxima estructura. Los puentes de hidrógeno forman una red hexagonal rígida. **El agua se expande y su densidad disminuye**, por eso el hielo flota."
            color = "#a0c4ff"
            css_layout = "display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; padding: 20px; justify-items: center;"
        elif temp < 100:
            estado = "Líquido (Agua)"
            explicacion = "Los puentes se rompen y forman continuamente. Las moléculas se agrupan estrechamente. **Estado de máxima densidad (a 4°C)**."
            color = "#4facfe"
            css_layout = "display: flex; flex-wrap: wrap; gap: 5px; justify-content: center; padding: 20px;"
        else:
            estado = "Gas (Vapor)"
            explicacion = "La energía cinética vence a los puentes de hidrógeno. Las moléculas se separan completamente interactuando muy poco."
            color = "#e5e5e5"
            css_layout = "display: flex; flex-wrap: wrap; gap: 40px; justify-content: space-around; padding: 50px;"

        st.success(f"**Estado Físico:** {estado} | **Dinámica:** {explicacion}")

        # Renderizado Visual CSS Ligero
        molecula_html = f"<div style='width: 30px; height: 30px; background-color: {color}; border-radius: 50%; box-shadow: inset -3px -3px 5px rgba(0,0,0,0.2);'></div>"
        matriz = molecula_html * 16 # 16 moléculas de agua
        
        visualizador_html = f"<div style='background-color: #f8f9fa; border-radius: 10px; {css_layout}'>{matriz}</div>"
        st.markdown(visualizador_html, unsafe_allow_html=True)


    # ==========================================
    # PESTAÑA 2: JUEGO - FUERZAS CRUZADAS
    # ==========================================
    with tab2:
        st.header("🎮 Fuerzas Cruzadas")
        st.markdown("Clasifica rápidamente la interacción intermolecular descrita en el caso clínico/biológico.")
        
        st.metric("Puntaje Acumulado", st.session_state.d3_juego_score)
        st.markdown("---")
        
        escenario = st.session_state.d3_escenario_actual
        
        st.subheader("Caso de Estudio:")
        st.info(f"**{escenario['caso']}**")
        
        def verificar_fuerza(seleccion):
            st.session_state.d3_juego_intentos += 1
            if seleccion == escenario["fuerza"]:
                st.session_state.d3_juego_score += 10
                st.toast(f"¡Correcto! {escenario['razon']}", icon="✅")
                st.session_state.d3_escenario_actual = random.choice(ESCENARIOS_D3)
            else:
                st.session_state.d3_juego_score -= 5
                st.toast("Interacción incorrecta. Revisa las polaridades.", icon="❌")

        col1, col2, col3 = st.columns(3)
        if col1.button("Puentes de Hidrógeno", use_container_width=True): verificar_fuerza("Puentes de Hidrógeno"); st.rerun()
        if col2.button("Van der Waals", use_container_width=True): verificar_fuerza("Van der Waals"); st.rerun()
        if col3.button("Ion-Dipolo", use_container_width=True): verificar_fuerza("Ion-Dipolo"); st.rerun()


    # ==========================================
    # PESTAÑA 3: QUIZ DE CERTIFICACIÓN
    # ==========================================
    with tab3:
        st.header("📝 Quiz de Certificación")
        st.markdown("Aplica la biofísica del agua a la patología y la fisiología.")
        
        deshabilitar = st.session_state.d3_quiz_enviado

        q1 = st.radio(
            "1. En neonatología, el surfactante pulmonar es vital porque reduce la tensión superficial en los alvéolos. ¿Qué fuerza intermolecular rompe el surfactante para evitar el colapso alveolar?",
            ["A) Fuerzas de dispersión de Van der Waals entre los gases.", "B) Puentes de hidrógeno entre las moléculas de agua alveolares.", "C) Enlaces iónicos del epitelio pulmonar."],
            disabled=deshabilitar,
            key="d3_q1"
        )
        
        q2 = st.radio(
            "2. ¿Por qué la congelación no controlada (congelamiento tisular en invierno) causa necrosis celular por ruptura de la membrana?",
            ["A) Porque el agua se comprime al enfriarse, encogiendo la célula.", "B) Porque la baja temperatura desnaturaliza directamente los lípidos.", "C) Porque los puentes de H forman una red cristalina que expande el volumen del agua."],
            disabled=deshabilitar,
            key="d3_q2"
        )
        
        q3 = st.radio(
            "3. Cuando inyectas solución salina (NaCl en agua), los iones se separan y se estabilizan porque:",
            ["A) Los polos del agua forman interacciones ion-dipolo alrededor del Na⁺ y el Cl⁻.", "B) El agua forma enlaces covalentes fuertes con los iones.", "C) Los iones sufren evaporación inmediata al contacto celular."],
            disabled=deshabilitar,
            key="d3_q3"
        )
        
        st.markdown("**4. Pregunta Analítica (Respuesta Numérica)**")
        st.markdown("Considera la estructura tetraédrica de una sola molécula de agua (un O central y dos H).")
        q4 = st.number_input(
            "¿Cuál es el número MÁXIMO teórico de puentes de hidrógeno que una molécula de agua puede formar simultáneamente con sus vecinas?",
            value=0, step=1, disabled=deshabilitar, key="d3_q4"
        )

        if st.button("Enviar Respuestas y Guardar", type="primary", disabled=deshabilitar, use_container_width=True):
            aciertos = 0
            if q1.startswith("B"): aciertos += 1
            if q2.startswith("C"): aciertos += 1
            if q3.startswith("A"): aciertos += 1
            if q4 == 4: aciertos += 1  # 2 por los H, 2 por los pares libres del O
            
            precision = (aciertos / 4) * 100
            
            metadata = {
                "juego_score_final": st.session_state.d3_juego_score,
                "juego_intentos_totales": st.session_state.d3_juego_intentos,
                "quiz_respuestas": [q1[0], q2[0], q3[0], q4],
                "enfoque_seleccionado": enfoque
            }
            
            correo_alumno = st.session_state.get("usuario_correo", "estudiante_invitado@unam.mx")
            
            exito = guardar_registro_juego(
                alumno_id=correo_alumno,
                dia_modulo=3,
                puntaje=st.session_state.d3_juego_score,
                precision_pct=int(precision),
                metadata_juego=metadata
            )
            
            st.session_state.d3_quiz_enviado = True
            
            if exito:
                st.success(f"¡Resultados guardados de forma segura! Precisión: {precision}%")
            else:
                st.warning(f"Evaluación completada (Precisión: {precision}%). Módulo finalizado en modo local.")
            
            st.rerun()
