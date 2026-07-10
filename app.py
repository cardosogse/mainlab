import streamlit as st
import pandas as pd
import database as db
from assets import cargar_estilos

# 1. Carga de módulos con manejo de errores
try:
    from modulos.m1_dia1 import mostrar_dia1
    from modulos.m1_dia2 import mostrar_dia2
    from modulos.m1_dia3 import mostrar_dia3
    from modulos.m1_dia4 import mostrar_dia4
except ImportError as e:
    st.error(f"Error cargando módulos: {e}")
    st.stop()

# 2. Configuración e inicialización
st.set_page_config(page_title="MainLab", layout="wide")
cargar_estilos()
db.inicializar_db()

# 3. Interfaz
st.markdown("<h1 class='main-title'>MainLab</h1>", unsafe_allow_html=True)
entrada = st.text_input("Ingresa credencial:", type="password")

if entrada:
    if entrada == db.obtener_password_admin():
        st.subheader("🔑 Consola de Gestión")
        t1, t2, t3 = st.tabs(["🆕 Tokens", "📊 Monitor", "🩺 Diagnóstico"])
        with t1:
            if st.button("Emitir Token"): st.code(db.generar_token(30))
        with t2:
            st.dataframe(pd.DataFrame(db.listar_todos_los_tokens(), columns=["Token", "Uso", "Exp", "Puntos", "Vidas", "Mod"]))
        with t3:
            if st.button("Ejecutar Auditoría"):
                rep = db.verificar_salud_sistema()
                for d in rep["detalles"]: st.write(f"- {d}")
    else:
        es_valido, _ = db.validar_token(entrada)
        if es_valido:
            st.success("Acceso Autorizado")
            estacion = st.radio("Día:", ["Día 1", "Día 2", "Día 3", "Día 4"], horizontal=True)
            if estacion == "Día 1": mostrar_dia1()
            elif estacion == "Día 2": mostrar_dia2()
            elif estacion == "Día 3": mostrar_dia3()
            else: mostrar_dia4()
        else:
            st.error("Credencial incorrecta.")
