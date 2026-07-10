import streamlit as st
import pandas as pd
import database as db
from assets import cargar_estilos

# --- CONFIGURACIÓN E INICIALIZACIÓN ---
st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
cargar_estilos()
db.inicializar_db()

# Inicialización de estado si no existe
if 'auth' not in st.session_state: st.session_state['auth'] = None
if 'token_actual' not in st.session_state: st.session_state['token_actual'] = None
if 'puntos_acumulados' not in st.session_state: st.session_state['puntos_acumulados'] = 0
if 'vidas' not in st.session_state: st.session_state['vidas'] = 3
if 'errores_quiz' not in st.session_state: st.session_state['errores_quiz'] = 0
if 'advertencia_ph' not in st.session_state: st.session_state['advertencia_ph'] = False
if 'memo_reveladas' not in st.session_state: st.session_state['memo_reveladas'] = []
if 'memo_resueltas' not in st.session_state: st.session_state['memo_resueltas'] = []
if 'memo_tablero' not in st.session_state: st.session_state['memo_tablero'] = [] # Debes inicializar esto con los pares
if 'racha_consecutiva' not in st.session_state: st.session_state['racha_consecutiva'] = 0
if 'licencia_extendida' not in st.session_state: st.session_state['licencia_extendida'] = False

pass_maestra_actual = db.obtener_password_admin()

st.markdown("<h1 class='main-title'>Main<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)

# --- PANEL ADMINISTRADOR ---
def panel_administrador():
    st.subheader("🔑 Consola de Gestión")
    tab_gen, tab_mon, tab_seg, tab_diag = st.tabs(["🆕 Tokens", "📊 Monitor", "⚙️ Seguridad", "🩺 Diagnóstico"])
    
    with tab_gen:
        vigencia = st.number_input("Días de vigencia:", min_value=1, value=30)
        if st.button("Emitir Token"):
            st.code(f"TOKEN: {db.generar_token(vigencia)}", language="text")
            
    with tab_mon:
        datos = db.listar_todos_los_tokens()
        if datos:
            st.dataframe(pd.DataFrame(datos))
            token_sel = st.selectbox("Token:", [d['token'] for d in datos])
            if st.button("🔓 Forzar Cierre"): 
                db.forzar_liberacion_sesion(token_sel)
                st.rerun()
        else: st.info("Base vacía.")
            
    with tab_seg:
        nueva_pass = st.text_input("Nueva Clave Maestra:", type="password")
        if st.button("Actualizar"): 
            db.actualizar_password_admin(nueva_pass)
            st.success("Guardado.")
            
    with tab_diag:
        if st.button("Ejecutar Auditoría"):
            rep = db.verificar_salud_sistema()
            st.success(rep["status"])
            for d in rep["detalles"]: st.write(f"- {d}")
            if st.button("🛠️ Reparar"): 
                st.success(db.limpiar_inconsistencias_db()); st.rerun()

# --- LÓGICA DE ACCESO CON IMPORTACIÓN DIFERIDA ---
entrada = st.text_input("Ingresa Token o Clave Maestra:", type="password")

if st.button("🚀 ACCEDER AL LABORATORIO"):
    if entrada == pass_maestra_actual:
        st.session_state['auth'] = 'admin'
        st.rerun()
    else:
        es_valido, msg = db.validar_token(entrada)
        if es_valido:
            st.session_state['auth'] = 'usuario'
            st.session_state['token_actual'] = entrada
            st.rerun()
        else:
            st.error("Credencial inválida.")

# --- NAVEGACIÓN ---
if st.session_state['auth'] == 'admin':
    panel_administrador()
elif st.session_state['auth'] == 'usuario':
    # Importación solo cuando el usuario está autenticado
    from modulos.m1_dia1 import mostrar_dia1
    from modulos.m1_dia2 import mostrar_dia2
    from modulos.m1_dia3 import mostrar_dia3
    from modulos.m1_dia4 import mostrar_dia4
    
    estacion = st.radio("Cronograma:", ["Día 1", "Día 2", "Día 3", "Día 4"], horizontal=True)
    if "Día 1" in estacion: mostrar_dia1()
    elif "Día 2" in estacion: mostrar_dia2()
    elif "Día 3" in estacion: mostrar_dia3()
    else: mostrar_dia4()
