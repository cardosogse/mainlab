import streamlit as st
import random
import database as db

# Base de datos analítica de Isomería y Grupos Funcionales
DB_GRUPOS_M1 = [
    {
        "id": "tiol",
        "pregunta": "Identifica el grupo funcional responsable de formar enlaces covalentes cruzados (puentes disulfuro) indispensables para la estabilidad estructural proteica:",
        "opciones": ["Tiol (-SH)", "Carbonilo (=O)", "Metilo (-CH₃)"],
        "correcta": "Tiol (-SH)",
        "fundamento": "Los grupos tiol (-SH) de las cisteínas sufren oxidación para formar puentes disulfuro (-S-S-), estabilizando estructuras terciarias y cuaternarias moleculares."
    },
    {
        "id": "quiralidad",
        "pregunta": "¿Qué característica define termodinámicamente a una molécula quiral en el entorno celular?",
        "opciones": ["Posee un carbono asimétrico con 4 sustituyentes distintos.", "Es completamente simétrica y soluble en lípidos.", "Carece de isómeros espaciales funcionales."],
        "correcta": "Posee un carbono asimétrico con 4 sustituyentes distintos.",
        "fundamento": "La presencia de un carbono quiral da origen a enantiómeros (imágenes especulares no superponibles), alterando por completo el reconocimiento por receptores metabólicos."
    }
]

def inicializar_estado_dia7():
    if "d7_juego_score" not in st.session_state: st.session_state.d7_juego_score = 0
    if "d7_juego_intentos" not in st.session_state: st.session_state.d7_juego_intentos = 0
    if "d7_quiz_enviado" not in st.session_state: st.session_state.d7_quiz_enviado = False
    if "d7_caso_actual" not in st.session_state:
        st.session_state.d7_caso_actual = random.choice(DB_GRUPOS_M1)
        caso = st.session_state.d7_caso_actual
        opc = caso["opciones"].copy()
        random.shuffle(opc)
        st.session_state.d7_opciones_fijadas = opc
    if "d7_retroalimentacion" not in st.session_state: st.session_state.d7_retroalimentacion = None

def procesar_respuesta_dia7(seleccion: str, token_alumno: str):
    st.session_state.d7_juego_intentos += 1
    caso = st.session_state.d7_caso_actual
    
    if seleccion == caso["correcta"]:
        st.session_state.d7_juego_score += 20
        st.toast(f"¡Precisión Molecular Excepcional! {caso['fundamento']}", icon="✅")
    else:
        st.session_state.d7_juego_score = max(0, st.session_state.d7_juego_score - 10)
        st.toast("Fallo en la lectura de hibridación atómica.", icon="❌")
        
    st.session_state.d7_caso_actual = random.choice(DB_GRUPOS_M1)
    nuevo_caso = st.session_state.d7_caso_actual
    opc_nuevas = nuevo_caso["opciones"].copy()
    random.shuffle(opc_nuevas)
    st.session_state.d7_opciones_fijadas = opc_nuevas

