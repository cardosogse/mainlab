import streamlit as st
import pandas as pd
import database as db
from assets import cargar_estilos, mezclar_memorama

st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
cargar_estilos()
db.inicializar_db()

# 1. Configuración de Estado Base
if 'auth' not in st.session_state: st.session_state['auth'] = None

pass_maestra_actual = db.obtener_password_admin()
st.markdown("<h1 class='main-title'>Main<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)

# 2. Funciones de Interfaz
def inicializar_variables_usuario(token):
    st.session_state['token_actual'] = token
    st.session_state['puntos_acumulados'] = 0
    st.session_state['vidas'] = 3
    st.session_state['errores_quiz'] = 0
    st.session_state['advertencia_ph'] = False
    st.session_state['memo_reveladas'] = []
    st.session_state['memo_resueltas'] = []
    st.session_state['racha_consecutiva'] = 0
    st.session_state['licencia_extendida'] = False
    st.session_state['memo_completado'] = False
    if 'memo_tablero' not in st.session_state or not st.session_state['memo_tablero']:
        st.session_state['memo_tablero'] = mezclar_memorama()

def panel_administrador():
    st.subheader("🔑 Consola de Gestión")
    t_gen, t_mon = st.tabs(["🆕 Tokens", "📊 Monitor"])
    with t_gen:
        vigencia = st.number_input("Días de vigencia:", min_value=1, value=30)
        if st.button("Emitir Token"): st.code(f"TOKEN: {db.generar_token(vigencia)}")
    with t_mon:
        datos = db.listar_todos_los_tokens()
        if datos:
            st.dataframe(pd.DataFrame(datos))
            token_sel = st.selectbox("Token a forzar cierre:", [d[0] for d in datos])
            if st.button("🔓 Forzar Cierre"): 
                db.forzar_liberacion_sesion(token_sel)
                st.rerun()

# 3. Flujo Principal
if not st.session_state['auth']:
    entrada = st.text_input("Ingresa Token o Clave Maestra:", type="password")
    if st.button("🚀 ACCEDER AL LABORATORIO"):
        if entrada == pass_maestra_actual:
            st.session_state['auth'] = 'admin'
            st.rerun()
        else:
            es_valido, msg = db.validar_token(entrada)
            if es_valido:
                st.session_state['auth'] = 'usuario'
                inicializar_variables_usuario(entrada)
                st.rerun()
            else:
                st.error("Credencial inválida.")

# 4. Navegación (Carga Diferida Estricta)
if st.session_state['auth'] == 'admin':
    panel_administrador()
elif st.session_state['auth'] == 'usuario':
    # Importamos LOS MÓDULOS AQUÍ. Cero riesgo de ImportErrors al arrancar.
    from modulos.m1_dia1 import mostrar_dia1
    from modulos.m1_dia2 import mostrar_dia2
    from modulos.m1_dia3 import mostrar_dia3
    from modulos.m1_dia4 import mostrar_dia4
    
    # Barra de Vidas superior
    st.markdown(f"**Vidas Restantes:** {'❤️' * st.session_state['vidas']}")
    
    estacion = st.radio("Cronograma:", ["Día 1", "Día 2", "Día 3", "Día 4"], horizontal=True)
    if "Día 1" in estacion: mostrar_dia1()
    elif "Día 2" in estacion: mostrar_dia2()
    elif "Día 3" in estacion: mostrar_dia3()
    else: mostrar_dia4()
