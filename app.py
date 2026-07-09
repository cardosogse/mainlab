import streamlit as st
import pandas as pd

try:
    from database import (
        inicializar_db, validar_token, liberar_token, obtener_datos_usuario,
        generar_token, listar_todos_los_tokens, revocar_eliminar_token, forzar_liberacion_sesion,
        obtener_password_admin, actualizar_password_admin
    )
    from assets import cargar_estilos, mezclar_memorama
    from modulos.m1_dia1 import mostrar_dia1
    from modulos.m1_dia2 import mostrar_dia2
    from modulos.m1_dia3 import mostrar_dia3
    from modulos.m1_dia4 import mostrar_dia4
    from modulos.modulo2 import mostrar_modulo2

except Exception as e:
    st.set_page_config(page_title="MainLab - Diagnóstico", layout="wide", page_icon="🚨")
    st.error("🚨 MONITOR DE CONTROL: ERROR DE COMPILACIÓN DETECTADO EN LOS MÓDULOS")
    st.markdown("---")
    st.markdown(f"**Tipo de Fallo detectado:** `{type(e).__name__}`")
    if hasattr(e, 'filename') and e.filename:
        st.error(f"📁 **Archivo roto real:** `{e.filename}`")
    if hasattr(e, 'lineno') and e.lineno:
        st.warning(f"🔢 **Línea exacta del conflicto:** Renglón `{e.lineno}`")
    if hasattr(e, 'text') and e.text:
        st.code(f"Código conflictivo: {e.text}", language="python")
    st.exception(e)
    st.stop()

st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
cargar_estilos()
inicializar_db()

# Recuperar dinámicamente la contraseña maestra actual desde SQLite
pass_maestra_actual = obtener_password_admin()

st.markdown("<h1 class='main-title'>Main<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Bioquímica aplicada. Ciencia interactiva. Sin límites.</p>", unsafe_allow_html=True)

st.sidebar.title("🛠️ Consola del Sistema")
modo_acceso = st.sidebar.radio("Selecciona tu Terminal:", ["Portal del Estudiante", "Consola del Administrador"])

if "auth" not in st.session_state: st.session_state["auth"] = False
if "token_actual" not in st.session_state: st.session_state["token_actual"] = ""
if "vidas" not in st.session_state: st.session_state["vidas"] = 3
if "errores_quiz" not in st.session_state: st.session_state["errores_quiz"] = 0
if "advertencia_ph" not in st.session_state: st.session_state["advertencia_ph"] = False
if "puntos_acumulados" not in st.session_state: st.session_state["puntos_acumulados"] = 0
if "racha_consecutiva" not in st.session_state: st.session_state["racha_consecutiva"] = 0
if "licencia_extendida" not in st.session_state: st.session_state["licencia_extendida"] = False
if "memo_reveladas" not in st.session_state: st.session_state["memo_reveladas"] = []
if "memo_resueltas" not in st.session_state: st.session_state["memo_resueltas"] = []
if "memo_completado" not in st.session_state: st.session_state["memo_completado"] = False
if "memo_tablero" not in st.session_state: st.session_state["memo_tablero"] = mezclar_memorama()

