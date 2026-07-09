# === ARCHIVO COMPLETO: app.py ===
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
        st.code(f"Código conflictivo:\n{e.text}")
    st.stop()

# Configuración estructural de Streamlit
st.set_page_config(page_title="MainLab Pro - Entorno Químico", layout="wide", page_icon="🔬")
inicializar_db()
cargar_estilos()

# Inicialización segura de st.session_state
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'token_actual' not in st.session_state: st.session_state['token_actual'] = None
if 'identificador_usuario' not in st.session_state: st.session_state['identificador_usuario'] = ""
if 'modulo_actual' not in st.session_state: st.session_state['modulo_actual'] = 1
if 'puntos_acumulados' not in st.session_state: st.session_state['puntos_acumulados'] = 0
if 'vidas' not in st.session_state: st.session_state['vidas'] = 3
if 'errores_quiz' not in st.session_state: st.session_state['errores_quiz'] = 0
if 'modo_acceso_index' not in st.session_state: st.session_state['modo_acceso_index'] = 0
if 'admin_auth' not in st.session_state: st.session_state['admin_auth'] = False

# Título de Infraestructura Centralizada Original e Inmutable
st.markdown("<h1 class='main-title'>🔬 MainLab Academic</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#8a99ad; margin-bottom:30px;'>Bioquímica aplicada. Ciencia interactiva. Sin límites.</p>", unsafe_allow_html=True)

# Configuración de navegación lateral reactiva
modo_acceso = st.sidebar.radio(
    "Navegación del Entorno:",
    options=["🎓 Portal del Estudiante", "💻 Consola del Administrador"],
    index=st.session_state['modo_acceso_index']
)

# Sincronizar el estado del radio por si el usuario hace clic directamente
if modo_acceso == "🎓 Portal del Estudiante":
    st.session_state['modo_acceso_index'] = 0
else:
    st.session_state['modo_acceso_index'] = 1

