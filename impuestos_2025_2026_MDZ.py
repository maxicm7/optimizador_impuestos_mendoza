# simulador_fiscal.py
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Simulador Fiscal 2026",
    page_icon="📊",
    layout="wide"
)

# --- PARÁMETROS FISCALES 2026 (PROYECTO DE LEY) ---
# Estos valores están basados en el proyecto de Ley Impositiva 2026
UMBRAL_ALICUOTA_REDUCIDA = 450_000_000
UMBRAL_ALICUOTA_INCREMENTADA = 4_500_000_000

# Descuentos para contribuyentes cumplidores en Inmobiliario y Automotor
DESC_BUEN_CUMPLIDOR_ANO_ACTUAL = 0.10 # 10% por tener 2025 al día
DESC_BUEN_CUMPLIDOR_ANO_ANT = 0.10  # 10% adicional por tener 2024 al día
DESC_PAGO_ANUAL = 0.05             # 5% por cancelar el impuesto anual 2026 de una vez

# --- CREACIÓN DE LA INTERFAZ DE USUARIO (WIDGETS EN LA BARRA LATERAL) ---
st.sidebar.header("📊 Parámetros de la Simulación")
st.sidebar.markdown("Ajusta los valores para ver el impacto en tiempo real.")

# --- Widgets de Ingresos ---
ingresos_anuales = st.sidebar.slider(
    'Ingresos Brutos Anuales (proyectados para 2025):',
    min_value=0.0,
    max_value=5_000_000_000.0,
    value=400_000_000.0,
    step=1_000_000.0,
    format="%.0f"  # CORRECCIÓN AQUÍ: Eliminado el '$' y usando '%.0f' para números enteros
)

st.sidebar.subheader("Tus Alícuotas de IIBB (%)")
col1, col2, col3 = st.sidebar.columns(3)
with col1:
    alicuota_reducida = st.number_input('Reducida', value=3.0, step=0.1, format="%.2f")
with col2:
    alicuota_general = st.number_input('General', value=4.0, step=0.1, format="%.2f")
with col3:
    alicuota_incrementada = st.number_input('Incrementada', value=5.0, step=0.1, format="%.2f")

# --- Widgets de Otros Impuestos y Beneficios ---
st.sidebar.subheader("Otros Impuestos Anuales")
impuesto_inmobiliario = st.sidebar.number_input(
    'Impuesto Inmobiliario Anual Total:',
    value=500000.0,
    step=1000.0,
    format="%.0f"  # CORRECCIÓN AQUÍ
)
impuesto_automotor = st.sidebar.number_input(
    'Impuesto Automotor Anual Total:',
    value=300000.0,
    step=1000.0,
    format="%.0f"  # CORRECIÓN AQUÍ
)

tiene_deuda = st.sidebar.radio(
    '¿Tienes deuda vencida al 31/12/2025?:',
    ('No, estoy al día', 'Sí, tengo deuda vencida'),
    index=0
)


# --- TÍTULO Y DESCRIPCIÓN PRINCIPAL ---
st.title("Simulador de Optimización Fiscal 2026 (Mendoza)")
st.markdown("Esta herramienta te ayuda a proyectar tu carga fiscal para 2026 y a entender cómo las decisiones de cumplimiento pueden generar ahorros significativos.")

# --- LÓGICA DE SIMULACIÓN Y VISUALIZACIÓN ---

# 1. ANÁLISIS DE INGRESOS BRUTOS
if ingresos_anuales <= UMBRAL_ALICUOTA_REDUCIDA:
    alicuota_aplicable = alicuota_reducida
    categoria = f"ALÍCUOTA REDUCIDA (hasta ${UMBRAL_ALICUOTA_REDUCIDA:,.0f})"
elif ingresos_anuales > UMBRAL_ALICUOTA_INCREMENTADA:
    alicuota_aplicable = alicuota_incrementada
    categoria = f"ALÍCUOTA INCREMENTADA (superior a ${UMBRAL_ALICUOTA_INCREMENTADA:,.0f})"
else:
    alicuota_aplicable = alicuota_general
    categoria = "ALÍCUOTA GENERAL"

iibb_anual = ingresos_anuales * (alicuota_aplicable / 100)

# 2. ANÁLISIS DE BENEFICIOS POR CUMPLIMIENTO
cumplidor = (tiene_deuda == 'No, estoy al día')
ahorro_inmobiliario = 0
ahorro_automotor = 0

if cumplidor:
    # Se asume que por estar al día, el contribuyente cumple los requisitos para todos los descuentos
    ahorro_inmobiliario = impuesto_inmobiliario * (DESC_BUEN_CUMPLIDOR_ANO_ACTUAL + DESC_BUEN_CUMPLIDOR_ANO_ANT + DESC_PAGO_ANUAL)
    ahorro_automotor = impuesto_automotor * (DESC_BUEN_CUMPLIDOR_ANO_ACTUAL + DESC_BUEN_CUMPLIDOR_ANO_ANT + DESC_PAGO_ANUAL)

inmobiliario_optimizado = impuesto_inmobiliario - ahorro_inmobiliario
automotor_optimizado = impuesto_automotor - ahorro_automotor
ahorro_total_cumplidor = ahorro_inmobiliario + ahorro_automotor

