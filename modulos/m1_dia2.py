import streamlit as st

def mostrar_dia2():
    st.subheader("Día 2: El Micro-Constructor Atómico y Propiedades Periódicas")
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🛠️ Configuración de Partículas Subatómicas")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        protones = st.slider("Protones (Número Atómico Z):", min_value=1, max_value=20, value=6)
        neutrones = st.slider("Neutrones (Masa Nuclear N):", min_value=0, max_value=22, value=6)
        electrones = st.slider("Electrones (Capa de Valencia):", min_value=0, max_value=20, value=6)
        
    masa_atomica = protones + neutrones
    carga_neta = protones - electrones
    estado_quimico = "Átomo Neutro" if carga_neta == 0 else (f"Catión (+{carga_neta})" if carga_neta > 0 else f"Anión ({carga_neta})")
    
    with col2:
        st.markdown("#### Matriz Atómica")
        st.metric("Identidad (Z)", f"Protones: {protones}")
        st.metric("Masa Total (A)", f"{masa_atomica} u")
        if carga_neta == 0: 
            st.info(estado_quimico)
        elif carga_neta > 0: 
            st.success(estado_quimico)
        else: 
            st.error(estado_quimico)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🗺️ Casillas Periódicas y Roles Clínicos Veterinarios")
    
    tabla_elementos = {
        1: {"simbolo": "H", "nombre": "Hidrógeno", "electneg": "2.20", "bio": "Regulador directo del pH y balance hídrico."},
        6: {"simbolo": "C", "nombre": "Carbono", "electneg": "2.55", "bio": "Esqueleto maestro capaz de estructurar hasta 4 enlaces covalentes."},
        7: {"simbolo": "N", "nombre": "Nitrógeno", "electneg": "3.04", "bio": "Constituyente intrínseco de aminoácidos y bases del ADN."},
        8: {"simbolo": "O", "nombre": "Oxígeno", "electneg": "3.44", "bio": "Aceptor final de electrones en la respiración mitocondrial."},
        11: {"simbolo": "Na", "nombre": "Sodio", "electneg": "0.93", "bio": "Catión extracelular; gobierna la presión osmótica plasmática."},
        12: {"simbolo": "Mg", "nombre": "Magnesio", "electneg": "1.31", "bio": "Cofactor indispensable para estabilizar energéticamente el ATP."},
        15: {"simbolo": "P", "nombre": "Fósforo", "electneg": "2.19", "bio": "Constituyente de enlaces fosfodiéster y transferencia energética."},
        16: {"simbolo": "S", "nombre": "Azufre", "electneg": "2.58", "bio": "Forma puentes disulfuro cruzados determinantes en la queratina."},
        17: {"simbolo": "Cl", "nombre": "Cloro", "electneg": "3.16", "bio": "Anión extracelular maestro encargado de la neutralidad salina."},
        20: {"simbolo": "Ca", "nombre": "Calcio", "electneg": "1.00", "bio": "Segundo mensajero; crítico en contracción miocárdica y soporte óseo."}
    }
    
    if protones in tabla_elementos:
        el = tabla_elementos[protones]
        st.markdown(f"""
        <div style="display: flex; gap: 15px; align-items: center; background-color: #0f172a; padding: 20px; border-radius: 8px; border: 1px solid #334155;">
            <div style="background-color: #00e5ff; color: #000; font-size: 2.3rem; font-weight: 900; width: 75px; height: 75px; display: flex; align-items: center; justify-content: center; border-radius: 8px;">{el['simbolo']}</div>
            <div>
                <b style='color:#ffffff; font-size:1.1rem;'>{el['nombre']}</b><br>
                <b>Electronegatividad:</b> {el['electneg']} | <b>Impacto Fisiológico:</b> {el['bio']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.caption("Modifica los protones: Al construir H(1), C(6), N(7), O(8), Na(11), Mg(12), P(15), S(16), Cl(17) o Ca(20) emergerá su rol clínico.")
    st.markdown("</div>", unsafe_allow_html=True)