# ==========================================
# INTERFAZ 1: PORTAL DEL ESTUDIANTE
# ==========================================
if modo_acceso == "🎓 Portal del Estudiante":
    if not st.session_state['auth']:
        st.markdown("<div class='lab-panel'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#ffffff; margin-top:0; text-align:center;'>🔑 Control de Acceso Cuántico</h3>", unsafe_allow_html=True)
        
        token_input = st.text_input("Introduce tu Token de Acceso o Clave Maestra:", type="password", placeholder="SYNAPSIS-PRO-XXXX")
        password_maestra = obtener_password_admin()
        
        if st.button("Validar Credenciales en Red", use_container_width=True):
            if token_input == "":
                st.warning("Por favor, ingrese un token válido.")
            elif token_input == password_maestra:
                st.success("🔓 ¡ACCESO DE ADMINISTRADOR AUTENTICADO!")
                st.session_state['admin_auth'] = True
                st.session_state['modo_acceso_index'] = 1  # Forzar redirección limpia a consola
                st.rerun()
            else:
                es_valido, usuario, modulo, pts, vds = validar_token(token_input)
                if es_valido:
                    st.session_state['auth'] = True
                    st.session_state['token_actual'] = token_input
                    st.session_state['identificador_usuario'] = usuario
                    st.session_state['modulo_actual'] = modulo
                    st.session_state['puntos_acumulados'] = pts
                    st.session_state['vidas'] = vds
                    st.success(f"🔬 Conexión establecida. Bienvenido, Operador {usuario}.")
                    st.rerun()
                else:
                    st.error("🚨 Token inválido, revocado o en uso en otra sesión.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    # Barra lateral informativa del Alumno
    with st.sidebar:
        st.markdown("### 👨‍🔬 Operador Activo")
        st.write(f"**Usuario:** `{st.session_state['identificador_usuario']}`")
        st.write(f"**Token:** `{st.session_state['token_actual']}`")
        st.metric("Puntuación Acumulada", f"{st.session_state['puntos_acumulados']} PTS")
        st.markdown(f"**Estabilidad:** `💔 {st.session_state['vidas']} / 3`")
        st.markdown("---")
        if st.button("🚪 Cerrar Sesión Segura", use_container_width=True):
            if st.session_state['token_actual']:
                liberar_token(st.session_state['token_actual'])
            st.session_state.clear()
            st.rerun()

    # Procesar lógica de vidas agotadas
    if st.session_state['vidas'] <= 0:
        st.error("🚨 COLAPSO METABÓLICO: Lisis celular detectada por acumulación de fallos.")
        if st.button("Reiniciar Entorno Fisiológico"):
            st.session_state['vidas'] = 3
            st.rerun()
    else:
        if st.session_state['modulo_actual'] == 1:
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
        else:
            mostrar_modulo2()

# ==========================================
# INTERFAZ 2: CONSOLA DEL ADMINISTRADOR
# ==========================================
else:
    st.markdown("<h2 style='color:#00e5ff; margin-top:0;'>💻 Panel de Control de Infraestructura</h2>", unsafe_allow_html=True)
    pass_maestra = obtener_password_admin()
    
    # Control estricto de accesos aislados
    if not st.session_state['admin_auth']:
        input_pass = st.text_input("Contraseña del Sistema:", type="password")
        if st.button("Desbloquear Consola"):
            if input_pass == pass_maestra:
                st.session_state['admin_auth'] = True
                st.rerun()
            else:
                st.error("Acceso denegado. Credenciales incorrectas.")
        st.stop()

    # Pestañas de administración de base de datos
    tab1, tab2, tab3 = st.tabs(["🎫 Emisión de Cupones", "📊 Monitor de Sesiones", "⚙️ Seguridad"])
    
    with tab1:
        st.markdown("### Generador de Licencias Únicas")
        c1, c2 = st.columns(2)
        with c1:
            u_id = st.text_input("Identificador / Matrícula del Alumno:", placeholder="JuanPerez_2026")
            dias_val = st.slider("Días de vigencia del Token:", 1, 90, 30)
        with c2:
            st.write("")
            st.write("")
            if st.button("Fabricar Token Autorizado", use_container_width=True):
                if u_id:
                    nuevo_tok = generar_token(dias_val, u_id)
                    st.success(f"Token Creado: `{nuevo_tok}` asignado a {u_id}")
                else:
                    st.warning("Introduzca un identificador.")
                    
    with tab2:
        st.markdown("### Estado de la Capa de Persistencia (SQLite)")
        tokens_db = listar_todos_los_tokens()
        if tokens_db:
            df = pd.DataFrame(tokens_db, columns=["Token de Acceso", "Estado de Sesión", "Vigencia Remanente", "Puntos", "Vidas", "Progreso Actual"])
            st.dataframe(df, use_container_width=True)
            
            st.markdown("### Acciones Quirúrgicas de Rescate")
            c_tok = st.selectbox("Seleccionar Token Objetivo:", df["Token de Acceso"].tolist())
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("Forzar Liberación de Sesión (Anti-Bloqueo)", use_container_width=True):
                    forzar_liberacion_sesion(c_tok)
                    st.success("Sesión restaurada a estado Libre.")
                    st.rerun()
            with col_b2:
                if st.button("Revocar y Eliminar Token del Registro", use_container_width=True):
                    revocar_eliminar_token(c_tok)
                    st.error("Token eliminado.")
                    st.rerun()
        else:
            st.info("No hay tokens registrados en la base de datos.")
            
    with tab3:
        st.markdown("### Configuración de Seguridad Global")
        nueva_pass = st.text_input("Actualizar Contraseña Maestra de Administrador:", type="password", placeholder="Mínimo 6 caracteres")
        if st.button("Sobrescribir Credencial"):
            if len(nueva_pass) >= 4:
                actualizar_password_admin(nueva_pass)
                st.success("Contraseña del sistema actualizada con éxito.")
            else:
                st.error("Contraseña demasiado corta.")
                
    if st.sidebar.button("🚪 Salir de Consola", use_container_width=True):
        st.session_state.clear()
        st.rerun()import streamlit as st
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
