import streamlit as st
import pandas as pd
import database as db

# # --- CONFIGURACIÓN E IMPORTACIONES ---
try:
    from database import (
        inicializar_db, validar_token, liberar_token, obtener_datos_usuario,
        generar_token, listar_todos_los_tokens, eliminar_token, 
        forzar_liberacion_sesion, obtener_password_admin, actualizar_password_admin,
        sincronizar_progreso_db, otorgar_tiempo_extra_db, verificar_salud_sistema, limpiar_inconsistencias_db
    )
    from assets import cargar_estilos, mezclar_memorama
    from modulos.m1_dia1 import mostrar_dia1
    from modulos.m1_dia2 import mostrar_dia2
    from modulos.m1_dia3 import mostrar_dia3
    from modulos.m1_dia4 import mostrar_dia4
    from modulos.modulo2 import mostrar_modulo2
except ImportError as e:
    st.error(f"Error crítico de configuración: {e}")
    st.stop()

# # --- INICIALIZACIÓN ---
st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
cargar_estilos()
inicializar_db()
pass_maestra_actual = obtener_password_admin()

st.markdown("<h1 class='main-title'>Main<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Bioquímica aplicada. Ciencia interactiva. Sin límites.</p>", unsafe_allow_html=True)

# # --- ESTADOS DE SESIÓN ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if "token_actual" not in st.session_state: st.session_state["token_actual"] = ""
if "vidas" not in st.session_state: st.session_state["vidas"] = 3
if "puntos_acumulados" not in st.session_state: st.session_state["puntos_acumulados"] = 0
if "memo_completado" not in st.session_state: st.session_state["memo_completado"] = False
if "memo_tablero" not in st.session_state: st.session_state["memo_tablero"] = mezclar_memorama()

# # --- CONSOLA DEL ADMINISTRADOR ---
def panel_administrador():
    st.sidebar.title("⚙️ Consola Admin")
    tab_gen, tab_mon, tab_seg, tab_diag = st.tabs(["🆕 Tokens", "📊 Monitor", "⚙️ Seguridad", "🩺 Diagnóstico Absoluto"])
    
    with tab_gen:
        vigencia = st.number_input("Días de vigencia del token:", min_value=1, max_value=365, value=30)
        if st.button("Emitir Cupón de Acceso"):
            nuevo_tok = generar_token(vigencia)
            st.code(f"TOKEN EMITIDO: {nuevo_tok}", language="text")
    
    with tab_mon:
        datos_raw = listar_todos_los_tokens()
        if datos_raw:
            df = pd.DataFrame(datos_raw, columns=["Token", "Activo", "Exp", "Puntos", "Vidas", "Mod", "Intents", "Tiempo", "Err"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            token_sel = st.selectbox("Selecciona Token:", df["Token"].tolist())
            if st.button("🔓 Forzar Cierre"): forzar_liberacion_sesion(token_sel); st.rerun()
        else: st.info("Base de datos vacía.")

    with tab_seguridad:
        nueva_pass = st.text_input("Nueva Contraseña:", type="password")
        if st.button("Guardar Cambios"): actualizar_password_admin(nueva_pass); st.success("Actualizado.")

    with tab_diag:
        st.subheader("Auditoría de Sistema")
        if st.button("Ejecutar Auditoría Profunda"):
            reporte = verificar_salud_sistema()
            if "Estable" in reporte["status"]: st.success(reporte["status"])
            else: st.error(reporte["status"])
            for detalle in reporte["detalles"]: st.write(f"- {detalle}")
            if "Alerta" in reporte["status"]:
                if st.button("🛠️ Limpiar Inconsistencias Ahora"):
                    st.success(limpiar_inconsistencias_db())
                    st.rerun()

# # --- PORTAL DEL ESTUDIANTE ---
def portal_estudiante():
    if not st.session_state["auth"]:
        st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
        token_input = st.text_input("Introduce tu Token:", type="password")
        if st.button("Conectar"):
            es_valido, mensaje = validar_token(token_input)
            if es_valido:
                datos = obtener_datos_usuario(token_input.strip().upper())
                st.session_state["auth"] = True
                st.session_state['token_actual'] = token_input.strip().upper()
                st.session_state['puntos_acumulados'] = datos[0]
                st.session_state['vidas'] = datos[1]
                st.rerun()
            else: st.error(f"Fallo: {mensaje}")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        with st.sidebar:
            if st.button("🚪 Cerrar Sesión"): liberar_token(st.session_state['token_actual']); st.session_state.clear(); st.rerun()
        if st.session_state['vidas'] <= 0: st.error("🚨 COLAPSO METABÓLICO.")
        else:
            estacion = st.radio("Cronograma:", ["Día 1", "Día 2", "Día 3", "Día 4"], horizontal=True)
            if "Día 1" in estacion: mostrar_dia1()
            elif "Día 2" in estacion: mostrar_dia2()
            elif "Día 3" in estacion: mostrar_dia3()
            else: mostrar_dia4()

# # --- FLUJO PRINCIPAL ---
modo_acceso = st.sidebar.radio("Selecciona tu Terminal:", ["Portal del Estudiante", "Consola del Administrador"])
if modo_acceso == "Consola del Administrador":
    clave = st.sidebar.text_input("Clave Maestra:", type="password")
    if clave == pass_maestra_actual: panel_administrador()
    else: st.warning("Autenticación necesaria.")
else: portal_estudiante()
