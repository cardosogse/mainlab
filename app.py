import streamlit as st
import database as db
from assets import cargar_estilos

# 1. Configuración
st.set_page_config(page_title="MainLab", layout="wide")
cargar_estilos()
db.inicializar_db()

# 2. Carga módulos
from modulos.m1_dia1 import mostrar_dia1
from modulos.m1_dia2 import mostrar_dia2
from modulos.m1_dia3 import mostrar_dia3
from modulos.m1_dia4 import mostrar_dia4

# 3. Flujo Lógico Central
st.markdown("<h1 class='main-title'>MainLab</h1>", unsafe_allow_html=True)

entrada = st.text_input("Introduce tu acceso (Token o Clave Admin):", type="password")

if st.button("Conectar"):
    # ESTRATEGIA DE SEGURIDAD: Validar primero Admin, luego Estudiante
    if entrada == db.obtener_password_admin():
        st.session_state['auth_admin'] = True
        st.rerun()
    elif db.validar_token(entrada):
        st.session_state['auth_user'] = entrada
        st.rerun()
    else:
        st.error("Credencial no reconocida.")

# Renderizado seguro
if st.session_state.get('auth_admin'):
    st.subheader("🔑 Consola de Gestión")
    # Restauración de los tabs que funcionaban
    t1, t2, t3 = st.tabs(["🆕 Tokens", "📊 Monitor", "🩺 Diagnóstico"])
    with t1:
        if st.button("Emitir Token"): st.code(db.generar_token(30))
    with t2:
        st.dataframe(db.listar_todos_los_tokens())
    with t3:
        if st.button("Ejecutar Auditoría Completa"):
            rep = db.verificar_salud_sistema()
            for d in rep["detalles"]: st.write(f"- {d}")
elif st.session_state.get('auth_user'):
    estacion = st.radio("Día:", ["Día 1", "Día 2", "Día 3", "Día 4"], horizontal=True)
    if estacion == "Día 1": mostrar_dia1()
    elif estacion == "Día 2": mostrar_dia2()
    elif estacion == "Día 3": mostrar_dia3()
    else: mostrar_dia4()
