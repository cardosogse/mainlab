import streamlit as st
from modulos import m1_dia1, m1_dia2, m1_dia3, m1_dia4, m1_dia5, m1_dia6

def app():
    st.sidebar.subheader("🧬 U1: Agua y Equilibrio")
    menu = ["Día 1: Bioelementos", "Día 2: Enlaces", "Día 3: Estructura del Agua", "Día 4: Solubilidad", "Día 5: pH", "Día 6: Fluidoterapia"]
    eleccion = st.sidebar.radio("Selecciona:", menu)
    if eleccion == "Día 1: Bioelementos": m1_dia1.app()
    elif eleccion == "Día 2: Enlaces": m1_dia2.app()
    elif eleccion == "Día 3: Estructura del Agua": m1_dia3.app()
    elif eleccion == "Día 4: Solubilidad": m1_dia4.app()
    elif eleccion == "Día 5: pH": m1_dia5.app()
    elif eleccion == "Día 6: Fluidoterapia": m1_dia6.app()
