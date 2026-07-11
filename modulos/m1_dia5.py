import streamlit as st
import random
from database import guardar_registro_juego

# Base de datos de casos para el juego "Balanza de Protones"
CASOS_CLINICOS_pH = [
    {
        "cuadro": "Perro con cetoacidosis diabética. Producción masiva de cuerpos cetónicos ácidos (exceso de H⁺).",
        "accion_correcta": "El Bicarbonato (HCO₃⁻) se une a los protones libres para formar H₂CO₃ y neutralizarlos.",
        "accion_incorrecta": "El ácido carbónico libera más protones al plasma."
    },
    {
        "cuadro": "Gato con vómitos crónicos severos. Pérdida masiva de ácido clorhídrico estomacal (déficit de H⁺).",
        "accion_correcta": "El sistema libera protones desde los ácidos débiles para compensar la alcalosis.",
        "accion_incorrecta": "El paciente hiperventila para expulsar todo el CO₂ posible."
    },
    {
        "cuadro": "Caballo con asfixia temporal (hipoxia). Acumulación de CO₂ en la sangre.",
        "accion_correcta": "El CO₂ reacciona con agua y aumenta la cantidad de protones, causando acidosis respiratoria.",
        "accion_incorrecta": "El CO₂ reacciona con los iones hidroxilo (OH⁻) causando alcalosis severa."
    }
]

def inicializar_estado():
    """Blindaje de variables de sesión para el Día 5."""
    if "d5_juego_score" not in st.session_state:
        st.session_state.d5_juego_score = 0
    if "d5_juego_intentos" not in st.session_state:
        st.session_state.d5_juego_intentos = 0
    if "d5_quiz_enviado" not in st.session_state:
        st.session_state.d5_quiz_enviado = False
    if "d5_caso_actual" not in st.session_state:
        st.session_state.d5_caso_actual = random.choice(CASOS_CLINICOS_pH)

