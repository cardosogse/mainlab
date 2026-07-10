import streamlit as st
import database as db  # Importación unificada por consistencia
from assets import ELEMENTOS, generar_svg_enlace

def mostrar_dia3():
    """
    Renderiza las lecciones e interacciones del Día 3 utilizando un diseño modular de pestañas.
    Optimiza el flujo del reactor químico y expande la calculadora de soluciones con fórmulas formales.
    """
    st.subheader("Día 3: El Reactor de Fusión Atómica e Interacciones Moleculares")
    st.write("Estudia cómo la disparidad en la tracción de electrones determina la estabilidad de las uniones y la solvatación biológica celular.")
    
    # Segmentación por pestañas para optimizar la navegación móvil
    tab_reactor, tab_calculadora = st.tabs([
        "🧬 Reactor de Enlaces Químicos", 
        "🧮 Concentración y Soluciones Molares"
    ])
    
    # Diccionario maestro de electronegatividades (Escala de Pauling)
    escala_pauling = {
        "Oxígeno (O)": 3.44, 
        "Hidrógeno (H)": 2.20, 
        "Carbono (C)": 2.55, 
        "Sodio (Na)": 0.93, 
        "Cloro (Cl)": 3.16, 
        "Nitrógeno (N)": 3.04
    }

    # ==========================================
    # PESTAÑA 1: REACTOR DE ENLACES QUÍMICOS
    # ==========================================
    with tab_reactor:
        st.markdown("### 🧬 Reactor de Fusión de Enlaces")
        st.write(
            "Selecciona dos átomos para colisionar sus capas de valencia. El sistema calculará la diferencia de electronegatividad "
            "$$\Delta\chi = |\chi_A - \chi_B|$$ para predecir el tipo de enlace molecular resultante y su comportamiento en entornos citoplasmáticos."
        )
        
        with st.container(border=True):
            col_controles, col_resultado = st.columns(2)
            
            with col_controles:
                atomo_a = st.selectbox("Selecciona el Átomo Central (A):", list(escala_pauling.keys()), key="sb_atomo_a")
                atomo_b = st.selectbox("Selecciona el Átomo de Reacción (B):", list(escala_pauling.keys()), key="sb_atomo_b")
                
                # Botón de colisión protegido contra ejecución paralela descontrolada
                btn_fusionar = st.button(
                    "💥 Colisionar Capas de Valencia", 
                    use_container_width=True,
                    disabled=st.session_state.get('procesando', False)
                )
            
            with col_resultado:
                # Mantener el estado visual del reactor de forma limpia
                if btn_fusionar:
                    st.session_state['procesando'] = True
                    diff = abs(escala_pauling[atomo_a] - escala_pauling[atomo_b])
                    st.metric("Diferencia de Electronegatividad ($\Delta\chi$)", f"{diff:.2f}")
                    
                    # Extracción y limpieza segura de símbolos químicos para el generador gráfico SVG
                    sym_a = atomo_a.split(" ")[1].replace("(", "").replace(")", "")
                    sym_b = atomo_b.split(" ")[1].replace("(", "").replace(")", "")
                    
                    color_a = ELEMENTOS.get(atomo_a, {"color": "#00e5ff"})["color"]
                    color_b = ELEMENTOS.get(atomo_b, {"color": "#ff5252"})["color"]
                    
                    # Renderizado seguro del componente HTML del enlace químico
                    try:
                        svg_render = generar_svg_enlace(sym_a, escala_pauling[atomo_a], color_a, sym_b, escala_pauling[atomo_b], color_b)
                        st.components.v1.html(svg_render, height=140, scrolling=False)
                    except Exception:
                        st.caption("Diagrama de orbitales moleculares no disponible temporalmente.")
                    
                    # Clasificación pedagógica estricta basada en el gradiente de Pauling
                    if diff < 0.4:
                        st.success("🔬 **Enlace Covalente No Polar (Apolar)**")
                        st.markdown(
                            "> **Importancia Biomédica:** Existe una distribución equitativa de la densidad electrónica. "
                            "Los libros de texto clásicos de bioquímica demuestran que esta simetría molecular origina las interacciones "
                            "hidrofóbicas fundamentales para estabilizar las bicapas lipídicas de las membranas celulares."
                        )
                    elif 0.4 <= diff <= 1.7:
                        st.warning("🌊 **Enlace Covalente Polar**")
                        st.markdown(
                            "> **Importancia Biomédica:** Se genera un dipolo permanente debido a la atracción asimétrica de electrones. "
                            "Este fenómeno induce la alta constante dieléctrica del agua ($78.5$), permitiéndole interponerse y romper "
                            "las redes cristalinas de los compuestos salinos para solvatarlos."
                        )
                    else:
                        st.error("⚡ **Enlace Iónico (Atracción Electrostática)**")
                        st.markdown(
                            "> **Importancia Biomédica:** Ocurre una transferencia neta de electrones de un átomo a otro. "
                            "Genera uniones altamente electrostáticas que se disocian de inmediato en iones libres (electrolitos) "
                            "al entrar en contacto con las soluciones acuosas citoplasmáticas hídricas."
                        )
                    st.session_state['procesando'] = False
                else:
                    st.info("Configura los átomos y presiona el botón para iniciar la colisión cuántica de los orbitales.")

    # ==========================================
    # PESTAÑA 2: CALCULADORA DE CONCENTRACIÓN MOLAR
    # ==========================================
    with tab_calculadora:
        st.markdown("### 🗮️ Calculadora de Concentración Molar")
        st.write(
            "La molaridad ($M$) expresa la cantidad de moles de soluto disueltos por cada litro de solución. "
            "Se calcula matemáticamente aplicando la relación fundamental:"
        )
        st.latex(r"M = \frac{n}{V} = \frac{\left(\frac{m}{PM}\right)}{V}")
        
        with st.container(border=True):
            c1, c2 = st.columns(2)
            
            with c1:
                # Banco de solutos biológicos para dar mayor versatilidad académica universitaria
                soluto_seleccionado = st.selectbox(
                    "Selecciona el Soluto de Trabajo:",
                    ["Cloruro de Sodio (NaCl)", "Glucosa ($C_6H_{12}O_6$)", "Urea ($CH_4N_2O$)"],
                    key="sb_soluto"
                )
                
                # Asignación de pesos moleculares exactos según la selección
                if "NaCl" in soluto_seleccionado:
                    peso_molecular = 58.44
                    etiqueta_masa = "Masa de Soluto (g de NaCl):"
                elif "Glucosa" in soluto_seleccionado:
                    peso_molecular = 180.16
                    etiqueta_masa = "Masa de Soluto (g de Glucosa):"
                else:
                    peso_molecular = 60.06
                    etiqueta_masa = "Masa de Soluto (g de Urea):"
                
                sample_mass = st.slider(etiqueta_masa, min_value=1.0, max_value=100.0, value=5.8, step=0.1, key="sld_masa_soluto")
                sample_vol = st.slider("Volumen Total de la Solución (Litros de $H_2O$):", min_value=0.1, max_value=5.0, value=1.0, step=0.1, key="sld_vol_solucion")
                
            # Algoritmo de estequiometría analítica libre de errores de redondeo
            moles = sample_mass / peso_molecular
            molaridad = moles / sample_vol
            
            with c2:
                st.markdown("#### **Parámetros de Solubilidad**")
                st.write(f"🧬 **Masa Molecular (PM):** `{peso_molecular} g/mol`")
                st.write(f"⚖️ **Cantidad de Soluto:** `{moles:.4f} moles`")
                
                # Métrica final destacada de concentración
                st.metric("Molaridad Resultante ($M$):", f"{molaridad:.3f} mol/L")
                
                # Nota clínica veterinaria contextualizada según el soluto
                if "NaCl" in soluto_seleccionado:
                    if 0.150 <= molaridad <= 0.160:
                        st.success("🩺 Solución Isotónica: Equivalente a la salinidad fisiológica del plasma (Suero fisiológico al 0.9%).")
                    elif molaridad < 0.150:
                        st.warning("⚠️ Solución Hipotónica: Puede provocar lisis (ruptura) de eritrocitos por entrada masiva de agua.")
                    else:
                        st.error("⚠️ Solución Hipertónica: Provocará crenación (deshidratación celular) en los tejidos del paciente.")
