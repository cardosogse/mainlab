import streamlit as st
from assets import ELEMENTOS, generar_svg_enlace

def mostrar_dia3():
    st.subheader("Día 3: El Reactor de Fusión Atómica e Interacciones Moleculares")
    st.write("Estudia cómo la disparidad en la tracción de electrones determina la estabilidad de las uniones y la solvatación biológica celular.")
    
    escala_pauling = {"Oxígeno (O)": 3.44, "Hidrógeno (H)": 2.20, "Carbono (C)": 2.55, "Sodio (Na)": 0.93, "Cloro (Cl)": 3.16, "Nitrógeno (N)": 3.04}
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🧬 Reactor de Fusión de Enlaces")
    
    col1, col2 = st.columns(2)
    with col1:
        atomo_a = st.selectbox("Selecciona el Átomo Central (A):", list(escala_pauling.keys()), key="at_a")
        atomo_b = st.selectbox("Selecciona el Átomo de Reacción (B):", list(escala_pauling.keys()), key="at_b")
        fusionar = st.button("Colisionar Capas de Valencia")
        
    with col2:
        if fusionar:
            diff = abs(escala_pauling[atomo_a] - escala_pauling[atomo_b])
            st.metric("Diferencia de Electronegatividad (Δχ)", f"{diff:.2f}")
            
            sym_a = atomo_a.split(" ")[1].replace("(", "").replace(")", "")
            sym_b = atomo_b.split(" ")[1].replace("(", "").replace(")", "")
            color_a = ELEMENTOS.get(atomo_a, {"color": "#00e5ff"})["color"]
            color_b = ELEMENTOS.get(atomo_b, {"color": "#ff5252"})["color"]
            
            st.components.v1.html(generar_svg_enlace(sym_a, escala_pauling[atomo_a], color_a, sym_b, escala_pauling[atomo_b], color_b), height=140, scrolling=False)
            
            if diff < 0.4:
                st.success("🔬 Enlace Covalente No Polar (Apolar)")
                st.caption("*Lehninger* demuestra que esta simetría origina las fuerzas hidrofóbicas que estabilizan las bicapas lipídicas.")
            elif 0.4 <= diff <= 1.7:
                st.warning("🌊 Enlace Covalente Polar")
                st.caption("Dipolo permanente. Induce la alta constante dieléctrica del agua (78.5), rompiendo redes cristalinas salinas.")
            else:
                st.error("⚡ Enlace Iónico (Atracción Electrostática)")
                st.caption("Transferencia neta de electrones. Genera uniones que se disocian de inmediato en soluciones citoplasmáticas hídricas.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🧮 Calculadora de Concentración Molar")
    c1, c2 = st.columns(2)
    with c1:
        sample_mass = st.slider("Masa de Soluto (g de NaCl):", min_value=1.0, max_value=100.0, value=5.8)
        sample_vol = st.slider("Volumen (Litros de H2O):", min_value=0.1, max_value=5.0, value=1.0)
        
    peso_molecular_nacl = 58.44
    moles = sample_mass / peso_molecular_nacl
    molaridad = moles / sample_vol
    with c2:
        st.markdown("#### Parámetros Solubilidad")
        st.write(f"**Masa Molecular:** {peso_molecular_nacl} g/mol")
        st.metric("Molaridad Resultante (M):", f"{molaridad:.3f} mol/L")
    st.markdown("</div>", unsafe_allow_html=True)
