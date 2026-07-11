import streamlit as st
import random
from database import guardar_registro_juego

# Base de datos local de bioelementos y su electronegatividad (Escala de Pauling)
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

# Base de preguntas para "El Intruso Químico"
INTRUSOS_DB = [
    {"opciones": ["O-O (O₂)", "C-H (Metano)", "N-N (N₂)", "Na-Cl (Sal)"], "intruso": "Na-Cl (Sal)", "razon": "El NaCl es Iónico, los demás son Covalentes Apolares."},
    {"opciones": ["O-H (Agua)", "N-H (Amoníaco)", "C-O (Carbonilo)", "O-O (O₂)"], "intruso": "O-O (O₂)", "razon": "El O₂ es Apolar puro, los demás son Covalentes Polares."},
    {"opciones": ["Ca-Cl (Cloruro de Calcio)", "K-Cl (Cloruro de Potasio)", "Na-Cl (Cloruro de Sodio)", "C-H (Metano)"], "intruso": "C-H (Metano)", "razon": "El enlace C-H es Apolar, los demás son Iónicos clásicos."}
]

def inicializar_estado():
    """Blindaje de variables de sesión para el Día 2."""
    if "d2_juego_score" not in st.session_state:
        st.session_state.d2_juego_score = 0
    if "d2_juego_intentos" not in st.session_state:
        st.session_state.d2_juego_intentos = 0
    if "d2_quiz_enviado" not in st.session_state:
        st.session_state.d2_quiz_enviado = False
    if "d2_ronda_actual" not in st.session_state:
        st.session_state.d2_ronda_actual = random.choice(INTRUSOS_DB)

