import streamlit as st
import pandas as pd
import database as db
from assets import cargar_estilos
from modulos.m1_dia1 import mostrar_dia1
from modulos.m1_dia2 import mostrar_dia2
from modulos.m1_dia3 import mostrar_dia3
from modulos.m1_dia4 import mostrar_dia4

st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
cargar_estilos()
db.inicializar_db()

# --- PANEL ADMINISTRADOR ---
def panel_administrador():
    st.subheader("🔑 Consola de Gestión")
    t1, t2, t3, t4 = st.tabs(["🆕 Tokens", "📊 Monitor", "⚙️ Seguridad", "🩺 Diagnóstico"])
    with t1:
        vig = st.number_input("Días de vigencia:", 1, 90, 30)
        if st.button("Emitir Token"): st.code(db.generar_token(vig))
    with t2:
        datos = db.listar_todos_los_tokens()
        if datos:
            st.dataframe(pd.DataFrame(datos, columns=["Token", "Uso", "Exp", "Puntos", "Vidas", "Mod", "Int", "Tiempo", "Err"]))
            t_sel = st.selectbox("Token:", [d[0] for d in datos])
            c1, c2 = st.columns(2)
            if c1.button("🚫 Eliminar"): db.eliminar_token(t_sel); st.rerun()
            if c2.button("🔓 Liberar"): db.liberar_token(t_sel); st.rerun()
    with t3:
        n_p = st.text_input("Nueva Clave:", type="password")
        if st.button("Actualizar"): db.actualizar_password_admin(n_p); st.success("Guardado")
    with t4:
        if st.button("Auditoría"):
            r = db.verificar_salud_sistema()
            for d in r["detalles"]: st.write(f"- {d}")
        if st.button("🛠️ Reparar"): st.success(db.limpiar_inconsistencias_db()); st.rerun()

# --- FLUJO PRINCIPAL ---
st.markdown("<h1 class='main-title'>MainLab</h1>", unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state['auth'] = None

entrada = st.text_input("Ingresa Token o Clave:", type="password", placeholder="🔑 ...")

if st.button("🚀 ACCEDER AL LABORATORIO"):
    if entrada == db.obtener_password_admin():
        st.session_state['auth'] = 'admin'
        st.rerun()
    elif db.validar_token(entrada)[0]:
        st.session_state['auth'] = entrada
        st.rerun()
    else:
        st.error("Credencial inválida")

if st.session_state['auth'] == 'admin':
    panel_administrador()
elif st.session_state['auth']:
    estacion = st.radio("Día:", ["Día 1", "Día 2", "Día 3", "Día 4"], horizontal=True)
    if estacion == "Día 1": mostrar_dia1()
    elif estacion == "Día 2": mostrar_dia2()
    elif estacion == "Día 3": mostrar_dia3()
    else: mostrar_dia4()
