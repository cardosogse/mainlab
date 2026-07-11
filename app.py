import streamlit as st
import pandas as pd
import time
import traceback
import database as db
from assets import cargar_estilos

st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬", initial_sidebar_state="expanded")
cargar_estilos()
db.inicializar_db()

class ControlEstadoGlobal:
    @staticmethod
    def asegurar_hidratacion():
        esquema_estados = {
            'auth': None, 'token_actual': None, 'procesando': False,
            'puntos_acumulados': 0, 'vidas': 3, 'tiempo_historico_min': 0,
            'tiempo_estudio_min': 0, 'inicio_sesion_unix': None, 'modulo_actual': "1",
            'ultimo_token_generado': None
        }
        for clave, valor_defecto in esquema_estados.items():
            if clave not in st.session_state:
                st.session_state[clave] = valor_defecto

ControlEstadoGlobal.asegurar_hidratacion()
pass_maestra = db.obtener_password_admin()

if st.session_state['auth'] is None and "token" in st.query_params:
    token_candidato = st.query_params["token"].strip()
    if token_candidato:
        valido, datos_payload = db.validar_token(token_candidato)
        if valido:
            st.session_state['auth'] = 'usuario'
            st.session_state['token_actual'] = token_candidato
            st.session_state['puntos_acumulados'] = datos_payload.get("puntos", 0)
            st.session_state['vidas'] = datos_payload.get("vidas", 3)
            st.session_state['tiempo_historico_min'] = datos_payload.get("tiempo", 0)
            st.session_state['inicio_sesion_unix'] = time.time()
            st.rerun()
        else:
            st.query_params.clear()
            st.rerun()

# El título principal se mantiene como bloque HTML aislado en la parte superior
st.markdown(
    '<div class="logo-container"><h1 class="main-title">Main<span class="main-title-suffix">Lab</span></h1>'
    '<p class="main-subtitle">Bioquímica aplicada. Ciencia interactiva. Sin límites.</p></div>', 
    unsafe_allow_html=True
)

# --- PANEL DE ACCESO PURIFICADO (100% COMPATIBLE CON MÓVILES) ---
if st.session_state['auth'] is None:
    
    # SECCIÓN A: Formulario de Entrada Estándar
    st.markdown("### 🔑 ACCESO AL LABORATORIO")
    
    credencial = st.text_input(
        "Introduce tu Licencia o Clave Maestra:", 
        type="password", 
        key="login_input_credencial",
        label_visibility="visible"
    )
    
    if st.button("🚀 INICIAR INVESTIGACIÓN", use_container_width=True, key="login_btn_acceder"):
        credencial_limpia = credencial.strip()
        if credencial_limpia == pass_maestra:
            st.session_state['auth'] = 'admin'
            st.rerun()
        else:
            es_valido, payload = db.validar_token(credencial_limpia)
            if es_valido:
                st.session_state['auth'] = 'usuario'
                st.session_state['token_actual'] = credencial_limpia
                st.session_state['puntos_acumulados'] = payload["puntos"]
                st.session_state['vidas'] = payload["vidas"]
                st.session_state['tiempo_historico_min'] = payload["tiempo"]
                st.session_state['inicio_sesion_unix'] = time.time()
                st.query_params["token"] = credencial_limpia
                st.rerun()
            else:
                st.error("❌ Credencial inválida o vencida.")
    
    # Separador estructural nativo
    st.markdown("---")
    
    # SECCIÓN B: Gancho Interactivo Abierto
    st.markdown("### 🔬 ANALIZADOR ORGÁNICO EXPRÉS")
    st.caption("Prueba el potencial del laboratorio interactivo antes de ingresar tu licencia clínica:")
    
    grupo_test = st.selectbox(
        "Selecciona un Grupo Funcional para analizar su comportamiento hídrico:",
        ["Metilo (-CH₃)", "Hidroxilo (-OH)", "Fosforilo (-PO₄²⁻)"],
        key="login_teaser_select"
    )
    
    if grupo_test == "Metilo (-CH₃)":
        st.error("❌ **Naturaleza Apolar (Hidrofóbico):** Enlaces covalentes simétricos. Repele activamente las redes de puentes de hidrógeno del agua.")
        st.latex(r"\Delta\chi \text{ entre C e H } = 0.35 \rightarrow \text{Apolar}")
    elif grupo_test == "Hidroxilo (-OH)":
        st.warning("⚠️ **Naturaleza Polar (Hidrofílico):** Alta densidad electrónica sobre el oxígeno. Forma dipolos estables con el solvente celular.")
        st.latex(r"\Delta\chi \text{ entre O e H } = 1.24 \rightarrow \text{Polar Dipolar}")
    else:
        st.success("⚡ **Naturaleza Iónica (Altamente Hidrofílico):** Carga neta negativa. Rompe la tensión superficial del agua mediante interacciones ion-dipolo extremas.")
        st.latex(r"\text{Carga Neta Exterior: } -2")