def app():
    inicializar_estado_dia7()
    token_alumno = st.session_state.get("token_actual", "DEMO")
    
    enfoque = st.radio(
        "🔬 Configurar el Espectrómetro de Hibridación:", 
        ["🐾 Veterinaria", "🩺 Medicina", "🧬 Biología"], 
        horizontal=True,
        key="d7_enfoque_radio"
    )
    
    t_teoria, t_juego, t_quiz = st.tabs(["🔬 Arquitectura Funcional", "🎮 Desafío Estereoquímico", "📝 Certificación"])

    with t_teoria:
        st.markdown("### Grupos Funcionales y Estereoquímica Celular")
        
        if enfoque == "🐾 Veterinaria":
            st.warning("🐾 **Enfoque Veterinario (Salud de Dermis y Faneras):** Los puentes disulfuro derivados de grupos **tiol (-SH)** dictan la dureza mecánica de la queratina en cascos y pezuñas en equinos y bovinos. La deficiencia de azufre interrumpe esta hibridación intermolecular.")
        elif enfoque == "🩺 Medicina":
            st.warning("🩺 **Enfoque Médico (Quiralidad Farmacológica):** La quiralidad espacial determina la afinidad por receptores. La mezcla racémica de compuestos químicos puede ser letal; el enantiómero $R\text{-adrenalina}$ presenta una afinidad diez veces superior sobre receptores adrenérgicos frente a su isómero espacial $S$.")
        else:
            st.info("🧬 **Enfoque Biológico (Evolución Molecular):** La vida celular exhibe una **homoquiralidad** absoluta: todas las proteínas biológicas se construyen exclusivamente a partir de aminoácidos en configuración espacial $L$, mientras que los ácidos nucleicos utilizan azúcares en configuración $D$.")

        st.markdown("---")
        st.markdown("#### 🔬 Simulador de Isomería Espacial e Hibridación Carbonada")
        st.latex(r"\text{Carbono Quiral: } C^* \rightarrow 4 \text{ Radicales Diferentes } (R_1 \neq R_2 \neq R_3 \neq R_4)")
        
        rad1 = st.selectbox("Sustituyente 1:", ["-H", "-OH", "-COOH", "-NH₂"], index=0, key="d7_s1")
        rad2 = st.selectbox("Sustituyente 2:", ["-H", "-OH", "-COOH", "-NH₂"], index=1, key="d7_s2")
        rad3 = st.selectbox("Sustituyente 3:", ["-H", "-OH", "-COOH", "-NH₂"], index=2, key="d7_s3")
        rad4 = st.selectbox("Sustituyente 4:", ["-H", "-OH", "-COOH", "-NH₂"], index=3, key="d7_s4")
        
        conjunto = {rad1, rad2, rad3, rad4}
        if len(conjunto) == 4:
            st.success("✨ **CENTRO QUIRAL DETECTADO:** El átomo de carbono es asimétrico. Esta molécula posee actividad óptica y genera enantiómeros no superponibles.")
        else:
            st.error("🧱 **ÁTOMO ACÍCLICO SIMÉTRICO:** Existen sustituyentes idénticos. La molécula es aquiral y carece de enantiómeros espaciales.")

    with t_juego:
        st.markdown("### 🎮 Desafío Estructural")
        c1, c2 = st.columns(2)
        c1.metric("Score Acumulado", f"{st.session_state.d7_juego_score} pts")
        c2.metric("Lecturas Realizadas", st.session_state.d7_juego_intentos)
        
        caso = st.session_state.d7_caso_actual
        st.info(f"📋 **Desafío Estructural:** {caso['pregunta']}")
        
        opc = st.session_state.d7_opciones_fijadas
        for o in opc:
            if st.button(o, use_container_width=True, key=f"d7_btn_{o}"):
                procesar_respuesta_dia7(o, token_alumno)
                st.rerun()

    with t_quiz:
        st.markdown("### 📝 Evaluación Formativa del Día 7")
        bloqueado = st.session_state.d7_quiz_enviado
        
        q1 = st.radio("1. ¿Qué enlace intermolecular covalente estabiliza directamente la estructura terciaria de las proteínas mediante la oxidación de grupos Tiol?", ["A) Puentes de Hidrógeno", "B) Enlaces por puentes Disulfuro", "C) Fuerzas dipolo-dipolo inducido"], disabled=bloqueado, key="d7_q1")
        q2 = st.radio("2. La quiralidad en los carbohidratos biológicos determina que las células metabolicen preferencialmente:", ["A) Isómeros espaciales en configuración D", "B) Enantiómeros puros en configuración L", "C) Compuestos puramente apolares simétricos"], disabled=bloqueado, key="d7_q2")
        
        if bloqueado and st.session_state.d7_retroalimentacion:
            prec = st.session_state.d7_retroalimentacion["precision"]
            st.success(f"🏆 Certificación Concluida: Precisión del {prec}%.")
            
        if st.button("🔒 Enviar Bloque de Estereoquímica", type="primary", disabled=bloqueado, use_container_width=True, key="d7_submit"):
            aciertos = sum([q1.startswith("B"), q2.startswith("A")])
            precision = int((aciertos / 2) * 100)
            
            puntos_ganados = aciertos * 20
            st.session_state.puntos_acumulados += puntos_ganados
            st.session_state.d7_retroalimentacion = {"precision": precision}
            
            db.sincronizar_progreso_db(token_alumno, st.session_state.puntos_acumulados, "1", st.session_state.vidas, st.session_state.tiempo_estudio_min)
            st.session_state.d7_quiz_enviado = True
            st.rerun()
