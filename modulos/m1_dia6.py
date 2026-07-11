import streamlit as st
import random
import database as db

# Base de datos analítica con escenarios críticos de triage y fluidoterapia clínica
CASOS_TRIAGE = [
    {
        "id": "shock",
        "cuadro_vet": "Canino ingresado con deshidratación severa (10%) y signos inminentes de shock hipovolémico.",
        "cuadro_med": "Paciente humano politraumatizado ingresado a urgencias con shock hipovolémico por hemorragia masiva.",
        "cuadro_bio": "Muestra de tejido celular animal que ha perdido su matriz de agua extracelular de forma aguda.",
        "fluidos": ["Solución Salina Isotónica (NaCl 0.9%)", "Agua destilada estéril IV"],
        "correcta": "Solución Salina Isotónica (NaCl 0.9%)",
        "razon": "Permite expandir el volumen del compartimento intravascular de forma inmediata sin alterar la presión osmótica celular."
    },
    {
        "id": "edema",
        "cuadro_vet": "Felino politraumatizado que desarrolla edema cerebral severo secundario a traumatismo craneoencefálico.",
        "cuadro_med": "Paciente humano con traumatismo craneal cerrado que presenta signos agudos de hipertensión intracraneal.",
        "cuadro_bio": "Modelo biológico de edema celular tisular donde las células han absorbido un exceso patológico de solvente.",
        "fluidos": ["Solución Hipertónica (NaCl 7.5%)", "Solución Salina Hipotónica (NaCl 0.45%)"],
        "correcta": "Solución Hipertónica (NaCl 7.5%)",
        "razon": "Crea un gradiente osmótico transitorio que extrae el agua del parénquima hacia el espacio vascular, reduciendo la presión."
    }
]

def inicializar_estado_dia6():
    if "d6_juego_score" not in st.session_state:
        st.session_state.d6_juego_score = 0
    if "d6_quiz_enviado" not in st.session_state:
        st.session_state.d6_quiz_enviado = False
    if "d6_caso_actual" not in st.session_state:
        st.session_state.d6_caso_actual = random.choice(CASOS_TRIAGE)
    if "d6_retroalimentacion" not in st.session_state:
        st.session_state.d6_retroalimentacion = None

