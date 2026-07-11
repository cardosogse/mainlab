import streamlit as st
import random
import database as db

# Base de datos analítica con escenarios críticos de triage y fluidoterapia clínica
CASOS_TRIAGE = [
    {
        "paciente": "Canino de 4 años ingresado con deshidratación severa (10%) y signos inminentes de shock hipovolémico.", 
        "fluidos": ["Solución Salina Isotónica (NaCl 0.9%)", "Agua destilada estéril IV"], 
        "correcta": "Solución Salina Isotónica (NaCl 0.9%)", 
        "razon": "Permite expandir y restaurar el volumen del compartimento intravascular de forma inmediata sin alterar la presión osmótica de los eritrocitos, evitando lisis masiva."
    },
    {
        "paciente": "Felino politraumatizado que desarrolla edema cerebral severo secundario a traumatismo craneoencefálico.", 
        "fluidos": ["Solución Hipertónica (NaCl 7.5%)", "Solución Salina Hipotónica (NaCl 0.45%)"], 
        "correcta": "Solución Hipertónica (NaCl 7.5%)", 
        "razon": "Crea un gradiente osmótico transitorio que extrae el exceso de agua desde el parénquima cerebral hacia el espacio intravascular, disminuyendo la presión intracraneal."
    },
    {
        "paciente": "Bovino neonato con un cuadro de hipernatremia severa (intoxicación por sal y privación de agua).", 
        "fluidos": ["Solución Hipotónica (Dextrosa 5% en agua)", "Solución Salina al 0.9%"], 
        "correcta": "Solución Hipotónica (Dextrosa 5% en agua)", 
        "razon": "Aporta agua libre al metabolizarse la dextrosa, diluyendo gradualmente el Sodio plasmático sin provocar un edema cerebral por cambios osmóticos abruptos."
    }
]

def inicializar_estado_dia6():
    """Garantiza el aislamiento y persistencia de las variables de control para el Día 6."""
    if "d6_juego_score" not in st.session_state:
        st.session_state.d6_juego_score = 0
    if "d6_juego_intentos" not in st.session_state:
        st.session_state.d6_juego_intentos = 0
    if "d6_quiz_enviado" not in st.session_state:
        st.session_state.d6_quiz_enviado = False
    if "d6_caso_actual" not in st.session_state:
        st.session_state.d6_caso_actual = random.choice(CASOS_TRIAGE)
    if "d6_retroalimentacion" not in st.session_state:
        st.session_state.d6_retroalimentacion = None

