import streamlit as st
import pandas as pd
import database as db

# --- CONFIGURACIÓN E IMPORTACIONES ---
# Asegúrate de tener los módulos en la carpeta 'modulos/'
try:
    from database import (
        inicializar_db, validar_token, liberar_token, obtener_datos_usuario,
        generar_token, listar_todos_los_tokens, eliminar_token, 
        forzar_liberacion_sesion, obtener_password_admin, actualizar_password_admin,
        sincronizar_progreso_db, verificar_salud_sistema, limpiar_inconsistencias_db
    )
    from assets import cargar_estilos, mezclar_memorama
    from modulos.m1_dia1 import mostrar_dia1
    from modulos.m1_dia2 import mostrar_dia2
    from modulos.m1_dia3 import mostrar_dia3
    from modulos.m1_dia4 import mostrar_dia4
except ImportError as e:
    st.error(f"Error crítico en la carga de módulos: {e}")
    st.stop()

# --- INICIALIZACIÓN ---
st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
cargar_estilos()
inicializar_db()
pass_maestra_actual = obtener_password_admin()

st.markdown("<h1 class='main-title'>Main<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)

# --- PANEL ADMINISTRADOR ---
def panel_administrador():
    st.subheader("🔑 Consola de Gestión")
    # Definición limpia de todos los tabs necesarios
    tab_gen, tab_mon, tab_seg, tab_diag = st.tabs(["🆕 Tokens", "📊 Monitor", "⚙️ Seguridad", "🩺 Diagnóstico"])
    
    with tab_gen:
        vigencia = st.number_input("Días de vigencia:", min_value=1, value=30)
        if st.button("Emitir Token"):
            st.code(f"TOKEN: {generar_token(vigencia)}", language="text")
            
    with tab_mon:
        datos = listar_todos_los_tokens()
        if datos:
            st.dataframe(pd.DataFrame(datos, columns=["Token", "Activo", "Exp", "Puntos", "Vidas", "Mod", "Intents", "Tiempo", "Err"]))
            token_sel = st.selectbox("Token:", [d[0] for d in datos])
            if st.button("🔓 Forzar Cierre"): forzar_liberacion_sesion(token_sel); st.rerun()
        else: st.info("Base vacía.")
            
    with tab_seg:
        nueva_pass = st.text_input("Nueva Clave Maestra:", type="password")
        if st.button("Actualizar"): actualizar_password_admin(nueva_pass); st.success("Guardado.")
            
    with tab_diag:
        if st.button("Ejecutar Auditoría"):
            rep = verificar_salud_sistema()
            st.success(rep["status"]) if "Estable" in rep["status"] else st.error(rep["status"])
            for d in rep["detalles"]: st.write(f"- {d}")
            if "Alerta" in rep["status"]:
                if st.button("🛠️ Reparar"): st.success(limpiar_inconsistencias_db()); st.rerun()

# --- LÓGICA DE ACCESO ---
entrada = st.text_input("Ingresa Token o Clave Maestra:", type="password")

if entrada:
    if entrada == pass_maestra_actual:
        panel_administrador()
    else:
        es_valido, msg = validar_token(entrada)
        if es_valido:
            if "auth" not in st.session_state: st.session_state["auth"] = True
            st.success("Acceso concedido.")
            estacion = st.radio("Cronograma:", ["Día 1", "Día 2", "Día 3", "Día 4"], horizontal=True)
            if "Día 1" in estacion: mostrar_dia1()
            elif "Día 2" in estacion: mostrar_dia2()
            elif "Día 3" in estacion: mostrar_dia3()
            else: mostrar_dia4()
        else:
            st.error("Credencial inválida.")
