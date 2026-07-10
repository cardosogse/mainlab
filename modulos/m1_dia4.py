import streamlit as st
import time
import database as db

def mostrar_dia4():
    """
    Renderiza las lecciones e interacciones del Día 4 utilizando una disposición de pestañas
    responsivas. Corrige errores sintácticos previos e implementa retroalimentación diagnóstica inmediata.
    """
    st.subheader("Día 4: Equilibrio Ácido-Base y Sistemas Amortiguadores Celulares")
    
    # Segmentación por pestañas para optimizar la navegación móvil y la lectura focalizada
    tab_grupos, tab_camara, tab_certificacion = st.tabs([
        "🔬 Grupos Orgánicos", 
        "🌡️ Cámara de Perfusión", 
        "🚑 Certificación Fisiológica"
    ])

    # ==========================================
    # PESTAÑA 1: INSPECCIÓN DE GRUPOS FUNCIONALES
    # ==========================================
    with tab_grupos:
        st.markdown("### Estructura de los Grupos Funcionales Orgánicos")
        st.write(
            "Los grupos funcionales son arreglos específicos de átomos que determinan las propiedades químicas, "
            "la polaridad y la reactividad metabólica de las biomoléculas dentro de los fluidos corporales."
        )
        
        with st.container(border=True):
            grupo = st.selectbox(
                "Grupo Funcional a Inspeccionar:", 
                ["Carbonilo (C=O)", "Metilo (CH3)", "Hidroxilo (-OH)", "Tiol / Disulfuro (-SH)"],
                key="sb_grupos_funcionales"
            )
            
            # Corrección de lógica sintáctica limpia y segura
            if "Carbonilo" in grupo: 
                st.warning("**Carbonilo ($C=O$):** Grupo polar presente en aldehídos y cetonas; constituye el centro neurálgico para la reactividad estequiométrica del metabolismo de glúcidos.")
            elif "Metilo" in grupo:
                st.warning("**Metilo ($-CH_3$):** Agrupación hidrofóbica apolar. Es crítico tanto en el empaquetamiento estructural de las membranas lipídicas como en las marcas epigenéticas de metilación en el ADN.")
            elif "Hidroxilo" in grupo:
                st.info("**Hidroxilo ($-OH$):** Confiere un marcado carácter polar a las cadenas hidrocarbonadas. Facilita la formación de puentes de hidrógeno y gobierna la solubilidad de alcoholes y carbohidratos en soluciones acuosas.")
            elif "Tiol" in grupo:
                st.warning("**Tiol / Disulfuro ($-SH$):** Capaz de formar enlaces covalentes cruzados estables (puentes disulfuro). Es un elemento determinante en la estabilización de la queratina que conforma las pezuñas, cuernos y pelo.")

    # ==========================================
    # PESTAÑA 2: CÁMARA DE PERFUSIÓN (TAMPÓN DE ACIDEZ)
    # ==========================================
    with tab_camara:
        st.markdown("### 🌡️ Cámara de Perfusión y Desnaturalización Proteica")
        st.write(
            "Evalúa la capacidad de amortiguación de los fluidos biológicos midiendo el impacto del pH "
            "sobre la integridad molecular ante una carga súbita de ácido clorhídrico ($HCl$)."
        )
        
        with st.container(border=True):
            solucion = st.radio(
                "Configura la solución de la Cámara de Perfusión Sanguínea:", 
                ["Plasma con Amortiguador Bicarbonato (pH 7.4)", "Agua Destilada Pura (pH 7.0)"],
                key="rd_camara_solucion"
            )
            
            # Botón protegido contra clics múltiples simultáneos
            btn_inyectar = st.button(
                "💉 Inyectar 10 mL de HCl", 
                use_container_width=True,
                disabled=st.session_state.get('procesando', False)
            )
            
            if btn_inyectar:
                st.session_state['procesando'] = True
                token = st.session_state['token_actual']
                
                if "Agua" in solucion:
                    # Mecanismo de doble validación defensiva antes de descontar vidas
                    if not st.session_state.get("advertencia_ph", False):
                        st.markdown("<div class='card-hint'>💡 <b>ALERTA DE SEGURIDAD CLÍNICA:</b> El agua destilada carece por completo de sistemas buffer. Presiona el botón una vez más si estás seguro de desnaturalizar las proteínas de la muestra por alteración de cargas electrostáticas.</div>", unsafe_allow_html=True)
                        st.session_state["advertencia_ph"] = True
                    else:
                        st.session_state["vidas"] = max(0, st.session_state["vidas"] - 1)
                        try:
                            db.sincronizar_progreso_db(
                                token, 
                                st.session_state["puntos_acumulados"], 
                                "1", 
                                st.session_state["vidas"], 
                                st.session_state['tiempo_estudio_min']
                            )
                        except Exception:
                            pass
                        st.markdown("<div class='card-error'>🚨 <b>CHOQUE DE ACIDOSIS CATASTRÓFICO:</b> El pH cayó bruscamente a 2.0. Las proteínas perdieron su conformación nativa y se desnaturalizaron irreversiblemente. <b>-1 Vida Crítica.</b></div>", unsafe_allow_html=True)
                        st.session_state["advertencia_ph"] = False
                        st.session_state['procesando'] = False
                        time.sleep(1.5)
                        st.rerun()
                else:
                    st.markdown("<div class='card-success'>🛡️ <b>SISTEMA DE TAMPÓN EXITOSO:</b> El amortiguador químico capturó eficientemente los protones libres ($H^+$) mediante el equilibrio del ácido carbónico ($H_2CO_3$), absorbiendo la carga ácida sin alterar la viabilidad biológica celular.</div>", unsafe_allow_html=True)
                    st.session_state["advertencia_ph"] = False
                
                st.session_state['procesando'] = False

    # ==========================================
    # PESTAÑA 3: CUESTIONARIO CON RETROALIMENTACIÓN FORMATIVA
    # ==========================================
    with tab_certificacion:
        st.markdown("### 🚑 Cuestionario de Certificación Fisiológica")
        st.write("Responde las siguientes interrogantes bioquímicas para procesar la firma del módulo y autorizar tu ascenso en el escalafón del laboratorio.")
        
        with st.container(border=True):
            Q1 = st.radio(
                "1. ¿Por qué la evolución orgánica seleccionó de forma ubicua la D-Glucosa sobre la L-Glucosa en los sistemas vivos?", 
                ["A) Posee una propiedad óptica física intrínseca que desvía el haz de luz hacia la derecha.", 
                 "B) Su configuración espacial ofrece un ajuste estereoespecífico óptimo (llave-cerradura) con los sitios activos de las enzimas glucolíticas."], 
                index=None,
                key="rd_q1"
            )
            
            Q2 = st.radio(
                "2. La D-Glucosa y la D-Galactosa difieren únicamente en la orientación tridimensional del grupo hidroxilo en el carbono asimétrico número 4 (C-4); por lo tanto, se clasifican como:", 
                ["A) Isótopos estructurales en equilibrio de fases.", 
                 "B) Epímeros moleculares."], 
                index=None,
                key="rd_q2"
            )
            
            # Botón de evaluación protegido
            btn_evaluar = st.button(
                "📜 Firmar y Evaluar Módulo", 
                use_container_width=True,
                disabled=st.session_state.get('procesando', False)
            )
            
            if btn_evaluar:
                st.session_state['procesando'] = True
                token = st.session_state['token_actual']
                
                if not Q1 or not Q2: 
                    st.warning("⚠️ **Examen incompleto:** Es obligatorio registrar un diagnóstico para ambas preguntas antes de someter el módulo al comité evaluador.")
                    st.session_state['procesando'] = False
                else:
                    errores = 0
                    if "B)" not in Q1: errores += 1
                    if "B)" not in Q2: errores += 1
                    
                    # RENDERIZADO INMEDIATO DE BLOQUE DE RETROALIMENTACIÓN FORMATIVA DETALLADA
                    st.markdown("#### 📝 Reporte Analítico de Respuestas")
                    
                    # Análisis Pregunta 1
                    if "B)" in Q1:
                        st.success("✅ **Pregunta 1: Correcto**")
                    else:
                        st.error("❌ **Pregunta 1: Incorrecto**")
                    st.markdown(
                        "> **Fundamento Didáctico (Q1):** Las rutas metabólicas celulares están regidas por enzimas que actúan bajo una complementariedad geométrica y de cargas tridimensional rígida. "
                        "La D-Glucosa encaja perfectamente en el sitio activo de transportadores y quinasas; su propiedad de desviar la luz polarizada (opción A) es una consecuencia física de su asimetría molecular, "
                        "no la causa de su selectividad metabólica."
                    )
                    
                    # Análisis Pregunta 2
                    if "B)" in Q2:
                        st.success("✅ **Pregunta 2: Correcto**")
                    else:
                        st.error("❌ **Pregunta 2: Incorrecto**")
                    st.markdown(
                        "> **Fundamento Didáctico (Q2):** Los **epímeros** se definen estrictamente en bioquímica molecular como aquellos diastereoisómeros "
                        "que alternan su configuración espacial en un solo carbono asimétrico (centro quiral). Dado que la D-Glucosa y la D-Galactosa solo difieren en la posición "
                        "del $-OH$ en el carbono $C-4$, entran de manera perfecta en este criterio químico. Los isótopos (opción A) son variaciones en el número de neutrones de un núcleo atómico, no arreglos espaciales."
                    )
                    
                    # PROCESAMIENTO DE ESTADOS Y PERSISTENCIA DE CALIFICACIONES
                    if errores == 0:
                        st.balloons()
                        st.session_state["puntos_acumulados"] += 200
                        try:
                            db.registrar_intento_quiz(token, nuevos_errores=0, nuevas_vidas=st.session_state["vidas"], tiempo_min=st.session_state['tiempo_estudio_min'])
                            db.sincronizar_progreso_db(token, st.session_state["puntos_acumulados"], "2", st.session_state["vidas"], st.session_state['tiempo_estudio_min'])
                        except Exception:
                            pass
                        st.success("🏆 **CERTIFICACIÓN COMPLETADA:** Récord perfecto detectado. Se ha guardado tu progreso e iniciado el desbloqueo automático de la Unidad 2.")
                        st.session_state["errores_quiz"] = 0
                        st.session_state['procesando'] = False
                        time.sleep(3.5)  # Tiempo de búfer ergonómico para permitir leer la retroalimentación antes de conmutar vistas
                        st.rerun()
                    else:
                        st.session_state["errores_quiz"] += 1
                        if st.session_state["errores_quiz"] == 1:
                            try:
                                db.registrar_intento_quiz(token, nuevos_errores=errores, nuevas_vidas=st.session_state["vidas"], tiempo_min=st.session_state['tiempo_estudio_min'])
                            except Exception:
                                pass
                            st.markdown(f"<div class='card-hint'>💡 El diagnóstico arroja {errores} error(es) crítico(s). Analiza las descripciones científicas de arriba para corregir tu enfoque antes de comprometer tus vidas clínicas.</div>", unsafe_allow_html=True)
                        else:
                            st.session_state["vidas"] = max(0, st.session_state["vidas"] - 1)
                            try:
                                db.registrar_intento_quiz(token, nuevos_errores=errores, nuevas_vidas=st.session_state["vidas"], tiempo_min=st.session_state['tiempo_estudio_min'])
                            except Exception:
                                pass
                            st.error("❌ **FALLO CLÍNICAL SEVERO:** Has errado consecutivamente la validación conceptual del módulo. Se ha deducido 1 Vida de tu cuenta.")
                            st.session_state["errores_quiz"] = 0
                            st.session_state['procesando'] = False
                            time.sleep(3.0)
                            st.rerun()
                            
                    st.session_state['procesando'] = False
