import streamlit as st
import random
import database as db

# Base de datos estática para los escenarios del simulador de anfipatía y exclusión
ESCENARIOS_D4 = [
    {
        "entorno": "Gotas de grasa e hidrocarburos apolares rodeadas por jugo digestivo acuoso.", 
        "solucion": "Micela Clásica", 
        "desc": "Las cabezas hidrofílicas se orientan al exterior en contacto con el agua, mientras que las colas apolares se empaquetan en el núcleo."
    },
    {
        "entorno": "Líquido extracelular hidrofílico separado del citoplasma acuoso por una barrera estructural celular.", 
        "solucion": "Bicapa Lipídica", 
        "desc": "Dos capas de fosfolípidos orientan sus colas hidrofóbicas frente a frente en el centro, aislando los dos compartimentos acuosos."
    },
    {
        "entorno": "Pequeña microgota de agua atrapada en el centro de un tejido adiposo o matriz lipídica pura.", 
        "solucion": "Micela Inversa", 
        "desc": "Las colas lipofílicas se extienden hacia el exterior hidrofóbico y las cabezas polares se agrupan hacia el centro protegiendo el agua."
    }
]

def inicializar_estado_dia4():
    """Garantiza el aislamiento y persistencia de las variables de control para el Día 4."""
    if "d4_juego_score" not in st.session_state:
        st.session_state.d4_juego_score = 0
    if "d4_juego_intentos" not in st.session_state:
        st.session_state.d4_juego_intentos = 0
    if "d4_quiz_enviado" not in st.session_state:
        st.session_state.d4_quiz_enviado = False
    if "d4_escenario_actual" not in st.session_state:
        st.session_state.d4_escenario_actual = random.choice(ESCENARIOS_D4)
    if "d4_retroalimentacion" not in st.session_state:
        st.session_state.d4_retroalimentacion = None

