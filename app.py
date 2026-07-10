import streamlit as st
import pandas as pd
import database as db

# --- CONFIGURACIÓN E IMPORTACIONES ---
st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
db.inicializar_db()

# --- FUNCIONES DE INTERFAZ ---

def panel_administrador():
    st.subheader("🔑 Consola de Gestión")
    # Definición limpia de tabs
    tab_gen, tab_mon, tab_seg, tab_diag = st.tabs(["🆕 Tokens", "📊 Monitor", "⚙️ Seguridad", "🩺 Diagnóstico"])
    
    with tab_gen:
        vigencia = st.number_input("Días de vigencia:", min_value=1, value=30)
        if st.button("Emitir Token"):
            token = db.generar_token(vigencia)
            st.code(f"TOKEN: {token}", language="text")
            
    with tab_mon:
        datos = db.listar_todos_los_tokens()
        if datos:
            df = pd.DataFrame(datos, columns=["Token", "Activo", "Exp", "Puntos", "Vidas", "Mod", "Intents", "Tiempo", "Err"])
            st.dataframe(df, use_container_width=True)
            token_sel = st.selectbox("Selecciona un Token:", [d[0] for d in datos])
            if st.button("🔓 Forzar Cierre"): 
                db.forzar_liberacion_sesion(token_sel)
                st.rerun()
        else: 
            st.info("No hay tokens registrados.")
            
    with tab_seg:
        nueva_pass = st.text_input("Nueva Clave Maestra:", type="password")
        if st.button("Actualizar Clave"): 
            db.actualizar_password_admin(nueva_pass)
            st.success("Configuración guardada.")
            
    with tab_diag:
        st.write("Estado del Sistema:")
        if st.button("Ejecutar Auditoría Completa"):
            reporte = db.verificar_salud_sistema()
            # Mostramos el estado con semáforo
            if "Estable" in reporte["status"]:
                st.success(reporte["status"])
            else:
                st.error(reporte["status"])
            
            # Mostramos detalles
            for d in reporte["detalles"]:
                st.write(f"- {d}")
                
            # Si hay errores, habilitamos el botón de reparación
            if "Alerta" in reporte["status"] or "CRÍTICO" in reporte["status"]:
                if st.button("🛠️ Limpiar Inconsistencias"):
                    st.success(db.limpiar_inconsistencias_db())
                    st.rerun()

# --- FLUJO PRINCIPAL ---
st.markdown("<h1 class='main-title'>Main<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)

# Entrada única
entrada = st.text_input("Ingresa Token o Clave Maestra:", type="password")

if entrada:
    # Verificamos si es administrador
    if entrada == db.obtener_password_admin():
        panel_administrador()
    # Verificamos si es estudiante
    else:
        es_valido, msg = db.validar_token(entrada)
        if es_valido:
            # Importación dinámica para evitar errores de carga inicial
            from modulos.m1_dia1 import mostrar_dia1
            from modulos.m1_dia2 import mostrar_dia2
            from modulos.m1_dia3 import mostrar_dia3
            from modulos.m1_dia4 import mostrar_dia4
            
            st.success("Acceso concedido.")
            estacion = st.radio("Cronograma:", ["Día 1", "Día 2", "Día 3", "Día 4"], horizontal=True)
            if "Día 1" in estacion: mostrar_dia1()
            elif "Día 2" in estacion: mostrar_dia2()
            elif "Día 3" in estacion: mostrar_dia3()
            else: mostrar_dia4()
        else:
            st.error("Credencial inválida.")
