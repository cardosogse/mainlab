import streamlit as st
import pandas as pd
import database as db
from assets import cargar_estilos

# Inicialización
st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
cargar_estilos()
db.inicializar_db()

st.markdown("<h1 class='main-title'>Main<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)

# Entrada Única
entrada = st.text_input("Ingresa Token o Clave Maestra:", type="password")

if entrada:
    if entrada == db.obtener_password_admin():
        st.subheader("🔑 Consola de Gestión")
        t1, t2, t3, t4 = st.tabs(["🆕 Tokens", "📊 Monitor", "⚙️ Seguridad", "🩺 Diagnóstico"])
        
        with t1:
            if st.button("Emitir Token"): st.code(db.generar_token(30))
        with t2:
            datos = db.listar_todos_los_tokens()
            if datos: st.dataframe(pd.DataFrame(datos))
            if st.button("🔓 Liberar Todo"): db.limpiar_inconsistencias_db(); st.rerun()
        with t3:
            nueva = st.text_input("Nueva Clave:", type="password")
            if st.button("Guardar"): db.actualizar_password_admin(nueva)
        with t4:
            if st.button("Ejecutar Auditoría Completa"):
                rep = db.verificar_salud_sistema()
                if "Estable" in rep["status"]: st.success(rep["status"])
                else: st.error(rep["status"])
                for d in rep["detalles"]: st.write(f"- {d}")
                if "Alerta" in rep["status"]:
                    if st.button("🛠️ Limpiar"): st.success(db.limpiar_inconsistencias_db()); st.rerun()
    else:
        valido, msg = db.validar_token(entrada)
        if valido:
            st.success("Acceso Estudiante")
            # Carga tus módulos aquí
        else:
            st.error("Credencial incorrecta.")
