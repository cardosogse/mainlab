import streamlit as st
import pandas as pd
import database as db
from assets import cargar_estilos

# Importar módulos de forma segura
try:
    from modulos.m1_dia1 import mostrar_dia1
    from modulos.m1_dia2 import mostrar_dia2
    from modulos.m1_dia3 import mostrar_dia3
    from modulos.m1_dia4 import mostrar_dia4
except Exception as e:
    st.error(f"Error cargando módulos: {e}")

# Configuración Inicial
st.set_page_config(page_title="MainLab", layout="wide")
cargar_estilos()
db.inicializar_db()

# --- FUNCIONES DE RENDERIZADO ---
def render_admin():
    st.subheader("🔑 Consola de Gestión")
    t1, t2, t3 = st.tabs(["🆕 Tokens", "📊 Monitor", "🩺 Diagnóstico"])
    with t1:
        if st.button("Emitir Token"): st.code(f"TOKEN: {db.generar_token(30)}")
    with t2:
        st.dataframe(pd.DataFrame(db.listar_todos_los_tokens()))
    with t3:
        if st.button("Ejecutar Auditoría"):
            rep = db.verificar_salud_sistema()
            st.write(rep["status"])
            for d in rep["detalles"]: st.write(f"- {d}")

def render_estudiante():
    st.success("Acceso Estudiante Autorizado")
    # Usamos un radio para seleccionar el módulo
    estacion = st.radio("Día:", ["Día 1", "Día 2", "Día 3", "Día 4"], horizontal=True)
    if estacion == "Día 1": mostrar_dia1()
    elif estacion == "Día 2": mostrar_dia2()
    elif estacion == "Día 3": mostrar_dia3()
    else: mostrar_dia4()

# --- FLUJO PRINCIPAL ---
st.markdown("<h1 class='main-title'>MainLab</h1>", unsafe_allow_html=True)
entrada = st.text_input("Ingresa credencial:", type="password")

if entrada:
    if entrada == db.obtener_password_admin():
        render_admin()
    else:
        es_valido, _ = db.validar_token(entrada)
        if es_valido:
            render_estudiante()
        else:
            st.error("Credencial incorrecta.")