# --- CONSOLA DE ADMINISTRACIÓN ---
elif st.session_state['auth'] == 'admin':
    st.subheader("🔑 Consola de Control de Infraestructura")
    
    if st.button("🚪 Cerrar Sesión de Administrador", key="admin_btn_salir", type="primary"):
        st.session_state['auth'] = None
        st.session_state['token_actual'] = None
        st.session_state['ultimo_token_generado'] = None
        st.query_params.clear()
        st.rerun()
        
    st.markdown("---")
    
    opcion_admin = st.radio(
        "Selecciona la acción a realizar:",
        ["🆕 Crear Licencias", "📊 Monitorear Alumnos"],
        horizontal=True,
        key="admin_menu_selector"
    )
    
    st.markdown("---")

    if opcion_admin == "🆕 Crear Licencias":
        dias_vigencia = st.number_input("Días de vigencia activa:", min_value=1, value=30, key="admin_dias_input")
        if st.button("Generar Nueva Licencia", key="admin_btn_generar"):
            try:
                token_nuevo = db.generar_token(dias_vigencia)
                if token_nuevo: 
                    st.session_state['ultimo_token_generado'] = token_nuevo
                    st.success("🎉 ¡Licencia registrada de manera segura!")
                else:
                    st.error("Error: La función de base de datos devolvió un token vacío.")
            except Exception as ex:
                st.error(f"🚨 Error crítico al ejecutar la generación: {str(ex)}")
                st.text(traceback.format_exc())
                
        if st.session_state['ultimo_token_generado']:
            st.info("Copia el último token generado para el alumno:")
            st.code(st.session_state['ultimo_token_generado'], language="text")
            if st.button("🗑️ Limpiar Pantalla", key="admin_clear_token_view"):
                st.session_state['ultimo_token_generado'] = None
                st.rerun()
            
    elif opcion_admin == "📊 Monitorear Alumnos":
        try:
            tabla_datos = db.listar_todos_los_tokens()
            if tabla_datos:
                dataframe_tokens = pd.DataFrame(tabla_datos)
                st.dataframe(dataframe_tokens, use_container_width=True)
                
                st.markdown("---")
                token_a_eliminar = st.selectbox(
                    "Selecciona una licencia para su purga física:", 
                    dataframe_tokens["Token"].tolist(),
                    key="admin_select_revocar"
                )
                if st.button("❌ DESTRUIR LICENCIA DEFINITIVAMENTE", use_container_width=True, key="admin_btn_revocar"):
                    db.eliminar_token(token_a_eliminar)
                    if st.session_state['ultimo_token_generado'] == token_a_eliminar:
                        st.session_state['ultimo_token_generado'] = None
                    st.toast(f"Licencia {token_a_eliminar} revocada del servidor.", icon="🗑️")
                    time.sleep(0.3)
                    st.rerun()
            else:
                st.info("No existen licencias registradas en el clúster de datos.")
        except Exception as ex:
            st.error(f"🚨 Error crítico en el monitoreo: {str(ex)}")
            st.text(traceback.format_exc())

# --- VISTA DEL ALUMNO ---
elif st.session_state['auth'] == 'usuario':
    minutos_de_sesion = int((time.time() - st.session_state['inicio_sesion_unix']) / 60)
    st.session_state['tiempo_estudio_min'] = st.session_state['tiempo_historico_min'] + minutes_de_sesion
    
    st.markdown("<div class='dashboard-triage'>", unsafe_allow_html=True)
    c_tk, c_vd, c_pt, c_tm = st.columns(4)
    c_tk.metric("🔬 Licencia Activa", st.session_state['token_actual'])
    c_vd.metric("❤️ Vitalidad Clínica", f"{st.session_state['vidas']} / 3")
    c_pt.metric("🏆 Puntos de Score", f"{st.session_state['puntos_acumulados']} pts")
    c_tm.metric("⏱️ Tiempo Acumulado", f"{st.session_state['tiempo_estudio_min']} min")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.session_state['vidas'] <= 0:
        st.error("🚨 **ACCESO SUSPENDIDO:** El alumno ha agotado su vitalidad metabólica. Contacta al docente.")
    else:
        from modulos.modulo1 import app as enrutador_modulo1
        enrutador_modulo1()