def app():
    inicializar_estado_dia6()
    token_alumno = st.session_state.get("token_actual", "DEMO")

    enfoque = st.radio(
        "🔬 Configurar el Analizador de Fluidos:", 
        ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], 
        horizontal=True,
        key="d6_enfoque_radio"
    )

    tab1, tab2, tab3 = st.tabs(["🔬 Consola de Fluidoterapia", "🎮 Triage Clínico", "📝 Certificación Unidad 1"])

    with tab1:
        st.markdown("### Fundamentos: Tonicidad, Ósmosis y Dinámica de Fluidos")
        st.markdown(
            """
            La fluidoterapia es la aplicación práctica de los principios de ósmosis y tracción de solutos. 
            La **tonicidad** mide la capacidad de una solución externa para mover agua hacia adentro o hacia afuera de una célula, 
            regulando directamente la morfología de los eritrocitos.
            """
        )
        
        st.markdown("---")
        st.markdown("#### 🔬 Simulador de Tonicidad de Fluidos Intravenosos")
        tonicidad = st.slider("Ajustar la Tonicidad del Fluido plasmático (0.5x a 1.5x):", min_value=0.5, max_value=1.5, value=1.0, step=0.1)

        if tonicidad < 0.9:
            est_vis, msg = "eritrocito-hipotonico", "🚨 ENTORNO HIPOTÓNICO: El agua entra a la célula. Riesgo crítico de Lisis Celular."
            detalle = "La osmolaridad del fluido plasmático es menor a la intracelular. El agua difunde hacia el interior, inflando el eritrocito."
        elif tonicidad <= 1.1:
            est_vis, msg = "eritrocito-isotonico", "🟢 ENTORNO ISOTÓNICO: Homeostasis y equilibrio osmótico perfecto."
            detalle = "El flujo neto de agua es cero. Los eritrocitos mantienen su morfología bicóncava óptima para el transporte gaseoso."
        else:
            est_vis, msg = "eritrocito-hypertonico", "🔵 ENTORNO HIPERTÓNICO: El agua sale de la célula. El eritrocito se crenó."
            detalle = "La alta concentración de solutos extracelulares deshidrata el citoplasma, encogiendo la membrana celular (crenación)."

        st.info(msg)
        st.caption(f"ℹ️ *Reporte morfológico celular:* {detalle}")
        st.markdown(f"<div class='plasma-sanguineo'><div class='{est_vis}'></div></div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("### 🎮 Simulador de Emergencias: Triage Clínico")
        c_score = st.columns(1)[0]
        c_score.metric("Puntaje Acumulado en Triage", f"{st.session_state.d6_juego_score} pts")
        
        caso = st.session_state.d6_caso_actual
        
        if enfoque == "🐾 Veterinaria": cuadro_texto = caso["cuadro_vet"]
        elif enfoque == "🩺 Medicina": cuadro_texto = caso["cuadro_med"]
        else: cuadro_texto = caso["cuadro_bio"]
            
        st.warning(f"📋 **Paciente en Triage:** {cuadro_texto}")
        st.info("Determina de forma inmediata el fluido de elección basándote en la osmolaridad requerida:")
        
        def verificar_triage(seleccion):
            if seleccion == caso["correcta"]:
                st.session_state.d6_juego_score += 25
                st.toast(f"¡Excelente Triage! {caso['razon']}", icon="✅")
                st.session_state.d6_caso_actual = random.choice(CASOS_TRIAGE)
            else:
                st.session_state.d6_juego_score = max(0, st.session_state.d6_juego_score - 15)
                st.toast("Fluido incorrecto. Choque osmótico provocado.", icon="❌")

        for opcion in caso["fluidos"]:
            if st.button(opcion, use_container_width=True, key=f"d6_btn_{opcion}"):
                verificar_triage(opcion)
                st.rerun()

    with tab3:
        st.markdown("### 📝 Cuestionario de Certificación Final de Unidad")
        bloqueado = st.session_state.d6_quiz_enviado

        q1 = st.radio("1. ¿Qué fenómeno físico-químico experimentará un eritrocito mamífero si es sumergido en una solución pura de agua destilada?", ["A) Mantendrá su volumen inalterado por falta de solutos externos.", "B) Se crenará inmediatamente debido a la salida masiva de agua por ósmosis.", "C) Se lisará (explotará) debido a la entrada masiva de agua por gradiente osmótico."], disabled=bloqueado, key="d6_q1")
        q2 = st.radio("2. ¿Por qué está estrictamente contraindicado administrar agua pura (sin electrólitos) por vía intravenosa a un paciente?", ["A) Porque induce una hemólisis intravascular masiva que puede causar daño renal severo y anoxia.", "B) Porque altera drásticamente el costo comercial del tratamiento veterinario.", "C) Porque actúa como un buffer demasiado potente que alcaliniza el plasma."], disabled=bloqueado, key="d6_q2")
        q3 = st.radio("3. ¿Cuál es el objetivo primario inmediato al instaurar un protocolo de fluidoterapia en un paciente con choque hemorrágico?", ["A) Modificar la coloración y viscosidad del tejido conectivo.", "B) Restaurar el volumen intravascular efectivo para asegurar la perfusión tisular y el transporte de oxígeno.", "C) Incrementar artificialmente los niveles plasmáticos de urea."], disabled=bloqueado, key="d6_q3")
        
        q4 = st.number_input("4. Escribe el valor promedio ideal de la osmolaridad plasmática fisiológica normal en mamíferos ($mOsm/L$):", value=290, min_value=0, step=1, disabled=bloqueado, key="d6_q4")

        if bloqueado and st.session_state.d6_retroalimentacion:
            prec = st.session_state.d6_retroalimentacion["precision"]
            if prec == 100: st.success(f"🏆 **Unidad 1 Finalizada exitosamente:** Rendimiento perfecto del {prec}%.")
            else: st.warning(f"⚠️ **Unidad Concluida con observaciones:** Precisión del {prec}%.")
            st.markdown(f"<div class='lab-panel'><strong>Reporte Clínico de Fluidoterapia:</strong><br>• Pregunta 1: {'✅ Correcto.' if q1.startswith('C') else '❌ Incorrecto.'}<br>• Pregunta 2: {'✅ Correcto.' if q2.startswith('A') else '❌ Incorrecto.'}<br>• Pregunta 3: {'✅ Correcto.' if q3.startswith('B') else '❌ Incorrecto.'}<br>• Pregunta 4: {'✅ Correcto. Rango normal entre 280 y 300 mOsm/L.' if 280 <= q4 <= 300 else '❌ Incorrecto. La osmolaridad normal oscila entre 280 y 300 mOsm/L.'}</div>", unsafe_allow_html=True)

        if st.button("🔒 Concluir y Sellar Unidad 1", type="primary", disabled=bloqueado, use_container_width=True, key="d6_submit"):
            aciertos = sum([q1.startswith("C"), q2.startswith("A"), q3.startswith("B"), 280 <= q4 <= 300])
            precision = int((aciertos / 4) * 100)
            
            if precision < 50:
                st.session_state.vidas = max(0, st.session_state.vidas - 1)
                st.toast("Rendimiento crítico en fluidoterapia.", icon="❤️")
            
            puntos_ganados = aciertos * 15
            st.session_state.puntos_acumulados += puntos_ganados
            st.session_state.d6_retroalimentacion = {"precision": precision, "aciertos": aciertos}
            
            db.guardar_registro_juego(token_alumno, 6, st.session_state.d6_juego_score + puntos_ganados, precision, {"enfoque": enfoque})
            db.sincronizar_progreso_db(token_alumno, st.session_state.puntos_acumulados, "1", st.session_state.vidas, st.session_state.tiempo_estudio_min)
            st.session_state.d6_quiz_enviado = True
            st.rerun()
