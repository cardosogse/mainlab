import streamlit as st
import random
import database as db

# Base de datos analítica con escenarios de desequilibrio ácido-base y amortiguación
CASOS_CLINICOS_pH = [
    {
        "id": "cetoacidosis",
        "cuadro_vet": "Paciente canino con cetoacidosis diabética severa (acumulación crítica de cuerpos cetónicos y protones $H^+$).",
        "cuadro_med": "Paciente humano con cetoacidosis diabética en terapia intensiva (acumulación de acetoacetato y protones $H^+$).",
        "cuadro_bio": "Sistema de cultivo celular expuesto a una carga metabólica ácida extrema por acumulación de protones $H^+$.",
        "accion_correcta": "El Bicarbonato ($HCO_3^-$) plasmático capta los protones libres para formar ácido carbónico ($H_2CO_3$).", 
        "accion_incorrecta": "El ácido carbónico plasmático se disocia liberando una mayor cantidad de protones libres al medio.",
        "fundamento": "Ante una carga de ácidos, el amortiguador bicarbonato actúa como base conjugada, atrapando protones libres para mitigar la caída del pH."
    },
    {
        "id": "vomito",
        "cuadro_vet": "Felino con obstrucción pilórica y vómitos crónicos profusos (pérdida masiva de jugos gástricos ricos en $HCl$).",
        "cuadro_med": "Paciente humano con estenosis pilórica y emesis severa (pérdida masiva de ácido clorhídrico estomacal).",
        "cuadro_bio": "Medio biológico experimental donde se han removido artificialmente los hidrogeniones libres del entorno.",
        "accion_correcta": "El sistema amortiguador libera protones libres ($H^+$) a partir de la disociación del ácido carbónico ($H_2CO_3$).", 
        "accion_incorrecta": "El centro respiratorio induce de manera inmediata una hiperventilación compensatoria masiva.",
        "fundamento": "La pérdida de hidrogeniones eleva el pH (alcalosis). El organismo compensa disociando el ácido débil del buffer para restaurar los protones faltantes."
    }
]

def inicializar_estado_dia5():
    if "d5_juego_score" not in st.session_state:
        st.session_state.d5_juego_score = 0
    if "d5_juego_intentos" not in st.session_state:
        st.session_state.d5_juego_intentos = 0
    if "d5_quiz_enviado" not in st.session_state:
        st.session_state.d5_quiz_enviado = False
    if "d5_caso_actual" not in st.session_state:
        st.session_state.d5_caso_actual = random.choice(CASOS_CLINICOS_pH)
        caso = st.session_state.d5_caso_actual
        opciones = [
            {"texto": caso["accion_correcta"], "es_correcta": True},
            {"texto": caso["accion_incorrecta"], "es_correcta": False}
        ]
        random.shuffle(opciones)
        st.session_state.d5_opciones_fijadas = opciones
    if "d5_retroalimentacion" not in st.session_state:
        st.session_state.d5_retroalimentacion = None

