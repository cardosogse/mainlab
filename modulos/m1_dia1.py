import streamlit as st
import random
import time
# Importamos la función centralizada con Failsafe
from database import guardar_registro_juego

def inicializar_estado():
    """Inicializa las variables de sesión específicas del Día 1 para evitar fugas de datos."""
    if "d1_juego_score" not in st.session_state:
        st.session_state.d1_juego_score = 0
    if "d1_juego_intentos" not in st.session_state:
        st.session_state.d1_juego_intentos = 0
    if "d1_quiz_enviado" not in st.session_state:
        st.session_state.d1_quiz_enviado = False
    if "d1_juego_actual_p" not in st.session_state:
        # Genera el primer problema del juego
        st.session_state.d1_juego_actual_p = random.randint(8, 20)
        st.session_state.d1_juego_actual_e = st.session_state.d1_juego_actual_p + random.choice([-2, -1, 0, 1, 2])

def app():
    st.title("🧬 Día 1: Bioelementos e Ionización")
    st.markdown("La base de la fisiología animal y celular radica en el equilibrio de cargas atómicas.")
    
    inicializar_estado()

    # Selector de Enfoque Clínico (Simulado para contexto)
    enfoque = st.radio("Selecciona tu enfoque de análisis:", ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], horizontal=True)

    # Estructura de 3 Pestañas
    tab1, tab2, tab3 = st.tabs(["🔬 Teoría y Laboratorio", "🎮 Juego: Carga Cuántica", "📝 Quiz de Certificación"])

    # ==========================================
    # PESTAÑA 1: TEORÍA Y SIMULADOR
    # ==========================================
    with tab1:
        st.header("Fundamentos: El Balance Iónico")
        st.markdown(
            "En los líquidos corporales (plasma, líquido intersticial, citosol), los bioelementos casi nunca "
            "se encuentran en estado neutro. La pérdida o ganancia de **electrones** modifica su carga neta, "
            "convirtiéndolos en **iones** esenciales para la conducción nerviosa, contracción muscular y equilibrio osmótico."
        )
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.info("**Catión (+)**\nPierde electrones. Predomina la carga de los protones. Ejemplo: $Ca^{2+}$, $Na^+$, $K^+$.")
        with col_t2:
            st.error("**Anión (-)**\nGana electrones. Predomina la carga negativa. Ejemplo: $Cl^-$, $HCO_3^-$.")

        st.markdown("---")
        st.subheader("🔬 Espectrómetro de Masas: Simulador de Ionización")
        st.markdown("Modifica el número de protones y electrones para observar la carga neta del átomo.")

        col_p, col_e = st.columns(2)
        with col_p:
            protones = st.slider("🔴 Protones (Carga Positiva)", min_value=1, max_value=20, value=11)
        with col_e:
            electrones = st.slider("🔵 Electrones (Carga Negativa)", min_value=1, max_value=20, value=10)

        carga_neta = protones - electrones

        # Identificador de Iones de interés clínico
        identidad = "Desconocido"
        if protones == 11 and carga_neta == 1: identidad = "Ión Sodio (Na+) - Principal catión extracelular"
        elif protones == 20 and carga_neta == 2: identidad = "Ión Calcio (Ca2+) - Clave en contracción muscular"
        elif protones == 17 and carga_neta == -1: identidad = "Ión Cloruro (Cl-) - Principal anión extracelular"
        elif carga_neta == 0: identidad = "Átomo Neutro (Inestable en solución acuosa)"
        else: identidad = f"Ión con carga neta de {carga_neta}"

        st.success(f"**Identidad Clínica:** {identidad}")

        # Renderizado Visual HTML usando las clases CSS de assets.py
        html_protones = "<div class='particula proton'></div>" * protones
        html_electrones = "<div class='particula electron'></div>" * electrones
        
        visualizador_html = f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;">
            <div style="margin-bottom: 10px;">
                <strong>Núcleo (Protones):</strong><br>
                {html_protones}
            </div>
            <div>
                <strong>Nube (Electrones):</strong><br>
                {html_electrones}
            </div>
        </div>
        """
        st.markdown(visualizador_html, unsafe_allow_html=True)


    # ==========================================
    # PESTAÑA 2: JUEGO - CARGA CUÁNTICA
    # ==========================================
    with tab2:
        st.header("🎮 Carga Cuántica: Semáforo Estático")
        st.markdown("Identifica rápidamente si la configuración atómica corresponde a un Catión, Anión o es Neutra.")
        
        st.metric("Puntaje Acumulado", st.session_state.d1_juego_score)
        st.markdown("---")
        
        # Mostrar el problema actual
        p_actual = st.session_state.d1_juego_actual_p
        e_actual = st.session_state.d1_juego_actual_e
        carga_real = p_actual - e_actual
        
        st.subheader(f"🔴 Protones: {p_actual}  |  🔵 Electrones: {e_actual}")
        
        col_b1, col_b2, col_b3 = st.columns(3)
        
        def verificar_respuesta(respuesta_usuario):
            st.session_state.d1_juego_intentos += 1
            if (respuesta_usuario == "Catión" and carga_real > 0) or \
               (respuesta_usuario == "Anión" and carga_real < 0) or \
               (respuesta_usuario == "Neutro" and carga_real == 0):
                st.session_state.d1_juego_score += 10
                st.toast("¡Correcto! Velocidad y precisión.", icon="✅")
            else:
                st.session_state.d1_juego_score -= 5
                st.toast("Error. Revisa el balance de cargas.", icon="❌")
                
            # Generar siguiente problema
            st.session_state.d1_juego_actual_p = random.randint(8, 20)
            st.session_state.d1_juego_actual_e = st.session_state.d1_juego_actual_p + random.choice([-2, -1, 0, 1, 2])

        if col_b1.button("Catión (+)", use_container_width=True): verificar_respuesta("Catión")
        if col_b2.button("Neutro (0)", use_container_width=True): verificar_respuesta("Neutro")
        if col_b3.button("Anión (-)", use_container_width=True): verificar_respuesta("Anión")


    # ==========================================
    # PESTAÑA 3: QUIZ DE CERTIFICACIÓN
    # ==========================================
    with tab3:
        st.header("📝 Quiz de Certificación")
        st.markdown("Responde las siguientes preguntas. Al enviar, tus resultados se registrarán en tu expediente.")
        
        # Candado de bloqueo
        deshabilitar = st.session_state.d1_quiz_enviado

        q1 = st.radio(
            "1. En medicina veterinaria, una deficiencia sérica de $Ca^{2+}$ causa tetania. ¿Qué estructura atómica define al calcio ionizado?",
            ["A) Tiene 2 protones más que electrones.", "B) Tiene 2 electrones más que protones.", "C) Perdió 2 neutrones en el plasma."],
            disabled=deshabilitar,
            key="d1_q1"
        )
        
        q2 = st.radio(
            "2. ¿Por qué el Cloro ($Cl^-$) es considerado el principal anión del líquido extracelular?",
            ["A) Porque cede su electrón para unirse al Sodio.", "B) Porque ha ganado un electrón para completar su octeto.", "C) Porque expulsa protones del núcleo."],
            disabled=deshabilitar,
            key="d1_q2"
        )
        
        q3 = st.radio(
            "3. En un paciente deshidratado, el Sodio ($Na^+$) se concentra. ¿Cuál es el mecanismo físico que formó este ion?",
            ["A) Aumento de temperatura corporal.", "B) Síntesis de protones en la mitocondria.", "C) Pérdida de un electrón de valencia."],
            disabled=deshabilitar,
            key="d1_q3"
        )
        
        st.markdown("**4. Pregunta Analítica (Respuesta Numérica)**")
        q4 = st.number_input(
            "Un átomo en una muestra de sangre tiene 12 protones y 10 electrones. Escribe el valor numérico exacto de su carga neta (Usa el signo - si es negativo):",
            value=0, step=1, disabled=deshabilitar, key="d1_q4"
        )

        if st.button("Enviar Respuestas y Guardar", type="primary", disabled=deshabilitar, use_container_width=True):
            # Evaluación
            aciertos = 0
            if q1.startswith("A"): aciertos += 1
            if q2.startswith("B"): aciertos += 1
            if q3.startswith("C"): aciertos += 1
            if q4 == 2: aciertos += 1
            
            precision = (aciertos / 4) * 100
            
            # Construcción del Payload Híbrido (Metadata)
            metadata = {
                "juego_score_final": st.session_state.d1_juego_score,
                "juego_intentos_totales": st.session_state.d1_juego_intentos,
                "quiz_respuestas": [q1[0], q2[0], q3[0], q4],
                "enfoque_seleccionado": enfoque
            }
            
            # Identificador simulado (Si tienes un sistema de login, usa st.session_state.usuario_correo)
            correo_alumno = st.session_state.get("usuario_correo", "estudiante_invitado@unam.mx")
            
            # Guardado Failsafe
            exito = guardar_registro_juego(
                alumno_id=correo_alumno,
                dia_modulo=1,
                puntaje=st.session_state.d1_juego_score,
                precision_pct=int(precision),
                metadata_juego=metadata
            )
            
            # Bloqueo de UI
            st.session_state.d1_quiz_enviado = True
            
            if exito:
                st.success(f"¡Resultados guardados con éxito! Precisión: {precision}%")
            else:
                st.warning(f"Evaluación completada (Precisión: {precision}%). Módulo finalizado en modo local.")
            
            st.rerun()
