import streamlit as st
import random
import database as db

# Base de datos estática optimizada para los escenarios del simulador de interacciones
ESCENARIOS_D3 = [
    {
        "caso": "Unión intermolecular dinámica entre dos moléculas adyacentes de agua (H₂O - H₂O).", 
        "fuerza": "Puentes de Hidrógeno", 
        "razon": "El átomo de Hidrógeno con carga parcial positiva atrae electrostáticamente al par de electrones no compartidos del Oxígeno de la molécula vecina."
    },
    {
        "caso": "Colas hidrofóbicas de ácidos grasos interactuando fuertemente en el núcleo lipídico de la membrana celular.", 
        "fuerza": "Van der Waals", 
        "razon": "Regiones moleculares netamente apolares que experimentan atracciones dipolo inducido-dipolo inducido debido a fluctuaciones electrónicas transitorias."
    },
    {
        "caso": "Un ión disociado de Sodio (Na⁺) rodeado e hidratado por moléculas de agua en el interior del plasma sanguíneo.", 
        "fuerza": "Ion-Dipolo", 
        "razon": "La carga neta completa del catión Na⁺ atrae con gran afinidad a la densidad de carga parcial negativa localizada sobre el Oxígeno del agua."
    }
]

def inicializar_estado_dia3():
    """Garantiza el aislamiento y consistencia de las variables de control para el Día 3."""
    if "d3_juego_score" not in st.session_state:
        st.session_state.d3_juego_score = 0
    if "d3_juego_intentos" not in st.session_state:
        st.session_state.d3_juego_intentos = 0
    if "d3_quiz_enviado" not in st.session_state:
        st.session_state.d3_quiz_enviado = False
    if "d3_escenario_actual" not in st.session_state:
        st.session_state.d3_escenario_actual = random.choice(ESCENARIOS_D3)
    if "d3_retroalimentacion" not in st.session_state:
        st.session_state.d3_retroalimentacion = None

