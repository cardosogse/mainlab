import streamlit as st
import random
import database as db

# Base de datos analítica con escenarios de desequilibrio ácido-base y amortiguación
CASOS_CLINICOS_pH = [
    {
        "cuadro": "Paciente canino con cetoacidosis diabética severa (acumulación crítica de protones $H^+$).", 
        "accion_correcta": "El Bicarbonato ($HCO_3^-$) plasmático capta los protones libres para formar ácido carbónico ($H_2CO_3$).", 
        "accion_incorrecta": "El ácido carbónico plasmático se disocia liberando una mayor cantidad de protones libres.",
        "fundamento": "Ante una carga de ácidos metabólicos, el amortiguador bicarbonato actúa como base conjugada, atrapando los protones libres para mitigar la caída del pH."
    },
    {
        "cuadro": "Feline con obstrucción pilórica y vómitos crónicos profusos (pérdida masiva de jugos gástricos ricos en $HCl$).", 
        "accion_correcta": "El sistema amortiguador amortigua liberando protones libres ($H^+$) a partir del ácido carbónico.", 
        "accion_incorrecta": "El centro respiratorio induce una hiperventilación compensatoria severa inmediata.",
        "fundamento": "La pérdida de hidrogeniones gástricos eleva el pH (alcalosis). El organismo compensa disociando el ácido débil del buffer para restaurar los protones faltantes."
    },
    {
        "cuadro": "Equino con asfixia mecánica temporal u obstrucción de vías aéreas altas, acumulando $CO_2$.", 
        "accion_correcta": "El exceso de $CO_2$ hidrata en eritrocitos y se desplaza hacia la producción de protones y bicarbonato.", 
        "accion_incorrecta": "El $CO_2$ disuelto reacciona directamente con los iones hidroxilo ($OH^-$) neutralizándolos.",
        "fundamento": "La retención de anhídrido carbónico desplaza el equilibrio químico hacia la derecha (ley de acción de masas), incrementando la concentración de $H^+$ (acidosis respiratoria)."
    }
]

def inicializar_estado_dia5():
    """Establece de forma aislada y segura el almacenamiento de variables de control del Día 5."""
    if "d5_juego_score" not in st.session_state:
        st.session_state.d5_juego_score = 0
    if "d5_juego_intentos" not in st.session_state:
        st.session_state.d5_juego_intentos = 0
    if "d5_quiz_enviado" not in st.session_state:
        st.session_state.d5_quiz_enviado = False
    if "d5_caso_actual" not in st.session_state:
        st.session_state.d5_caso_actual = random.choice(CASOS_CLINICOS_pH)
    if "d5_retroalimentacion" not in st.session_state:
        st.session_state.d5_retroalimentacion = None

