import streamlit as st
import pandas as pd
import database as db  # Referenciamos a tu archivo como 'db'
from assets import cargar_estilos

# 1. Configuración de página y estilos
st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
cargar_estilos()

# 2. Inicialización de base de datos
db.inicializar_db()

# 3. Carga de módulos protegida (evita que un módulo roto detenga toda la App)
try:
    from modulos.m1_dia1 import mostrar_dia1
    from modulos.m1_dia2 import mostrar_dia2
    from modulos.m1_dia3 import mostrar_dia3
    from modulos.m1_dia4 import mostrar_dia4
except Exception as e:
    st.error(f"Error al cargar los módulos: {e}")

# --- PANEL ADMINISTRADOR (Función aislada) ---
def panel_administrador():
    st.subheader("🔑 Consola de Gestión")
    t1, t2, t3, t4 = st.tabs(["🆕 Tokens", "📊 Monitor", "⚙️ Seguridad", "🩺 Diagnóstico"])
    
    with t1:
        vigencia = st.number_input("Días de vigencia:", min_value=1, value=30)
        if st.button("Emitir Token"): st.code(db.generar_token(vigencia))
    with t2:
        datos = db.listar_todos_los_tokens()
        if datos:
            df = pd.DataFrame(datos, columns=["Token", "Uso", "Exp", "Puntos", "Vidas", "Mod", "Intents", "Tiempo", "Err"])
            st.dataframe(df)
            token_sel = st.selectbox("Seleccionar Token", [d[0] for d in datos])
            if st.button("🔓 Forzar Cierre"): db.forzar_liberacion_sesion(token_sel); st.rerun()
    with t3:
        nueva_pass = st.text_input("Nueva Clave:", type="password")
        if st.button("Actualizar Clave"): db.actualizar_password_admin(nueva_pass); st.success("Guardado")
    with t4:
        if st.button("Ejecutar Auditoría"):
            rep = db.verificar_salud_sistema()
            st.write(rep["status"])
            for d in rep["detalles"]: st.write(f"- {d}")
        if st.button("🛠️ Limpiar Base de Datos"):
            st.success(db.limpiar_inconsistencias_db())
            st.rerun()

# --- FLUJO PRINCIPAL ---
st.markdown("<h1 class='main-title'>Main<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)

entrada = st.text_input("Ingresa Token o Clave Maestra:", type="password")

if entrada:
    # Lógica de Administrador
    if entrada == db.obtener_password_admin():
        panel_administrador() # Llamada directa sin st.write
    else:
        # Lógica de Estudiante
        es_valido, _ = db.validar_token(entrada)
        if es_valido:
            # Guardamos el token en session_state para que los módulos puedan usarlo
            st.session_state["token_activo"] = entrada
            st.success("Acceso Estudiante Autorizado")
            
            estacion = st.radio("Día:", ["Día 1", "Día 2", "Día 3", "Día 4"], horizontal=True)
            if estacion == "Día 1": mostrar_dia1()
            elif estacion == "Día 2": mostrar_dia2()
            elif estacion == "Día 3": mostrar_dia3()
            else: mostrar_dia4()
        else:
            st.error("Credencial inválida.")