# Forzar el desvío si se ingresa la clave de administrador como cupón en el portal estudiantil
if modo_acceso == "Consola del Administrador":
    st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
    st.subheader("🔑 Autenticación de Seguridad del Administrador")
    clave_admin = st.text_input("Introduce la Clave Maestra de Infraestructura:", type="password")
    
    if clave_admin == pass_maestra_actual:
        st.success("Acceso verificado a los servicios centrales de SQLite.")
        tab_generar, tab_control, tab_seguridad = st.tabs(["🆕 Generar Nuevos Tokens", "📊 Monitor de Alumnos en Tiempo Real", "⚙️ Seguridad de Infraestructura"])
        
        with tab_generar:
            vigencia = st.number_input("Días de vigencia del token:", min_value=1, max_value=365, value=30)
            if st.button("Emitir Cupón de Acceso"):
                nuevo_tok = generar_token(vigencia)
                st.code(f"TOKEN EMITIDO: {nuevo_tok}", language="text")
                st.toast(f"Token {nuevo_tok} inyectado con éxito.")
                
        with tab_control:
            datos_raw = listar_todos_los_tokens()
            if datos_raw:
                df = pd.DataFrame(datos_raw, columns=["Token", "Activo", "Días Restantes", "Puntos", "Vidas", "Módulo Máx"])
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                st.markdown("#### Operaciones Críticas sobre la Base de Datos")
                col_tok_sel, col_btn_lib, col_btn_del = st.columns([2, 1, 1])
                with col_tok_sel:
                    token_seleccionado = st.selectbox("Selecciona un Token para Operar:", df["Token"].tolist())
                with col_btn_lib:
                    if st.button("🔓 Forzar Cierre", use_container_width=True):
                        forzar_liberacion_sesion(token_seleccionado)
                        st.success("Sesión liberada.")
                        st.rerun()
                with col_btn_del:
                    if st.button("🚨 Revocar Licencia", use_container_width=True):
                        revocar_eliminar_token(token_seleccionado)
                        st.warning("Token destruido.")
                        st.rerun()
            else: st.info("Base de datos vacía.")
            
        with tab_seguridad:
            st.markdown("#### Actualizar Contraseña de Infraestructura")
            st.write("Cambiar esta credencial modificará el acceso a la Consola y la puerta de validación del Portal de Estudiantes.")
            nueva_pass = st.text_input("Nueva Contraseña del Administrador:", type="password")
            confirmar_pass = st.text_input("Confirmar Nueva Contraseña:", type="password")
            if st.button("Guardar Cambios en Base de Datos"):
                if nueva_pass.strip() == "":
                    st.error("La contraseña no puede estar vacía.")
                elif nueva_pass == confirmar_pass:
                    actualizar_password_admin(nueva_pass)
                    st.success("Contraseña actualizada con éxito en SQLite. Se requiere recargar la consola.")
                else:
                    st.error("Las contraseñas no coinciden.")
                    
    elif clave_admin != "": st.error("Clave incorrecta.")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # PUERTA TRASERA: Si el estado auth no está activo pero se digita la contraseña maestra, redirige de inmediato
    if not st.session_state["auth"]:
        st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
        st.subheader("🔒 Acceso a Estaciones de Trabajo")
        token_input = st.text_input("Introduce tu Token de Suscripción Autorizado:", type="password")
        
        if st.button("Conectar e Inicializar Simuladores", use_container_width=True):
            if token_input.strip() == pass_maestra_actual:
                st.warning("Código de Infraestructura detectado. Redirigiendo a Consola...")
                st.info("Por favor, selecciona 'Consola del Administrador' en la barra de herramientas lateral.")
            elif token_input.strip():
                es_valido, mensaje = validar_token(token_input)
                if es_valido:
                    datos = obtener_datos_usuario(token_input.strip().upper())
                    st.session_state["auth"] = True
                    st.session_state['token_actual'] = token_input.strip().upper()
                    st.session_state['puntos_acumulados'] = datos[0]
                    st.session_state['vidas'] = datos[1]
                    if datos[2] >= 2: st.session_state["memo_completado"] = True
                    st.rerun()
                else: st.error(f"Fallo de conexión: {mensaje}")
            else: st.warning("Digita un token.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        with st.sidebar:
            st.markdown(f"**Usuario:** `{st.session_state['token_actual']}`")
            st.markdown(f"**Marcador:** `🪙 {st.session_state['puntos_acumulados']} PTS`")
            st.markdown(f"**Estabilidad:** `💔 {st.session_state['vidas']} / 3`")
            if st.button("🚪 Cerrar Sesión Segura", use_container_width=True):
                liberar_token(st.session_state['token_actual'])
                st.session_state.clear()
                st.rerun()
        
        if st.session_state['vidas'] <= 0:
            st.error("🚨 COLAPSO METABÓLICO: Lisis celular detectada por acumulación de fallos.")
            if st.button("Reiniciar Entorno Fisiológico"):
                st.session_state['vidas'] = 3
                st.rerun()
        else:
            st.markdown("<h2 style='color:#ffffff; margin-top:0;'>Unidad 1: Fundamentos de Química Biológica</h2>", unsafe_allow_html=True)
            
            estacion_actual = st.radio(
                "Cronograma de Trabajo:",
                options=[
                    "📅 Estación: Día 1 (Fases y Modelos)",
                    "📅 Estación: Día 2 (Estructura y Bioelementos)",
                    "📅 Estación: Día 3 (Fusión e Interacciones)",
                    "📅 Estación: Día 4 (Homeostasis y pH)"
                ],
                horizontal=True,
                label_visibility="collapsed"
            )

            if "Día 1" in estacion_actual:
                mostrar_dia1()
            elif "Día 2" in estacion_actual:
                mostrar_dia2()
            elif "Día 3" in estacion_actual:
                mostrar_dia3()
            else:
                mostrar_dia4()