def app():
    inicializar_estado_dia3()
    
    # Telemetría automatizada de inicio de sesión instruccional
    if "d3_telemetria_iniciada" not in st.session_state:
        db.registrar_evento_telemetria(st.session_state.get("token_actual", "DEMO"), 3, "ingreso_pestana_teoria")
        st.session_state.d3_telemetria_iniciada = True
        
    enfoque = st.radio(
        "🔬 Canal de análisis del espectrómetro:", 
        ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], 
        horizontal=True, 
        key="d3_enfoque",
        disabled=st.session_state.procesando
    )
    
    # ESTRUCTURA EN PESTAÑAS (Mitigación del scroll vertical)
    tab1, tab2, tab3 = st.tabs(["🔬 Dinámica Molecular", "🎮 Minijuego: Fuerzas Cruzadas", "📝 Cuestionario de Certificación"])

    with tab1:
        st.markdown("### Fundamentos: El Agua como Solvente Biológico Universal")
        st.markdown(
            """
            La vida celular ocurre en medio acuoso. La geometría angular de la molécula de agua y la elevada 
            electronegatividad del Oxígeno generan un **dipolo permanente**. Las interacciones no covalentes 
            entre dipolos determinan las propiedades térmicas y la homeostasis de los organismos.
            """
        )
        
        st.markdown("---")
        st.markdown("#### 🔬 Red Térmica Estructural del Agua")
        temp = st.slider("Ajustar Temperatura del Analizador (°C):", min_value=-10, max_value=120, value=25, disabled=st.session_state.procesando)

        if temp < 0:
            estado, color, css = "Sólido (Hielo Cristalino)", "#a0c4ff", "display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; padding: 20px;"
            detalle = "Los puentes de hidrógeno se estabilizan al máximo formando una red cristalina hexagonal rígida expansiva."
        elif temp < 100:
            estado, color, css = "Líquido (Agua Metabólica)", "#00f2fe", "display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; padding: 20px;"
            detalle = "Interacciones dinámicas continuas; los puentes de hidrógeno se rompen y reforman en picosegundos permitiendo fluidez."
        else:
            estado, color, css = "Gas (Vapor de Agua)", "#e5e5e5", "display: flex; flex-wrap: wrap; gap: 40px; justify-content: space-around; padding: 50px;"
            detalle = "La energía cinética supera la energía de enlace de las interacciones moleculares, disociando los puentes por completo."

        st.success(f"**Estado Físico del Fluido:** {estado}")
        st.caption(f"ℹ️ *Comportamiento a nivel atómico:* {detalle}")
        
        matriz = f"<div style='width: 25px; height: 25px; background-color: {color}; border-radius: 50%; box-shadow: 0 0 8px {color};'></div>" * 16
        st.markdown(f"<div style='background-color: #161b22; border-radius: 12px; border: 1px solid #30363d; {css}'>{matriz}</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("### 🎮 Desafío: Fuerzas Cruzadas")
        
        c_score, c_intentos = st.columns(2)
        c_score.metric("Puntaje Acumulado", f"{st.session_state.d3_juego_score} pts")
        c_intentos.metric("Casos Clínicos Evaluados", st.session_state.d3_juego_intentos)
        
        escenario = st.session_state.d3_escenario_actual
        st.info(f"📋 **Escenario Clínico/Biológico:** {escenario['caso']}")
        
        def verificar_fuerza(seleccion):
            st.session_state.d3_juego_intentos += 1
            if seleccion == escenario["fuerza"]:
                st.session_state.d3_juego_score += 10
                st.toast(f"¡Correcto! {escenario['razon']}", icon="✅")
                st.session_state.d3_escenario_actual = random.choice(ESCENARIOS_D3)
            else:
                st.session_state.d3_juego_score = max(0, st.session_state.d3_juego_score - 5)
                st.toast("Fallo en el reconocimiento de la fuerza intermolecular.", icon="❌")

        col1, col2, col3 = st.columns(3)
        if col1.button("Puentes de Hidrógeno", use_container_width=True, disabled=st.session_state.procesando, key="d3_btn1"): 
            verificar_fuerza("Puentes de Hidrógeno")
            st.rerun()
        if col2.button("Van der Waals", use_container_width=True, disabled=st.session_state.procesando, key="d3_btn2"): 
            verificar_fuerza("Van der Waals")
            st.rerun()
        if col3.button("Ion-Dipolo", use_container_width=True, disabled=st.session_state.procesando, key="d3_btn3"): 
            verificar_fuerza("Ion-Dipolo")
            st.rerun()

    with tab3:
        st.markdown("### 📝 Cuestionario de Certificación del Día 3")
        bloqueado = st.session_state.d3_quiz_enviado

        q1 = st.radio(
            "1. En la fisiología del sistema respiratorio, ¿qué fuerzas intermoleculares rompe específicamente el surfactante pulmonar para evitar el colapso alveolar?",
            ["A) Fuerzas de dispersión débiles de Van der Waals.", 
             "B) Los puentes de hidrógeno intermoleculares del agua, disminuyendo la tensión superficial.", 
             "C) Enlaces iónicos intramembranales."],
            disabled=bloqueado, key="d3_q1"
        )
        
        q2 = st.radio(
            "2. ¿Por qué el congelamiento severo de los tejidos periféricos provoca necrosis celular directa e irreversible?",
            ["A) Porque el agua disminuye bruscamente su densidad molecular.", 
             "B) Porque desnaturaliza covalentemente la estructura lipídica.", 
             "C) Porque los puentes de hidrógeno forman una red cristalina fija que expande el volumen del agua, rompiendo la membrana celular."],
            disabled=bloqueado, key="d3_q2"
        )
        
        q3 = st.radio(
            "3. Tras la infusión intravenosa de una solución electrolítica, ¿gracias a qué mecanismo físico-químico se estabilizan los iones libres en la matriz del plasma?",
            ["A) Interacciones de tipo ion-dipolo formadas con las zonas de carga parcial del agua.", 
             "B) El establecimiento de enlaces covalentes covalentes coordinados.", 
             "C) Evaporación selectiva del solvente."],
            disabled=bloqueado, key="d3_q3"
        )
        
        q4 = st.number_input(
            "4. Determina el máximo teórico de puentes de hidrógeno estables que puede coordinar una única molécula de agua en estado cristalino:",
            value=0, step=1, disabled=bloqueado, key="d3_q4"
        )

        # ENGINE DE RETROALIMENTACIÓN FORMATIVA INMEDIATA POST-ENVÍO
        if bloqueado and st.session_state.d3_retroalimentacion:
            st.markdown("#### 🔬 Reporte de Evaluación Bioquímica")
            prec = st.session_state.d3_retroalimentacion["precision"]
            
            if prec == 100:
                st.success(f"🏆 **Certificación Completada:** Precisión del {prec}%. Control maestro de las interacciones moleculares.")
            elif prec >= 75:
                st.warning(f"⚠️ **Aprobación Concedida:** Precisión del {prec}%. Repasa el comportamiento volumétrico del hielo.")
            else:
                st.error(f"❌ **Certificación Denegada:** Precisión del {prec}%. Es necesario revisar las propiedades coligativas y estructurales.")

            st.markdown(
                f"""
                <div class='lab-panel'>
                    <strong>Dictamen Clínico Formativo:</strong><br>
                    • <strong>Pregunta 1:</strong> {'✅ Correcto. El surfactante reduce la alta tensión superficial rompiendo la red cohesiva de puentes de H.' if q1.startswith('B') else '❌ Incorrecto. La tensión superficial del alvéolo está dada por la fuerza cohesiva de los puentes de hidrógeno.'}<br>
                    • <strong>Pregunta 2:</strong> {'✅ Correcto. La geometría del hielo expande el volumen molecular, causando lisis mecánica de la membrana.' if q2.startswith('C') else '❌ Incorrecto. El hielo es menos denso pero ocupa mayor volumen tridimensional, rasgando la célula.'}<br>
                    • <strong>Pregunta 3:</strong> {'✅ Correcto. Las capas de solvatación estabilizan los iones libres mediante fuerzas ion-dipolo.' if q3.startswith('A') else '❌ Incorrecto. Los electrólitos en solución interaccionan electrostáticamente con los polos parciales del agua.'}<br>
                    • <strong>Pregunta 4:</strong> {'✅ Correcto. Una molécula puede donar 2 hidrógenos y aceptar 2 enlaces en sus pares libres (Total = 4).' if q4 == 4 else '❌ Incorrecto. El máximo tridimensional exacto es de 4 puentes de hidrógeno coordinados.'}
                </div>
                """, 
                unsafe_allow_html=True
            )

        # Botón de envío blindado contra condiciones de carrera
        if st.button(
            "🔒 Enviar Respuestas del Analizador", 
            type="primary", 
            disabled=st.session_state.procesando or bloqueado, 
            use_container_width=True, 
            key="d3_submit"
        ):
            st.session_state.procesando = True
            
            # Registro de telemetría de salida del quiz
            db.registrar_evento_telemetria(st.session_state.get("token_actual", "DEMO"), 3, "intento_envio_quiz")
            
            # Evaluación
            aciertos = sum([
                q1.startswith("B"),
                q2.startswith("C"),
                q3.startswith("A"),
                q4 == 4
            ])
            precision = int((aciertos / 4) * 100)
            
            # Control de vitalidad
            if precision < 50:
                st.session_state.vidas = max(0, st.session_state.vidas - 1)
                st.toast("Bajo rendimiento en dinámica molecular. Pérdida de 1 vida clínica.", icon="❤️")
            
            puntos_ganados = aciertos * 15
            st.session_state.puntos_acumulados += puntos_ganados
            
            st.session_state.d3_retroalimentacion = {
                "precision": precision,
                "aciertos": aciertos
            }
            
            # Sincronización atómica
            db.guardar_registro_juego(
                st.session_state.get("token_actual", "DEMO"),
                3,
                st.session_state.d3_juego_score + puntos_ganados,
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
            
            st.session_state.d3_quiz_enviado = True
            st.session_state.procesando = False
            st.rerun()
