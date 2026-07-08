import streamlit as st
from modulos.m1_dia1 import mostrar_dia1
from modulos.m1_dia2 import mostrar_dia2
from modulos.m1_dia3 import mostrar_dia3
from modulos.m1_dia4 import mostrar_dia4

def mostrar_modulo1():
    st.markdown("<h2 style='color:#ffffff; margin-top:0;'>Unidad 1: Fundamentos de Química Biológica</h2>", unsafe_allow_html=True)
    
    estacion_actual = st.radio(
        "Cronograma de Trabajo:",
        options=[
            "📅 Estación: Día 1 (Fases y Modelos)",
            "📅 Estación: Día 2 (Estructura y Bioelementos)",
            "📅 Estación: Día 3 (Fusión e Interacciones)",
            "📅 Estación: Día 4 (Homeostasis y pH)"
        ],
        horizontal=True,
        label_visibility="collapsed"
    )

    if "Día 1" in estacion_actual:
        mostrar_dia1()
    elif "Día 2" in estacion_actual:
        mostrar_dia2()
    elif "Día 3" in estacion_actual:
        mostrar_dia3()
    else:
        mostrar_dia4()
