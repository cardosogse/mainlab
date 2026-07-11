import streamlit as st
import random
import database as db

def inicializar_estado_dia1():
    if "d1_juego_score" not in st.session_state:
        st.session_state.d1_juego_score = 0
    if "d1_juego_intentos" not in st.session_state:
        st.session_state.d1_juego_intentos = 0
    if "d1_quiz_enviado" not in st.session_state:
        st.session_state.d1_quiz_enviado = False
    if "d1_juego_actual_p" not in st.session_state:
        st.session_state.d1_juego_actual_p = random.randint(8, 20)
        st.session_state.d1_juego_actual_e = st.session_state.d1_juego_actual_p + random.choice([-2, -1, 0, 1, 2])
    if "d1_retroalimentacion" not in st.session_state:
        st.session_state.d1_retroalimentacion = None

def app():
    inicializar_estado_dia1()
    token_alumno = st.session_state.get("token_actual", "DEMO")
    
    # Selector de Enfoque con Transductor Dinámico de Texto
    enfoque = st.radio(
        "🔬 Configurar el Analizador Metabólico:", 
        ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], 
        horizontal=True
    )
    
    tab1, tab2, tab3 = st.tabs(["🔬 Marco Teórico Adaptativo", "🎮 Simulador Cuántico", "📝 Evaluación Formativa"])

    with tab1:
        st.markdown("### Fundamentos Químicos: El Balance Iónico")
        
        # --- Dinamismo real según el Perfil Seleccionado ---
        if enfoque == "🐾 Veterinaria":
            st.warning("⚠️ **Enfoque Clínico Veterinario:** El desbalance de electrólitos altera los potenciales de membrana musculares, provocando patologías graves como la eclampsia en perras lactantes o la hipocalcemia posparto en vacas lecheras.")
        elif enfoque == "🩺 Medicina":
            st.warning("🩺 **Enfoque Médico Humano:** La homeostasis iónica en el plasma controla la volemia sistémica y la conducción del haz de His en el corazón humano; una hiperpotasemia puede inducir paro cardíaco.")
        else:
            st.info("🧬 **Enfoque de Biología Molecular:** El gradiente electroquímico generado por cationes y aniones a través de las membranas lipídicas es el motor termodinámico de la síntesis de ATP mitocondrial y el transporte activo secundario.")

        st.markdown(
            """
            En los compartimentos líquidos del organismo, los bioelementos no se encuentran en estado neutro; 
            existen disociados como **iones** debido a la ganancia o pérdida de electrones de valencia.
            """
        )
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("<div class='lab-panel' style='border-left: 4px solid #00f2fe;'><h4 style='color:#00f2fe; margin-top:0;'>Catión (+)</h4><p style='font-size:0.9rem; margin-bottom:0;'>Especie química que <strong>perdió electrones</strong>. Carga nuclear positiva predominante.<br><em>Ejemplos:</em> Na⁺, K⁺, Ca²⁺.</p></div>", unsafe_allow_html=True)
        with col_t2:
            st.markdown("<div class='lab-panel' style='border-left: 4px solid #ff0844;'><h4 style='color:#ff0844; margin-top:0;'>Anión (-)</h4><p style='font-size:0.9rem; margin-bottom:0;'>Especie química que <strong>ganó electrones</strong>. Carga negativa predominante.<br><em>Ejemplos:</em> Cl⁻, HCO₃⁻.</p></div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🔬 Espectrómetro de Masas: Simulador de Carga Neta")
        col_p, col_e = st.columns(2)
        protones = col_p.slider("🔴 Protones (Z)", min_value=1, max_value=20, value=11)
        electrones = col_e.slider("🔵 Electrones (e⁻)", min_value=1, max_value=20, value=10)

        carga_neta = protones - electrones
        
        if protones == 11 and carga_neta == 1: identidad = "Catión Sodio ($Na^+$) — Regula la presión osmótica extracelular."
        elif protones == 20 and carga_neta == 2: identidad = "Catión Calcio ($Ca^{2+}$) — Mediador de la contracción muscular."
        elif protones == 17 and carga_neta == -1: identidad = "Anión Cloruro ($Cl^-$) — Mantiene la electroneutralidad salina."
        elif carga_neta == 0: identidad = "Átomo Neutro — Inestable y altamente reactivo en solución acuosa."
        else: identidad = f"Elemento Ionizado con carga neta de {carga_neta:+}."

        st.info(f"**Elemento Identificado:** {identidad}")
        
        html_protones = "<div class='particula proton'></div>" * protones
        html_electrones = "<div class='particula electron'></div>" * electrones
        st.markdown(f"<div style='background-color:#161b22; padding:20px; border-radius:12px; border:1px solid #30363d; text-align:center;'><div style='margin-bottom:15px;'><strong>Núcleo (Protones):</strong><br>{html_protones}</div><div><strong>Nube de Valencia (Electrones):</strong><br>{html_electrones}</div></div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("### 🎮 Desafío Cuántico: Identificador de Especies")
        c_score, c_intentos = st.columns(2)
        c_score.metric("Puntaje en la Ronda", f"{st.session_state.d1_juego_score} pts")
        c_intentos.metric("Intentos Realizados", st.session_state.d1_juego_intentos)
        
        p_actual = st.session_state.d1_juego_actual_p
        e_actual = st.session_state.d1_juego_actual_e
        carga_real = p_actual - e_actual
        
        st.markdown(f"<div class='lab-panel' style='text-align:center;'><span style='font-size:1.2rem;'>Analizador reporta:</span><br><strong style='color:#ff6b6b; font-size:1.5rem;'>🔴 Protones: {p_actual}</strong> | <strong style='color:#64d8cb; font-size:1.5rem;'>🔵 Electrones: {e_actual}</strong></div>", unsafe_allow_html=True)
        
        def procesar_respuesta_juego(categoria_usuario):
            st.session_state.d1_juego_intentos += 1
            correcto = (categoria_usuario == "Catión" and carga_real > 0) or (categoria_usuario == "Anión" and carga_real < 0) or (categoria_usuario == "Neutro" and carga_real == 0)
            if correcto:
                st.session_state.d1_juego_score += 10
                st.toast("¡Carga identificada con precisión!", icon="✅")
            else:
                st.session_state.d1_juego_score = max(0, st.session_state.d1_juego_score - 5)
                st.toast("Fallo en la lectura de carga neta.", icon="❌")
            st.session_state.d1_juego_actual_p = random.randint(8, 20)
            st.session_state.d1_juego_actual_e = st.session_state.d1_juego_actual_p + random.choice([-2, -1, 0, 1, 2])

        col_b1, col_b2, col_b3 = st.columns(3)
        if col_b1.button("Catión (+)", use_container_width=True, key="d1_b1"): procesar_respuesta_juego("Catión"); st.rerun()
        if col_b2.button("Neutro (0)", use_container_width=True, key="d1_b2"): procesar_respuesta_juego("Neutro"); st.rerun()
        if col_b3.button("Anión (-)", use_container_width=True, key="d1_b3"): procesar_respuesta_juego("Anión"); st.rerun()

    with tab3:
        st.markdown("### 📝 Evaluación de Certificación")
        bloqueado = st.session_state.d1_quiz_enviado

        q1 = st.radio("1. En medicina veterinaria, una caída drástica de Calcio sérico ($Ca^{2+}$) libre provoca tetania. ¿Qué alteración sufrió el átomo?", ["A) Perdió 2 electrones de valencia, predominando las cargas positivas del núcleo.", "B) Absorbió 2 electrones del medio plasmático.", "C) El núcleo expulsó 2 protones al espacio intersticial."], disabled=bloqueado, key="d1_q1_r")
        q2 = st.radio("2. ¿Por qué el Cloro ($Cl^-$) actúa inherentemente como el anión predominante del líquido extracelular?", ["A) Porque comparte de manera equitativa sus electrones con el carbono.", "B) Porque capturó un electrón para completar su última capa de valencia.", "C) Porque posee un déficit crónico de electrones."], disabled=bloqueado, key="d1_q2_r")
        q3 = st.radio("3. Durante un estado de deshidratación severa, el Sodio plasmático ($Na^+$) se concentra. ¿Cuál fue el fenómeno atómico que dio origen a este ion?", ["A) La ganancia neta de un protón metabólico.", "B) La fusión térmica de su envoltura atómica.", "C) La pérdida de un único electrón de su orbital externo."], disabled=bloqueado, key="d1_q3_r")
        q4 = st.number_input("4. Un ion detectado en una muestra biológica presenta 12 protones en su núcleo y 10 electrones orbitando. Determina su carga neta entera:", value=0, step=1, disabled=bloqueado, key="d1_q4_n")

        if bloqueado and st.session_state.d1_retroalimentacion:
            prec = st.session_state.d1_retroalimentacion["precision"]
            if prec == 100: st.success(f"🏆 **Certificación Exitosa:** Precisión del {prec}%. Balance iónico comprendido a la perfección.")
            else: st.error(f"❌ **Certificación Rechazada:** Precisión del {prec}%. Se requiere revisión del marco teórico.")
            st.markdown(f"<div class='lab-panel'><strong>Dictamen de Respuestas:</strong><br>• Pregunta 1: {'✅ Correcto.' if q1.startswith('A') else '❌ Incorrecto.'}<br>• Pregunta 2: {'✅ Correcto.' if q2.startswith('B') else '❌ Incorrecto.'}<br>• Pregunta 3: {'✅ Correcto.' if q3.startswith('C') else '❌ Incorrecto.'}<br>• Pregunta 4: {'✅ Correcto.' if q4 == 2 else '❌ Incorrecto.'}</div>", unsafe_allow_html=True)

        if st.button("🔒 Validar Bloque de Respuestas", type="primary", disabled=bloqueado, use_container_width=True, key="d1_submit"):
            aciertos = sum([q1.startswith("A"), q2.startswith("B"), q3.startswith("C"), q4 == 2])
            precision = int((aciertos / 4) * 100)
            
            if precision < 50:
                st.session_state.vidas = max(0, st.session_state.vidas - 1)
                st.toast("Pérdida de estabilidad vital por bajo rendimiento.", icon="❤️")
            
            puntos_ganados = aciertos * 15
            st.session_state.puntos_acumulados += puntos_ganados
            st.session_state.d1_retroalimentacion = {"precision": precision, "aciertos": aciertos}
            
            db.guardar_registro_juego(token_alumno, 1, st.session_state.d1_juego_score + puntos_ganados, precision, {"enfoque": enfoque, "respuestas": [q1[0], q2[0], q3[0], q4]})
            db.sincronizar_progreso_db(token_alumno, st.session_state.puntos_acumulados, "1", st.session_state.vidas, st.session_state.tiempo_estudio_min)
            st.session_state.d1_quiz_enviado = True
            st.rerun()
