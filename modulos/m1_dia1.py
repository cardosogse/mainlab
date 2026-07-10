import streamlit as st
import time
import database as db
from assets import obtener_svg_atomo

def mostrar_dia1():
    """
    Renderiza el contenido y simuladores interactivos del Día 1 utilizando una disposición 
    de pestañas para optimizar la ergonomía visual y asegurar un flujo defensivo libre de bloqueos.
    """
    st.subheader("Día 1: Niveles de Organización y Separación de Fases")
    
    # Implementación de sub-pestañas para segmentar los componentes de la lección diaria
    tab_simulador, tab_modelos, tab_reto = st.tabs([
        "🔬 Fraccionamiento de Fases", 
        "⚛️ Evolución Atómica", 
        "🧠 Reto de Afinidad"
    ])
    
    # ==========================================
    # PESTAÑA 1: SIMULADOR DE CENTRIFUGACIÓN
    # ==========================================
    with tab_simulador:
        st.markdown("### 🔬 Simulador de Centrifugación Macromolecular")
        st.write(
            "La bioquímica es una ciencia aplicada; los procesos generados *in vitro* constituyen las bases del diagnóstico clínico. "
            "La separación de fases mediante aceleración centrífuga se fundamenta en la **Ley de Stokes**, donde la velocidad de sedimentación "
            "depende directamente del radio de la partícula y la diferencia de densidad con el medio."
        )
        
        with st.container(border=True):
            muestra = st.selectbox(
                "Selecciona la muestra biológica a procesar en el rotor:", 
                ["Plasma Sanguíneo", "Sangre Entera (Muestra anticoagulada)"],
                key="sb_muestra"
            )
            
            # Botón controlado defensivamente por el estado global de procesamiento
            btn_centrifugar = st.button(
                "🧬 Ejecutar Fuerzas G (Centrifugar)", 
                use_container_width=True,
                disabled=st.session_state.get('procesando', False)
            )
            
            if btn_centrifugar:
                st.session_state['procesando'] = True
                progreso = st.progress(0)
                
                # Simulación fluida y acelerada del giro del rotor
                for i in range(100):
                    time.sleep(0.003)
                    progreso.progress(i + 1)
                
                if muestra == "Plasma Sanguíneo":
                    st.success("🔬 **Diagnóstico Clínico: Mezcla Homogénea (Fase Coloidal Continua)**")
                    st.markdown(
                        "> **Fundamento Bioquímico:** El plasma mantiene una fase uniforme debido a que las proteínas plasmáticas "
                        "(como la albúmina y las globulinas) permanecen dispersas en el agua sin precipitar bajo fuerzas centrífugas ordinarias, "
                        "sostenidas por sus capas de solvatación y cargas eléctricas superficiales moleculares."
                    )
                else:
                    st.warning("🩸 **Diagnóstico Clínico: Mezcla Heterogénea en Suspensión**")
                    st.markdown(
                        "> **Fundamento Bioquímico:** La aceleración centrífuga precipita los elementos formes celulares más densos "
                        "(eritrocitos, leucocitos) hacia el fondo del tubo de ensayo por gradiente físico, separándolos por completo del "
                        "plasma acelular que queda retenido de forma sobrenadante en la superficie."
                    )
                st.session_state['procesando'] = False

    # ==========================================
    # PESTAÑA 2: TEORÍAS Y MODELOS ATÓMICOS
    # ==========================================
    with tab_modelos:
        st.markdown("### 🗛️ Deslizador de Teorías Cuánticas y Modelos Atómicos")
        st.write(
            "Comprender la configuración electrónica de la materia es el pilar para entender los enlaces químicos moleculares "
            "y las interacciones hidrofóbicas en los sistemas vivos. Navega cronológicamente para examinar la evolución del átomo."
        )
        
        with st.container(border=True):
            modelo = st.select_slider(
                "Navegación Cronológica del Desarrollo Atómico:",
                options=["Dalton (1810)", "Thomson (1897)", "Rutherford (1911)", "Bohr (1913)", "Schrödinger (1926)"],
                key="slider_teorias"
            )
            
            col_txt, col_svg = st.columns([2.5, 1.5])
            
            with col_txt:
                if "Dalton" in modelo:
                    st.markdown("#### **Modelo de la Esfera Sólida**")
                    st.info("Dalton (1810): El átomo es concebido como una partícula esférica sólida, indivisible y sin cargas internas. Permite fundamentar las primeras leyes de proporciones estequiométricas combinatorias elementales.")
                elif "Thomson" in modelo:
                    st.markdown("#### **Modelo del Budín de Pasas**")
                    st.info("Thomson (1897): Descubre el electrón mediante tubos de rayos catódicos. Introduce la naturaleza eléctrica intrínseca de la materia al postular cargas negativas incrustadas en una masa de carga positiva continua.")
                elif "Rutherford" in modelo:
                    st.markdown("#### **Modelo Planetario / Nuclear**")
                    st.info("Rutherford (1911): Demuestra mediante el bombardeo de láminas de oro con partículas alfa que el átomo posee un núcleo central diminuto y masivo con carga positiva, donde los electrones giran en órbitas distantes.")
                elif "Bohr" in modelo:
                    st.markdown("#### **Modelo de Estados Estacionarios**")
                    st.info("Bohr (1913): Introduce la cuantización al postular órbitas circulares fijas permitidas. Los electrones solo transitan en niveles fijos de energía radiando o absorbiendo fotones únicamente al cambiar de nivel.")
                else:
                    st.markdown("#### **Modelo Mecano-Cuántico Probabilístico**")
                    st.info("Schrödinger (1926): Substituye las órbitas rígidas por ecuaciones de onda probabilísticas. Introduce el concepto de **orbital atómico** como regiones moleculares 3D de máxima probabilidad electrónica.")
            
            with col_svg:
                try:
                    svg_html = obtener_svg_atomo(modelo)
                    st.components.v1.html(
                        f"<div style='display:flex; justify-content:center; align-items:center; width:100%; height:120px; background-color:rgba(255,255,255,0.03); border-radius:8px;'>{svg_html}</div>", 
                        height=130, 
                        scrolling=False
                    )
                except Exception:
                    st.caption("Visualización gráfica del modelo no disponible.")

    # ==========================================
    # PESTAÑA 3: DESAFÍO DE CONSOLIDACIÓN
    # ==========================================
    with tab_reto:
        st.markdown("### 🧠 Desafío de Consolidación: Memorama Atómico")
        st.write("Estabiliza los enlaces lógicos emparejando los conceptos correctos para obtener bonificaciones directas sobre tu cuenta de investigador.")
        
        if "memo_tablero" in st.session_state:
            with st.container(border=True):
                # Renderizado controlado de la cuadrícula adaptativa de tarjetas
                cols_memo = st.columns(5)
                for i in range(10):
                    col_idx = i % 5
                    with cols_memo[col_idx]:
                        val_tarjeta, id_par = st.session_state["memo_tablero"][i]
                        
                        if id_par in st.session_state.get("memo_resueltas", []):
                            st.button(f"✅ {val_tarjeta}", key=f"btn_res_{i}", disabled=True, use_container_width=True)
                        elif i in st.session_state.get("memo_reveladas", []):
                            st.button(f"👀 {val_tarjeta}", key=f"btn_rev_{i}", disabled=True, use_container_width=True)
                        else:
                            # Bloqueo estricto si ya hay dos tarjetas abiertas o si el sistema está procesando datos por red
                            bloqueo_clic = len(st.session_state.get("memo_reveladas", [])) >= 2 or st.session_state.get('procesando', False)
                            if st.button("⚛️", key=f"btn_act_{i}", use_container_width=True, disabled=bloqueo_clic):
                                st.session_state["memo_reveladas"].append(i)
                                st.rerun()
            
            # MOTOR DE EVALUACIÓN EN SEGUNDO PLANO
            if len(st.session_state.get("memo_reveladas", [])) == 2:
                st.session_state['procesando'] = True
                idx1, idx2 = st.session_state["memo_reveladas"]
                val1, id_par1 = st.session_state["memo_tablero"][idx1]
                val2, id_par2 = st.session_state["memo_tablero"][idx2]
                
                if id_par1 == id_par2:
                    if id_par1 not in st.session_state["memo_resueltas"]:
                        st.session_state["memo_resueltas"].append(id_par1)
                        st.session_state["racha_consecutiva"] += 1
                        puntos_ganados = 100
                        
                        # Manejo seguro de la extensión de la licencia por racha cuántica
                        if st.session_state["racha_consecutiva"] >= 2 and not st.session_state.get("licencia_extendida", False):
                            puntos_ganados += 300
                            st.session_state["licencia_extendida"] = True
                            try:
                                db.otorgar_tiempo_extra_db(st.session_state["token_actual"], dias_adicionales=7)
                                st.toast("🚀 ¡RACHA CUÁNTICA! +7 días de licencia extendida con éxito.", icon="🎁")
                            except Exception:
                                pass
                            
                        st.session_state["puntos_acumulados"] += puntos_ganados
                        
                        # Persistencia síncrona controlada sin duplicidad
                        try:
                            db.sincronizar_progreso_db(
                                st.session_state["token_actual"], 
                                st.session_state["puntos_acumulados"], 
                                "1", 
                                st.session_state["vidas"],
                                st.session_state["tiempo_estudio_min"]
                            )
                        except Exception:
                            pass
                            
                    st.toast("⚡ ¡Afinidad molecular correcta! Enlace lógicamente estable.", icon="✅")
                    st.session_state["memo_reveladas"] = []
                    st.session_state['procesando'] = False
                    st.rerun()
                else:
                    st.session_state["racha_consecutiva"] = 0
                    st.error(f"❌ Incompatibilidad: Las tarjetas '{val1}' y '{val2}' no pertenecen al mismo modelo.")
                    
                    # Reducción estratégica del tiempo de espera para evitar lag severo percibido por el usuario
                    time.sleep(1.2)
                    st.session_state["memo_reveladas"] = []
                    st.session_state['procesando'] = False
                    st.rerun()
        else:
            st.info("Inicializando los componentes moleculares del tablero...")
