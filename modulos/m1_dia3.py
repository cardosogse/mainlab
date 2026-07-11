import streamlit as st
import random
import database as db

ESCENARIOS_D3 = [
    {
        "caso": "Unión intermolecular dinámica entre dos moléculas adyacentes de agua (H₂O - H₂O).", 
        "fuerza": "Puentes de Hidrógeno", 
        "razon": "El átomo de Hidrógeno con carga parcial positiva atrae electrostáticamente al Oxígeno de la molécula vecina."
    },
    {
        "caso": "Colas hidrofóbicas de ácidos grasos interactuando en el núcleo lipídico de la membrana celular.", 
        "fuerza": "Van der Waals", 
        "razon": "Regiones moleculares apolares que experimentan atracciones dipolo inducido transitorias por fluctuaciones electrónicas."
    },
    {
        "caso": "Un ión disociado de Sodio (Na⁺) rodeado e hidratado por moléculas de agua en el interior del plasma.", 
        "fuerza": "Ion-Dipolo", 
        "razon": "La carga completa del catión Na⁺ atrae con gran afinidad a la densidad de carga parcial negativa del Oxígeno del agua."
    }
]

def inicializar_estado_dia3():
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
    token_alumno = st.session_state.get("token_actual", "DEMO")
    
    enfoque = st.radio(
        "🔬 Configurar el Analizador Térmico:", 
        ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], 
        horizontal=True,
        key="d3_enfoque_radio"
    )
    
    tab1, tab2, tab3 = st.tabs(["🔬 Dinámica Molecular", "🎮 Fuerzas Cruzadas", "📝 Certificación del Día 3"])

    with tab1:
        st.markdown("### Fundamentos: El Agua como Solvente Biológico Universal")
        
        if enfoque == "🐾 Veterinaria":
            st.warning("🐾 **Caso Veterinario (Fisiología del Jadeo):** Los mamíferos domésticos como el perro carecen de glándulas sudoríparas eficientes en su dermis. Dependen críticamente del elevado calor de vaporización del agua; al jadear, rompen los puentes de hidrógeno superficiales en las vías respiratorias para disipar calor latente.")
        elif enfoque == "🩺 Medicina":
            st.warning("🩺 **Caso Médico (Tensión Superficial Alveolar):** En los pulmones humanos, la interfase agua-aire genera una elevada tensión superficial debido a las fuerzas cohesivas de los puentes de H. Las células alveolares tipo II deben sintetizar surfactante pulmonar para interponerse entre estos puentes.")
        else:
            st.info("🧬 **Caso Biológico (Estructura de Macromoléculas):** En el citosol celular, los puentes de hidrógeno no solo gobiernan el solvente, sino que estabilizan la estructura secundaria en alfa-hélice de las proteínas.")

        st.markdown("La polaridad de un enlace molecular se rige bajo la diferencia de electronegatividad ($\Delta\chi$):")
        
        st.markdown("---")
        st.markdown("#### 🔬 Red Térmica Estructural del Agua")
        temp = st.slider("Ajustar Temperatura del Analizador (°C):", min_value=-10, max_value=120, value=25)

        if temp < 0:
            estado, color, css = "Sólido (Hielo Cristalino)", "#a0c4ff", "display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; padding: 20px;"
            detalle = "Los puentes de hidrógeno se estabilizan al máximo formando una red cristalina hexagonal rígida."
        elif temp < 100:
            estado, color, css = "Líquido (Agua Metabólica)", "#00f2fe", "display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; padding: 20px;"
            detalle = "Interacciones dinámicas continuas; los puentes de hidrógeno se rompen y reforman en picosegundos."
        else:
            estado, color, css = "Gas (Vapor de Agua)", "#e5e5e5", "display: flex; flex-wrap: wrap; gap: 40px; justify-content: space-around; padding: 50px;"
            detalle = "La energía cinética supera la energía de enlace de las interacciones moleculares."

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
        st.info(f"📋 **Escenario Organizado:** {escenario['caso']}")
        
        def verificar_fuerza(seleccion):
            st.session_state.d3_juego_intentos += 1
            if seleccion == escenario["fuerza"]:
                st.session_state.d3_juego_score += 10
                st.toast(f"¡Correcto! {escenario['razon']}", icon="✅")
                st.session_state.d3_escenario_actual = random.choice(ESCENARIOS_D3)
            else:
                st.session_state.d3_juego_score = max(0, st.session_state.d3_juego_score - 5)
                st.toast("Interacción intermolecular incorrecta.", icon="❌")

        col1, col2, col3 = st.columns(3)
        if col1.button("Puentes de Hidrógeno", use_container_width=True, key="d3_b1"): 
            verificar_fuerza("Puentes de Hidrógeno")
            st.rerun()
        if col2.button("Van der Waals", use_container_width=True, key="d3_b2"): 
            verificar_fuerza("Van der Waals")
            st.rerun()
        if col3.button("Ion-Dipolo", use_container_width=True, key="d3_b3"): 
            verificar_fuerza("Ion-Dipolo")
            st.rerun()

    with tab3:
        st.markdown("### 📝 Cuestionario de Certificación del Día 3")
        bloqueado = st.session_state.d3_quiz_enviado

        q1 = st.radio("1. En la fisiología respiratoria, ¿qué fuerzas intermoleculares rompe específicamente el surfactante pulmonar?", ["A) Fuerzas de dispersión débiles de Van der Waals.", "B) Los puentes de hidrógeno intermoleculares del agua.", "C) Enlaces iónicos intramembranales."], disabled=bloqueado, key="d3_q1")
        q2 = st.radio("2. ¿Por qué el congelamiento severo de los tejidos periféricos provoca necrosis celular directa?", ["A) Porque el agua disminuye bruscamente su densidad molecular.", "B) Porque desnaturaliza covalentemente la envoltura lipídica.", "C) Porque los puentes de hidrógeno forman una red cristalina que expande el volumen del agua."], disabled=bloqueado, key="d3_q2")
        q3 = st.radio("3. Tras la infusión intravenosa de una solución electrolítica, ¿gracias a qué mecanismo se de el equilibrio?", ["A) Interacciones electrostáticas de tipo ion-dipolo.", "B) El establecimiento de enlaces covalentes coordinados.", "C) Fenómenos de evaporación selectiva."], disabled=bloqueado, key="d3_q3")
        q4 = st.number_input("4. Máximo teórico de puentes de hidrógeno que puede coordinar una única molécula de agua:", value=0, step=1, disabled=bloqueado, key="d3_q4")

        if bloqueado and st.session_state.d3_retroalimentacion:
            prec = st.session_state.d3_retroalimentacion["precision"]
            if prec == 100: st.success(f"🏆 **Certificación Completada:** Precisión del {prec}%.")
            else: st.error(f"❌ **Certificación Denegada:** Precisión del {prec}%.")
            st.markdown(f"<div class='lab-panel'><strong>Dictamen Clínico Formativo:</strong><br>• Pregunta 1: {'✅ Correcto.' if q1.startswith('B') else '❌ Incorrecto.'}<br>• Pregunta 2: {'✅ Correcto.' if q2.startswith('C') else '❌ Incorrecto.'}<br>• Pregunta 3: {'✅ Correcto.' if q3.startswith('A') else '❌ Incorrecto.'}<br>• Pregunta 4: {'✅ Correcto.' if q4 == 4 else '❌ Incorrecto.'}</div>", unsafe_allow_html=True)

        if st.button("🔒 Enviar Respuestas del Analizador", type="primary", disabled=bloqueado, use_container_width=True, key="d3_submit"):
            aciertos = sum([q1.startswith("B"), q2.startswith("C"), q3.startswith("A"), q4 == 4])
            precision = int((aciertos / 4) * 100)
            
            if precision < 50:
                st.session_state.vidas = max(0, st.session_state.vidas - 1)
                st.toast("Bajo rendimiento en dinámica molecular.", icon="❤️")
            
            puntos_ganados = aciertos * 15
            st.session_state.puntos_acumulados += puntos_ganados
            st.session_state.d3_retroalimentacion = {"precision": precision, "aciertos": aciertos}
            
            db.guardar_registro_juego(token_alumno, 3, st.session_state.d3_juego_score + puntos_ganados, precision, {"enfoque": enfoque})
            db.sincronizar_progreso_db(token_alumno, st.session_state.puntos_acumulados, "1", st.session_state.vidas, st.session_state.tiempo_estudio_min)
            st.session_state.d3_quiz_enviado = True
            st.rerun()
