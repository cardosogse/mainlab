import streamlit as st
import time
import database as db
from assets import obtener_svg_atomo

def mostrar_dia1():
    st.subheader("Día 1: Niveles de Organización y Separación de Fases")
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🔬 Simulador de Centrifugación Macromolecular")
    muestra = st.selectbox("Selecciona la Muestra:", ["Plasma Sanguíneo", "Sangre Entera"])
    if st.button("Ejecutar Fuerzas G"):
        progreso = st.progress(0)
        for i in range(100):
            time.sleep(0.005)
            progreso.progress(i + 1)
        if "Plasma" in muestra: st.success("Mezcla Homogénea (Coloidal)")
        else: st.warning("Mezcla Heterogénea en Suspensión")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.markdown("### 🧠 Desafío de Consolidación: Memorama Atómico")
    
    # Lógica de juego completamente saneada
    if len(st.session_state["memo_reveladas"]) == 2:
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
                    # Llamada segura a la DB
                    db.otorgar_tiempo_extra_db(st.session_state["token_actual"], 7)
                    st.toast("🚀 ¡RACHA CUÁNTICA! +7 días de licencia.", icon="🎁")
                
                st.session_state["puntos_acumulados"] += puntos_ganados
                db.sincronizar_progreso_db(st.session_state["token_actual"], st.session_state["puntos_acumulados"], "1")
            st.toast("⚡ ¡Afinidad correcta!", icon="✅")
        else:
            st.session_state["racha_consecutiva"] = 0
            st.toast("❌ No interactúan.", icon="⚠️")
        st.session_state["memo_reveladas"] = []

    cols_memo = st.columns(5)
    for i in range(10):
        with cols_memo[i % 5]:
            val_tarjeta, id_par = st.session_state["memo_tablero"][i]
            if id_par in st.session_state["memo_resueltas"]:
                st.button(f"✅ {val_tarjeta}", key=f"btn_res_{i}", disabled=True, use_container_width=True)
            elif i in st.session_state["memo_reveladas"]:
                st.button(f"👀 {val_tarjeta}", key=f"btn_rev_{i}", disabled=True, use_container_width=True)
            else:
                if st.button("⚛️", key=f"btn_act_{i}", use_container_width=True):
                    st.session_state["memo_reveladas"].append(i)
                    st.rerun()
