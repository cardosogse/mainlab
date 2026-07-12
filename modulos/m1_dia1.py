import streamlit as st
import random
import database as db

def inicializar_estado_dia1():
    """Garantiza la hidratación segura de las variables analíticas en la sesión local."""
    if "d1_juego_score" not in st.session_state: 
        st.session_state.d1_juego_score = 0
    if "d1_juego_intentos" not in st.session_state: 
        st.session_state.d1_juego_intentos = 0
    if "d1_quiz_enviado" not in st.session_state: 
        st.session_state.d1_quiz_enviado = False
    if "d1_juego_actual_p" not in st.session_state:
        st.session_state.d1_juego_actual_p = random.choice([1, 6, 7, 8, 12, 15, 16, 17, 20])
        st.session_state.d1_juego_actual_e = st.session_state.d1_juego_actual_p + random.choice([-2, -1, 0, 1, 2])
    if "d1_retroalimentacion" not in st.session_state: 
        st.session_state.d1_retroalimentacion = None

def obtener_datos_elemento(protones: int):
    """
    Matriz analítica de bioelementos esenciales con relevancia fisiológica de alta jerarquía.
    Mapea el número atómico (Z) contra las tarjetas adaptativas profesionales.
    """
    tabla = {
        1: {
            "nombre": "Hidrógeno", "simbolo": "H", "base_neutrones": 0,
            "🐾 Veterinaria": "El ion $\\text{H}^+$ determina la escala de pH ruminal; desbalances fermentativos crónicos por dietas ricas en concentrados inducen acidosis ruminal aguda.",
            "🩺 Medicina": "La fluctuación de protones $\\text{H}^+$ en el plasma altera la afinidad de la hemoglobina por el oxígeno en los tejidos metabólicamente activos (Efecto Bohr).",
            "🧬 Biología": "El gradiente electroquímico transmembranal de protones $\\text{H}^+$ es la fuerza motriz que acopla el giro de la ATP sintasa mitocondrial."
        },
        6: {
            "nombre": "Carbono", "simbolo": "C", "base_neutrones": 6,
            "🐾 Veterinaria": "Estructura el esqueleto de los ácidos grasos volátiles (acetato, propionato, butirato), principal fuente energética en rumiantes.",
            "🩺 Medicina": "Es el eje de la química orgánica farmacéutica; sus enlaces covalentes estables permiten el diseño de anillos moleculares terapéuticos.",
            "🧬 Biología": "Su propiedad de tetravalencia le permite establecer cuatro enlaces simétricos interconectados, formando la columna de las macromoléculas."
        },
        7: {
            "nombre": "Nitrógeno", "simbolo": "N", "base_neutrones": 7,
            "🐾 Veterinaria": "Clave en el reciclaje de nitrógeno no proteico (urea) a través de la saliva hacia el rumen para la síntesis proteica bacteriana.",
            "🩺 Medicina": "Componente mandatorio del grupo amino; su acumulación plasmática en forma de amonio delata un fallo del ciclo de la urea hepático.",
            "🧬 Biología": "Presente en los anillos heterocíclicos de las bases nitrogenadas purinas y pirimidinas que codifican el código genético."
        },
        8: {
            "nombre": "Oxígeno", "simbolo": "O", "base_neutrones": 8,
            "🐾 Veterinaria": "Indispensable para el metabolismo tisular; aves comerciales seleccionadas genéticamente sufren de síndrome ascítico por alta demanda de $\\text{O}_2$.",
            "🩺 Medicina": "Aceptor final de electrones en la cadena respiratoria. Su privación induce hipoxia tisular y detiene la fosforilación oxidativa.",
            "🧬 Biología": "Su elevada electronegatividad genera la asimetría electrónica de carga parcial en los enlaces intramolares del agua."
        },
        12: {
            "nombre": "Magnesio", "simbolo": "Mg", "base_neutrones": 12,
            "🐾 Veterinaria": "La caída súbita de $\\text{Mg}^{2+}$ provoca 'tetania de los pastos' en bovinos, caracterizada por rigidez muscular e hiperexcitabilidad sináptica.",
            "🩺 Medicina": "Actúa como un antagonista fisiológico natural de los canales de calcio; estabiliza el potencial de acción celular miocárdico.",
            "🧬 Biología": "Cofactor obligatorio encargado de coordinar y estabilizar las cargas electrostáticas negativas de los grupos fosfato en el $\\text{ATP}$."
        },
        15: {
            "nombre": "Fósforo", "simbolo": "P", "base_neutrones": 16,
            "🐾 Veterinaria": "El desbalance crónico en la relación dietaria Calcio:Fósforo induce hiperparatiroidismo secundario nutricional (osteodistrofia fibrosa).",
            "🩺 Medicina": "Componente principal del sistema amortiguador intracelular y urinario, manteniendo el equilibrio ácido-base renal.",
            "🧬 Biología": "Enlazado covalentemente mediante uniones fosfodiéster de alta energía que estructuran el chasis del $\\text{ADN}$ y $\\text{ARN}$."
        },
        16: {
            "nombre": "Azufre", "simbolo": "S", "base_neutrones": 16,
            "🐾 Veterinaria": "Requerido por los microbios ruminales para la síntesis de aminoácidos azufrados, determinantes en la calidad estructural de la lana.",
            "🩺 Medicina": "Componente crítico de la coenzima A y de la matriz de glucosaminoglucanos que brindan elasticidad mecánica a los cartílagos.",
            "🧬 Biología": "Permite el plegamiento tridimensional de las proteínas mediante la oxidación y acoplamiento covalente de puentes disulfuro."
        },
        17: {
            "nombre": "Cloro", "simbolo": "Cl", "base_neutrones": 18,
            "🐾 Veterinaria": "El secuestro abomasal de fluidos por torsión gástrica desencadena una alcalosis metabólica hipoclorémica grave en rumiantes.",
            "🩺 Medicina": "Principal anión del líquido extracelular, crucial para el mantenimiento de la osmolaridad y la síntesis gástrica de $\\text{HCl}$.",
            "🧬 Biología": "Modula el potencial eléctrico postsináptico; su flujo transmembranal selectivo hiperpolariza la membrana plasmática neuronal."
        },
        20: {
            "nombre": "Calcio", "simbolo": "Ca", "base_neutrones": 20,
            "🐾 Veterinaria": "La demanda masiva de calcio al inicio de la lactación induce la paresia puerperal ('fiebre de leche') en vacas lecheras altamente productivas.",
            "🩺 Medicina": "Ion mensajero que se une a la troponina C para desplazar la tropomiosina y activar los puentes cruzados de actina-miosina en el corazón.",
            "🧬 Biología": "Segundo mensajero universal; su liberación desde el retículo endoplásmico activa cascadas de señalización intracelular efectoras."
        }
    }
    return tabla.get(protones, {"nombre": "Elemento Inestable", "simbolo": "X", "base_neutrones": protones, "🐾 Veterinaria": "Especie inestable.", "🩺 Medicina": "Especie inestable.", "🧬 Biología": "Especie inestable."})

