import streamlit as st
import pandas as pd
import database as db

# --- CONFIGURACIÓN E IMPORTACIONES ---
st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
db.inicializar_db()
db.verificar_salud_sistema() # Auditoría silenciosa al iniciar

# --- FUNCIONES DE INTERFAZ ---
def panel_administrador():
    st.subheader("🔑 Consola de Gestión de Infraestructura")
    tab_gen, tab_mon, tab_seg, tab_diag = st.tabs(["🆕 Tokens", "📊 Monitor", "⚙️ Seguridad", "🩺 Diagnóstico"])
    
    with tab_gen:
        vigencia = st.number_input("Días de vigencia del token:", min_value=1, value=30)
        if st.button("Emitir Cupón de Acceso"):
            nuevo_tok = db.generar_token(vigencia)
            st.code(f"TOKEN EMITIDO: {nuevo_tok}", language="text")
            
    with tab_mon:
        datos_raw = db.listar_todos_los_tokens()
        if datos_raw:
            df = pd.DataFrame(datos_raw, columns=["Token", "Activo", "Exp", "Puntos", "Vidas", "Mod", "Intents", "Tiempo", "Err"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            token_sel = st.selectbox("Selecciona Token para gestión:", df["Token"].tolist())
            if st.button("🔓 Forzar Cierre de Sesión"):
                db.forzar_liberacion_sesion(token_sel)
                st.rerun()
        else:
            st.info("Base de datos vacía.")
            
    with tab_seg:
        nueva_pass = st.text_input("Nueva Contraseña Maestra:", type="password")
        if st.button("Actualizar Contraseña"):
            db.actualizar_password_admin(nueva_pass)
            st.success("Contraseña actualizada.")
            
    with tab_diag:
        st.subheader("Auditoría de Salud")
        if st.button("Ejecutar Auditoría Profunda"):
            reporte = db.verificar_salud_sistema()
            if "Estable" in reporte["status"]: st.success(reporte["status"])
            else: st.error(reporte["status"])
            for detalle in reporte["detalles"]: st.write(f"- {detalle}")
            
            if "Alerta" in reporte["status"]:
                if st.button("🛠️ Limpiar Inconsistencias"):
                    st.success(db.limpiar_inconsistencias_db())
                    st.rerun()

# --- FLUJO PRINCIPAL ---
st.markdown("<h1 class='main-title'>Main<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)

# Entrada única: El sistema detecta el rol automáticamente
entrada = st.text_input("Ingresa tu Token o Clave de Administrador:", type="password")

if entrada:
    # 1. Acceso Administrador
    if entrada == db.obtener_password_admin():
        panel_administrador()
    # 2. Acceso Estudiante
    else:
        es_valido, msg = db.validar_token(entrada)
        if es_valido:
            # Aquí va la carga de tus módulos pedagógicos
            from modulos.m1_dia1 import mostrar_dia1
            from modulos.m1_dia2 import mostrar_dia2
            from modulos.m1_dia3 import mostrar_dia3
            from modulos.m1_dia4 import mostrar_dia4
            
            st.success("Conexión establecida.")
            estacion = st.radio("Cronograma:", ["Día 1", "Día 2", "Día 3", "Día 4"], horizontal=True)
            if "Día 1" in estacion: mostrar_dia1()
            elif "Día 2" in estacion: mostrar_dia2()
            elif "Día 3" in estacion: mostrar_dia3()
            else: mostrar_dia4()
        else:
            st.error("Credencial no reconocida.")
