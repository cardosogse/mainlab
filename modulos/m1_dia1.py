import streamlit as st
import random
import time
import database as db

def inicializar_estado_dia1():
    """Inicializa de forma aislada y segura el estado de sesión para el Día 1."""
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
    
    # Registro de telemetría de entrada al módulo si no se ha realizado
    if "d1_telemetria_teoria" not in st.session_state:
        db.registrar_evento_telemetria(st.session_state.get("token_actual", "DEMO"), 1, "ingreso_pestana_teoria")
        st.session_state.d1_telemetria_teoria = True

    # Selector de enfoque instruccional adaptativo
    enfoque = st.radio(
        "🔬 Cambiar perspectiva del analizador:", 
        ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], 
        horizontal=True,
        disabled=st.session_state.procesando
    )
    
    # FRAGMENTACIÓN EN PESTAÑAS: Mitigación de scroll y fatiga visual
    tab1, tab2, tab3 = st.tabs(["🔬 Marco Teórico", "🎮 Simulador Cuántico", "📝 Evaluación Formativa"])

    with tab1:
        st.markdown("### Fundamentos Químicos: El Balance Iónico")
        st.markdown(
            """
            En los compartimentos líquidos del organismo animal (intracelular, intersticial y plasma), 
            los bioelementos no se encuentran en estado fundamental neutro; existen disociados como 
            **iones** debido a la ganancia o pérdida de electrones de valencia.
            """
        )
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown(
                """
                <div class='lab-panel' style='border-left: 4px solid #00f2fe;'>
                    <h4 style='color: #00f2fe; margin-top:0;'>Catión (<span style='color:#4facfe;'>+</span>)</h4>
                    <p style='font-size:0.9rem; margin-bottom:0;'>
                        Especie química que <strong>perdió electrones</strong>. Predomina la carga nuclear positiva. 
                        <br><em>Ejemplos clínicos:</em> Na⁺ (principal extracelular), K⁺ (principal intracelular), Ca²⁺.
                    </p>
                </div>
                """, 
                unsafe_allow_html=True
            )
        with col_t2:
            st.markdown(
                """
                <div class='lab-panel' style='border-left: 4px solid #ff0844;'>
                    <h4 style='color: #ff0844; margin-top:0;'>Anión (<span style='color:#ff0844;'>-</span>)</h4>
                    <p style='font-size:0.9rem; margin-bottom:0;'>
                        Especie química que <strong>ganó electrones</strong> en su orbital externo. Predomina la carga negativa.
                        <br><em>Ejemplos clínicos:</em> Cl⁻ (balance osmótico), HCO₃⁻ (amortiguador de pH plasmático).
                    </p>
                </div>
                """, 
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown("#### 🔬 Espectrómetro de Masas: Simulador de Carga Neta")
        
        col_p, col_e = st.columns(2)
        protones = col_p.slider("🔴 Protones (Z - Carga Positiva)", min_value=1, max_value=20, value=11, disabled=st.session_state.procesando)
        electrones = col_e.slider("🔵 Electrones (Carga Negativa)", min_value=1, max_value=20, value=10, disabled=st.session_state.procesando)

        carga_neta = protones - electrones
        
        # Identificación biológica guiada por las constantes atómicas
        if protones == 11 and carga_neta == 1:
            identidad = "Catión Sodio ($Na^+$) — Regula la presión osmótica extracelular."
        elif protones == 20 and carga_neta == 2:
            identidad = "Catión Calcio ($Ca^{2+}$) — Mediador de la contracción miocárdica y muscular."
        elif protones == 17 and carga_neta == -1:
            identidad = "Anión Cloruro ($Cl^-$) — Mantiene la electroneutralidad sistémica."
        elif carga_neta == 0:
            identidad = "Átomo Neutro — Altamente reactivo, inestable en soluciones acuosas biológicas."
        else:
            identidad = f"Elemento Ionizado con carga neta de {carga_neta:+}."

        st.info(f"**Elemento Identificado:** {identidad}")
        
        # Inyección visual de partículas reactivas desde assets.py
        html_protones = "<div class='particula proton'></div>" * protones
        html_electrones = "<div class='particula electron'></div>" * electrones
        st.markdown(
            f"""
            <div style="background-color: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; text-align: center;">
                <div style="margin-bottom: 15px;"><strong>Núcleo Atómico (Protones):</strong><br>{html_protones}</div>
                <div><strong>Nube de Valencia (Electrones):</strong><br>{html_electrones}</div>
            </div>
            """, 
            unsafe_allow_html=True
        )

    with tab2:
        st.markdown("### 🎮 Desafío Cuántico: Identificador de Especies")
        
        c_score, c_intentos = st.columns(2)
        c_score.metric("Puntaje en la Ronda", f"{st.session_state.d1_juego_score} pts")
        c_intentos.metric("Intentos Realizados", st.session_state.d1_juego_intentos)
        
        p_actual = st.session_state.d1_juego_actual_p
        e_actual = st.session_state.d1_juego_actual_e
        carga_real = p_actual - e_actual
        
        st.markdown(
            f"""
            <div class='lab-panel' style='text-align: center;'>
                <span style='font-size: 1.2rem;'>Analizador cuántico reporta:</span><br>
                <strong style='color:#ff6b6b; font-size:1.5rem;'>🔴 Protones: {p_actual}</strong> | 
                <strong style='color:#64d8cb; font-size:1.5rem;'>🔵 Electrones: {e_actual}</strong>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        def procesar_respuesta_juego(categoria_usuario):
            st.session_state.d1_juego_intentos += 1
            es_correcto = False
            if categoria_usuario == "Catión" and carga_real > 0: es_correcto = True
            elif categoria_usuario == "Anión" and carga_real < 0: es_correcto = True
            elif categoria_usuario == "Neutro" and carga_real == 0: es_correcto = True
            
            if es_correcto:
                st.session_state.d1_juego_score += 10
                st.toast("¡Carga identificada con precisión!", icon="✅")
            else:
                st.session_state.d1_juego_score = max(0, st.session_state.d1_juego_score - 5)
                st.toast("Fallo en la lectura de carga neta.", icon="❌")
                
            # Regenerar estado del juego de forma aleatoria
            st.session_state.d1_juego_actual_p = random.randint(8, 20)
            st.session_state.d1_juego_actual_e = st.session_state.d1_juego_actual_p + random.choice([-2, -1, 0, 1, 2])

        col_b1, col_b2, col_b3 = st.columns(3)
        if col_b1.button("Catión (+)", use_container_width=True, disabled=st.session_state.procesando, key="d1_btn_cat"):
            procesar_respuesta_juego("Catión")
            st.rerun()
        if col_b2.button("Neutro (0)", use_container_width=True, disabled=st.session_state.procesando, key="d1_btn_neu"):
            procesar_respuesta_juego("Neutro")
            st.rerun()
        if col_b3.button("Anión (-)", use_container_width=True, disabled=st.session_state.procesando, key="d1_btn_ani"):
            procesar_respuesta_juego("Anión")
            st.rerun()

    with tab3:
        st.markdown("### 📝 Evaluación de Certificación")
        bloqueado = st.session_state.d1_quiz_enviado

        # Reactivos estructurados
        q1 = st.radio(
            "1. En medicina veterinaria, una caída drástica de Calcio sérico ($Ca^{2+}$) libre provoca tetania hipocalcémica. ¿Qué alteración sufrió el átomo?",
            ["A) Perdió 2 electrones de valencia, predominando las cargas positivas del núcleo.", 
             "B) Absorbió 2 electrones del medio plasmático.", 
             "C) El núcleo expulsó 2 protones al espacio intersticial."],
            disabled=bloqueado, key="d1_radio_q1"
        )
        
        q2 = st.radio(
            "2. ¿Por qué el Cloro ($Cl^-$) actúa inherentemente como el anión predominante del líquido extracelular?",
            ["A) Porque comparte de manera equitativa sus electrones con el carbono.", 
             "B) Porque capturó un electrón para estabilizar su última capa de valencia.", 
             "C) Porque posee un déficit crónico de electrones."],
            disabled=bloqueado, key="d1_radio_q2"
        )
        
        q3 = st.radio(
            "3. Durante un estado de deshidratación severa, el Sodio plasmático ($Na^+$) se concentra. ¿Cuál fue el fenómeno atómico que dio origen a este ion?",
            ["A) La ganancia neta de un protón metabólico.", 
             "B) La fusión térmica de su envoltura atómica.", 
             "C) La pérdida de un único electrón de su orbital externo."],
            disabled=bloqueado, key="d1_radio_q3"
        )
        
        q4 = st.number_input(
            "4. Un ion detectado en una muestra biológica presenta 12 protones en su núcleo y 10 electrones orbitando. Determina su carga neta entera:",
            value=0, step=1, disabled=bloqueado, key="d1_input_q4"
        )

        # RENDERIZADO DE RETROALIMENTACIÓN FORMATIVA INMEDIATA POST-ENVÍO
        if bloqueado and st.session_state.d1_retroalimentacion:
            st.markdown("#### 🔬 Dictamen Clínico e Historial Técnico")
            prec = st.session_state.d1_retroalimentacion["precision"]
            
            if prec == 100:
                st.success(f"🏆 **Certificación Exitosa:** Precisión del {prec}%. Balance iónico comprendido a la perfección.")
            elif prec >= 70:
                st.warning(f"⚠️ **Aprobado con Observaciones:** Precisión del {prec}%. Repasa las pérdidas de electrones.")
            else:
                st.error(f"❌ **Certificación Rechazada:** Precisión del {prec}%. Se requiere revisión del marco teórico.")

            # Desglose científico formativo inline
            st.markdown(
                f"""
                <div class='lab-panel'>
                    <strong>Análisis de Reactivos:</strong><br>
                    • <strong>Pregunta 1:</strong> {'✅ Correcto. Los cationes pierden electrones.' if q1.startswith('A') else '❌ Incorrecto. El Calcio ionizado perdió electrones, no ganó ni alteró su núcleo.'}<br>
                    • <strong>Pregunta 2:</strong> {'✅ Correcto. El Cloro gana un electrón completando su octeto.' if q2.startswith('B') else '❌ Incorrecto. Al ser un anión, el cloro ha ganado carga negativa.'}<br>
                    • <strong>Pregunta 3:</strong> {'✅ Correcto. La ionización del Sodio ocurre al ceder su electrón de valencia.' if q3.startswith('C') else '❌ Incorrecto. Los protones nunca cambian en procesos metabólicos comunes.'}<br>
                    • <strong>Pregunta 4:</strong> {'✅ Correcto. 12 protones - 10 electrones = +2.' if q4 == 2 else '❌ Incorrecto. La operación matemática elemental reporta una carga neta de +2.'}
                </div>
                """, 
                unsafe_allow_html=True
            )

        # Botón de envío blindado contra clicks dobles y condiciones de carrera
        if st.button(
            "🔒 Validar Bloque de Respuestas", 
            type="primary", 
            disabled=st.session_state.procesando or bloqueado, 
            use_container_width=True, 
            key="d1_submit_quiz"
        ):
            st.session_state.procesando = True
            
            # Registrar marca de tiempo exacta de finalización
            db.registrar_evento_telemetria(st.session_state.get("token_actual", "DEMO"), 1, "intento_envio_quiz")
            
            # Validación exacta
            aciertos = sum([
                q1.startswith("A"), 
                q2.startswith("B"), 
                q3.startswith("C"), 
                q4 == 2
            ])
            precision = int((aciertos / 4) * 100)
            
            # Penalización de vidas en tiempo real si el rendimiento es crítico
            if precision < 50:
                st.session_state.vidas = max(0, st.session_state.vidas - 1)
                st.toast("Pérdida de estabilidad vital por bajo rendimiento.", icon="❤️")
            
            # Inyección de recompensa en el estado global
            puntos_ganados = aciertos * 15
            st.session_state.puntos_acumulados += puntos_ganados
            
            # Almacenamiento local del payload para persistencia ante refrescos
            st.session_state.d1_retroalimentacion = {
                "precision": precision,
                "aciertos": aciertos
            }
            
            # Sincronización atómica hacia Supabase
            db.guardar_registro_juego(
                st.session_state.get("token_actual", "DEMO"),
                1,
                st.session_state.d1_juego_score + puntos_ganados,
                precision,
                {"enfoque": enfoque, "respuestas": [q1[0], q2[0], q3[0], q4]}
            )
            
            db.sincronizar_progreso_db(
                st.session_state.token_actual,
                st.session_state.puntos_acumulados,
                "1",
                st.session_state.vidas,
                st.session_state.tiempo_estudio_min
            )
            
            st.session_state.d1_quiz_enviado = True
            st.session_state.procesando = False
            st.rerun()