def app():
    st.title("🩸 Día 5: pH y Amortiguadores")
    st.markdown("El límite entre la vida y la muerte en terapia intensiva se mide en una estrecha ventana de protones libres: $pH = 7.35$ a $7.45$.")
    
    inicializar_estado()

    enfoque = st.radio("Selecciona tu enfoque de análisis:", ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], horizontal=True)

    tab1, tab2, tab3 = st.tabs(["🔬 Curva de Titulación", "⚖️ Balanza de Protones", "📝 Quiz de Certificación"])

    # ==========================================
    # PESTAÑA 1: TEORÍA Y SIMULADOR
    # ==========================================
    with tab1:
        st.header("Fundamentos: El Poder de los Buffers")
        st.markdown(
            "El **pH** es el logaritmo negativo de la concentración de protones ($H^+$). "
            "Debido a que es una escala logarítmica, una caída de solo 1 unidad (ej. de 7.0 a 6.0) significa "
            "que hay **10 veces más ácido** destruyendo las células."
        )
        
        st.info("**Ecuación de Henderson-Hasselbalch:** Permite calcular el pH exacto si conocemos "
                "la cantidad de base conjugada y ácido débil. Los amortiguadores (buffers) como el Bicarbonato "
                "actúan como 'esponjas' termodinámicas, absorbiendo o liberando $H^+$ para mantener el pH fisiológico estable.")

        st.markdown("---")
        st.subheader("🔬 Simulador Clínico: Capacidad Amortiguadora")
        st.markdown("Inyecta ácido (H⁺) o base (OH⁻) al plasma del paciente. Observa cómo el buffer resiste el cambio hasta agotarse.")

        # Slider de estrés ácido-base
        estres = st.slider("Inyección de Equivalentes Ácidos (-) o Básicos (+)", min_value=-15, max_value=15, value=0, step=1)

        # Lógica matemática de la curva de titulación (Aproximación didáctica)
        ph_base = 7.40
        if -5 <= estres <= 5:
            # Zona de amortiguación óptima (Cambios mínimos)
            ph_actual = ph_base + (estres * 0.02)
            estado_clinico = "🟢 Homeostasis (Buffer resistiendo)"
            color_barra = "green"
        elif estres < -5:
            # Agotamiento de la base conjugada
            exceso = abs(estres) - 5
            ph_actual = (ph_base - 0.1) - (exceso * 0.15)
            estado_clinico = "🔴 Acidosis Grave (Buffer agotado)"
            color_barra = "red"
        else:
            # Agotamiento del ácido débil
            exceso = estres - 5
            ph_actual = (ph_base + 0.1) + (exceso * 0.15)
            estado_clinico = "🔵 Alcalosis Grave (Buffer agotado)"
            color_barra = "blue"

        # Mostrar métricas del paciente
        st.metric("pH Sanguíneo del Paciente", f"{ph_actual:.2f}")
        st.subheader(estado_clinico)

        # Visualizador de tolerancia
        st.progress(max(0.0, min(1.0, (ph_actual - 6.0) / 3.0))) # Normalizado entre pH 6 y 9
        
        st.caption("Nota: Observa que en la zona de -5 a +5, el pH apenas cambia gracias al sistema buffer. Fuera de ese rango, la curva se dispara.")


    # ==========================================
    # PESTAÑA 2: JUEGO - BALANZA DE PROTONES
    # ==========================================
    with tab2:
        st.header("⚖️ Balanza de Protones (Triage Rápido)")
        st.markdown("Lee el caso de urgencia y selecciona la compensación química correcta para salvar al paciente.")
        
        st.metric("Puntaje Acumulado", st.session_state.d5_juego_score)
        st.markdown("---")
        
        caso = st.session_state.d5_caso_actual
        
        st.error(f"🚨 **Paciente en Crisis:** {caso['cuadro']}")
        
        opciones = [caso["accion_correcta"], caso["accion_incorrecta"]]
        # Para que el botón correcto no siempre sea el primero, los mezclamos temporalmente en UI
        # Usaremos el índice para saber cuál presionó
        
        def verificar_accion(es_correcta):
            st.session_state.d5_juego_intentos += 1
            if es_correcta:
                st.session_state.d5_juego_score += 20
                st.toast("¡Correcto! Has equilibrado la balanza química.", icon="✅")
                st.session_state.d5_caso_actual = random.choice(CASOS_CLINICOS_pH)
            else:
                st.session_state.d5_juego_score -= 10
                st.toast("Error fatal. El paciente se descompensó.", icon="❌")

        st.write("¿Qué mecanismo químico ocurre para intentar compensarlo?")
        
        col1, col2 = st.columns(2)
        
        # Mezcla visual rápida
        if random.choice([True, False]):
            if col1.button(caso["accion_correcta"], use_container_width=True): verificar_accion(True); st.rerun()
            if col2.button(caso["accion_incorrecta"], use_container_width=True): verificar_accion(False); st.rerun()
        else:
            if col1.button(caso["accion_incorrecta"], use_container_width=True): verificar_accion(False); st.rerun()
            if col2.button(caso["accion_correcta"], use_container_width=True): verificar_accion(True); st.rerun()


    # ==========================================
    # PESTAÑA 3: QUIZ DE CERTIFICACIÓN
    # ==========================================
    with tab3:
        st.header("📝 Quiz de Certificación")
        st.markdown("Validación analítica del equilibrio ácido-base.")
        
        deshabilitar = st.session_state.d5_quiz_enviado

        q1 = st.radio(
            "1. Según la fórmula del pH (logaritmo negativo), si el pH de una solución pasa de 7.0 a 6.0, esto significa que la concentración de protones (H⁺):",
            ["A) Aumentó al doble (x2).", "B) Disminuyó a la mitad (/2).", "C) Aumentó diez veces (x10)."],
            disabled=deshabilitar,
            key="d5_q1"
        )
        
        q2 = st.radio(
            "2. El sistema buffer más importante del plasma sanguíneo, encargado de neutralizar los ácidos metabólicos, es:",
            ["A) El sistema Bicarbonato / Ácido Carbónico.", "B) El sistema Fosfato monobásico / dibásico.", "C) Las micelas de colesterol."],
            disabled=deshabilitar,
            key="d5_q2"
        )
        
        q3 = st.radio(
            "3. La ecuación de Henderson-Hasselbalch demuestra que un buffer alcanza su MÁXIMA capacidad de amortiguación cuando:",
            ["A) Todo el ácido se ha evaporado como CO₂.", "B) El pH del medio es exactamente igual a su pKa.", "C) La concentración de agua supera a la de solutos."],
            disabled=deshabilitar,
            key="d5_q3"
        )
        
        st.markdown("**4. Pregunta Analítica (Respuesta Numérica)**")
        q4 = st.number_input(
            "Escribe con precisión decimal el límite inferior del pH sanguíneo normal (fisiológico) en mamíferos antes de declararse Acidemia clínica:",
            value=7.00, step=0.01, format="%.2f", disabled=deshabilitar, key="d5_q4"
        )

        if st.button("Enviar Respuestas y Guardar", type="primary", disabled=deshabilitar, use_container_width=True):
            aciertos = 0
            if q1.startswith("C"): aciertos += 1
            if q2.startswith("A"): aciertos += 1
            if q3.startswith("B"): aciertos += 1
            if q4 == 7.35: aciertos += 1
            
            precision = (aciertos / 4) * 100
            
            metadata = {
                "juego_score_final": st.session_state.d5_juego_score,
                "juego_intentos_totales": st.session_state.d5_juego_intentos,
                "quiz_respuestas": [q1[0], q2[0], q3[0], q4],
                "enfoque_seleccionado": enfoque
            }
            
            correo_alumno = st.session_state.get("usuario_correo", "estudiante_invitado@unam.mx")
            
            exito = guardar_registro_juego(
                alumno_id=correo_alumno,
                dia_modulo=5,
                puntaje=st.session_state.d5_juego_score,
                precision_pct=int(precision),
                metadata_juego=metadata
            )
            
            st.session_state.d5_quiz_enviado = True
            
            if exito:
                st.success(f"¡Resultados guardados! Eres un experto en balances químicos. Precisión: {precision}%")
            else:
                st.warning(f"Evaluación completada (Precisión: {precision}%). Módulo finalizado en modo local.")
            
            st.rerun()
