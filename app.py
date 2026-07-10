import streamlit as st
import database as db
from assets import cargar_estilos

# 1. Configuración
st.set_page_config(page_title="MainLab", layout="wide")
cargar_estilos()
db.inicializar_db()

# 2. Carga protegida
try:
    from modulos.m1_dia1 import mostrar_dia1
    from modulos.m1_dia2 import mostrar_dia2
    from modulos.m1_dia3 import mostrar_dia3
    from modulos.m1_dia4 import mostrar_dia4
except:
    st.error("Error cargando módulos")

# 3. Flujo Lógico
st.markdown("<h1 class='main-title'>MainLab</h1>", unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state['auth'] = None

entrada = st.text_input("Ingresa tu credencial:", type="password")

if st.button("Acceder al Laboratorio"):
    if entrada == db.obtener_password_admin():
        st.session_state['auth'] = 'admin'
        st.rerun()
    elif db.validar_token(entrada)[0]:
        st.session_state['auth'] = entrada
        st.rerun()
    else:
        st.error("Credencial incorrecta")

# 4. Renderizado
if st.session_state['auth'] == 'admin':
    st.subheader("🔑 Consola de Gestión")
    # Auditoría que incluye Supabase
    if st.button("Ejecutar Auditoría Completa"):
        rep = db.verificar_salud_sistema()
        for d in rep["detalles"]: st.write(f"- {d}")
elif st.session_state['auth']:
    estacion = st.radio("Día:", ["Día 1", "Día 2", "Día 3", "Día 4"], horizontal=True)
    if estacion == "Día 1": mostrar_dia1()
    elif estacion == "Día 2": mostrar_dia2()
    elif estacion == "Día 3": mostrar_dia3()
    else: mostrar_dia4()
