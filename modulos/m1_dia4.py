import streamlit as st
import random
from database import guardar_registro_juego

# Base de datos de escenarios para el Ensamblador Termodinámico
ESCENARIOS_D4 = [
    {
        "entorno": "Gotas de grasa rodeadas del jugo digestivo acuoso (Intestino).",
        "solucion": "Micela Clásica",
        "descripcion": "Cabezas hidrofílicas al exterior interactuando con el agua; colas hidrofóbicas ocultas al centro."
    },
    {
        "entorno": "Líquido extracelular e intracelular acuosos separados por una barrera celular.",
        "solucion": "Bicapa Lipídica",
        "descripcion": "Dos capas de cabezas hidrofílicas apuntando a los extremos acuosos, con las colas enfrentadas en el centro."
    },
    {
        "entorno": "Pequeña gota de agua atrapada dentro de un bloque de aceite o tejido adiposo puro.",
        "solucion": "Micela Inversa",
        "descripcion": "Colas hidrofóbicas apuntando al exterior (aceite); cabezas hidrofílicas apuntando al centro (agua)."
    }
]

def inicializar_estado():
    """Blindaje de variables de sesión para el Día 4."""
    if "d4_juego_score" not in st.session_state:
        st.session_state.d4_juego_score = 0
    if "d4_juego_intentos" not in st.session_state:
        st.session_state.d4_juego_intentos = 0
    if "d4_quiz_enviado" not in st.session_state:
        st.session_state.d4_quiz_enviado = False
    if "d4_escenario_actual" not in st.session_state:
        st.session_state.d4_escenario_actual = random.choice(ESCENARIOS_D4)