def app():
    inicializar_estado_dia6()
    
    # Telemetría automatizada de inicio de sesión instruccional del Día 6
    if "d6_telemetria_iniciada" not in st.session_state:
        db.registrar_evento_telemetria(st.session_state.get("token_actual", "DEMO"), 6, "ingreso_pestana_teoria")
        st.session_state.d6_telemetria_iniciada = True
        
    enfoque = st.radio(
        "🔬 Modificar el espectro del analizador:", 
        ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], 
        horizontal=True, 
        key="d6_enfoque",
        disabled=st.session_state.procesando
    )
    
    # COMPONENTES DE INTERFAZ: Fragmentación en pestañas para mitigar fatiga visual
    tab1, tab2, tab3 = st.tabs(["🔬 Consola de Fluidoterapia", "🎮 Triage Clínico", "📝 Certificación Unidad 1"])

    with tab1:
        st.markdown("### Fundamentos: Tonicidad, Ósmosis y Dinámica de Fluidos")
        st.markdown(
            """
            La fluidoterapia es la aplicación práctica de los principios de ósmosis y tonicidad. 
            La **tonicidad** mide la capacidad de una solución externa para mover agua hacia adentro o 
            hacia afuera de una célula mediante ósmosis, regulando directamente el volumen celular de los eritrocitos.
            """
        )
        
        st.markdown("---")
        st.markdown("#### 🔬 Simulador de Tonicidad de Fluidos Intravenosos")
        tonicidad = st.slider(
            "Ajustar la Tonicidad del Fluido plasmático (0.5x a 1.5x):", 
            min_value=0.5, max_value=1.5, value=1.0, step=0.1, disabled=st.session_state.procesando
        )

        # Enrutamiento y asignación dinámica de clases CSS inyectadas en assets.py
        if tonicidad < 0.9:
            est_vis, msg = "eritrocito-hipotonico", "🚨 ¡ENTORNO HIPOTÓNICO! El agua entra a la célula. Riesgo crítico de Lisis Celular."
            detalle = "La osmolaridad del fluido plasmático es menor a la intracelular. El agua difunde hacia el interior, inflando el eritrocito."
        elif tonicidad <= 1.1:
            est_vis, msg = "eritrocito-isotonico", "🟢 ENTORNO ISOTÓNICO. Homeostasis y equilibrio osmótico perfecto."
            detalle = "El flujo neto de agua es cero. Los eritrocitos mantienen su morfología bicóncava óptima para el transporte de oxígeno."
        else:
            est_vis, msg = "eritrocito-hipertonico", "🔵 ¡ENTORNO HIPERTÓNICO! El agua sale de la célula. El eritrocito se crenó."
            detalle = "La alta concentración de solutos extracelulares deshidrata el citoplasma, encogiendo la membrana en forma de crenación."

        st.info(msg)
        st.caption(f"ℹ️ *Reporte morfológico celular:* {detalle}")
        st.markdown(f"<div class='plasma-sanguineo'><div class='{est_vis}'></div></div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("### 🎮 Simulador de Emergencias: Triage Clínico")
        
        c_score, c_intentos = st.columns(2)
        c_score.metric("Puntaje Acumulado", f"{st.session_state.d6_juego_score} pts")
        c_intentos.metric("Casos Resueltos", st.session_state.d6_juego_intentos)
        
        caso = st.session_state.d6_caso_actual
        st.warning(f"📋 **Paciente en Triage:** {caso['paciente']}")
        st.info("Determina de forma inmediata el fluido de elección basándote en la osmolaridad requerida:")
        
        def verificar_triage(seleccion):
            st.session_state.d6_juego_intentos += 1
            if seleccion == caso["correcta"]:
                st.session_state.d6_juego_score += 25
                st.toast(f"¡Excelente Triage! {caso['razon']}", icon="✅")
                st.session_state.d6_caso_actual = random.choice(CASOS_TRIAGE)
            else:
                st.session_state.d6_juego_score = max(0, st.session_state.d6_juego_score - 15)
                st.toast("Fluido incorrecto. Choque osmótico provocado.", icon="❌")

        # Botonera interactiva blindada contra clicks dobles
        for opcion in caso["fluidos"]:
            if st.button(opcion, use_container_width=True, key=f"d6_btn_{opcion}", disabled=st.session_state.procesando):
                verificar_triage(opcion)
                st.rerun()

    with tab3:
        st.markdown("### 📝 Cuestionario de Certificación Final de Unidad")
        bloqueado = st.session_state.d6_quiz_enviado

        q1 = st.radio(
            "1. ¿Qué fenómeno físico-químico experimentará un eritrocito mamífero si es sumergido en una solución pura de agua destilada?",
            ["A) Mantendrá su volumen inalterado por falta de solutos.", 
             "B) Se crenará inmediatamente debido a la salida masiva de agua.", 
             "C) Se lisará (explotará) debido a la entrada masiva de agua por gradiente osmótico."],
            disabled=bloqueado, key="d6_q1"
        )
        
        q2 = st.radio(
            "2. ¿Por qué está estrictamente contraindicado administrar agua pura (sin electrólitos) por vía intravenosa a un paciente deshidratado?",
            ["A) Porque induce una hemólisis intravascular masiva que puede causar daño renal severo y la muerte del animal.", 
             "B) Porque eleva drásticamente el costo comercial del tratamiento.", 
             "C) Porque actúa como un buffer demasiado potente que alcaliniza el plasma."],
            disabled=bloqueado, key="d6_q2"
        )
        
        q3 = st.radio(
            "3. ¿Cuál es el objetivo primario inmediato al instaurar un protocolo de fluidoterapia en un paciente con choque hemorrágico?",
            ["A) Modificar la coloración del tejido conectivo.", 
             "B) Restaurar el volumen intravascular efectivo para asegurar la perfusión tisular y el transporte de oxígeno.", 
             "C) Incrementar artificialmente los niveles plasmáticos de urea."],
            disabled=bloqueado, key="d6_q3"
        )
        
        q4 = st.number_input(
            "4. Escribe el valor promedio aproximado de la osmolaridad plasmática fisiológica normal en mamíferos domésticos ($mOsm/L$):",
            value=290, min_value=0, step=1, disabled=bloqueado, key="d6_q4"
        )

        # RETROALIMENTACIÓN CIENTÍFICA FORMATIVA INMEDIATA POST-ENVÍO
        if bloqueado and st.session_state.d6_retroalimentacion:
            st.markdown("#### 🔬 Dictamen y Cierre Académico de la Unidad 1")
            prec = st.session_state.d6_retroalimentacion["precision"]
            
            if prec == 100:
                st.success(f"🏆 **Felicidades, Investigador:** Certificación Completa con {prec}%. Has dominado los fundamentos moleculares y clínicos.")
            elif prec >= 75:
                st.warning(f"⚠️ **Aprobado:** Precisión del {prec}%. Repasa los rangos exactos de osmolaridad biológica.")
            else:
                st.error(f"❌ **Certificación Denegada:** Precisión del {prec}%. Es obligatorio repasar la dinámica celular de la ósmosis.")

            st.markdown(
                f"""
                <div class='lab-panel'>
                    <strong>Reporte Clínico Formativo de Fluidoterapia:</strong><br>
                    • <strong>Pregunta 1:</strong> {'✅ Correcto. El agua destilada es una solución intensamente hipotónica; el agua difunde al interior celular hasta romper la membrana.' if q1.startswith('C') else '❌ Incorrecto. Al no tener solutos externos, el agua destilada fuerza la entrada de líquido al eritrocito provocando lisis.'}<br>
                    • <strong>Pregunta 2:</strong> {'✅ Correcto. Al carecer de solutos, destruye instantáneamente los eritrocitos al entrar en contacto con el torrente sanguíneo.' if q2.startswith('A') else '❌ Incorrecto. La inyección de agua pura genera lisis de eritrocitos masiva por choque osmótico agudo.'}<br>
                    • <strong>Pregunta 3:</strong> {'✅ Correcto. Ante pérdidas masivas de sangre, restaurar la volemia intracardíaca y la perfusión de órganos vitales es la prioridad absoluta.' if q3.startswith('B') else '❌ Incorrecto. La fluidoterapia en choque busca expandir el espacio vascular y salvar la perfusión orgánica.'}<br>
                    • <strong>Pregunta 4:</strong> {'✅ Correcto. El rango fisiológico oscila estrictamente entre 280 y 300 mOsm/L, situando a 290 como el valor medio ideal.' if 280 <= q4 <= 300 else '❌ Incorrecto. La osmolaridad normal de los mamíferos domésticos se ubica en el intervalo de 280 a 300 mOsm/L.'}
                </div>
                """, 
                unsafe_allow_html=True
            )

        # Botón de envío final blindado contra condiciones de carrera
        if st.button(
            "🔒 Concluir y Sellar Unidad 1", 
            type="primary", 
            disabled=st.session_state.procesando or bloqueado, 
            use_container_width=True, 
            key="d6_submit"
        ):
            st.session_state.procesando = True
            
            # Registrar marca de tiempo exacta de finalización en Supabase
            db.registrar_evento_telemetria(st.session_state.get("token_actual", "DEMO"), 6, "finalizacion_modulo_completo")
            
            # Evaluación
            aciertos = sum([
                q1.startswith("C"),
                q2.startswith("A"),
                q3.startswith("B"),
                280 <= q4 <= 300
            ])
            precision = int((aciertos / 4) * 100)
            
            # Penalización sistémica de vitalidad
            if precision < 50:
                st.session_state.vidas = max(0, st.session_state.vidas - 1)
                st.toast("Rendimiento crítico en fluidoterapia. Pérdida de 1 vida clínica.", icon="❤️")
            
            puntos_ganados = aciertos * 15
            st.session_state.puntos_acumulados += puntos_ganados
            
            st.session_state.d6_retroalimentacion = {
                "precision": precision,
                "aciertos": aciertos
            }
            
            # Sincronización atómica final de la unidad hacia Supabase
            db.guardar_registro_juego(
                st.session_state.get("token_actual", "TOKEN-DEMO-MVZ"),
                6,
                st.session_state.d6_juego_score + puntos_ganados,
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
            
            st.session_state.d6_quiz_enviado = True
            st.session_state.procesando = False
            st.rerun()
