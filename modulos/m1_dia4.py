import streamlit as st
import random
import database as db

ESCENARIOS_D4 = [
    {
        "entorno": "Gotas de grasa y lípidos apolares rodeadas por jugo digestivo acuoso en el lumen duodenal.", 
        "solucion": "Micela Clásica", 
        "desc": "Las cabezas hidrofílicas se orientan al exterior en contacto con el agua; las colas apolares al núcleo."
    },
    {
        "entorno": "Líquido extracelular acuoso separado del citosol hidrofílico por una barrera estructural.", 
        "solucion": "Bicapa Lipídica", 
        "desc": "Dos capas de fosfolípidos orientan sus colas apolares frente a frente en el centro."
    },
    {
        "entorno": "Microgota de agua metabólica atrapada en el centro de una matriz lipídica.", 
        "solucion": "Micela Inversa", 
        "desc": "Las colas lipofílicas se extienden al exterior hidrofóbico; las cabezas polares al centro."
    }
]

def inicializar_estado_dia4():
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
    token_alumno = st.session_state.get("token_actual", "DEMO")
    
    enfoque = st.radio(
        "🔬 Configurar Cámara de Exclusión:", 
        ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], 
        horizontal=True,
        key="d4_enfoque_radio"
    )
    
    tab1, tab2, tab3 = st.tabs(["🔬 Cámara de Exclusión", "🎮 Ensamblador de Micelas", "📝 Certificación del Día 4"])

    with tab1:
        st.markdown("### Fundamentos: Anfipatía y el Efecto Hidrofóbico")
        
        if enfoque == "🐾 Veterinaria":
            st.warning("🐾 **Contexto Veterinario (Digestión de Lípidos):** Las sales biliares (compuestos anfipáticos) actúan como detergentes biológicos, autoensamblándolas en micelas clásicas.")
        elif enfoque == "🩺 Medicina":
            st.warning("🩺 **Contexto Médico (Farmacología - Liposomas):** Los liposomas encapsulan medicamentos hidrofílicos en su núcleo acuoso central.")
        else:
            st.info("🧬 **Contexto Biológico (Fisiología de Membranas):** Las moléculas de agua circundantes ganan entropía al obligar a los lípidos a agruparse.")

        st.markdown("Las moléculas **anfipáticas** poseen una cabeza polar hidrofílica y una cola apolar hidrofóbica.")
        
        st.markdown("---")
        st.markdown("#### 🔬 Cámara de Exclusión de Biomoléculas")
        inyeccion = st.selectbox(
            "Selecciona la biomolécula a inyectar:", 
            ["Glucosa (Altamente Polar)", "Ácido Graso (Altamente Apolar)", "Fosfolípido (Anfipático)"]
        )

        if inyeccion == "Glucosa (Altamente Polar)":
            est, desc = "Solvatación Completa", "Formación de una capa de solvatación estable mediante puentes de hidrógeno."
            html = "<div style='background-color:#161b22; border: 1px solid #30363d; padding:30px; text-align:center; font-size:2rem; border-radius:12px;'>💧 💠 💧</div>"
        elif inyeccion == "Ácido Graso (Altamente Apolar)":
            est, desc = "Exclusión Hidrofóbica", "El agua expulsa las cadenas carbonadas apolares para no romper su red cohesiva."
            html = "<div style='background-color:#161b22; border: 1px solid #30363d; padding:30px; text-align:center; border-radius:12px;'><div style='background-color:#ffd166; width:65px; height:65px; display:inline-block; border-radius:50%; box-shadow: 0 0 15px #ffd166;'></div></div>"
        else:
            est, desc = "Auto-ensamblaje Termodinámico", "Formación espontánea de agregados supramolares para ocultar las colas."
            html = "<div style='background-color:#161b22; border: 1px solid #30363d; padding:30px; text-align:center; border-radius:12px;'><div style='border:5px dashed #00f2fe; width:85px; height:85px; display:inline-block; border-radius:50%; box-shadow: 0 0 20px rgba(0,242,254,0.3);'></div></div>"
            
        st.success(f"**Mecanismo Termodinámico:** {est}")
        st.caption(f"📋 *Descripción estructural:* {desc}")
        st.markdown(html, unsafe_allow_html=True)

    with tab2:
        st.markdown("### 🎮 Minijuego: Ensamblador de Estructuras Lipídicas")
        c_score, c_intentos = st.columns(2)
        c_score.metric("Puntaje Acumulado", f"{st.session_state.d4_juego_score} pts")
        c_intentos.metric("Estructuras Orientadas", st.session_state.d4_juego_intentos)
        
        escenario = st.session_state.d4_escenario_actual
        st.info(f"🧬 **Entorno Químico:** {escenario['entorno']}")
        
        def verificar_ensamblaje(seleccion):
            st.session_state.d4_juego_intentos += 1
            if seleccion == escenario["solucion"]:
                st.session_state.d4_juego_score += 15
                st.toast(f"¡Orientación Molecular Correcta! {escenario['desc']}", icon="✅")
                st.session_state.d4_escenario_actual = random.choice(ESCENARIOS_D4)
            else:
                st.session_state.d4_juego_score = max(0, st.session_state.d4_juego_score - 5)
                st.toast("Error de ensamblaje.", icon="❌")

        if st.button("🔵 Ensamblar Micela Clásica", use_container_width=True, key="d4_b_mc"): 
            verificar_ensamblaje("Micela Clásica")
            st.rerun()
        if st.button("🍔 Ensamblar Micela Inversa", use_container_width=True, key="d4_b_mi"): 
            verificar_ensamblaje("Micela Inversa")
            st.rerun()
        if st.button("🧱 Ensamblar Bicapa Lipídica", use_container_width=True, key="d4_b_bl"): 
            verificar_ensamblaje("Bicapa Lipídica")
            st.rerun()

    with tab3:
        st.markdown("### 📝 Cuestionario de Certificación del Día 4")
        bloqueado = st.session_state.d4_quiz_enviado

        q1 = st.radio("1. En el lumen del intestino, ¿por qué las sales biliares son indispensables?", ["A) Porque son moléculas puramente polares.", "B) Porque son compuestos anfipáticos que emulsionan las grasas.", "C) Porque actúan como enzimas proteolíticas."], disabled=bloqueado, key="d4_q1")
        q2 = st.radio("2. El fenómeno conocido como 'efecto hidrofóbico' está impulsado por:", ["A) Una ganancia de entropía en las moléculas de agua circundantes.", "B) Fuerzas magnéticas nucleares repelentes.", "C) El establecimiento de enlaces covalentes."], disabled=bloqueado, key="d4_q2")
        q3 = st.radio("3. Cuando se administra una inyección de un mineral polar como el Calcio, ¿qué pasa?", ["A) El agua se auto-ensambla en micelas clásicas.", "B) Genera enlaces por puentes disulfuro.", "C) Forma una capa de solvatación hidrofílica."], disabled=bloqueado, key="d4_q3")
        q4 = st.number_input("4. ¿Cuántas colas de ácidos grasos posee un fosfolípido celular estándar?", value=0, step=1, disabled=bloqueado, key="d4_q4")

        if bloqueado and st.session_state.d4_retroalimentacion:
            prec = st.session_state.d4_retroalimentacion["precision"]
            if prec == 100: st.success(f"🏆 **Certificación Completada:** Precisión del {prec}%.")
            else: st.error(f"❌ **Certificación Denegada:** Precisión del {prec}%.")
            st.markdown(f"<div class='lab-panel'><strong>Dictamen de Estructuras Lipídicas:</strong><br>• Pregunta 1: {'✅ Correcto.' if q1.startswith('B') else '❌ Incorrecto.'}<br>• Pregunta 2: {'✅ Correcto.' if q2.startswith('A') else '❌ Incorrecto.'}<br>• Pregunta 3: {'✅ Correcto.' if q3.startswith('C') else '❌ Incorrecto.'}<br>• Pregunta 4: {'✅ Correcto.' if q4 == 2 else '❌ Incorrecto.'}</div>", unsafe_allow_html=True)

        if st.button("🔒 Enviar Bloque al Servidor", type="primary", disabled=bloqueado, use_container_width=True, key="d4_submit"):
            aciertos = sum([q1.startswith("B"), q2.startswith("A"), q3.startswith("C"), q4 == 2])
            precision = int((aciertos / 4) * 100)
            
            if precision < 50:
                st.session_state.vidas = max(0, st.session_state.vidas - 1)
                st.toast("Fallo en la dinámica hidrofóbica.", icon="❤️")
            
            puntos_ganados = aciertos * 15
            st.session_state.puntos_acumulados += puntos_ganados
            st.session_state.d4_retroalimentacion = {"precision": precision, "aciertos": aciertos}
            
            db.guardar_registro_juego(token_alumno, 4, st.session_state.d4_juego_score + puntos_ganados, precision, {"enfoque": enfoque})
            db.sincronizar_progreso_db(token_alumno, st.session_state.puntos_acumulados, "1", st.session_state.vidas, st.session_state.tiempo_estudio_min)
            st.session_state.d4_quiz_enviado = True
            st.rerun()