def app():
    inicializar_estado_dia1()
    token_alumno = st.session_state.get("token_actual", "DEMO")
    
    # CAPA 2: Lectura directa y limpia del enfoque global del chasis raíz
    enfoque = st.session_state.get("enfoque_global", "🐾 Veterinaria")
    
    tab1, tab2, tab3 = st.tabs(["📚 Marco Teórico de Alta Jerarquía", "🔬 Espectrómetro Cuántico", "📝 Evaluación Formativa"])

    with tab1:
        st.markdown("## Fundamentos Químicos: Balance Iónico y Estructura Atómica")
        
        # --- LITERATURA DE ALTA JERARQUÍA REFERENCIADA ---
        st.markdown(
            r"""
            > **La Lógica Molecular de la Vida (Lehninger):** Los organismos vivos son sistemas termodinámicamente abiertos que 
            > operan en un estado estacionario dinámico. La homeostasis celular se mantiene mediante el intercambio metabólico 
            > controlado de electrones y la disociación selectiva de bioelementos en especies ionizadas activas.
            
            > **La Matriz Fisiológica (Harper):** Los bioelementos esenciales no se distribuyen en estado molecular neutro dentro de los 
            > compartimentos celulares. Existen disociados en forma de **iones** debido a la ganancia o pérdida selectiva de electrones 
            > de valencia, alterando la presión osmótica y los potenciales de membrana electroquímicos.
            """
        )
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown(
                "<div class='lab-panel' style='border-left: 4px solid #00f2fe;'>"
                "<h4 style='color:#00f2fe; margin-top:0;'>Catión (+)</h4>"
                "<p style='font-size:0.9rem; margin-bottom:0;'>Especie química que experimentó la <strong>pérdida de electrones</strong>. "
                "Predominan las cargas del núcleo.<br><em>Ejemplos:</em> $\\text{Na}^+$, $\\text{K}^+$, $\\text{Ca}^{2+}$.</p></div>", 
                unsafe_allow_html=True
            )
        with col_t2:
            st.markdown(
                "<div class='lab-panel' style='border-left: 4px solid #ff0844;'>"
                "<h4 style='color:#ff0844; margin-top:0;'>Anión (-)</h4>"
                "<p style='font-size:0.9rem; margin-bottom:0;'>Especie química que experimentó la <strong>ganancia de electrones</strong>. "
                "Carga electrónica externa predominante.<br><em>Ejemplos:</em> $\\text{Cl}^-$, $\\text{HCO}_3^-$.</p></div>", 
                unsafe_allow_html=True
            )

    with tab2:
        st.markdown("### 🔬 Simulador Atómico de Carga y Masa")
        
        # --- MARQUESINA DE INSTRUCCIONES CLARAS PARA EL ALUMNO ---
        st.markdown(
            """
            <div style='background-color:rgba(0,242,254,0.05); padding:12px; border-radius:8px; border:1px solid rgba(0,242,254,0.2); margin-bottom:15px;'>
            <strong>📋 MANUAL DE OPERACIÓN CIENTÍFICA:</strong><br>
            1. <strong>Identidad (Z):</strong> Ajusta los Protones para sintonizar el bioelementos de la tabla periódica.<br>
            2. <strong>Masa (A):</strong> Modifica los Neutrones para alterar el peso del núcleo (Estabilización de Isótopos).<br>
            3. <strong>Tonicidad:</strong> Sintoniza los Electrones para ionizar el átomo y activar su tarjeta clínica.
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        col_p, col_n, col_e = st.columns(3)
        protones = col_p.slider("🔴 Protones (Número Atómico Z):", min_value=1, max_value=20, value=11, key="d1_sl_p")
        neutrones = col_n.slider("🔘 Neutrones (Masa Nuclear N):", min_value=0, max_value=22, value=12, key="d1_sl_n")
        electrones = col_e.slider("🔵 Electrones (Orbitales e⁻):", min_value=1, max_value=20, value=10, key="d1_sl_e")

        # Cálculos cuánticos y de estabilidad
        carga_neta = protones - electrones
        numero_masa = protones + neutrones
        info_elemento = obtener_datos_elemento(protones)
        
        if carga_neta > 0:
            estado_ion = f"**Catión (+)** con carga de ${carga_neta:+}$"
            formula_visual = f"\\text{{{info_elemento['simbolo']}}}^{{{carga_neta}+}}"
        elif carga_neta < 0:
            estado_ion = f"**Anión (-)** con carga de ${carga_neta}$"
            formula_visual = f"\\text{{{info_elemento['simbolo']}}}^{{{abs(carga_neta)}-}}"
        else:
            estado_ion = "**Átomo Neutro (0)**"
            formula_visual = f"\\text{{{info_elemento['simbolo']}}}"

        # --- CAPA 3: FILTRO DE INESTABILIDAD BIOLÓGICA ---
        es_inestable = False
        mensaje_error = ""
        
        if abs(carga_neta) > 3:
            es_inestable = True
            mensaje_error = f"⚠️ **COLAPSO ELECTROSTÁTICO METABÓLICO:** Una carga monoatómica de {carga_neta:+} genera fuerzas de repulsión destructivas. La célula no tolera esta inestabilidad."
        elif abs(neutrones - info_elemento["base_neutrones"]) > 4:
            es_inestable = True
            mensaje_error = "☢️ **RUPTURA ISOTÓPICA NUCLEAR:** La relación Protones:Neutrones está fuera de la banda de estabilidad. El núcleo sufre desintegración radiactiva."

        st.markdown("---")
        
        if es_inestable:
            st.error(mensaje_error)
        else:
            st.success(f"✨ **Elemento Sintonizado:** {info_elemento['nombre']} | {estado_ion}")
            st.latex(rf"\text{{Isótopo Estructurado: }}_{{{protones}}}^{{{numero_masa}}}{formula_visual}")
            st.info(f"📋 **Importancia Clínica ({enfoque}):** {info_elemento[enfoque]}")

        st.markdown(
            f"<div style='background-color:#161b22; padding:12px; border-radius:8px; border:1px solid #30363d; text-align:center; font-family:monospace; font-size:0.85rem; color:#8b949e;'>"
            f"Lectura del Núcleo: Número Atómico Z = {protones} | Masa Atómica A = {numero_masa}</div>", 
            unsafe_allow_html=True
        )

    with tab2.values()[0] if hasattr(tab2, 'values') else tab2: # Resguardo de flujo
        pass

    with tab3:
        st.markdown("### 📝 Cuestionario de Certificación")
        
        st.markdown(
            """
            <div style='background-color:rgba(255,255,255,0.02); padding:10px; border-radius:6px; margin-bottom:15px; font-size:0.85rem; color:#8b949e;'>
            🏁 <strong>REGLAS DEL DESAFÍO:</strong> Cada acierto otorga 15 puntos al Score global. 
            Obtener una precisión menor al 50% restará una vida del indicador de estabilidad de tu licencia.
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        bloqueado = st.session_state.d1_quiz_enviado

        q1 = st.radio("1. De acuerdo con el marco de Harper, ¿qué alteración fisicoquímica experimenta un átomo de Calcio plasmático para actuar como el catión activo $\\text{Ca}^{2+}$?", ["A) Perdió 2 electrones de valencia, predominando las cargas positivas del núcleo.", "B) Absorbió 2 electrones libres del medio citosólico.", "C) El núcleo atómico expulsó 2 protones al espacio intersticial."], disabled=bloqueado, key="d1_q1_r")
        q2 = st.radio("2. Un bioelemento detectado por el espectrómetro en una muestra biológica presenta 12 protones en su núcleo y 10 electrones en su nube de valencia. Determina su identidad estructural:", ["A) Es un anión estable de Cloro.", "B) Es el catión Magnesio $\\text{Mg}^{2+}$ esencial como cofactor del ATP.", "C) Es un átomo neutro altamente reactivo."], disabled=bloqueado, key="d1_q2_r")

        if bloqueado and st.session_state.d1_retroalimentacion:
            prec = st.session_state.d1_retroalimentacion["precision"]
            if prec == 100: 
                st.success(f"🏆 **Certificación Completada:** Precisión del {prec}%. Homeostasis iónica dominada.")
            else: 
                st.error(f"❌ **Certificación Rechazada:** Precisión del {prec}%. Se sugiere reevaluar los modelos moleculares.")

        if st.button("🔒 Validar Bloque de Respuestas", type="primary", disabled=bloqueado, use_container_width=True, key="d1_submit"):
            aciertos = sum([q1.startswith("A"), q2.startswith("B")])
            precision = int((aciertos / 2) * 100)
            
            if precision < 50:
                st.session_state.vidas = max(0, st.session_state.vidas - 1)
                st.toast("Pérdida de estabilidad vital por bajo rendimiento.", icon="❤️")
            
            puntos_ganados = aciertos * 15
            st.session_state.puntos_acumulados += puntos_ganados
            st.session_state.d1_retroalimentacion = {"precision": precision}
            
            db.sincronizar_progreso_db(token_alumno, st.session_state.puntos_acumulados, "1", st.session_state.vidas, st.session_state.tiempo_estudio_min)
            st.session_state.d1_quiz_enviado = True
            st.rerun()