def app():
    inicializar_estado_dia5()
    
    # Telemetría instruccional de ingreso a la lección
    if "d5_telemetria_iniciada" not in st.session_state:
        db.registrar_evento_telemetria(st.session_state.get("token_actual", "DEMO"), 5, "ingreso_pestana_teoria")
        st.session_state.d5_telemetria_iniciada = True
        
    enfoque = st.radio(
        "🔬 Ajustar la sensibilidad del transductor:", 
        ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], 
        horizontal=True, 
        key="d5_enfoque",
        disabled=st.session_state.procesando
    )
    
    # SEGMENTACIÓN EN PESTAÑAS (Ergonomía UI y Mitigación de Scroll)
    tab1, tab2, tab3 = st.tabs(["🔬 Curva de Titulación", "⚖️ Triage Ácido-Base", "📝 Cuestionario de Certificación"])

    with tab1:
        st.markdown("### Fundamentos: Homeostasis del pH y Sistemas Amortiguadores")
        st.markdown(
            """
            El pH de los líquidos corporales es una de las variables biológicas más celosamente reguladas. 
            Pequeñas variaciones alteran la estructura tridimensional de las proteínas y detienen los sistemas enzimáticos. 
            La ecuación de Henderson-Hasselbalch rige el comportamiento de estos sistemas químicos:
            """
        )
        
        st.latex(r"pH = pKa + \log\left(\frac{[A^-]}{[HA]}\right)")
        
        st.markdown("---")
        st.markdown("#### 🔬 Simulador de Estrés Químico Plasmático")
        estres = st.slider(
            "Inyectar Equivalentes Ácidos (-) o Básicos (+) en el sistema:", 
            min_value=-15, max_value=15, value=0, disabled=st.session_state.procesando
        )
        
        ph_base = 7.40
        # Simulación logarítmica suavizada por el efecto buffer
        if -5 <= estres <= 5:
            ph_act = ph_base + (estres * 0.02)
            est, col = "🟢 Homeostasis Fisiológica Estable", "green"
            detalle = "El sistema amortiguador absorbe las variaciones. La relación bicarbonato/ácido carbónico se mantiene próxima a 20:1."
        elif estres < -5:
            ph_act = (ph_base - 0.1) - (abs(estres) - 5) * 0.14
            est, col = "🔴 Acidosis Metabólica Descompensada", "red"
            detalle = "Los amortiguadores biológicos se han saturado. Riesgo inminente de disfunción enzimática sistémica."
        else:
            ph_act = (ph_base + 0.1) + (estres - 5) * 0.14
            est, col = "🔵 Alcalosis Metabólica Descompensada", "blue"
            detalle = "Exceso de bases conjugadas o pérdida severa de hidrogeniones. Alteración de la excitabilidad neuromuscular."

        st.metric("pH Sanguíneo Medido", f"{ph_act:.2f}")
        st.markdown(f"**Estado Clínico:** <span style='color:{col}; font-weight:bold;'>{est}</span>", unsafe_allow_html=True)
        st.caption(f"ℹ️ *Reporte del amortiguador:* {detalle}")
        st.progress(max(0.0, min(1.0, (ph_act - 6.0) / 2.5)))

    with tab2:
        st.markdown("### 🎮 Triage Rápido: Balanza de Protones")
        
        c_score, c_intentos = st.columns(2)
        c_score.metric("Puntaje Acumulado", f"{st.session_state.d5_juego_score} pts")
        c_intentos.metric("Casos Estabilizados", st.session_state.d5_juego_intentos)
        
        caso = st.session_state.d5_caso_actual
        st.error(f"🚨 **Cuadro Clínico Urgente:** {caso['cuadro']}")
        st.info("Elige la respuesta compensatoria exacta a nivel químico que ejecutará el organismo:")

        def verificar_compensacion(es_correcta):
            st.session_state.d5_juego_intentos += 1
            if es_correcta:
                st.session_state.d5_juego_score += 20
                st.toast(f"¡Estabilizado! {caso['fundamento']}", icon="✅")
                st.session_state.d5_caso_actual = random.choice(CASOS_CLINICOS_pH)
            else:
                st.session_state.d5_juego_score = max(0, st.session_state.d5_juego_score - 10)
                st.toast("Fallo en la compensación. Agravamiento del cuadro clínico.", icon="❌")

        col1, col2 = st.columns(2)
        if col1.button(caso["accion_correcta"], use_container_width=True, disabled=st.session_state.procesando, key="d5_btn_c1"): 
            verificar_compensacion(True)
            st.rerun()
        if col2.button(caso["accion_incorrecta"], use_container_width=True, disabled=st.session_state.procesando, key="d5_btn_c2"): 
            verificar_compensacion(False)
            st.rerun()

    with tab3:
        st.markdown("### 📝 Cuestionario de Certificación del Día 5")
        bloqueado = st.session_state.d5_quiz_enviado

        q1 = st.radio(
            "1. Si el pH sanguíneo de un paciente crítico transita de 7.4 a 6.4, ¿qué variación real ocurrió en la concentración de protones ($H^+$)?",
            ["A) La acidez aumentó exactamente el doble.", 
             "B) La concentración de protones disminuyó significativamente debido al logaritmo negativo.", 
             "C) La concentración de protones libres se incrementó diez veces (x10) debido a la escala logarítmica base 10."],
            disabled=bloqueado, key="d5_q1"
        )
        
        q2 = st.radio(
            "2. ¿Cuál es el sistema amortiguador fundamental encargado de contener las variaciones de pH frente a ácidos fijos de origen metabólico en el espacio extracelular?",
            ["A) El sistema tamponador Bicarbonato ($HCO_3^- / H_2CO_3$).", 
             "B) El sistema intracelular del Fosfato dibásico.", 
             "C) El amortiguador lipídico de membrana."],
            disabled=bloqueado, key="d5_q2"
        )
        
        q3 = st.radio(
            "3. De acuerdo con principios moleculares, ¿cuándo alcanza un sistema amortiguador acoplado su máxima capacidad de amortiguación química?",
            ["A) Cuando el solvente acuoso se satura y se evapora de la solución.", 
             "B) Cuando el pH del medio es exactamente equivalente al valor de su constante de disociación ($pKa$).", 
             "C) Cuando la base conjugada supera a la especie ácida en una relación de 50:1."],
            disabled=bloqueado, key="d5_q3"
        )
        
        q4 = st.number_input(
            "4. Escribe el límite inferior exacto del pH fisiológico normal de la sangre arterial en mamíferos domésticos (homeostasis estándar):",
            value=7.00, step=0.01, format="%.2f", disabled=bloqueado, key="d5_q4"
        )

        # ENGINE DE RETROALIMENTACIÓN FORMATIVA INMEDIATA POST-ENVÍO
        if bloqueado and st.session_state.d5_retroalimentacion:
            st.markdown("#### 🔬 Dictamen Metrológico y Diagnóstico")
            prec = st.session_state.d5_retroalimentacion["precision"]
            
            if prec == 100:
                st.success(f"🏆 **Certificación Completada:** Precisión del {prec}%. Control clínico absoluto sobre equilibrios ácido-base.")
            elif prec >= 75:
                st.warning(f"⚠️ **Aprobación Concedida:** Precisión del {prec}%. Repasa los rangos homeostáticos precisos de los mamíferos.")
            else:
                st.error(f"❌ **Certificación Denegada:** Precisión del {prec}%. Es crucial comprender la naturaleza matemática del pH.")

            st.markdown(
                f"""
                <div class='lab-panel'>
                    <strong>Reporte Técnico del Sistema Buffer:</strong><br>
                    • <strong>Pregunta 1:</strong> {'✅ Correcto. Al ser una escala logarítmica negativa de base 10, la reducción de una unidad decimal representa un aumento multiplicativo de 10 veces la concentración de $H^+$.' if q1.startswith('C') else '❌ Incorrecto. El pH es una función logarítmica; cambios de una unidad entera significan un cambio de diez veces la concentración real.'}<br>
                    • <strong>Pregunta 2:</strong> {'✅ Correcto. El par bicarbonato/ácido carbónico es el amortiguador principal del líquido extracelular debido a su acoplamiento con la eliminación pulmonar y renal.' if q2.startswith('A') else '❌ Incorrecto. El bicarbonato es el amortiguador primario extracelular; el fosfato predomina en el citoplasma.'}<br>
                    • <strong>Pregunta 3:</strong> {'✅ Correcto. En el punto donde pH = pKa, la concentración del ácido débil es idéntica a la de su base conjugada, optimizando la neutralización en ambos sentidos.' if q3.startswith('B') else '❌ Incorrecto. La máxima capacidad del buffer ocurre cuando las concentraciones de ácido y base conjugada son iguales ($pH = pKa$).'}<br>
                    • <strong>Pregunta 4:</strong> {'✅ Correcto. El rango estándar para mamíferos es de 7.35 a 7.45, estableciendo el límite inferior homeostático en 7.35.' if abs(q4 - 7.35) < 0.01 else '❌ Incorrecto. El límite exacto inferior de la normalidad fisiológica sistémica es 7.35.'}
                </div>
                """, 
                unsafe_allow_html=True
            )

        # Botón de envío blindado contra condiciones de carrera
        if st.button(
            "🔒 Sellar Evaluación Ácido-Base", 
            type="primary", 
            disabled=st.session_state.procesando or bloqueado, 
            use_container_width=True, 
            key="d5_submit"
        ):
            st.session_state.procesando = True
            
            # Registrar marca de tiempo exacta de salida de la evaluación en Supabase
            db.registrar_evento_telemetria(st.session_state.get("token_actual", "DEMO"), 5, "intento_envio_quiz")
            
            # Evaluación precisa
            aciertos = sum([
                q1.startswith("C"),
                q2.startswith("A"),
                q3.startswith("B"),
                abs(q4 - 7.35) < 0.01
            ])
            precision = int((aciertos / 4) * 100)
            
            # Penalización sistémica de vitalidad
            if precision < 50:
                st.session_state.vidas = max(0, st.session_state.vidas - 1)
                st.toast("Fallo crítico en balance ácido-base. Pérdida de 1 vida clínica.", icon="❤️")
            
            puntos_ganados = aciertos * 15
            st.session_state.puntos_acumulados += puntos_ganados
            
            st.session_state.d5_retroalimentacion = {
                "precision": precision,
                "aciertos": aciertos
            }
            
            # Sincronización atómica hacia Supabase
            db.guardar_registro_juego(
                st.session_state.get("token_actual", "DEMO"),
                5,
                st.session_state.d5_juego_score + puntos_ganados,
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
            
            st.session_state.d5_quiz_enviado = True
            st.session_state.procesando = False
            st.rerun()
