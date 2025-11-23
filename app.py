import streamlit as st
import pickle
import pandas as pd

# Cargar objetos guardados
scaler = pickle.load(open("scaler.pkl", "rb"))
model = pickle.load(open("hierarchical_model.pkl", "rb"))
with open("ordinal_encoder.pkl", "rb") as f:
    ordinal_encoder = pickle.load(f)
# Cargar datos originales desde CSV
data_original = pd.read_csv("muestra_38000.csv")  # <-- pon aquí tu archivo real


# Variables
cat_cols = [
    "DesagregadoDesembolsoBIE",
    "Posee Censo de Familia?",
    "Posee Censo de Habitabilidad?",
    "Posee Serv. Publicos Basicos",
    "Posee Conyuge o Compañero(a)?",
    "Sexo",
    "Grupo Etario",
    "BeneficioTRV",
    "BeneficioPDT",
    "Desembolso BIE",
    "Situacion Final frente al proceso"
]

num_cols = [
    "N° de Hijos"
]

# Función de transformación
def transform_input(df):
    df_copy = df.copy()

    df_copy[cat_cols] = ordinal_encoder.transform(df_copy[cat_cols].astype(str))
    df_copy[num_cols] = scaler.transform(df_copy[num_cols])

    return df_copy

# Aplicación Streamlit
st.set_page_config(
    page_title="Asignación de Estrategias",
    page_icon="📑",
    layout="centered",  # o "wide" si quieres más espacio
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* Color a TODOS los títulos h1, h2, h3 */
h1 {
    color: #8ea19b !important;   /* Naranja apagado */
}
h2 {
    color: #d1ab71 !important;   /* Naranja apagado */
}
h3 {
    color: #d1ab71 !important;   /* Turquesa apagado */
}

/* Espaciado más limpio */
h1, h2, h3 {
    font-weight: 700 !important;
    margin-top: 20px !important;
}

/* Evitar que los selectbox queden pegados */
.css-1v0mbdj {
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

div[data-baseweb="tab-list"] button {
    color: #7d8f86; /* Color texto pestañas inactivas */
    font-size: 18px;
}

div[data-baseweb="tab-list"] button[aria-selected="true"] {
    color: #d1ab71 !important; /* Color texto pestaña activa */
    border-bottom: 3px solid #d1ab71 !important; /* Línea roja */
}

div[data-baseweb="tab-highlight"] {
    background-color: transparent !important; /* Elimina highlight automático */
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* selector reforzado para botones */
button[kind="primary"], button[kind="secondary"], div.stButton > button {
    background-color: #bbcdc5 !important;
    color: #404040 !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 0.6em 1em !important;
    font-weight: 600 !important;
}

button[kind="primary"]:hover, button[kind="secondary"]:hover, div.stButton > button:hover {
    background-color: #a5bbb2 !important;
    color: #404040 !important;
}
</style>
""", unsafe_allow_html=True)



st.title("Observatorio de Permanencia")
st.markdown("Este sitio identifica las características del usuario y asigna una estrategía para asegurar que continue en el proceso de reintegración. ")

tab1, tab2 = st.tabs(["Asignación de Estrategias", "Definición de Perfiles"])


with tab1:
    st.header("Asignación de Estrategias")
    st.sidebar.header("Proceso de reintegración")
    st.sidebar.markdown("""
    La ley 975 de 2005 define en el artículo 9 a la desmovilización como:

    > El acto individual o colectivo de dejar las armas y abandonar el grupo armado organizado al margen de la ley, realizado ante autoridad competente.
                        
    Fortaleciendo la inclusión social y laboral de las personas desmovilizadas, mejorando la efectividad de los procesos de reintegración identificando los perfiles y previniendo los factores de abandono, se promueve el trabajo decente y crecimiento economico identificando barreras para la inserción productiva para poder intervenir de manera oportuna mejorando estos procesos de reintegración.
    """)

    st.markdown("### Datos Personales")

    # Primera fila: Sexo y Grupo Etario
    col1, col2 = st.columns(2)
    with col1:
        Sexo = st.selectbox("Sexo", ["Selecciona una opción","Masculino", "Femenino"])
    with col2:
        GrupoEtario = st.selectbox(
            "Grupo Etario", 
            ["Selecciona una opción","Entre 18 y 25 años", "Entre 26 y 40 años", "Entre 41 y 60 años", "Mayor de 60 años"]
        )

    st.markdown("---")  # separador visual

    # Segunda fila: Censos y servicios
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### Censo y Vivienda")
        CensoHabit = st.selectbox("Posee Censo de Habitabilidad?", ["Selecciona una opción","Sí", "No"])
        if CensoHabit == "Sí":
            Servicios = st.selectbox("Posee Servicios Públicos Básicos", ["Selecciona una opción","Sí", "No"])
        else:
            Servicios = "<No Aplica>"

    with col4:
        st.markdown("### Familia")
        CensoFam = st.selectbox("Posee Censo de Familia?", ["Selecciona una opción","Sí", "No"])
        if CensoFam == "Sí":
            Conyuge = st.selectbox("Posee Cónyuge o Compañero(a)?", ["Selecciona una opción","Sí", "No"])
            N_Hijos = st.number_input("Número de Hijos", min_value=0, max_value=10, step=1)
        else:
            Conyuge = "<No Aplica>"
            N_Hijos = -1

    st.markdown("---")  # separador visual

    # Tercera fila: Beneficios y situación final
    col5, col6 = st.columns(2)
    with col5:
        st.markdown("### Beneficios")
        DesagregadoDesembolsoBIE = st.selectbox(
            "Desagregado Desembolso BIE",
            [
                "Selecciona una opción",
                "Posee desembolso BIE",
                "No está en Proceso",
                "No posee desembolso BIE",
                "Culminado con agotamiento de tiempo para acceder a BIE",
                "Culminado sin agotamiento de tiempo para acceder a BIE"
            ]
        )
        BeneficioTRV = st.selectbox("Beneficio TRV", ["Selecciona una opción","Sí", "No"])
        BeneficioPDT = st.selectbox("Beneficio PDT", ["Selecciona una opción","Sí", "No"])
        DesembolsoBIE = st.selectbox("Desembolso BIE", ["Selecciona una opción","Sí", "No"])

    with col6:
        st.markdown("### Situación final frente al proceso")
        SituacionFinal = st.selectbox(
            "Situación Final frente al Proceso",
            ["Selecciona una opción","Culminado", "Fuera del proceso", "En proceso", "Ausente del proceso"]
        )

    if st.button("Predecir Estrategia"):

        campos = [
            Sexo, GrupoEtario, CensoHabit, Servicios,
            CensoFam, Conyuge, DesagregadoDesembolsoBIE,
            BeneficioTRV, BeneficioPDT, DesembolsoBIE,
            SituacionFinal
        ]

        if "Selecciona una opción" in campos:
            st.error("⚠️ Por favor completa todas las preguntas antes de continuar.")
            st.stop()

        input_df = pd.DataFrame([{
            "DesagregadoDesembolsoBIE": DesagregadoDesembolsoBIE,
            "Posee Censo de Familia?": CensoFam,
            "Posee Censo de Habitabilidad?": CensoHabit,
            "Posee Serv. Publicos Basicos": Servicios,
            "Posee Conyuge o Compañero(a)?": Conyuge,
            "Sexo": Sexo,
            "Grupo Etario": GrupoEtario,
            "BeneficioTRV": BeneficioTRV,
            "BeneficioPDT": BeneficioPDT,
            "Desembolso BIE": DesembolsoBIE,
            "Situacion Final frente al proceso": SituacionFinal,
            "N° de Hijos": N_Hijos
        }])

        #Estrategias
        estrategias ={
            0: 
        """
        * **Mantener acompañamiento ligero** y enfocado en la post-culminación.
        * Implementar **comunicación eficiente** (recordatorios de hitos y avances de proyectos productivos).
        * **Incentivar su participación** como líderes o mentores para reforzar su compromiso y el de otros grupos.
        * Articulación interinstitucional para garantizar la legalización o acceso a servicios públicos básicos pendientes (casi el 40% aún no los tiene).
        """,
            1:
        """
        * Implementar **seguimiento administrativo semanal** y un **checklist de trámites pendientes**, priorizando la validación de los censos y el Desembolso BIE.
        * Ofrecer **microasesorías rápidas** para completar documentación.
        * Investigar y resolver el alto porcentaje de variables familiares "No Aplica" para entender su red de apoyo real.
        * **Aceleración de desembolsos o procesos** una vez completada la documentación.
        """,
            2:
        """
        * **Seguimiento administrativo semanal** enfocado en las últimas etapas del proceso.
        * **Aceleración de desembolsos BIE** para recompensar el esfuerzo y cerrar el proceso.
        * Ofrecer apoyo psicosocial para el **manejo del estrés y la frustración** por la duración del proceso.
        * Focalizar las microasesorías académicas para asegurar la culminación exitosa.
        """,
            3:
        """
        * Mantener **acompañamiento ligero** centrado en la **sostenibilidad del proyecto de vida**.
        * **Mitigar el riesgo de resentimiento** ofreciendo **oportunidades económicas alternativas** (créditos, subsidios de formalización) que compensen el BIE perdido.
        * Incentivar la participación en actividades que refuercen el compromiso y el sentido de pertenencia a pesar de la falla administrativa.
        """,
            4:
        """
        * Mantener **acompañamiento ligero** enfocado en el **empoderamiento económico** y el apoyo a la crianza.
        * **Incentivar su liderazgo** como modelos de rol y mentoras para otras mujeres desmovilizadas.
        * Ofrecer **líneas de crédito o formación flexible** para emprendimientos que se adapten a sus responsabilidades de cuidado.
        """,
            5:
        """
        * **Priorizar el contacto directo (llamada, WhatsApp personalizado)** y la **detección de barreras** (tiempo, dinero, transporte).
        * Implementar un **programa de alcance comunitario (Brigadas de Acercamiento)** para la localización y re-vinculación de emergencia.
        * Ofrecer **priorización de apoyo psicosocial** y un paquete básico de emergencia antes de la reactivación formal del proceso.
        * **Mentoría entre pares** (con éxito del *Cluster 0* o *4*) para generar sentido de pertenencia.
        """,
            6:
        """
        * **Contacto directo** e investigación de la causa de la salida, enfocándose en la **capitalización de la inversión** (los censos ya realizados).
        * **Flexibilización de horarios** y oferta de **tutorías rápidas o material asincrónico** para re-engancharlos.
        * **Detección de barreras específicas** (edad, salud, tiempo) y compensación por la falta de BIE con acceso prioritario a líneas de fomento económico alternativas.
        """,
            7:
        """
        * **Detección de barreras** asociadas a la edad y la salud.
        * **Mentoría entre pares** para generar sentido de pertenencia.
        * Priorización de **apoyo psicosocial** y **programas de seguridad social/salud** (pensiones, subsidios de adulto mayor) dada la edad.
        * **Flexibilización** de la oferta formativa y generación de ingresos pasivos.
        """,
            8:
        """
        * **Contacto directo** para detectar barreras, especialmente las relacionadas con el **cuidado del hogar** y la inestabilidad de la vivienda.
        * **Flexibilización de horarios** y acceso a **material asincrónico** para adaptarse a la carga familiar.
        * **Priorización de apoyo psicosocial** para el manejo de la carga emocional.
        * **Acompañamiento especializado** para la gestión y estabilización de la situación de habitabilidad.
        """
        }

        #Nombres de cluster
        nombres_cluster ={
            0: "Perfil Estable y Cumplidor",
            1: " Perfil en Transición / Documentación Pendiente",
            2: "Perfil en Proceso Activo, con Cierto Riesgo",
            3: "Perfil Cumplidor con Apoyo Parcial",
            4: "Perfil Femenino con Acompañamiento Completo",
            5: "Perfil Desconectado del Proceso",
            6: "Perfil Fuera del Proceso, pero con Condiciones Básicas",
            7: "Perfil Retirado, sin Beneficios",
            8: "Perfil Femenino, Parcialmente Beneficiado"
        }

        # Transformar nuevo input
        transformed = transform_input(input_df)

        # Transformar dataset completo original
        data_original_transformed = transform_input(data_original)

        # Unir dataset completo + nuevo registro
        full_plus_new = pd.concat([data_original_transformed, transformed], ignore_index=True)

        # Recalcular clustering jerárquico completo
        labels = model.fit_predict(full_plus_new)

        # Cluster del nuevo cliente = último registro
        cluster = labels[-1]

        contenido = f"# Perfil Identificado: {nombres_cluster[cluster]}\n\n"
        
        st.success(contenido)
        st.markdown(estrategias[cluster])

with tab2:
    st.header("Definición de perfiles")

    # Primera fila: Sexo y Grupo Etario
    col1, col2 = st.columns(2)
    with col1:
       st.markdown("### Perfil Estable y Cumplidor (27.9% del Total)")
       st.markdown("""
        * **Características Predominantes:** Este es el grupo más grande, representando el **27.9%** de los desmovilizados. Predominan los hombres (100%) entre 26 y 40 años, con pareja. Son un perfil de éxito formal: no recibieron beneficios TRV ni PDT, pero sí tuvieron **desembolso BIE (100%)** y cuentan con **censos de familia y habitabilidad completos (100%)**. La gran mayoría, el **94.4%**, ha culminado su proceso y el 61.8% tiene servicios públicos básicos.
* **Lectura Ejecutiva (Bajo Riesgo):** Es un perfil relativamente **estable, con condiciones de hogar funcionales y baja vulnerabilidad**. Su probabilidad de deserción es baja. La prioridad es la sostenibilidad y la consolidación de logros.
                   """)
       
       st.markdown("### Perfil en Transición / Documentación Pendiente (6.6%)")
       st.markdown("""
        * **Características Predominantes:** Representa el **6.6%** del total, compuesto casi en su totalidad por hombres (96.6%) entre 26 y 40 años. No reciben beneficios TRV/PDT y el 70.2% no tiene desembolso BIE. Su principal característica es el **censo familiar incompleto (75.9% no lo posee)**. La situación final está dividida: 45.8% culmina y una cifra similar sigue en proceso. Un 76.1% aparece como "No Aplica" en variables familiares, sugiriendo desconexión o datos incompletos.
* **Lectura Ejecutiva (Riesgo Operativo):** Perfil intermedio, con **trámites a medias o rezagos administrativos**. No necesariamente vulnerable, pero con **riesgo operativo** por falta de definiciones en el proceso. La falta de censos es el cuello de botella.
                   """)
       
       st.markdown("### Perfil en Proceso Activo, con Cierto Riesgo (12%)")
       st.markdown("""
        * **Características Predominantes:** Este grupo, el **12.0%** del total, se caracteriza por ser el **único** donde el **100% recibió beneficios TRV y PDT**. Tienen censos completos y un **89.2% está activamente "En Proceso"**. Sin embargo, el **72.2% aún no posee el desembolso BIE**. Predominan los hombres (77.6%) entre 26 y 40 años.
* **Lectura Ejecutiva (Riesgo Operativo/Psicosocial):** Se consideran estudiantes activos, pero con **avances lentos en el cierre de etapas**. Aunque tienen apoyo económico inicial, el que el 89% no haya culminado los pone en **riesgo de deserción por carga, cansancio o falta de resultados visibles** (el BIE pendiente).
                   """)
       
       st.markdown("### Perfil Cumplidor con Apoyo Parcial (11.1%)")
       st.markdown("""
        * **Características Predominantes:** Representa el **11.1%** de la base, principalmente hombres (82.6%) entre 26 y 40 años. Similar al *Cluster 0*, tiene un **buen desempeño formal**: el 73.8% ha culminado el proceso, tienen censos al día y un alto porcentaje tiene servicios públicos. Su característica distintiva es que el **98.4% no tiene el desembolso BIE**, y el **72.5%** de esto se debe a **agotamiento de tiempo** para acceder al beneficio.
* **Lectura Ejecutiva (Riesgo de Frustración Económica):** Grupo con desempeño positivo y disciplina, pero con **grave vulnerabilidad económica** por la pérdida del capital BIE. Alto riesgo de **frustración y resentimiento** que podría minar la sostenibilidad de la reintegración.
                   """)
       
    with col2:
        st.markdown("### Perfil Desconectado del Proceso (20.1%)")
        st.markdown("""
        * **Características Predominantes:** Es un grupo **crítico y grande (20.1%)**, compuesto en su totalidad por hombres (100%) entre 26 y 40 años, sin hijos ni pareja. **No reciben ningún beneficio** (BIE, TRV, PDT). El dato más alarmante es que el **100% está Fuera del Proceso** y la información sobre familia y servicios aparece como "No aplica".
* **Lectura Ejecutiva (Altísimo Riesgo de Abandono):** Es un grupo crítico: **sin beneficios, sin conexión con el proceso y totalmente fuera del programa**. La desconexión total sugiere un **altísimo riesgo de deserción por falta de anclaje institucional y desarraigo social**.
                    """)
        
        st.markdown("### Perfil Fuera del Proceso, pero con Condiciones Básicas (6.6%)")
        st.markdown("""
        * **Características Predominantes:** Un **6.6%** de hombres (100%), de un rango de edad mayor (41-60 años). El **99.7% está Fuera del Proceso** y no tienen beneficios (BIE, TRV, PDT). Sin embargo, a diferencia del *Cluster 5*, este grupo **sí tienen censos de familia/habitabilidad y servicios públicos básicos (64.3%)**.
* **Lectura Ejecutiva (Alto Riesgo, Oportunidad de Rescate):** También tienen alto riesgo de abandono, pero con **mejores condiciones de hogar y un esfuerzo inicial completado (censos)**. Puede ser deserción por falta de tiempo, motivación, o expectativas no cumplidas en la etapa final.
                    """)
        
        st.markdown("### Perfil Retirado, sin Beneficios (6.7%)")
        st.markdown("""
        * **Características Predominantes:** El **6.7%** de hombres (100%) entre 26 y 40 años, de los cuales el **60.4% está Fuera del Proceso**. Es el único grupo de desmovilizados mayores (53.6% entre 41 y 60 años) que no accedió al BIE. No reciben beneficios ni tienen servicios públicos básicos.
* **Lectura Ejecutiva (Riesgo Silencioso):** Deserción asociada a **vulnerabilidad económica y posiblemente por edad**. Es un **perfil silencioso**: no se quejan, solo abandonan. El riesgo psicosocial es alto debido al desarraigo.
                    """)
        
        st.markdown("### Perfil Femenino, Parcialmente Beneficiado (2.7%)")
        st.markdown("""
        * **Características Predominantes:** El grupo más pequeño (**2.7%**), compuesto por mujeres (100%) entre 26 y 40 años. Es un perfil de riesgo moderado a alto: el **51% sí recibe BIE**, pero el **54% está Fuera del Proceso**. La mayoría (82.6%) no tiene Censo de Habitabilidad.
* **Lectura Ejecutiva (Riesgo Moderado a Alto):** Tienen apoyo económico (BIE), pero sus **condiciones del hogar o la carga familiar afectan la permanencia**. La falta de censo de habitabilidad sugiere inestabilidad residencial.
                    """)
        
        st.markdown("### Perfil Femenino con Acompañamiento Completo (6.3%)")
        st.markdown("""
        * **Características Predominantes:** Es el primer grupo **100% femenino** (6.3% del total), entre 26 y 40 años. Es un perfil de **éxito sobresaliente**: no reciben TRV/PDT, pero **sí tienen BIE (100%)**, censos completos y el **96.9% ha culminado**. Son cabezas de hogar, con un número significativo de hijos (27.9% con 1 hijo).
* **Lectura Ejecutiva (Bajo Riesgo):** Es el **mejor perfil en términos de éxito**. Cumplen, avanzan y requieren poco seguimiento. El riesgo principal es la **doble carga** como cabeza de hogar.

                   """)