def app():
    st.title("💥 Día 2: Enlaces y Polaridad")
    st.markdown("¿Por qué el agua disuelve la sangre pero no la grasa? La respuesta está en la geometría de sus nubes electrónicas.")
    
    inicializar_estado()

    # Selector de Enfoque Clínico
    enfoque = st.radio("Selecciona tu enfoque de análisis:", ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], horizontal=True)

    tab1, tab2, tab3 = st.tabs(["🔬 Reactor de Fusión", "🎮 Juego: El Intruso Químico", "📝 Quiz de Certificación"])

    # ==========================================
    # PESTAÑA 1: TEORÍA Y REACTOR DE FUSIÓN
    # ==========================================
    with tab1:
        st.header("Fundamentos: La Escala de Pauling")
        st.markdown(
            "La **Electronegatividad ($\chi$)** es la fuerza con la que un átomo atrae los electrones de un enlace hacia sí mismo. "
            "Para predecir el comportamiento biológico de una molécula, calculamos la diferencia ($\Delta \chi$) entre sus átomos:"
        )
        
        st.info("**$\Delta \chi < 0.4$ : Covalente Apolar** (Comparten por igual, lipofílicos, atraviesan membranas).")
        st.warning("**$\Delta \chi$ entre 0.4 y 1.7 : Covalente Polar** (Tienen polos eléctricos, hidrofílicos, solubles en plasma).")
        st.error("**$\Delta \chi > 1.7$ : Iónico** (Robo total de electrones, forman cristales, conducen electricidad).")

        st.markdown("---")
        st.subheader("🔬 Reactor de Fusión de Enlaces")
        st.markdown("Selecciona dos bioelementos para colisionarlos y observa cómo se deforma la nube electrónica.")

        col_a, col_b = st.columns(2)
        with col_a:
            atomo_a = st.selectbox("Átomo A:", list(BIOELEMENTOS.keys()), index=3) # Default H
        with col_b:
            atomo_b = st.selectbox("Átomo B:", list(BIOELEMENTOS.keys()), index=0) # Default O

        if st.button("💥 ¡COLISIONAR!", use_container_width=True, type="primary"):
            datos_a = BIOELEMENTOS[atomo_a]
            datos_b = BIOELEMENTOS[atomo_b]
            
            # Cálculo matemático absoluto del Delta Chi
            delta_chi = round(abs(datos_a["chi"] - datos_b["chi"]), 2)
            
            # Determinación de los roles para Iónico
            cat = datos_a["simbolo"] if datos_a["chi"] < datos_b["chi"] else datos_b["simbolo"]
            an = datos_b["simbolo"] if datos_a["chi"] < datos_b["chi"] else datos_a["simbolo"]

            st.markdown(f"### $\Delta \chi = | {datos_a['chi']} - {datos_b['chi']} | = {delta_chi}$")

            # Renderizado Condicional HTML/CSS
            if delta_chi < 0.4:
                st.success("**Diagnóstico:** Enlace Covalente Apolar. Compartición equitativa.")
                html = f"<div class='nube-apolar'><span>{datos_a['simbolo']}</span><span>{datos_b['simbolo']}</span></div>"
            elif delta_chi <= 1.7:
                st.warning("**Diagnóstico:** Enlace Covalente Polar. Nube deformada hacia el polo más electronegativo.")
                # Colocamos el más electronegativo a la derecha visualmente
                html = f"<div class='nube-polar'><span>{datos_a['simbolo']}</span><span>{datos_b['simbolo']}</span></div>"
            else:
                st.error("**Diagnóstico:** Enlace Iónico. Ruptura de la nube y formación de iones libres.")
                html = f"<div class='ruptura-ionica'><div class='ion-cat'>{cat}⁺</div><div class='ion-an'>{an}⁻</div></div>"

            st.markdown(html, unsafe_allow_html=True)


    # ==========================================
    # PESTAÑA 2: JUEGO - EL INTRUSO QUÍMICO
    # ==========================================
    with tab2:
        st.header("🎮 El Intruso Químico")
        st.markdown("Reconocimiento de patrones: Tres de estos enlaces pertenecen a la misma familia termodinámica. Uno es el intruso. **¡Encuéntralo!**")
        
        st.metric("Puntaje Acumulado", st.session_state.d2_juego_score)
        st.markdown("---")
        
        ronda = st.session_state.d2_ronda_actual
        opciones = ronda["opciones"]
        # Mezclamos las opciones visualmente
        opciones_mezcladas = random.sample(opciones, len(opciones))
        
        def verificar_intruso(seleccion):
            st.session_state.d2_juego_intentos += 1
            if seleccion == ronda["intruso"]:
                st.session_state.d2_juego_score += 15
                st.toast(f"¡Correcto! {ronda['razon']}", icon="✅")
                # Siguiente ronda aleatoria
                st.session_state.d2_ronda_actual = random.choice(INTRUSOS_DB)
            else:
                st.session_state.d2_juego_score -= 5
                st.toast("Ese no es el intruso. Analiza la polaridad.", icon="❌")

        # Botones de ancho completo para celular
        for op in opciones_mezcladas:
            if st.button(op, use_container_width=True):
                verificar_intruso(op)
                st.rerun()


    # ==========================================
    # PESTAÑA 3: QUIZ DE CERTIFICACIÓN
    # ==========================================
    with tab3:
        st.header("📝 Quiz de Certificación")
        st.markdown("Las interacciones a nivel atómico dictan la fisiología a nivel sistémico.")
        
        deshabilitar = st.session_state.d2_quiz_enviado

        q1 = st.radio(
            "1. La barrera hematoencefálica es rica en lípidos. ¿Qué tipo de fármacos la atraviesan con mayor facilidad mediante difusión simple?",
            ["A) Fármacos con múltiples enlaces iónicos.", "B) Fármacos con enlaces covalentes apolares (lipofílicos).", "C) Fármacos con alta polaridad y carga neta fuerte."],
            disabled=deshabilitar,
            key="d2_q1"
        )
        
        q2 = st.radio(
            "2. En la estructura del agua (H₂O), la alta electronegatividad del oxígeno atrae fuertemente los electrones del hidrógeno. Esto genera un:",
            ["A) Enlace covalente apolar que repele otras moléculas.", "B) Enlace covalente polar que genera densidades de carga parciales.", "C) Enlace iónico que cristaliza a temperatura ambiente."],
            disabled=deshabilitar,
            key="d2_q2"
        )
        
        q3 = st.radio(
            "3. En una solución de suero fisiológico intravenoso, el Sodio y el Cloro se encuentran:",
            ["A) Compartiendo un par de electrones equitativamente.", "B) Unidos por un enlace covalente polar fuerte.", "C) Disociados como iones libres (Na⁺ y Cl⁻) tras romperse su enlace iónico."],
            disabled=deshabilitar,
            key="d2_q3"
        )
        
        st.markdown("**4. Pregunta Analítica (Respuesta Numérica)**")
        st.markdown("Un átomo de Cloro ($\chi = 3.16$) interactúa con uno de Carbono ($\chi = 2.55$).")
        q4 = st.number_input(
            "Calcula la Diferencia de Electronegatividad ($\Delta \chi$) exacta (Usa dos decimales):",
            value=0.00, step=0.01, format="%.2f", disabled=deshabilitar, key="d2_q4"
        )

        if st.button("Enviar Respuestas y Guardar", type="primary", disabled=deshabilitar, use_container_width=True):
            aciertos = 0
            if q1.startswith("B"): aciertos += 1
            if q2.startswith("B"): aciertos += 1
            if q3.startswith("C"): aciertos += 1
            if q4 == 0.61: aciertos += 1
            
            precision = (aciertos / 4) * 100
            
            metadata = {
                "juego_score_final": st.session_state.d2_juego_score,
                "juego_intentos_totales": st.session_state.d2_juego_intentos,
                "quiz_respuestas": [q1[0], q2[0], q3[0], q4],
                "enfoque_seleccionado": enfoque
            }
            
            correo_alumno = st.session_state.get("usuario_correo", "estudiante_invitado@unam.mx")
            
            exito = guardar_registro_juego(
                alumno_id=correo_alumno,
                dia_modulo=2,
                puntaje=st.session_state.d2_juego_score,
                precision_pct=int(precision),
                metadata_juego=metadata
            )
            
            st.session_state.d2_quiz_enviado = True
            
            if exito:
                st.success(f"¡Resultados guardados! Precisión: {precision}%")
            else:
                st.warning(f"Evaluación completada (Precisión: {precision}%). Módulo finalizado en modo local.")
            
            st.rerun()
