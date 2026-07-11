import streamlit as st
import random
import database as db

# Base de datos estática optimizada para el simulador de enlaces
BIOELEMENTOS = {
    "Oxígeno (O)": {"simbolo": "O", "chi": 3.44},
    "Nitrógeno (N)": {"simbolo": "N", "chi": 3.04},
    "Carbono (C)": {"simbolo": "C", "chi": 2.55},
    "Hidrógeno (H)": {"simbolo": "H", "chi": 2.20},
    "Sodio (Na)": {"simbolo": "Na", "chi": 0.93},
    "Cloro (Cl)": {"simbolo": "Cl", "chi": 3.16},
    "Calcio (Ca)": {"simbolo": "Ca", "chi": 1.00},
    "Fósforo (P)": {"simbolo": "P", "chi": 2.19}
}

INTRUSOS_DB = [
    {"opciones": ["O-O (O₂)", "C-H (Metano)", "N-N (N₂)", "Na-Cl (Sal)"], "intruso": "Na-Cl (Sal)", "razon": "El NaCl posee un enlace Iónico debido a su gran diferencia de electronegatividad, mientras que los demás son enlaces Covalentes Apolares pura o prácticamente puros."},
    {"opciones": ["O-H (Agua)", "N-H (Amoníaco)", "C-O (Carbonilo)", "O-O (O₂)"], "intruso": "O-O (O₂)", "razon": "El O₂ es un enlace Covalente Apolar puro (Δχ = 0), mientras que los demás presentan enlaces Covalentes Polares debido a la distribución asimétrica de los electrones."},
    {"opciones": ["Ca-Cl (Cloruro de Calcio)", "K-Cl (Cloruro de Potasio)", "Na-Cl (Cloruro de Sodio)", "C-H (Metano)"], "intruso": "C-H (Metano)", "razon": "El enlace C-H tiene una Δχ de solo 0.35, clasificándose como Covalente Apolar, en contraste con los demás que exhiben un comportamiento fuertemente Iónico."}
]

def inicializar_estado_dia2():
    """Garantiza la existencia y aislamiento de las variables de control para el Día 2."""
    if "d2_juego_score" not in st.session_state:
        st.session_state.d2_juego_score = 0
    if "d2_juego_intentos" not in st.session_state:
        st.session_state.d2_juego_intentos = 0
    if "d2_quiz_enviado" not in st.session_state:
        st.session_state.d2_quiz_enviado = False
    if "d2_ronda_actual" not in st.session_state:
        st.session_state.d2_ronda_actual = random.choice(INTRUSOS_DB)
    if "d2_retroalimentacion" not in st.session_state:
        st.session_state.d2_retroalimentacion = None

