import streamlit as st
import pandas as pd

# --- IMPORTACIÓN ROBUSTA ---
try:
    from database import (
        inicializar_db, validar_token, liberar_token, obtener_datos_usuario,
        generar_token, listar_todos_los_tokens, revocar_eliminar_token, 
        forzar_liberacion_sesion, obtener_password_admin, actualizar_password_admin
    )
    from assets import cargar_estilos, mezclar_memorama
    from modulos.m1_dia1 import mostrar_dia1
    from modulos.m1_dia2 import mostrar_dia2
    from modulos.m1_dia3 import mostrar_dia3
    from modulos.m1_dia4 import mostrar_dia4
    from modulos.modulo2 import mostrar_modulo2
except ImportError as e:
    st.error(f"Error de conexión con base de datos: {e}")
    st.stop()

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
cargar_estilos()
inicializar_db()
pass_maestra_actual = obtener_password_admin()
st.markdown("<h1 class='main-title'>Main<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Bioquímica aplicada. Ciencia interactiva. Sin límites.</p>", unsafe_allow_html=True)
st.sidebar.title("🛠️ Consola del Sistema")
modo_acceso = st.sidebar.radio("Selecciona tu Terminal:", ["Portal del Estudiante", "Consola del Administrador"])
if "auth" not in st.session_state: st.session_state["auth"] = False
if "token_actual" not in st.session_state: st.session_state["token_actual"] = ""
if "vidas" not in st.session_state: st.session_state["vidas"] = 3
if "puntos_acumulados" not in st.session_state: st.session_state["puntos_acumulados"] = 0
if "memo_completado" not in st.session_state: st.session_state["memo_completado"] = False
if "memo_tablero" not in st.session_state: st.session_state["memo_tablero"] = mezclar_memorama()
if modo_acceso == "Consola del Administrador":
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.subheader("🔑 Autenticación de Seguridad del Administrador")
    clave_admin = st.text_input("Introduce la Clave Maestra de Infraestructura:", type="password")
    if clave_admin == pass_maestra_actual:
        st.success("Acceso verificado a los servicios centrales de SQLite.")
        tab_generar, tab_control, tab_seguridad = st.tabs(["🆕 Generar Nuevos Tokens", "📊 Monitor de Alumnos", "⚙️ Seguridad"])
        with tab_generar:
            vigencia = st.number_input("Días de vigencia del token:", min_value=1, max_value=365, value=30)
            if st.button("Emitir Cupón de Acceso"):
                nuevo_tok = generar_token(vigencia)
                st.code(f"TOKEN EMITIDO: {nuevo_tok}", language="text")
        with tab_control:
            datos_raw = listar_todos_los_tokens()
            if datos_raw:
                df = pd.DataFrame(datos_raw, columns=["Token", "Activo", "Días Restantes", "Puntos", "Vidas", "Módulo Máx"])
                st.dataframe(df, use_container_width=True, hide_index=True)
                token_seleccionado = st.selectbox("Selecciona un Token para Operar:", df["Token"].tolist())
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔓 Forzar Cierre"):
                        forzar_liberacion_sesion(token_seleccionado)
                        st.rerun()
                with col2:
    if st.button("🚨 Revocar Licencia", key="btn_revocar"):
        # Llamada directa y verificada
        revocar_eliminar_token(token_seleccionado)
        st.warning(f"Token {token_seleccionado} revocado.")
        # Forzar recarga inmediata de los datos
        st.rerun()
        with tab_seguridad:
            nueva_pass = st.text_input("Nueva Contraseña:", type="password")
            if st.button("Guardar Cambios"):
                actualizar_password_admin(nueva_pass)
                st.success("Actualizado.")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    if not st.session_state["auth"]:
        st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
        token_input = st.text_input("Introduce tu Token:", type="password")
        if st.button("Conectar"):
            if token_input.strip() == pass_maestra_actual:
                st.info("Redirigiendo a Consola...")
            else:
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
            if st.button("🚪 Cerrar Sesión"):
                liberar_token(st.session_state['token_actual'])
                st.session_state.clear()
                st.rerun()
        if st.session_state['vidas'] <= 0:
            st.error("🚨 COLAPSO METABÓLICO.")
        else:
            estacion = st.radio("Cronograma:", ["Día 1", "Día 2", "Día 3", "Día 4"], horizontal=True)
            if "Día 1" in estacion: mostrar_dia1()
            elif "Día 2" in estacion: mostrar_dia2()
            elif "Día 3" in estacion: mostrar_dia3()
            else: mostrar_dia4()
