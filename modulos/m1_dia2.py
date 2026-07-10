import streamlit as st
import pandas as pd
import database as db

def mostrar_dia2():
    """
    Renderiza las actividades lógicas del Día 2. Combina un laboratorio dinámico de 
    construcción nuclear e iónica con una matriz periódica de consulta clínica veterinaria.
    """
    st.subheader("Día 2: El Micro-Constructor Atómico y Propiedades Periódicas")
    
    # Segmentación por pestañas para optimizar la ergonomía visual en móviles y escritorio
    tab_constructor, tab_roles = st.tabs([
        "🔬 Constructor de Isótopos e Iones", 
        "🗺️ Matriz de Roles Clínicos Veterinarios"
    ])
    
    # Base de datos centralizada de bioelementos con sus propiedades físicas y fisiológicas
    tabla_elementos = {
        1: {"simbolo": "H", "nombre": "Hidrógeno", "electneg": "2.20", "bio": "Regulador directo del pH (iones hidronio) y del balance hídrico orgánico."},
        6: {"simbolo": "C", "nombre": "Carbono", "electneg": "2.55", "bio": "Esqueleto maestro orgánico capaz de estructurar hasta 4 enlaces covalentes estables."},
        7: {"simbolo": "N", "nombre": "Nitrógeno", "electneg": "3.04", "bio": "Constituyente intrínseco de aminoácidos, proteínas estructurales y bases nitrogenadas del ADN/ARN."},
        8: {"simbolo": "O", "nombre": "Oxígeno", "electneg": "3.44", "bio": "Aceptor final de electrones en la cadena respiratoria mitocondrial para la síntesis de ATP."},
        11: {"simbolo": "Na", "nombre": "Sodio", "electneg": "0.93", "bio": "Principal catión extracelular; gobierna la presión osmótica plasmática y la despolarización neuronal."},
        12: {"simbolo": "Mg", "nombre": "Magnesio", "electneg": "1.31", "bio": "Cofactor indispensable para estabilizar energéticamente la molécula de ATP y activar quinasas."},
        15: {"simbolo": "P", "nombre": "Fósforo", "electneg": "2.19", "bio": "Constituyente estructural de enlaces fosfodiéster, fosfolípidos de membrana y transferencia energética (ATP)."},
        16: {"simbolo": "S", "nombre": "Azufre", "electneg": "2.58", "bio": "Forma puentes disulfuro covalentes, determinantes para la estructura terciaria de proteínas y la queratina."},
        17: {"simbolo": "Cl", "nombre": "Cloro", "electneg": "3.16", "bio": "Anión extracelular maestro encargado de mantener la neutralidad eléctrica salina y el equilibrio ácido-base."},
        20: {"simbolo": "Ca", "nombre": "Calcio", "electneg": "1.00", "bio": "Segundo mensajero intracelular crítico para la contracción miocárdica, la cascada de coagulación y el soporte óseo."}
    }

    # ==========================================
    # PESTAÑA 1: LABORATORIO INTERACTIVO (CONSTRUCTOR)
    # ==========================================
    with tab_constructor:
        st.markdown("### 🛠️ Simulación de Estructura Nuclear y Estados de Oxidación")
        st.write(
            "Manipula los controles deslizantes para ensamblar partículas subatómicas. Observa cómo "
            "el balance de cargas determina si obtienes un átomo neutro o un **ion** "
            "(ya sea un *catión* [ion con carga neta positiva] o un *anión* [ion con carga neta negativa])."
        )
        
        with st.container(border=True):
            col_controles, col_matriz = st.columns([2, 1])
            
            with col_controles:
                protones = st.slider("Protones (Número Atómico $Z$):", min_value=1, max_value=20, value=6, key="sld_protones")
                neutrones = st.slider("Neutrones (Masa Nuclear $N$):", min_value=0, max_value=22, value=6, key="sld_neutrones")
                electrones = st.slider("Electrones (Nube Electrónica $e^-$):", min_value=0, max_value=20, value=6, key="sld_electrones")
                
            # Fórmulas de física nuclear aplicadas de forma automatizada
            masa_atomica = protones + neutrones  # A = Z + N
            carga_neta = protones - electrones   # q = Z - e-
            
            # Determinación cualitativa del estado de ionización
            if carga_neta == 0:
                estado_quimico = "Átomo Neutro (Estabilidad Eléctrica)"
                tipo_alerta = st.info
            elif carga_neta > 0:
                estado_quimico = f"Catión Clínico (+{carga_neta})"
                tipo_alerta = st.success
            else:
                estado_quimico = f"Anión Clínico ({carga_neta})"
                tipo_alerta = st.error
            
            with col_matriz:
                st.markdown("#### **Matriz Isotopicat**")
                st.metric("Identidad Química ($Z$)", f"{protones} p⁺")
                st.metric("Masa Total ($A$)", f"{masa_atomica} u")
                tipo_alerta(estado_quimico)
        
        # Integración Dinámica Inmediata: Renderiza la casilla correspondiente en el mismo flujo visual
        st.markdown("#### **Ficha del Elemento Resultante**")
        if protones in tabla_elementos:
            el = tabla_elementos[protones]
            
            # Estructura visual responsiva para la tarjeta del elemento configurado
            st.markdown(f"""
            <div style="display: flex; gap: 15px; align-items: center; background-color: #0f172a; padding: 20px; border-radius: 8px; border: 1px solid #334155;">
                <div style="background-color: #00e5ff; color: #000; font-size: 2.3rem; font-weight: 900; width: 75px; height: 75px; display: flex; align-items: center; justify-content: center; border-radius: 8px;">{el['simbolo']}</div>
                <div>
                    <b style='color:#ffffff; font-size:1.2rem;'>{el['nombre']} (Z = {protones})</b><br>
                    <span style='color: #94a3b8;'>Electronegatividad de Pauling:</span> <b style='color:#00e5ff;'>{el['electneg']}</b><br>
                    <p style='margin: 5px 0 0 0; color: #e2e8f0;'><b>Relevancia Médica:</b> {el['bio']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.caption(
                "🔬 **Átomo fuera de alcance biológico:** Sigue ajustando el número de protones. "
                "Cuando configures los números atómicos de los bioelementos esenciales (tales como Z=1, 6, 7, 8, 11, 12, 15, 16, 17 o 20) "
                "se desplegará automáticamente su ficha metabólica en este espacio."
            )

    # ==========================================
    # PESTAÑA 2: MATRIZ COMPLETA DE CONSULTA (TABLA ESTÁTICA HIGIÉNICA)
    # ==========================================
    with tab_roles:
        st.markdown("### 🗺️ Propiedades de los Bioelementos Esenciales")
        st.write(
            "A continuación se presenta el mapa analítico con los 10 elementos químicos fundamentales "
            "para la fisiología, diagnóstico clínico y terapéutica en medicina veterinaria y zootecnia."
        )
        
        # Transformación de la estructura del diccionario a un DataFrame limpio para evitar token-spew
        lista_elementos_df = [
            {
                "Z": k, 
                "Símbolo": v["simbolo"], 
                "Bioelemento": v["nombre"], 
                "Electronegatividad": v["electneg"], 
                "Impacto Fisiológico y Clínico": v["bio"]
            } 
            for k, v in tabla_elementos.items()
        ]
        
        df_elementos = pd.DataFrame(lista_elementos_df)
        
        # Despliegue seguro e interactivo del DataFrame de consulta
        st.dataframe(
            df_elementos.set_index("Z"), 
            use_container_width=True,
            column_config={
                "Símbolo": st.column_config.TextColumn("Símbolo", width="small"),
                "Electronegatividad": st.column_config.TextColumn("Electronegatividad", width="small"),
            }
        )
        
        st.markdown(
            "> **Nota del Experto:** La diferencia de *electronegatividad* (capacidad de un átomo para atraer electrones) "
            "entre estos elementos determinará si interactúan mediante enlaces covalentes polares, apolares o enlaces iónicos "
            "en los fluidos corporales del paciente."
        )