def app():
    st.title("🛡️ Día 4: Solubilidad y Micelas")
    st.markdown("La vida celular existe gracias a moléculas que tienen una 'doble personalidad' frente al agua.")
    
    inicializar_estado()

    # Selector de Enfoque Clínico
    enfoque = st.radio("Selecciona tu enfoque de análisis:", ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], horizontal=True)

    tab1, tab2, tab3 = st.tabs(["🔬 Cámara de Exclusión", "🎮 Ensamblador de Micelas", "📝 Quiz de Certificación"])

    # ==========================================
    # PESTAÑA 1: TEORÍA Y SIMULADOR
    # ==========================================
    with tab1:
        st.header("Fundamentos: El Efecto Hidrofóbico")
        st.markdown(
            "La regla de oro de la solubilidad es **'lo similar disuelve a lo similar'**. "
            "Sin embargo, la separación del agua y el aceite no es por repulsión electromagnética, sino por la **Entropía**."
        )
        
        st.info("**Moléculas Anfipáticas:** Tienen una región hidrofílica (polar/iónica) que ama el agua, y una hidrofóbica (apolar) que la perturba. "
                "Para no alterar la red de puentes de hidrógeno del agua, estas moléculas se autoensamblan espontáneamente.")

        st.markdown("---")
        st.subheader("🔬 Cámara de Exclusión Celular")
        st.markdown("Inyecta una molécula en el solvente acuoso para observar la reacción termodinámica.")

        inyeccion = st.selectbox(
            "Selecciona la biomolécula a inyectar:", 
            ["Glucosa (Altamente Polar)", "Ácido Graso (Altamente Apolar)", "Fosfolípido (Anfipático)"]
        )

        if inyeccion == "Glucosa (Altamente Polar)":
            estado = "Solvatación Completa"
            desc = "El agua forma una 'esfera de solvatación' alrededor de cada molécula de glucosa, disolviéndola por completo."
            # Representación HTML simple: Glucosa dispersa
            html_grafico = """
            <div style='background-color: #e3f2fd; padding: 40px; border-radius: 10px; text-align: center; border: 2px dashed #90caf9;'>
                <span style='font-size: 2rem; margin: 10px;'>💧💠💧</span>
                <span style='font-size: 2rem; margin: 10px;'>💠💧💠</span>
                <span style='font-size: 2rem; margin: 10px;'>💧💠💧</span>
            </div>
            """
        
        elif inyeccion == "Ácido Graso (Altamente Apolar)":
            estado = "Exclusión y Aglutinación (Efecto Hidrofóbico)"
            desc = "El agua expulsa a los lípidos para maximizar sus propios puentes de hidrógeno. Los lípidos se agrupan en una gran gota (entropía favorable)."
            # Representación HTML: Aceite agrupado al centro, agua alrededor
            html_grafico = """
            <div style='background-color: #e3f2fd; padding: 40px; border-radius: 10px; text-align: center; border: 2px dashed #90caf9;'>
                <div style='background-color: #fff59d; border-radius: 50%; width: 100px; height: 100px; display: inline-block; box-shadow: 0 0 15px rgba(0,0,0,0.2);'></div>
                <br>💧 💧 💧 💧 💧
            </div>
            """
            
        else: # Fosfolípido
            estado = "Auto-ensamblaje: Micela / Bicapa"
            desc = "Las colas se esconden del agua formando un núcleo apolar, mientras las cabezas polares hacen frente al solvente acuoso."
            # Representación HTML: Círculo de fosfolípidos (Micela simulada)
            html_grafico = """
            <div style='background-color: #e3f2fd; padding: 40px; border-radius: 10px; text-align: center; border: 2px dashed #90caf9;'>
                <div style='border: 8px dashed #ffab91; background-color: #fff59d; border-radius: 50%; width: 120px; height: 120px; display: inline-block; position: relative;'>
                   <div style='position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-weight: bold;'>Núcleo<br>Apolar</div>
                </div>
                <br><br><span style='color: #d84315; font-weight: bold;'>Cabezas Polares al Exterior 💧</span>
            </div>
            """

        st.success(f"**Reacción:** {estado}")
        st.markdown(desc)
        st.markdown(html_grafico, unsafe_allow_html=True)


    # ==========================================
    # PESTAÑA 2: JUEGO - ENSAMBLADOR DE MICELAS
    # ==========================================
    with tab2:
        st.header("🎮 Ensamblador de Micelas")
        st.markdown("Como biólogo/médico, debes orientar termodinámicamente las moléculas anfipáticas según el entorno del paciente.")
        
        st.metric("Puntaje Acumulado", st.session_state.d4_juego_score)
        st.markdown("---")
        
        escenario = st.session_state.d4_escenario_actual
        
        st.subheader("Entorno Biológico Actual:")
        st.info(f"🧬 **{escenario['entorno']}**")
        st.write("¿Cómo se orientan los fosfolípidos/sales biliares espontáneamente en este entorno?")
        
        def verificar_ensamblaje(seleccion):
            st.session_state.d4_juego_intentos += 1
            if seleccion == escenario["solucion"]:
                st.session_state.d4_juego_score += 15
                st.toast(f"¡Correcto! {escenario['descripcion']}", icon="✅")
                st.session_state.d4_escenario_actual = random.choice(ESCENARIOS_D4)
            else:
                st.session_state.d4_juego_score -= 5
                st.toast("Error de ensamblaje. Recuerda que las colas huyen del agua.", icon="❌")

        # Botones de orientación
        if st.button("🔵 Micela Clásica (Cabezas al exterior, colas ocultas)", use_container_width=True): 
            verificar_ensamblaje("Micela Clásica")
            st.rerun()
        if st.button("🍔 Micela Inversa (Colas al exterior, cabezas ocultas)", use_container_width=True): 
            verificar_ensamblaje("Micela Inversa")
            st.rerun()
        if st.button("🧱 Bicapa Lipídica (Dos barreras de cabezas, colas al centro)", use_container_width=True): 
            verificar_ensamblaje("Bicapa Lipídica")
            st.rerun()


    # ==========================================
    # PESTAÑA 3: QUIZ DE CERTIFICACIÓN
    # ==========================================
    with tab3:
        st.header("📝 Quiz de Certificación")
        st.markdown("Comprueba tu comprensión del comportamiento de los fluidos y grasas.")
        
        deshabilitar = st.session_state.d4_quiz_enviado

        q1 = st.radio(
            "1. Durante la digestión en el duodeno, las sales biliares emulsionan las grasas de la dieta. ¿Qué propiedad química les permite hacer esto?",
            ["A) Son moléculas estrictamente apolares.", "B) Son anfipáticas: su parte polar interactúa con los jugos gástricos y su parte apolar encapsula la grasa.", "C) Son enzimas que rompen enlaces peptídicos hidrofílicos."],
            disabled=deshabilitar,
            key="d4_q1"
        )
        
        q2 = st.radio(
            "2. El 'Efecto Hidrofóbico' es el motor termodinámico del plegamiento de proteínas y membranas. Este efecto ocurre fundamentalmente porque:",
            ["A) Las moléculas de agua buscan maximizar la aleatoriedad (entropía) de sus puentes de hidrógeno, empujando a los compuestos apolares.", "B) El agua repele magnéticamente a las moléculas sin carga neta.", "C) Los ácidos grasos se atraen entre sí con fuerzas más fuertes que los enlaces iónicos."],
            disabled=deshabilitar,
            key="d4_q2"
        )
        
        q3 = st.radio(
            "3. En una solución acuosa, si inyectamos iones de Calcio ($Ca^{2+}$), el agua los estabilizará formando:",
            ["A) Micelas inversas.", "B) Puentes de disulfuro.", "C) Una capa de solvatación orientando sus polos negativos (Oxígeno) hacia el ión."],
            disabled=deshabilitar,
            key="d4_q3"
        )
        
        st.markdown("**4. Pregunta Analítica (Respuesta Numérica)**")
        q4 = st.number_input(
            "Un fosfoglicérido típico de la membrana celular está compuesto por una cabeza de glicerol/fosfato y varias cadenas de ácidos grasos. "
            "¿Cuántas cadenas o 'colas' hidrofóbicas posee estructuralmente un fosfolípido celular estándar?",
            value=0, step=1, disabled=deshabilitar, key="d4_q4"
        )

        if st.button("Enviar Respuestas y Guardar", type="primary", disabled=deshabilitar, use_container_width=True):
            aciertos = 0
            if q1.startswith("B"): aciertos += 1
            if q2.startswith("A"): aciertos += 1
            if q3.startswith("C"): aciertos += 1
            if q4 == 2: aciertos += 1
            
            precision = (aciertos / 4) * 100
            
            metadata = {
                "juego_score_final": st.session_state.d4_juego_score,
                "juego_intentos_totales": st.session_state.d4_juego_intentos,
                "quiz_respuestas": [q1[0], q2[0], q3[0], q4],
                "enfoque_seleccionado": enfoque
            }
            
            correo_alumno = st.session_state.get("usuario_correo", "estudiante_invitado@unam.mx")
            
            exito = guardar_registro_juego(
                alumno_id=correo_alumno,
                dia_modulo=4,
                puntaje=st.session_state.d4_juego_score,
                precision_pct=int(precision),
                metadata_juego=metadata
            )
            
            st.session_state.d4_quiz_enviado = True
            
            if exito:
                st.success(f"¡Resultados guardados correctamente! Precisión: {precision}%")
            else:
                st.warning(f"Evaluación completada (Precisión: {precision}%). Módulo finalizado en modo local.")
            
            st.rerun()
