import streamlit as st
import time
import database as db
from assets import obtener_svg_atomo

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
            st.info("El plasma mantiene una fase uniforme debido a que las proteínas plasmáticas permanecen dispersas sin precipitar.")
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
            st.info("Rutherford (1911): El átomo concentra su masa positiva en un núcleo central diminuto.")
        elif "Bohr" in modelo:
            st.info("Bohr (1913): Órbitas circulares cuantizadas. Introduce niveles fijos de energía.")
        else:
            st.info("Schrödinger (1926): Orbitales de densidad probabilística 3D.")
            
    with col_svg:
        st.components.v1.html(f"<div style='display:flex; justify-content:center; align-items:center; width:100%; height:110px; background-color:rgba(255,255,255,0.02); border-radius:8px;'>{obtener_svg_atomo(modelo)}</div>", height=120, scrolling=False)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🧠 Desafío de Consolidación: Memorama Atómico")
    
    if len(st.session_state["memo_reveladas"]) == 2:
        st.warning("🧩 Tienes dos tarjetas volteadas en el laboratorio. Revisa sus contenidos y presiona el botón para evaluar afinidad.")
        
        if st.button("🔍 COMPROBAR PAREJA ELEMENTAL", use_container_width=True):
            idx1, idx2 = st.session_state["memo_reveladas"]
            _, id_par1 = st.session_state["memo_tablero"][idx1]
            _, id_par2 = st.session_state["memo_tablero"][idx2]
            
            if id_par1 == id_par2:
                if id_par1 not in st.session_state["memo_resueltas"]:
                    st.session_state["memo_resueltas"].append(id_par1)
                    st.session_state["racha_consecutiva"] += 1
                    puntos_ganados = 100
                    
                    if st.session_state["racha_consecutiva"] >= 2 and not st.session_state["licencia_extendida"]:
                        puntos_ganados += 300
                        st.session_state["licencia_extendida"] = True
                        db.otorgar_tiempo_extra_db(st.session_state["token_actual"], dias_adicionales=7)
                        st.toast("🚀 ¡RACHA CUÁNTICA! +7 días de licencia.", icon="🎁")
                        
                    st.session_state["puntos_acumulados"] += puntos_ganados
                    
                    db.sincronizar_progreso_db(
                        st.session_state["token_actual"], 
                        st.session_state["puntos_acumulados"], 
                        "1", 
                        st.session_state["vidas"],
                        st.session_state["tiempo_estudio_seg"]
                    )
                st.toast("⚡ ¡Afinidad molecular correcta!", icon="✅")
            else:
                st.session_state["racha_consecutiva"] = 0
                st.toast("❌ Las tarjetas no interactúan. Inténtalo de nuevo.", icon="⚠️")
            
            st.session_state["memo_reveladas"] = []
            st.rerun()

    cols_memo = st.columns(5)
    for i in range(10):
        col_idx = i % 5
        with cols_memo[col_idx]:
            val_tarjeta, id_par = st.session_state["memo_tablero"][i]
            
            if id_par in st.session_state["memo_resueltas"]:
                st.button(f"✅ {val_tarjeta}", key=f"btn_res_{i}", disabled=True, use_container_width=True)
            elif i in st.session_state["memo_reveladas"]:
                st.button(f"👀 {val_tarjeta}", key=f"btn_rev_{i}", disabled=True, use_container_width=True)
            else:
                bloqueo_clic = len(st.session_state["memo_reveladas"]) >= 2
                if st.button("⚛️", key=f"btn_act_{i}", use_container_width=True, disabled=bloqueo_clic):
                    st.session_state["memo_reveladas"].append(i)
                    st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