def app():
    inicializar_estado_dia4()
    
    # Telemetría de inicio de la lección del Día 4
    if "d4_telemetria_iniciada" not in st.session_state:
        db.registrar_evento_telemetria(st.session_state.get("token_actual", "DEMO"), 4, "ingreso_pestana_teoria")
        st.session_state.d4_telemetria_iniciada = True
        
    enfoque = st.radio(
        "🔬 Modificar espectro del analizador:", 
        ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], 
        horizontal=True, 
        key="d4_enfoque",
        disabled=st.session_state.procesando
    )
    
    # NAVEGACIÓN EN PESTAÑAS (UX Antifatiga de Scroll)
    tab1, tab2, tab3 = st.tabs(["🔬 Cámara de Exclusión", "🎮 Ensamblador de Micelas", "📝 Cuestionario de Certificación"])

    with tab1:
        st.markdown("### Fundamentos: Anfipatía y el Efecto Hidrofóbico")
        st.markdown(
            """
            Las moléculas **anfipáticas** (como los fosfolípidos o las sales biliares) poseen una cabeza polar hidrofílica 
            y una cola apolar hidrofóbica. Cuando se encuentran en un solvente polar como el agua, experimentan el 
            **efecto hidrofóbico**: un ordenamiento espontáneo termodinámico diseñado para maximizar la entropía del agua.
            """
        )
        
        st.markdown("---")
        st.markdown("#### 🔬 Cámara de Exclusión de Biomoléculas")
        inyeccion = st.selectbox(
            "Selecciona la biomolécula a inyectar en el solvente:", 
            ["Glucosa (Altamente Polar)", "Ácido Graso (Altamente Apolar)", "Fosfolípido (Anfipático)"],
            disabled=st.session_state.procesando
        )

        if inyeccion == "Glucosa (Altamente Polar)":
            est, desc = "Solvatación Completa", "Formación de una capa de solvatación altamente estable gracias a puentes de hidrógeno con los hidroxilos."
            html = "<div style='background-color:#161b22; border: 1px solid #30363d; padding:30px; text-align:center; font-size:2rem; border-radius:12px;'>💧 💠 💧</div>"
        elif inyeccion == "Ácido Graso (Altamente Apolar)":
            est, desc = "Exclusión Hidrofóbica", "El agua expulsa las cadenas carbonadas apolares para no romper su red de puentes de hidrógeno, forzando la separación de fases."
            html = "<div style='background-color:#161b22; border: 1px solid #30363d; padding:30px; text-align:center; border-radius:12px;'><div style='background-color:#ffd166; width:65px; height:65px; display:inline-block; border-radius:50%; box-shadow: 0 0 15px #ffd166;'></div></div>"
        else:
            est, desc = "Auto-ensamblaje Termodinámico", "Formación espontánea de agregados supramoleculares moleculares para ocultar las regiones hidrofóbicas."
            html = "<div style='background-color:#161b22; border: 1px solid #30363d; padding:30px; text-align:center; border-radius:12px;'><div style='border:5px dashed #00f2fe; width:85px; height:85px; display:inline-block; border-radius:50%; box-shadow: 0 0 20px rgba(0,242,254,0.3);'></div></div>"
            
        st.success(f"**Mecanismo Detectado:** {est}")
        st.caption(f"📋 *Descripción estructural:* {desc}")
        st.markdown(html, unsafe_allow_html=True)

    with tab2:
        st.markdown("### 🎮 Minijuego: Ensamblador de Estructuras Lipídicas")
        
        c_score, c_intentos = st.columns(2)
        c_score.metric("Puntaje Acumulado", f"{st.session_state.d4_juego_score} pts")
        c_intentos.metric("Estructuras Orientadas", st.session_state.d4_juego_intentos)
        
        escenario = st.session_state.d4_escenario_actual
        st.info(f"🧬 **Entorno Químico Organizado:** {escenario['entorno']}")
        
        def verificar_ensamblaje(seleccion):
            st.session_state.d4_juego_intentos += 1
            if seleccion == escenario["solucion"]:
                st.session_state.d4_juego_score += 15
                st.toast(f"¡Orientación Molecular Correcta! {escenario['desc']}", icon="✅")
                st.session_state.d4_escenario_actual = random.choice(ESCENARIOS_D4)
            else:
                st.session_state.d4_juego_score = max(0, st.session_state.d4_juego_score - 5)
                st.toast("Fallo de auto-ensamblaje. Colapso hidrofóbico.", icon="❌")

        # Botonera interactiva blindada contra clicks dobles
        if st.button("🔵 Ensamblar Micela Clásica", use_container_width=True, disabled=st.session_state.procesando, key="d4_btn_mc"): 
            verificar_ensamblaje("Micela Clásica")
            st.rerun()
        if st.button("🍔 Ensamblar Micela Inversa", use_container_width=True, disabled=st.session_state.procesando, key="d4_btn_mi"): 
            verificar_ensamblaje("Micela Inversa")
            st.rerun()
        if st.button("🧱 Ensamblar Bicapa Lipídica", use_container_width=True, disabled=st.session_state.procesando, key="d4_btn_bl"): 
            verificar_ensamblaje("Bicapa Lipídica")
            st.rerun()

    with tab3:
        st.markdown("### 📝 Cuestionario de Certificación del Día 4")
        bloqueado = st.session_state.d4_quiz_enviado

        q1 = st.radio(
            "1. En el lumen del intestino delgado de los mamíferos, ¿por qué las sales biliares son indispensables para la digestión y absorción de los lípidos de la dieta?",
            ["A) Porque son moléculas puramente polares que disuelven los lípidos.", 
             "B) Porque son compuestos anfipáticos que emulsionan las grasas, formando micelas clásicas que aumentan la superficie de acción de las lipasas.", 
             "C) Porque actúan como enzimas proteolíticas específicas."],
            disabled=bloqueado, key="d4_q1"
        )
        
        q2 = st.radio(
            "2. El fenómeno físico-químico conocido como 'efecto hidrofóbico' está impulsado energéticamente por:",
            ["A) Una ganancia termodinámica de entropía en las moléculas de agua circundantes, al minimizar su ordenamiento forzado alrededor de solutos apolares.", 
             "B) Fuerzas magnéticas nucleares repelentes de largo alcance.", 
             "C) El establecimiento de enlaces covalentes entre lípidos y agua."],
            disabled=bloqueado, key="d4_q2"
        )
        
        q3 = st.radio(
            "3. Cuando se administra una inyección endovenosa de un mineral altamente polar como el Calcio ($$Ca^{2+}$$), ¿qué estructura adopta el solvente a su alrededor?",
            ["A) Se auto-ensambla en micelas clásicas.", 
             "B) Genera enlaces por puentes disulfuro cruzados.", 
             "C) Forma una capa de solvatación orientando los átomos de Oxígeno (parcialmente negativos) del agua hacia el ión."],
            disabled=bloqueado, key="d4_q3"
        )
        
        q4 = st.number_input(
            "4. ¿Cuántas colas de ácidos grasos hidrofóbicas posee la estructura básica de una molécula de fosfolípido estándar de la membrana celular?",
            value=0, step=1, disabled=bloqueado, key="d4_q4"
        )

        # RENDERIZADO DE RETROALIMENTACIÓN FORMATIVA INMEDIATA POST-ENVÍO
        if bloqueado and st.session_state.d4_retroalimentacion:
            st.markdown("#### 🔬 Reporte Técnico de Estructuras Lipídicas")
            prec = st.session_state.d4_retroalimentacion["precision"]
            
            if prec == 100:
                st.success(f"🏆 **Certificación Completada:** Precisión del {prec}%. Comprensión absoluta del comportamiento anfipático.")
            elif prec >= 75:
                st.warning(f"⚠️ **Aprobación Concedida:** Precisión del {prec}%. Repasa la energética del efecto hidrofóbico.")
            else:
                st.error(f"❌ **Certificación Denegada:** Precisión del {prec}%. Es obligatorio repasar la estructura de los fosfolípidos.")

            st.markdown(
                f"""
                <div class='lab-panel'>
                    <strong>Dictamen Clínico Formativo:</strong><br>
                    • <strong>Pregunta 1:</strong> {'✅ Correcto. Las sales biliares actúan como detergentes biológicos anfipáticos reduciendo el tamaño de las gotas lipídicas.' if q1.startswith('B') else '❌ Incorrecto. Las sales biliares emulsionan los lípidos formando micelas gracias a su naturaleza anfipática.'}<br>
                    • <strong>Pregunta 2:</strong> {'✅ Correcto. El agrupamiento apolar libera moléculas de agua presas en jaulas de clatrato, aumentando la entropía.' if q2.startswith('A') else '❌ Incorrecto. El efecto hidrofóbico está gobernado por consideraciones entrópicas de la red de agua.'}<br>
                    • <strong>Pregunta 3:</strong> {'✅ Correcto. Los cationes atraen al polo negativo de los dipolos del agua en una capa de solvatación iónica.' if q3.startswith('C') else '❌ Incorrecto. Los iones libres forman capas de solvatación hidrofílicas ordinarias, no estructuras micelares.'}<br>
                    • <strong>Pregunta 4:</strong> {'✅ Correcto. La molécula cuenta con un glicerol unido a 2 colas de ácidos grasos y un grupo fosfato.' if q4 == 2 else '❌ Incorrecto. La estructura estructural típica de un fosfolípido bicapa presenta exactamente 2 colas hidrofóbicas.'}
                </div>
                """, 
                unsafe_allow_html=True
            )

        # Botón de envío blindado contra condiciones de carrera
        if st.button(
            "🔒 Enviar Bloque al Servidor", 
            type="primary", 
            disabled=st.session_state.procesando or bloqueado, 
            use_container_width=True, 
            key="d4_submit"
        ):
            st.session_state.procesando = True
            
            # Registrar marca de tiempo exacta del envío en Supabase
            db.registrar_evento_telemetria(st.session_state.get("token_actual", "DEMO"), 4, "intento_envio_quiz")
            
            # Evaluación
            aciertos = sum([
                q1.startswith("B"),
                q2.startswith("A"),
                q3.startswith("C"),
                q4 == 2
            ])
            precision = int((aciertos / 4) * 100)
            
            # Control vital del alumno
            if precision < 50:
                st.session_state.vidas = max(0, st.session_state.vidas - 1)
                st.toast("Fallo en la dinámica hidrofóbica. Pérdida de 1 vida clínica.", icon="❤️")
            
            puntos_ganados = aciertos * 15
            st.session_state.puntos_acumulados += puntos_ganados
            
            st.session_state.d4_retroalimentacion = {
                "precision": precision,
                "aciertos": aciertos
            }
            
            # Sincronización atómica
            db.guardar_registro_juego(
                st.session_state.get("token_actual", "DEMO"),
                4,
                st.session_state.d4_juego_score + puntos_ganados,
                precision,
                {"enfoque": enfoque}
            )
            
            db.sincronizar_progreso_db(
                st.session_state.token_actual,
                st.session_state.puntos_acumulados,
                "1",
                st.session_state.vidas,
                st.session_state.tiempo_estudio_min
            )
            
            st.session_state.d4_quiz_enviado = True
            st.session_state.procesando = False
            st.rerun()
