import streamlit as st
import random
import database as db

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
    {"opciones": ["O-O (O₂)", "C-H (Metano)", "N-N (N₂)", "Na-Cl (Sal)"], "intruso": "Na-Cl (Sal)", "razon": "El NaCl posee un enlace Iónico debido a su gran diferencia de electronegatividad, mientras que los demás son enlaces Covalentes Apolares."},
    {"opciones": ["O-H (Agua)", "N-H (Amoníaco)", "C-O (Carbonilo)", "O-O (O₂)"], "intruso": "O-O (O₂)", "razon": "El O₂ es un enlace Covalente Apolar puro (Δchi = 0), mientras que los demás presentan enlaces Covalentes Polares."}
]

def inicializar_estado_dia2():
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
    token_alumno = st.session_state.get("token_actual", "DEMO")
    
    enfoque = st.radio(
        "🔬 Ajustar Espectro del Analizador:", 
        ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], 
        horizontal=True,
        key="d2_enfoque_radio"
    )
    
    tab1, tab2, tab3 = st.tabs(["🔬 Escala de Pauling", "🎮 El Intruso Químico", "📝 Certificación del Día 2"])

    with tab1:
        st.markdown("### Fundamentos: Enlaces Químicos y la Escala de Pauling")
        
        if enfoque == "🐾 Veterinaria":
            st.info("🐾 **Aplicación Veterinaria:** La liposolubilidad de un antibiótico depende de sus enlaces apolares; si un fármaco es altamente apolar, cruzará con facilidad la membrana celular por difusión simple para combatir infecciones intracelulares.")
        elif enfoque == "🩺 Medicina":
            st.info("🩺 **Aplicación Médica:** Los anestésicos locales bloquean los canales de sodio dependientes de voltaje gracias a un equilibrio preciso entre sus porciones polares (solubles en citosol) e hidrofóbicas (afinidad por la membrana).")
        else:
            st.info("🧬 **Aplicación Biológica:** El empaquetamiento e interacciones termodinámicas de las macromoléculas (proteínas y ácidos nucleicos) están regidos por la sutil transición electrónica entre enlaces covalentes polares y apolares.")

        st.markdown("La polaridad de un enlace molecular se rige bajo la diferencia de electronegatividad ($$\Delta\chi$$):")
        st.markdown("> *   $$\Delta\chi < 0.4$$: **Covalente Apolar** (Lipofílicos)\n> *   $$0.4 \\le \\Delta\\chi \\le 1.7$$: **Covalente Polar** (Dipolos)\n> *   $$\Delta\\chi > 1.7$$: **Iónico** (Disociación Electrostática)")
        
        st.markdown("---")
        st.markdown("#### 💥 Simulador de Colisión Atómica")
        col_a, col_b = st.columns(2)
        atomo_a = col_a.selectbox("Selecciona el Átomo A:", list(BIOELEMENTOS.keys()), index=3)
        atomo_b = col_b.selectbox("Selecciona el Átomo B:", list(BIOELEMENTOS.keys()), index=0)

        datos_a, datos_b = BIOELEMENTOS[atomo_a], BIOELEMENTOS[atomo_b]
        delta_chi = round(abs(datos_a["chi"] - datos_b["chi"]), 2)
        
        cat = datos_a["simbolo"] if datos_a["chi"] < datos_b["chi"] else datos_b["simbolo"]
        an = datos_b["simbolo"] if datos_a["chi"] < datos_b["chi"] else datos_a["simbolo"]

        st.markdown(f"##### Análisis Cuántico: $$\Delta\chi = {delta_chi}$$")
        
        if delta_chi < 0.4:
            st.success("Resultado: **Enlace Covalente Apolar**")
            html = f"<div class='nube-apolar'><span>{datos_a['simbolo']}</span><span>{datos_b['simbolo']}</span></div>"
        elif delta_chi <= 1.7:
            st.warning("Resultado: **Enlace Covalente Polar**")
            html = f"<div class='nube-polar'><span>{datos_a['simbolo']}</span><span>{datos_b['simbolo']}</span></div>"
        else:
            st.error("Resultado: **Enlace Iónico**")
            html = f"<div class='ruptura-ionica'><div class='ion-cat'>{cat}⁺</div><div class='ion-an'>{an}⁻</div></div>"
            
        st.markdown(html, unsafe_allow_html=True)

    with tab2:
        st.markdown("### 🎮 El Intruso Químico")
        c_score, c_intentos = st.columns(2)
        c_score.metric("Puntaje Acumulado", f"{st.session_state.d2_juego_score} pts")
        c_intentos.metric("Rondas Evaluadas", st.session_state.d2_juego_intentos)
        
        ronda = st.session_state.d2_ronda_actual
        st.info("Identifica la molécula cuyo tipo de enlace **NO coincide** con la naturaleza de las demás:")
        
        def verificar_intruso(seleccion):
            st.session_state.d2_juego_intentos += 1
            if seleccion == ronda["intruso"]:
                st.session_state.d2_juego_score += 15
                st.toast("¡Excelente análisis estructural!", icon="✅")
                st.session_state.d2_ronda_actual = random.choice(INTRUSOS_DB)
            else:
                st.session_state.d2_juego_score = max(0, st.session_state.d2_juego_score - 5)
                st.toast("Error en la evaluación de polaridad.", icon="❌")

        for op in ronda["opciones"]:
            if st.button(op, use_container_width=True, key=f"d2_b_{op}"):
                verificar_intruso(op)
                st.rerun()

    with tab3:
        st.markdown("### 📝 Cuestionario de Certificación del Día 2")
        bloqueado = st.session_state.d2_quiz_enviado

        q1 = st.radio("1. En la práctica clínica, ¿qué fármacos logran atravesar pasivamente la barrera hematoencefálica con mayor facilidad?", ["A) Compuestos de naturaleza netamente Iónica.", "B) Fármacos con enlaces Covalentes Apolares (estructuras lipofílicas).", "C) Moléculas de alta polaridad hidrofílica."], disabled=bloqueado, key="d2_q1_r")
        q2 = st.radio("2. En una molécula de agua ($H_2O$), ¿cuál es el efecto provocado por la alta electronegatividad del Oxígeno frente al Hidrógeno?", ["A) Un enlace covalente apolar simétrico.", "B) Un enlace covalente polar con densidades de carga parciales y formación de un dipolo.", "C) La cesión completa de electrones formando un cristal iónico."], disabled=bloqueado, key="d2_q2_r")
        q3 = st.radio("3. Cuando se administra suero fisiológico, ¿en qué estado físico se encuentran los átomos de Sodio y Cloro en el plasma?", ["A) Unidos rígidamente compartiendo pares de electrones.", "B) Formando un enlace covalente polar débil.", "C) Completamente disociados e interactuando como iones libres rodeados de agua."], disabled=bloqueado, key="d2_q3_r")
        
        q4 = st.number_input("4. Escribe el valor exacto de la diferencia de electronegatividad ($\Delta\chi$) para un enlace entre Cloro (3.16) y Carbono (2.55):", value=0.00, step=0.01, format="%.2f", disabled=bloqueado, key="d2_q4_n")

        if bloqueado and st.session_state.d2_retroalimentacion:
            prec = st.session_state.d2_retroalimentacion["precision"]
            if prec == 100: st.success(f"🏆 **Certificación Completada:** Precisión del {prec}%.")
            else: st.error(f"❌ **Certificación Denegada:** Precisión del {prec}%.")
            st.markdown(f"<div class='lab-panel'><strong>Reporte Técnico:</strong><br>• Pregunta 1: {'✅ Correcto.' if q1.startswith('B') else '❌ Incorrecto.'}<br>• Pregunta 2: {'✅ Correcto.' if q2.startswith('B') else '❌ Incorrecto.'}<br>• Pregunta 3: {'✅ Correcto.' if q3.startswith('C') else '❌ Incorrecto.'}<br>• Pregunta 4: {'✅ Correcto.' if abs(q4 - 0.61) < 0.01 else '❌ Incorrecto.'}</div>", unsafe_allow_html=True)

        if st.button("🔒 Enviar Respuestas y Registrar Avance", type="primary", disabled=bloqueado, use_container_width=True, key="d2_submit"):
            # --- MEJORA: Validación con Margen de Tolerancia Seguro contra fallos de coma flotante ---
            aciertos = sum([q1.startswith("B"), q2.startswith("B"), q3.startswith("C"), abs(q4 - 0.61) < 0.01])
            precision = int((aciertos / 4) * 100)
            
            if precision < 50:
                st.session_state.vidas = max(0, st.session_state.vidas - 1)
                st.toast("Fallo grave en la precisión de enlaces.", icon="❤️")
            
            puntos_ronda = aciertos * 15
            st.session_state.puntos_acumulados += puntos_ronda
            st.session_state.d2_retroalimentacion = {"precision": precision, "aciertos": aciertos}
            
            db.guardar_registro_juego(token_alumno, 2, st.session_state.d2_juego_score + puntos_ronda, precision, {"enfoque": enfoque})
            db.sincronizar_progreso_db(token_alumno, st.session_state.puntos_acumulados, "1", st.session_state.vidas, st.session_state.tiempo_estudio_min)
            st.session_state.d2_quiz_enviado = True
            st.rerun()