def app():
    inicializar_estado_dia2()
    
    # Telemetría de entrada al módulo instruccional
    if "d2_telemetria_iniciada" not in st.session_state:
        db.registrar_evento_telemetria(st.session_state.get("token_actual", "DEMO"), 2, "ingreso_pestana_teoria")
        st.session_state.d2_telemetria_iniciada = True
        
    enfoque = st.radio(
        "🔬 Configuración del espectro del analizador:", 
        ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], 
        horizontal=True, 
        key="d2_enfoque",
        disabled=st.session_state.procesando
    )
    
    # ESTRUCTURA INSTRUCCIONAL BASADA EN PESTAÑAS (UX Antifatiga)
    tab1, tab2, tab3 = st.tabs(["🔬 Escala de Pauling", "🎮 Minijuego: Intruso Químico", "📝 Cuestionario de Certificación"])

    with tab1:
        st.markdown("### Fundamentos: Enlaces Químicos y la Escala de Pauling")
        st.markdown(
            """
            La polaridad de un enlace químico determina cómo interactúan los fármacos y las biomoléculas 
            en soluciones acuosas corporales. Todo se rige bajo la diferencia de electronegatividad ($$\Delta\chi$$):
            """
        )
        
        st.markdown(
            """
            > **Criterios de Clasificación Estricta:**
            > *   $$\Delta\chi < 0.4$$: **Covalente Apolar** (Compartición equitativa, lipofílicos).
            > *   $$0.4 \le \Delta\chi \le 1.7$$: **Covalente Polar** (Cargas parciales, dipolos solubles).
            > *   $$\Delta\chi > 1.7$$: **Iónico** (Transferencia completa de electrones, disociación iónica).
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        st.markdown("#### 💥 Simulador de Colisión Atómica")
        
        col_a, col_b = st.columns(2)
        atomo_a = col_a.selectbox("Selecciona el Átomo A:", list(BIOELEMENTOS.keys()), index=3, disabled=st.session_state.procesando)
        atomo_b = col_b.selectbox("Selecciona el Átomo B:", list(BIOELEMENTOS.keys()), index=0, disabled=st.session_state.procesando)

        datos_a, datos_b = BIOELEMENTOS[atomo_a], BIOELEMENTOS[atomo_b]
        delta_chi = round(abs(datos_a["chi"] - datos_b["chi"]), 2)
        
        cat = datos_a["simbolo"] if datos_a["chi"] < datos_b["chi"] else datos_b["simbolo"]
        an = datos_b["simbolo"] if datos_a["chi"] < datos_b["chi"] else datos_a["simbolo"]

        st.markdown(f"##### Análisis Cuántico: $$\Delta\chi = {delta_chi}$$")
        
        if delta_chi < 0.4:
            st.success("Resultado: **Enlace Covalente Apolar Puro/Práctico**")
            html = f"<div class='nube-apolar'><span>{datos_a['simbolo']}</span><span>{datos_b['simbolo']}</span></div>"
        elif delta_chi <= 1.7:
            st.warning("Resultado: **Enlace Covalente Polar (Dipolo Inducido)**")
            html = f"<div class='nube-polar'><span>{datos_a['simbolo']}</span><span>{datos_b['simbolo']}</span></div>"
        else:
            st.error("Resultado: **Enlace Iónico (Disociación Electrostática)**")
            html = f"<div class='ruptura-ionica'><div class='ion-cat'>{cat}⁺</div><div class='ion-an'>{an}⁻</div></div>"
            
        st.markdown(html, unsafe_allow_html=True)

    with tab2:
        st.markdown("### 🎮 El Intruso Químico")
        
        c_score, c_intentos = st.columns(2)
        c_score.metric("Puntaje Acumulado", f"{st.session_state.d2_juego_score} pts")
        c_intentos.metric("Rondas Evaluadas", st.session_state.d2_juego_intentos)
        
        ronda = st.session_state.d2_ronda_actual
        st.info("Identifica la molécula cuyo tipo de enlace **NO coincide** con la naturaleza electroquímica de las demás:")
        
        def verificar_intruso(seleccion):
            st.session_state.d2_juego_intentos += 1
            if seleccion == ronda["intruso"]:
                st.session_state.d2_juego_score += 15
                st.toast(f"¡Excelente! {ronda['razon']}", icon="✅")
                st.session_state.d2_ronda_actual = random.choice(INTRUSOS_DB)
            else:
                st.session_state.d2_juego_score = max(0, st.session_state.d2_juego_score - 5)
                st.toast("Error en el análisis del enlace.", icon="❌")

        # Renderizado seguro de botones con control anti-concurrencia
        for op in ronda["opciones"]:
            if st.button(op, use_container_width=True, key=f"d2_btn_{op}", disabled=st.session_state.procesando):
                verificar_intruso(op)
                st.rerun()

    with tab3:
        st.markdown("### 📝 Cuestionario de Certificación del Día 2")
        bloqueado = st.session_state.d2_quiz_enviado

        q1 = st.radio(
            "1. En la práctica clínica veterinaria, ¿qué fármacos logran atravesar pasivamente la barrera hematoencefálica (BHE) con mayor facilidad?",
            ["A) Compuestos de naturaleza netamente Iónica.", 
             "B) Fármacos con enlaces Covalentes Apolares (estructuras altamente lipofílicas).", 
             "C) Moléculas de alta polaridad hidrofílica."],
            disabled=bloqueado, key="d2_q1"
        )
        
        q2 = st.radio(
            "2. En una molécula de agua ($$H_2O$$), ¿cuál es el efecto físico provocado por la alta electronegatividad del Oxígeno frente al Hidrógeno?",
            ["A) Un enlace covalente apolar simétrico.", 
             "B) Un enlace covalente polar con densidades de carga parciales y formación de un dipolo.", 
             "C) La cesión completa de electrones formando un cristal iónico."],
            disabled=bloqueado, key="d2_q2"
        )
        
        q3 = st.radio(
            "3. Cuando se administra suero fisiológico, ¿en qué estado físico se encuentran los átomos de Sodio ($$Na$$) y Cloro ($$Cl$$) en el plasma?",
            ["A) Unidos rígidamente compartiendo pares de electrones.", 
             "B) Formando un enlace covalente polar débil.", 
             "C) Completamente disociados e interactuando como iones libres ($$Na^+$$ y $$Cl^-$$) rodeados de agua."],
            disabled=bloqueado, key="d2_q3"
        )
        
        q4 = st.number_input(
            "4. Calcula y escribe el valor exacto de $$\Delta\chi$$ para un enlace entre el Cloro ($$\chi = 3.16$$) y el Carbono ($$\chi = 2.55$$):",
            value=0.00, step=0.01, format="%.2f", disabled=bloqueado, key="d2_q4"
        )

        # RETROALIMENTACIÓN CIENTÍFICA FORMATIVA INMEDIATA POST-ENVÍO
        if bloqueado and st.session_state.d2_retroalimentacion:
            st.markdown("#### 🔬 Resultados del Análisis Clínico")
            prec = st.session_state.d2_retroalimentacion["precision"]
            
            if prec == 100:
                st.success(f"🏆 **Certificación Exitosa:** Precisión del {prec}%. Entendimiento absoluto de la polaridad molecular.")
            elif prec >= 75:
                st.warning(f"⚠️ **Aprobación Regular:** Precisión del {prec}%. Revisa el cálculo matemático de electronegatividad.")
            else:
                st.error(f"❌ **Certificación Denegada:** Precisión del {prec}%. Se requiere tutoría en la escala de Pauling.")

            st.markdown(
                f"""
                <div class='lab-panel'>
                    <strong>Reporte Técnico Formativo:</strong><br>
                    • <strong>Pregunta 1:</strong> {'✅ Correcto. Las estructuras apolares difunden a través de las membranas lipídicas de la BHE.' if q1.startswith('B') else '❌ Incorrecto. Los compuestos iónicos o muy polares no cruzan pasivamente membranas lipídicas sin transportadores.'}<br>
                    • <strong>Pregunta 2:</strong> {'✅ Correcto. Se genera un dipolo permanente debido al sesgo electrónico hacia el oxígeno.' if q2.startswith('B') else '❌ Incorrecto. La gran afinidad del oxígeno distorsiona el orbital de forma asimétrica (polar).'}<br>
                    • <strong>Pregunta 3:</strong> {'✅ Correcto. La alta constante dieléctrica del agua disocia las uniones iónicas del NaCl en iones libres.' if q3.startswith('C') else '❌ Incorrecto. En solución acuosa, los enlaces iónicos se disocian por completo.'}<br>
                    • <strong>Pregunta 4:</strong> {'✅ Correcto. El cálculo matemático exacto es: 3.16 - 2.55 = 0.61.' if abs(q4 - 0.61) < 0.01 else '❌ Incorrecto. La sustracción aritmética directa arroja 0.61.'}
                </div>
                """, 
                unsafe_allow_html=True
            )

        # Botón de envío blindado contra condiciones de carrera
        if st.button(
            "🔒 Enviar Respuestas y Registrar Avance", 
            type="primary", 
            disabled=st.session_state.procesando or bloqueado, 
            use_container_width=True, 
            key="d2_submit"
        ):
            st.session_state.procesando = True
            
            # Registro de telemetría de salida del quiz
            db.registrar_evento_telemetria(st.session_state.get("token_actual", "DEMO"), 2, "intento_envio_quiz")
            
            # Evaluación de aciertos
            aciertos = sum([
                q1.startswith("B"),
                q2.startswith("B"),
                q3.startswith("C"),
                abs(q4 - 0.61) < 0.01
            ])
            precision = int((aciertos / 4) * 100)
            
            # Manejo vital de errores
            if precision < 50:
                st.session_state.vidas = max(0, st.session_state.vidas - 1)
                st.toast("Fallo grave en la precisión de enlaces. Pérdida de 1 vida clínica.", icon="❤️")
            
            puntos_ronda = aciertos * 15
            st.session_state.puntos_acumulados += puntos_ronda
            
            # Hidratación interna del estado de retroalimentación
            st.session_state.d2_retroalimentacion = {
                "precision": precision,
                "aciertos": aciertos
            }
            
            # Sincronización asíncrona hacia Supabase
            db.guardar_registro_juego(
                st.session_state.get("token_actual", "DEMO"),
                2,
                st.session_state.d2_juego_score + puntos_ronda,
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
            
            st.session_state.d2_quiz_enviado = True
            st.session_state.procesando = False
            st.rerun()