def app():
    inicializar_estado_dia5()
    token_alumno = st.session_state.get("token_actual", "DEMO")
    enfoque = st.radio(
        "🔬 Ajustar la Sensibilidad del Transductor:", 
        ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], 
        horizontal=True,
        key="d5_enfoque_radio"
    )
    
    tab1, tab2, tab3 = st.tabs(["🔬 Curva de Titulación", "⚖️ Triage Ácido-Base", "📝 Cuestionario de Certificación"])

    with tab1:
        st.markdown("### Fundamentos: La Autoionización del Agua y el Origen del pH")
        st.markdown(
            """
            Para comprender el pH, primero debemos entender que el agua pura no es una masa inerte; es un electrolito débil que sufre 
            **autoionización espontánea** donde una molécula cede un protón a otra:
            """
        )
        st.latex(r"H_2O + H_2O \rightleftharpoons H_3O^+ + OH^-")
        st.markdown(
            """
            A $25^\circ\text{C}$, el producto iónico del agua ($K_w$) es una constante inmutable equivalente a $1 \times 10^{-14}$. 
            Dado que en agua pura la concentración de $[H^+]$ es exactamente $1 \times 10^{-7}\text{ mol/L}$, el bioquímico Søren Sørensen introdujo 
            la escala logarítmica para evitar el manejo de decimales incómodos: $pH = -\log[H^+]$. Una variación de **1 sola unidad de pH** 
            representa un cambio multiplicativo de **10 veces** en la acidez real.
            """
        )
        
        st.markdown("---")
        st.markdown("#### 🔬 Simulador de Estrés Químico Plasmático (Henderson-Hasselbalch)")
        st.latex(r"pH = pKa + \log\left(\frac{[A^-]}{[HA]}\right)")
        
        estres = st.slider("Inyectar Equivalentes Ácidos (-) o Básicos (+) en la muestra:", min_value=-15, max_value=15, value=0)
        
        ph_base = 7.40
        if -5 <= estres <= 5:
            ph_act = ph_base + (estres * 0.02)
            est, col = "🟢 Homeostasis Fisiológica Estable", "green"
            detalle = "El sistema amortiguador absorbe eficientemente las variaciones. La relación bicarbonato/ácido carbónico se mantiene próxima a 20:1."
        elif estres < -5:
            ph_act = (ph_base - 0.1) - (abs(estres) - 5) * 0.14
            est, col = "🔴 Acidosis Descompensada", "red"
            detalle = "Los amortiguadores biológicos extracelulares se han saturado por completo. Riesgo inminente de desnaturalización enzimática."
        else:
            ph_act = (ph_base + 0.1) + (estres - 5) * 0.14
            est, col = "🔵 Alcalosis Descompensada", "blue"
            detalle = "Exceso de bases conjugadas o pérdida severa de hidrogeniones libres. Altera gravemente la excitabilidad neuromuscular."

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
        if enfoque == "🐾 Veterinaria": cuadro_texto = caso["cuadro_vet"]
        elif enfoque == "🩺 Medicina": cuadro_texto = caso["cuadro_med"]
        else: cuadro_texto = caso["cuadro_bio"]
            
        st.error(f"🚨 **Alerta de Emergencia:** {cuadro_texto}")
        st.info("Elige la respuesta compensatoria exacta a nivel de amortiguación molecular:")

        def verificar_compensacion(es_correcta):
            st.session_state.d5_juego_intentos += 1
            if es_correcta:
                st.session_state.d5_juego_score += 20
                st.toast(f"¡Estabilizado! {caso['fundamento']}", icon="✅")
            else:
                st.session_state.d5_juego_score = max(0, st.session_state.d5_juego_score - 10)
                st.toast("Fallo en la compensación. Agravamiento crítico del cuadro.", icon="❌")
            
            st.session_state.d5_caso_actual = random.choice(CASOS_CLINICOS_pH)
            nuevo_caso = st.session_state.d5_caso_actual
            nuevas_opciones = [
                {"texto": nuevo_caso["accion_correcta"], "es_correcta": True},
                {"texto": nuevo_caso["accion_incorrecta"], "es_correcta": False}
            ]
            random.shuffle(nuevas_opciones)
            st.session_state.d5_opciones_fijadas = nuevas_opciones

        col1, col2 = st.columns(2)
        opc1 = st.session_state.d5_opciones_fijadas[0]
        opc2 = st.session_state.d5_opciones_fijadas[1]
        
        if col1.button(opc1["texto"], use_container_width=True, key="d5_btn_opt1"): 
            verificar_compensacion(opc1["es_correcta"])
            st.rerun()
        if col2.button(opc2["texto"], use_container_width=True, key="d5_btn_opt2"): 
            verificar_compensacion(opc2["es_correcta"])
            st.rerun()

    with tab3:
        st.markdown("### 📝 Cuestionario de Certificación del Día 5")
        bloqueado = st.session_state.d5_quiz_enviado

        q1 = st.radio("1. Si el pH sanguíneo de un paciente crítico transita de 7.4 a 6.4, ¿qué variación real ocurrió en la concentración de protones ($H^+$)?", ["A) La acidez real del plasma aumentó exactamente el doble.", "B) La concentración de protones disminuyó significativamente debido a la naturaleza negativa del logaritmo.", "C) La concentración de protones libres se incrementó diez veces (x10) debido a la naturaleza logarítmica base 10 de la escala."], disabled=bloqueado, key="d5_q1")
        q2 = st.radio("2. ¿Cuál es el sistema amortiguador fundamental encargado de contener las variaciones de pH frente a ácidos fijos de origen metabólico en el espacio extracelular?", ["A) El sistema tamponador Bicarbonato / Ácido Carbónico ($HCO_3^- / H_2CO_3$).", "B) El sistema intracelular del Fosfato dibásico / monobásico.", "C) El amortiguador lipídico hidrofóbico de membrana."], disabled=bloqueado, key="d5_q2")
        q3 = st.radio("3. De acuerdo con los principios de la ecuación de Henderson-Hasselbalch, ¿cuándo alcanza un sistema amortiguador su máxima capacidad de mitigación química?", ["A) Cuando el solvente acuoso se disocia y se evapora por completo de la solución.", "B) Cuando el pH del medio es exactamente equivalente al valor de su constante de disociación ($pKa$).", "C) Cuando la base conjugada supera a la especie ácida en una relación estricta de 50:1."], disabled=bloqueado, key="d5_q3")
        
        etiqueta_q4 = "4. Escribe el límite inferior exacto del pH fisiológico de la sangre arterial en mamíferos domésticos antes de declararse Acidemia clínica:" if enfoque == "🐾 Veterinaria" else "4. Escribe el límite inferior exacto del pH fisiológico normal de la sangre arterial humana en condiciones estándar:"
        q4 = st.number_input(etiqueta_q4, value=7.00, step=0.01, format="%.2f", disabled=bloqueado, key="d5_q4")

        if bloqueado and st.session_state.d5_retroalimentacion:
            prec = st.session_state.d5_retroalimentacion["precision"]
            if prec == 100: st.success(f"🏆 **Certificación Completada:** Precisión del {prec}%. Control clínico absoluto sobre balances ácido-base.")
            else: st.error(f"❌ **Certificación Denegada:** Precisión del {prec}%. Revisa los fundamentos logarítmicos.")
            st.markdown(f"<div class='lab-panel'><strong>Reporte Técnico del Sistema Buffer:</strong><br>• Pregunta 1: {'✅ Correcto.' if q1.startswith('C') else '❌ Incorrecto.'}<br>• Pregunta 2: {'✅ Correcto.' if q2.startswith('A') else '❌ Incorrecto.'}<br>• Pregunta 3: {'✅ Correcto.' if q3.startswith('B') else '❌ Incorrecto.'}<br>• Pregunta 4: {'✅ Correcto. El límite exacto inferior es 7.35.' if abs(q4 - 7.35) < 0.01 else '❌ Incorrecto. El límite homeostático inferior estricto es de 7.35.'}</div>", unsafe_allow_html=True)

        if st.button("🔒 Sellar Evaluación Ácido-Base", type="primary", disabled=bloqueado, use_container_width=True, key="d5_submit"):
            aciertos = sum([q1.startswith("C"), q2.startswith("A"), q3.startswith("B"), abs(q4 - 7.35) < 0.01])
            precision = int((aciertos / 4) * 100)
            
            if precision < 50:
                st.session_state.vidas = max(0, st.session_state.vidas - 1)
                st.toast("Fallo crítico en balance ácido-base. Pérdida de 1 vida.", icon="❤️")
            
            puntos_ganados = aciertos * 15
            st.session_state.puntos_acumulados += puntos_ganados
            st.session_state.d5_retroalimentacion = {"precision": precision, "aciertos": aciertos}
            
            db.guardar_registro_juego(token_alumno, 5, st.session_state.d5_juego_score + puntos_ganados, precision, {"enfoque": enfoque})
            db.sincronizar_progreso_db(token_alumno, st.session_state.puntos_acumulados, "1", st.session_state.vidas, st.session_state.tiempo_estudio_min)
            st.session_state.d5_quiz_enviado = True
            st.rerun()