# 3. CÁLCULO DE TOTALES
total_sin_optimizar = iibb_anual + impuesto_inmobiliario + impuesto_automotor
total_optimizado = iibb_anual + inmobiliario_optimizado + automotor_optimizado


# --- MOSTRAR RESULTADOS ---
st.header("📊 Resultados de la Simulación")

resumen_col1, resumen_col2 = st.columns(2)

with resumen_col1:
    st.metric(label="Carga Fiscal Total (Sin Optimizar)", value=f"${total_sin_optimizar:,.2f}")
with resumen_col2:
    st.metric(label="Carga Fiscal Total (Optimizada)", value=f"${total_optimizado:,.2f}", delta=f"-${ahorro_total_cumplidor:,.2f}", delta_color="inverse")


# --- Contenedores para detalles ---
with st.expander("Ver detalle del cálculo y recomendaciones", expanded=True):

    st.subheader("1. Impuesto sobre los Ingresos Brutos")
    st.markdown(f"**Ingresos Anuales Proyectados:** `${ingresos_anuales:,.2f}`")
    st.markdown(f"**Categoría de Alícuota Aplicable:** `{categoria}`")
    st.markdown(f"**Alícuota Efectiva:** `{alicuota_aplicable:.2f}%`")
    st.success(f"**Impuesto a los IIBB Anual Estimado: ${iibb_anual:,.2f}**")

    st.subheader("2. Beneficios por Contribuyente Cumplidor")
    if cumplidor:
        st.info("¡EXCELENTE! Al no tener deudas, puedes acceder a importantes descuentos.")
        col_ben1, col_ben2, col_ben3 = st.columns(3)
        col_ben1.metric("Ahorro Inmobiliario", f"${ahorro_inmobiliario:,.2f}")
        col_ben2.metric("Ahorro Automotor", f"${ahorro_automotor:,.2f}")
        col_ben3.metric("AHORRO TOTAL", f"${ahorro_total_cumplidor:,.2f}")
    else:
        st.warning("ATENCIÓN: Al tener deuda, no puedes acceder a los descuentos por buen cumplimiento.")
        st.metric("Costo de oportunidad (ahorro perdido):", f"${ahorro_total_cumplidor:,.2f}")

    st.subheader("💡 Recomendaciones de Optimización")
    # Recomendación sobre IIBB
    if UMBRAL_ALICUOTA_REDUCIDA < ingresos_anuales < UMBRAL_ALICUOTA_REDUCIDA * 1.1:
        costo_extra = (ingresos_anuales * (alicuota_general / 100)) - (ingresos_anuales * (alicuota_reducida / 100))
        st.markdown(f"  - **IIBB:** Estás cerca de perder la alícuota reducida. Superar los `${UMBRAL_ALICUOTA_REDUCIDA:,}` te costaría `${costo_extra:,.2f}` adicionales. Evalúa diferir facturación si es posible.")
    elif UMBRAL_ALICUOTA_INCREMENTADA < ingresos_anuales < UMBRAL_ALICUOTA_INCREMENTADA * 1.1:
         costo_extra = (ingresos_anuales * (alicuota_incrementada / 100)) - (ingresos_anuales * (alicuota_general / 100))
         st.markdown(f"  - **IIBB:** ¡Cuidado! Estás cerca de pasar a la alícuota incrementada. Superar los `${UMBRAL_ALICUOTA_INCREMENTADA:,}` te costaría `${costo_extra:,.2f}` adicionales. Es un punto crítico para la planificación fiscal.")
    else:
        st.markdown("  - **IIBB:** Tu nivel de ingresos te posiciona claramente en tu categoría actual. Monitorea tu facturación a fin de año.")

    # Recomendación sobre cumplimiento
    if not cumplidor:
        st.markdown(f"  - **CUMPLIMIENTO:** La recomendación más importante es regularizar tu deuda. Hacerlo te permitiría ahorrar **`${ahorro_total_cumplidor:,.2f}`** en otros impuestos.")
    else:
        st.markdown("  - **CUMPLIMIENTO:** ¡Felicitaciones! Mantenerte al día es la estrategia más rentable. Asegúrate de optar por el pago anual para maximizar los descuentos.")


# --- GRÁFICO COMPARATIVO ---
st.header("Comparación Gráfica de la Carga Tributaria")
labels = ['IIBB', 'Inmobiliario', 'Automotor']
valores_sin_opt = [iibb_anual, impuesto_inmobiliario, impuesto_automotor]
valores_opt = [iibb_anual, inmobiliario_optimizado, automotor_optimizado]

x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width/2, valores_sin_opt, width, label='Sin Optimizar', color='salmon')
rects2 = ax.bar(x + width/2, valores_opt, width, label='Optimizado (Cumplidor)', color='skyblue')

ax.set_ylabel('Monto Anual en $')
ax.set_title('Comparación de Carga Tributaria Anual')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

# Formatear el eje y para que muestre números con separadores de miles
ax.get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda y, p: format(int(y), ',')))

ax.bar_label(rects1, padding=3, fmt='{:,.0f}')
ax.bar_label(rects2, padding=3, fmt='{:,.0f}')

fig.tight_layout()

# Mostrar el gráfico en Streamlit
st.pyplot(fig)
