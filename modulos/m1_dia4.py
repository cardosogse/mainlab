import streamlit as st
import random
import database as db

# Base de datos de entornos termodinámicos para el minijuego de auto-ensamblaje
ESCENARIOS_D4 = [
    {
        "entorno": "Gotas de grasa y lípidos apolares rodeadas por jugo digestivo acuoso en el lumen duodenal.", 
        "solucion": "Micela Clásica", 
        "desc": "Las cabezas hidrofílicas se orientan al exterior en contacto con el agua; las colas apolares se empaquetan al núcleo."
    },
    {
        "entorno": "Líquido extracelular acuoso separado del citosol hidrofílico por una barrera estructural duradera.", 
        "solucion": "Bicapa Lipídica", 
        "desc": "Dos capas de fosfolípidos orientan sus colas apolares frente a frente en el centro, aislando los compartimentos acuosos."
    },
    {
        "entorno": "Microgota de agua metabólica atrapada en el centro de una matriz lipídica o tejido adiposo puro.", 
        "solucion": "Micela Inversa", 
        "desc": "Las colas lipofílicas se extienden al exterior hidrofóbico; las cabezas polares se agrupan al centro protegiendo el agua."
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
    token_alumno = st.session_state.get("token_actual", "DEMO")[cite: 20]
    
    enfoque = st.radio(
        "🔬 Configurar Cámara de Exclusión:", 
        ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], 
        horizontal=True,
        key="d4_enfoque_radio"
    )
    
    tab1, tab2, tab3 = st.tabs(["🔬 Cámara de Exclusión", "🎮 Ensamblador de Micelas", "📝 Certificación del Día 4"])

    with tab1:
        st.markdown("### Fundamentos: Anfipatía y el Efecto Hidrofóbico")
        
        # --- Contenido contextualizado dinámico ---
        if enfoque == "🐾 Veterinaria":
            st.warning("🐾 **Contexto Veterinario (Digestión de Lípidos):** Los animales monogástricos consumen lípidos neutros que no pueden disolverse en los jugos digestivos. Las **sales biliares** (compuestos anfipáticos derivados del colesterol) actúan como detergentes biológicos, rompiendo las grandes gotas de grasa y autoensamblándolas en **micelas clásicas** para permitir que las lipasas pancreáticas digieran la dieta.")
        elif enfoque == "🩺 Medicina":
            st.warning("🩺 **Contexto Médico (Farmacología - Liposomas):** La medicina moderna utiliza el autoensamblaje anfipático para el transporte dirigido de fármacos. Los **liposomas** (esferas artificiales formadas por una bicapa de fosfolípidos) encapsulan medicamentos hidrofílicos en su núcleo acuoso central o compuestos lipofílicos en su bicapa, permitiendo atravesar membranas biológicas sin degradarse.")
        else:
            st.info("🧬 **Contexto Biológico (Fisiología de Membranas):** El efecto hidrofóbico es el motor de la vida. No surge de una atracción electromagnética real entre los lípidos, sino de la termodinámica del agua: las moléculas de agua circundantes ganan **entropía** (aleatoriedad) al obligar a los lípidos a agruparse, liberando las estructuras rígidas en 'clatrato' que el agua forma alrededor de las colas hidrofóbicas.")

        st.markdown(
            """
            Las moléculas **anfipáticas** poseen una cabeza polar hidrofílica y una cola apolar hidrofóbica. 
            Su interacción con el solvente forzar agregados supramolares espontáneos.
            """
        )
        
        st.markdown("---")
        st.markdown("#### 🔬 Cámara de Exclusión de Biomoléculas")
        inyeccion = st.selectbox(
            "Selecciona la biomolécula a inyectar en el solvente polar:", 
            ["Glucosa (Altamente Polar)", "Ácido Graso (Altamente Apolar)", "Fosfolípido (Anfipático)"]
        )[cite: 23]

        if inyeccion == "Glucosa (Altamente Polar)":
            est, desc = "Solvatación Completa", "Formación de una capa de solvatación estable mediante puentes de hidrógeno con los hidroxilos de la glucosa."[cite: 23]
            html = "<div style='background-color:#161b22; border: 1px solid #30363d; padding:30px; text-align:center; font-size:2rem; border-radius:12px;'>💧 💠 💧</div>"[cite: 23]
        elif inyeccion == "Ácido Graso (Altamente Apolar)":
            est, desc = "Exclusión Hidrofóbica (Aglutinación)", "El agua expulsa las cadenas carbonadas apolares para no romper su red cohesiva de puentes, forzando la separación de fases."[cite: 23]
            html = "<div style='background-color:#161b22; border: 1px solid #30363d; padding:30px; text-align:center; border-radius:12px;'><div style='background-color:#ffd166; width:65px; height:65px; display:inline-block; border-radius:50%; box-shadow: 0 0 15px #ffd166;'></div></div>"[cite: 23]
        else:
            est, desc = "Auto-ensamblaje Termodinámico", "Formación espontánea de agregados supramolares (micelas o bicapas) para ocultar las colas apolares y exponer las cabezas hidrofílicas."[cite: 23]
            html = "<div style='background-color:#161b22; border: 1px solid #30363d; padding:30px; text-align:center; border-radius:12px;'><div style='border:5px dashed #00f2fe; width:85px; height:85px; display:inline-block; border-radius:50%; box-shadow: 0 0 20px rgba(0,242,254,0.3);'></div></div>"[cite: 23]
            
        st.success(f"**Mecanismo Termodinámico:** {est}")[cite: 23]
        st.caption(f"📋 *Descripción estructural:* {desc}")[cite: 23]
        st.markdown(html, unsafe_allow_html=True)[cite: 23]

    with tab2:
        st.markdown("### 🎮 Minijuego: Ensamblador de Estructuras Lipídicas")
        c_score, c_intentos = st.columns(2)[cite: 23]
        c_score.metric("Puntaje Acumulado", f"{st.session_state.d4_juego_score} pts")[cite: 23]
        c_intentos.metric("Estructuras Orientadas", st.session_state.d4_juego_intentos)[cite: 23]
        
        escenario = st.session_state.d4_escenario_actual[cite: 23]
        st.info(f"🧬 **Entorno Químico del Paciente:** {escenario['entorno']}")[cite: 23]
        st.write("¿Cómo se organizarán espacialmente las moléculas anfipáticas en este medio?")[cite: 23]
        
        def verificar_ensamblaje(seleccion):
            st.session_state.d4_juego_intentos += 1[cite: 23]
            if seleccion == escenario["solucion"]:[cite: 23]
                st.session_state.d4_juego_score += 15[cite: 23]
                st.toast(f"¡Orientación Molecular Correcta! {escenario['desc']}", icon="✅")[cite: 23]
                st.session_state.d4_escenario_actual = random.choice(ESCENARIOS_D4)[cite: 23]
            else:
                st.session_state.d4_juego_score = max(0, st.session_state.d4_juego_score - 5)[cite: 23]
                st.toast("Error de ensamblaje. Colapso hidrofóbico.", icon="❌")[cite: 23]

        if st.button("🔵 Ensamblar Micela Clásica", use_container_width=True, key="d4_b_mc"): verificar_ensamblaje("Micela Clásica"); st.rerun()[cite: 23]
        if st.button("🍔 Ensamblar Micela Inversa", use_container_width=True, key="d4_b_mi"): verificar_ensamblaje("Micela Inversa"); st.rerun()[cite: 23]
        if st.button("🧱 Ensamblar Bicapa Lipídica", use_container_width=True, key="d4_b_bl"): verificar_ensamblaje("Bicapa Lipídica"); st.rerun()[cite: 23]

    with tab3:
        st.markdown("### 📝 Cuestionario de Certificación del Día 4")
        bloqueado = st.session_state.d4_quiz_enviado[cite: 23]

        q1 = st.radio("1. En el lumen del intestino delgado de los mamíferos, ¿por qué las sales biliares son indispensables para la digestión de los lípidos?", ["A) Porque son moléculas puramente polares que disuelven químicamente los triglicéridos.", "B) Porque son compuestos anfipáticos que emulsionan las grasas formando micelas, aumentando la superficie de acción de las lipasas.", "C) Porque actúan como enzimas proteolíticas específicas en el jugo entérico."], disabled=bloqueado, key="d4_q1")[cite: 23]
        q2 = st.radio("2. El fenómeno físico-químico conocido como 'efecto hidrofóbico' está impulsado energéticamente por:", ["A) Una ganancia termodinámica de entropía en las moléculas de agua circundantes al minimizar su ordenamiento rígido alrededor de solutos apolares.", "B) Fuerzas magnéticas nucleares repelentes de largo alcance generadas por el núcleo del oxígeno.", "C) El establecimiento de enlaces covalentes fuertes cruzados entre los lípidos y el agua."], disabled=bloqueado, key="d4_q2")[cite: 23]
        q3 = st.radio("3. Cuando se administra una inyección de un mineral altamente polar como el Calcio ($Ca^{2+}$), ¿qué estructura adopta el solvente a su alrededor?", ["A) El agua se auto-ensambla en micelas clásicas protectoras.", "B) Genera enlaces por puentes disulfuro cruzados transitorios.", "C) Forma una capa de solvatación hidrofílica orientando los átomos de Oxígeno (parcialmente negativos) hacia el ión."], disabled=bloqueado, key="d4_q3")[cite: 23]
        q4 = st.number_input("4. ¿Cuántas colas de ácidos grasos hidrofóbicas posee la estructura básica de una molécula de fosfolípido celular estándar bicapa?", value=0, step=1, disabled=bloqueado, key="d4_q4")[cite: 23]

        if bloqueado and st.session_state.d4_retroalimentacion:[cite: 23]
            prec = st.session_state.d4_retroalimentacion["precision"][cite: 23]
            if prec == 100: st.success(f"🏆 **Certificación Completada:** Precisión del {prec}%.")[cite: 23]
            else: st.error(f"❌ **Certificación Denegada:** Precisión del {prec}%.")[cite: 23]
            st.markdown(f"<div class='lab-panel'><strong>Dictamen de Estructuras Lipídicas:</strong><br>• Pregunta 1: {'✅ Correcto.' if q1.startswith('B') else '❌ Incorrecto.'}<br>• Pregunta 2: {'✅ Correcto.' if q2.startswith('A') else '❌ Incorrecto.'}<br>• Pregunta 3: {'✅ Correcto.' if q3.startswith('C') else '❌ Incorrecto.'}<br>• Pregunta 4: {'✅ Correcto.' if q4 == 2 else '❌ Incorrecto.'}</div>", unsafe_allow_html=True)[cite: 23]

        if st.button("🔒 Enviar Bloque al Servidor", type="primary", disabled=bloqueado, use_container_width=True, key="d4_submit"):[cite: 23]
            aciertos = sum([q1.startswith("B"), q2.startswith("A"), q3.startswith("C"), q4 == 2])[cite: 23]
            precision = int((aciertos / 4) * 100)[cite: 23]
            
            if precision < 50:[cite: 23]
                st.session_state.vidas = max(0, st.session_state.vidas - 1)[cite: 23]
                st.toast("Fallo en la dinámica hidrofóbica.", icon="❤️")[cite: 23]
            
            puntos_ganados = aciertos * 15[cite: 23]
            st.session_state.puntos_acumulados += puntos_ganados[cite: 23]
            st.session_state.d4_retroalimentacion = {"precision": precision, "aciertos": aciertos}[cite: 23]
            
            db.guardar_registro_juego(token_alumno, 4, st.session_state.d4_juego_score + puntos_ganados, precision, {"enfoque": enfoque})[cite: 23]
            db.sincronizar_progreso_db(token_alumno, st.session_state.puntos_acumulados, "1", st.session_state.vidas, st.session_state.tiempo_estudio_min)[cite: 23]
            st.session_state.d4_quiz_enviado = True[cite: 23]
            st.rerun()[cite: 23]
