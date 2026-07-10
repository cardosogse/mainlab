import streamlit as st
import pandas as pd
import database as db  # Usamos alias para evitar conflictos
from assets import cargar_estilos, mezclar_memorama
from modulos.m1_dia1 import mostrar_dia1
from modulos.m1_dia2 import mostrar_dia2
from modulos.m1_dia3 import mostrar_dia3
from modulos.m1_dia4 import mostrar_dia4

# --- CONFIGURACIÓN E INICIALIZACIÓN ---
st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
cargar_estilos()
db.inicializar_db()

# Obtenemos la clave maestra desde la base de datos
pass_maestra_actual = db.obtener_password_admin()

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
            st.dataframe(pd.DataFrame(datos, columns=["Token", "Activo", "Exp", "Puntos", "Vidas", "Mod", "Intents", "Tiempo", "Err"]))
            token_sel = st.selectbox("Token:", [d[0] for d in datos])
            if st.button("🔓 Forzar Cierre"): 
                db.forzar_liberacion_sesion(token_sel)
                st.rerun()
        else: 
            st.info("Base vacía.")
            
    with tab_seg:
        nueva_pass = st.text_input("Nueva Clave Maestra:", type="password")
        if st.button("Actualizar"): 
            db.actualizar_password_admin(nueva_pass)
            st.success("Guardado.")
            
    with tab_diag:
        if st.button("Ejecutar Auditoría"):
            rep = db.verificar_salud_sistema()
            if "Estable" in rep["status"]: st.success(rep["status"])
            else: st.error(rep["status"])
            for d in rep["detalles"]: st.write(f"- {d}")
            if "Alerta" in rep["status"]:
                if st.button("🛠️ Reparar"): 
                    st.success(db.limpiar_inconsistencias_db())
                    st.rerun()

# --- FLUJO PRINCIPAL ---
st.markdown("<h1 class='main-title'>Main<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)

entrada = st.text_input("Ingresa Token o Clave Maestra:", type="password")

if entrada:
    # Si la clave coincide, EJECUTAMOS la función, NO imprimimos el objeto
    if entrada == pass_maestra_actual:
        panel_administrador() 
    else:
        # Lógica de estudiante
        es_valido, msg = db.validar_token(entrada)
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
