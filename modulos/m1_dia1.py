import streamlit as st
import time
from database import sincronizar_progreso_db, otorgar_tiempo_extra_db
from assets import obtener_svg_atomo, mezclar_memorama

def mostrar_dia1():
    st.subheader("Día 1: Niveles de Organización y Separación de Fases")
    st.write("La bioquímica es una ciencia aplicada; los procesos generados in vitro constituyen las bases del diagnóstico clínico.")
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🔬 Simulador de Centrifugación Macromolecular")
    muestra = st.selectbox("Selecciona la Muestra de Fluido:", ["Plasma Sanguíneo", "Sangre Entera (Muestra anticoagulada)"])
    
    if st.button("Ejecutar Fuerzas G (Centrifugar)"):
        progreso = st.progress(0)
        for i in range(100):
            time.sleep(0.005)
            progreso.progress(i + 1)
            
        if muestra == "Plasma Sanguíneo":
            st.success("🔬 Diagnóstico: Mezcla Homogénea (Solución Coloidal)")
            st.info("El plasma mantiene una phase uniforme debido a que las proteínas plasmáticas permanecen dispersas sin precipitar.")
        else:
            st.warning("🩸 Diagnóstico: Mezcla Heterogénea en Suspensión")
            st.info("La fuerza centrífuga precipita los elementos celulares densos al fondo, dejando el plasma libre en la superficie.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🗛️ Deslizador de Teorías Cuánticas y Modelos Atómicos")
    
    modelo = st.select_slider(
        "Navegación Cronológica:",
        options=["Dalton (1810)", "Thomson (1897)", "Rutherford (1911)", "Bohr (1913)", "Schrödinger (1926)"]
    )
    
    col_txt, col_svg = st.columns([3, 1])
    with col_txt:
        if "Dalton" in modelo:
            st.info("Dalton (1810): Esfera sólida sin cargas. Explica las proporciones estequiométricas elementales.")
        elif "Thomson" in modelo:
            st.info("Thomson (1897): Descubre el electrón. Introduce la naturaleza eléctrica de la materia.")
        elif "Rutherford" in modelo:
            st.info("Rutherford (1911): El átomo concentra su masa positiva en un núcleo central diminuto, estando mayormente vacío.")
        elif "Bohr" in modelo:
            st.info("Bohr (1913): Órbitas circulares cuantizadas. Introduce niveles fijos de energía periférica.")
        else:
            st.info("Schrödinger (1926): Orbitales de densidad probabilística 3D que dictan las geometrías tridimensionales moleculares.")
            
    with col_svg:
        st.components.v1.html(f"<div style='display:flex; justify-content:center; align-items:center; width:100%; height:110px; background-color:rgba(255,255,255,0.02); border-radius:8px;'>{obtener_svg_atomo(modelo)}</div>", height=120, scrolling=False)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🧠 Desafío de Consolidación: Memorama Atómico")
    
    if len(st.session_state["memo_reveladas"]) == 2:
        idx1, idx2 = st.session_state["memo_reveladas"]
        val1, id_par1 = st.session_state["memo_tablero"][idx1]
        val2, id_par2 = st.session_state["memo_tablero"][idx2]
        
        if id_par1 == id_par2:
            if id_par1 not in st.session_state["memo_resueltas"]:
                st.session_state["memo_resueltas"].append(id_par1)
                if not st.session_state["memo_completado"]:
                    st.session_state["racha_consecutiva"] += 1
                    puntos_ganados = 100
                    if st.session_state["racha_consecutiva"] >= 2 and not st.session_state["licencia_extendida"]:
                        puntos_ganados += 300
                        st.session_state["licencia_extendida"] = True
                        otorgar_tiempo_extra_db(st.session_state["token_actual"], dias=7)
                        st.toast("🚀 ¡RACHA CUÁNTICA! +7 días de licencia extra.", icon="🎁")
                    st.session_state["puntos_acumulados"] += puntos_ganados
                    sincronizar_progreso_db(st.session_state["token_actual"], st.session_state["puntos_acumulados"], 1)
            st.toast("⚡ ¡Afinidad molecular correcta!", icon="✅")
        else:
            st.session_state["racha_consecutiva"] = 0
            st.toast("❌ No interactúan.", icon="⚠️")
        st.session_state["memo_reveladas"] = []

    if len(st.session_state["memo_resueltas"]) == 5 and not st.session_state["memo_completado"]:
        st.session_state["memo_completado"] = True
        sincronizar_progreso_db(st.session_state["token_actual"], st.session_state["puntos_acumulados"], 1)

    cols_memo = st.columns(5)
    for i in range(10):
        col_idx = i % 5
        with cols_memo[col_idx]:
            val_tarjeta, id_par = st.session_state["memo_tablero"][i]
            if id_par in st.session_state["memo_resueltas"]:
                st.button(f"✅ {val_tarjeta}", key=f"btn_m1_d1_res_{i}", disabled=True, use_container_width=True)
            elif i in st.session_state["memo_reveladas"]:
                st.button(f"👀 {val_tarjeta}", key=f"btn_m1_d1_rev_{i}", disabled=True, use_container_width=True)
            else:
                if st.button("⚛️ Revelar", key=f"btn_m1_d1_act_{i}", use_container_width=True):
                    st.session_state["memo_reveladas"].append(i)
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    c_reset, _ = st.columns([1, 3])
    with c_reset:
        if st.button("🔄 Reiniciar Memorama", use_container_width=True):
            st.session_state["memo_tablero"] = mezclar_memorama()
            st.session_state["memo_reveladas"] = []
            st.session_state["memo_resueltas"] = []
            if not st.session_state["memo_completado"]:
                st.session_state["racha_consecutiva"] = 0
            st.rerun()

    if st.session_state["memo_completado"]:
        st.markdown(f"<div class='card-success'>🏆 <b>¡Afinidad Atómica Consolidada!</b> Marcador: <b>{st.session_state['puntos_acumulados']} PTS</b>.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
