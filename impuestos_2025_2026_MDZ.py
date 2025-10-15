import ipywidgets as widgets
from ipywidgets import Layout
from IPython.display import display, clear_output
import matplotlib.pyplot as plt
import numpy as np

# --- PARÁMETROS FISCALES 2026 (PROYECTO DE LEY) ---
# Estos valores están basados en el proyecto de Ley Impositiva 2026
UMBRAL_ALICUOTA_REDUCIDA = 450_000_000
UMBRAL_ALICUOTA_INCREMENTADA = 4_500_000_000

# Descuentos para contribuyentes cumplidores en Inmobiliario y Automotor
DESC_BUEN_CUMPLIDOR_ANO_ACTUAL = 0.10 # 10% por tener 2025 al día
DESC_BUEN_CUMPLIDOR_ANO_ANT = 0.10  # 10% adicional por tener 2024 al día
DESC_PAGO_ANUAL = 0.05             # 5% por cancelar el impuesto anual 2026 de una vez

# --- CREACIÓN DE LA INTERFAZ DE USUARIO (WIDGETS) ---
style = {'description_width': 'initial'}
layout_amplio = Layout(width='80%')

# --- Widgets de Ingresos ---
ingresos_anuales = widgets.FloatSlider(
    value=400_000_000, min=0, max=5_000_000_000, step=1_000_000,
    description='Ingresos Brutos Anuales (proyectados para 2025):',
    style=style, layout=layout_amplio, readout_format=','
)
alicuota_general = widgets.FloatText(
    value=4.0, description='Tu Alícuota General de IIBB (%):', style=style
)
alicuota_reducida = widgets.FloatText(
    value=3.0, description='Tu Alícuota Reducida de IIBB (%):', style=style
)
alicuota_incrementada = widgets.FloatText(
    value=5.0, description='Tu Alícuota Incrementada de IIBB (%):', style=style
)

# --- Widgets de Otros Impuestos y Beneficios ---
impuesto_inmobiliario = widgets.FloatText(
    value=500000, description='Impuesto Inmobiliario Anual Total:', style=style,
    layout=Layout(width='300px')
)
impuesto_automotor = widgets.FloatText(
    value=300000, description='Impuesto Automotor Anual Total:', style=style,
    layout=Layout(width='300px')
)
tiene_deuda = widgets.RadioButtons(
    options=['No, estoy al día', 'Sí, tengo deuda vencida'],
    value='No, estoy al día', description='¿Tienes deuda vencida al 31/12/2025?:',
    style=style, layout=Layout(width='auto')
)

# --- Contenedor para la salida de la simulación ---
output = widgets.Output()

# --- FUNCIÓN PRINCIPAL DE SIMULACIÓN ---
def simular_impuestos(ingresos, alic_reducida, alic_general, alic_incrementada, inmob, autom, deuda):
    with output:
        clear_output(wait=True)

        # 1. ANÁLISIS DE INGRESOS BRUTOS
        if ingresos <= UMBRAL_ALICUOTA_REDUCIDA:
            alicuota_aplicable = alic_reducida
            # FIX: Changed :_, to :,
            categoria = f"ALÍCUOTA REDUCIDA (hasta ${UMBRAL_ALICUOTA_REDUCIDA:,})"
        elif ingresos > UMBRAL_ALICUOTA_INCREMENTADA:
            alicuota_aplicable = alic_incrementada
            # FIX: Changed :_, to :,
            categoria = f"ALÍCUOTA INCREMENTADA (superior a ${UMBRAL_ALICUOTA_INCREMENTADA:,})"
        else:
            alicuota_aplicable = alic_general
            categoria = "ALÍCUOTA GENERAL"

        iibb_anual = ingresos * (alicuota_aplicable / 100)

        # 2. ANÁLISIS DE BENEFICIOS POR CUMPLIMIENTO
        cumplidor = (deuda == 'No, estoy al día')
        ahorro_inmobiliario = 0
        ahorro_automotor = 0

        if cumplidor:
            # Se asume que por estar al día, el contribuyente cumple los requisitos para todos los descuentos
            ahorro_inmobiliario = inmob * (DESC_BUEN_CUMPLIDOR_ANO_ACTUAL + DESC_BUEN_CUMPLIDOR_ANO_ANT + DESC_PAGO_ANUAL)
            ahorro_automotor = autom * (DESC_BUEN_CUMPLIDOR_ANO_ACTUAL + DESC_BUEN_CUMPLIDOR_ANO_ANT + DESC_PAGO_ANUAL)

        inmobiliario_optimizado = inmob - ahorro_inmobiliario
        automotor_optimizado = autom - ahorro_automotor
        ahorro_total_cumplidor = ahorro_inmobiliario + ahorro_automotor

        # 3. CÁLCULO DE TOTALES
        total_sin_optimizar = iibb_anual + inmob + autom
        total_optimizado = iibb_anual + inmobiliario_optimizado + automotor_optimizado

        # --- MOSTRAR RESULTADOS ---
        print("="*60)
        print("📊 RESULTADOS DE LA SIMULACIÓN FISCAL 2026 (MENDOZA)")
        print("="*60)

        # Sección IIBB
        print("\n--- 1. Impuesto sobre los Ingresos Brutos ---")
        # FIX: Changed :_, to :,
        print(f"Ingresos Anuales Proyectados: ${ingresos:,}")
        print(f"Categoría de Alícuota Aplicable: {categoria}")
        print(f"Alícuota Efectiva: {alicuota_aplicable:.2f}%")
        # FIX: Changed :_,.2f to :_2f
        print(f"Impuesto a los IIBB Anual Estimado: ${iibb_anual:,.2f}")

        # Sección Beneficios
        print("\n--- 2. Beneficios por Contribuyente Cumplidor ---")
        if cumplidor:
            print("¡EXCELENTE! Al no tener deudas, puedes acceder a importantes descuentos.")
            # FIX: Changed :_,.2f to :_2f
            print(f"Ahorro Potencial en Imp. Inmobiliario: ${ahorro_inmobiliario:,.2f}")
            print(f"Ahorro Potencial en Imp. Automotor: ${ahorro_automotor:,.2f}")
            print(f"AHORRO TOTAL POR BUEN CUMPLIMIENTO: ${ahorro_total_cumplidor:,.2f}")
        else:
            print("ATENCIÓN: Al tener deuda, no puedes acceder a los descuentos por buen cumplimiento.")
            # FIX: Changed :_,.2f to :_2f
            print(f"Costo de oportunidad (ahorro perdido): ${ahorro_total_cumplidor:,.2f}")


        # Sección Resumen y Optimización
        print("\n--- 3. Resumen y Recomendaciones de Optimización ---")
        # FIX: Changed :_,.2f to :_2f
        print(f"Carga Fiscal Total (Sin Optimizar): ${total_sin_optimizar:,.2f}")
        print(f"Carga Fiscal Total (Optimizada): ${total_optimizado:,.2f}")

        print("\n💡 RECOMENDACIONES:")
        # Recomendación sobre IIBB
        if UMBRAL_ALICUOTA_REDUCIDA < ingresos < UMBRAL_ALICUOTA_REDUCIDA * 1.1:
            costo_extra = (ingresos * (alic_general / 100)) - (ingresos * (alic_reducida / 100))
            # FIX: Changed :_, to :, and :_,.2f to :_2f
            print(f"  - IIBB: Estás cerca de perder la alícuota reducida. Superar los ${UMBRAL_ALICUOTA_REDUCIDA:,} te costaría ${costo_extra:,.2f} adicionales en IIBB. Evalúa diferir facturación si es posible.")
        elif UMBRAL_ALICUOTA_INCREMENTADA < ingresos < UMBRAL_ALICUOTA_INCREMENTADA * 1.1:
             costo_extra = (ingresos * (alic_incrementada / 100)) - (ingresos * (alic_general / 100))
             # FIX: Changed :_, to :, and :_,.2f to :_2f
             print(f"  - IIBB: ¡Cuidado! Estás cerca de pasar a la alícuota incrementada. Superar los ${UMBRAL_ALICUOTA_INCREMENTADA:,} te costaría ${costo_extra:,.2f} adicionales. Es un punto crítico para la planificación fiscal.")
        else:
            print("  - IIBB: Tu nivel de ingresos te posiciona claramente en tu categoría actual. Monitorea tu facturación a fin de año.")

        # Recomendación sobre cumplimiento
        if not cumplidor:
            # FIX: Changed :_,.2f to :_2f
            print(f"  - CUMPLIMIENTO: La recomendación más importante es regularizar tu deuda. Hacerlo te permitiría ahorrar ${ahorro_total_cumplidor:,.2f} en otros impuestos.")
        else:
            print("  - CUMPLIMIENTO: ¡Felicitaciones! Mantenerte al día es la estrategia más rentable. Asegúrate de optar por el pago anual para maximizar los descuentos.")

        # --- GRÁFICO COMPARATIVO ---
        labels = ['IIBB', 'Inmobiliario', 'Automotor']
        valores_sin_opt = [iibb_anual, inmob, autom]
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

        # FIX: Changed fmt='{:_,.0f}' to fmt='{:,.0f}'
        ax.bar_label(rects1, padding=3, fmt='{:,.0f}')
        ax.bar_label(rects2, padding=3, fmt='{:,.0f}')

        fig.tight_layout()
        plt.show()

# --- VINCULAR LA INTERFAZ CON LA FUNCIÓN ---
controles = widgets.VBox([
    widgets.HTML("<h2>Simulador de Optimización Fiscal 2026 (Mendoza)</h2>"),
    widgets.HTML("<p>Mueve el deslizador de ingresos y ajusta los otros valores para ver el impacto en tiempo real.</p>"),
    ingresos_anuales,
    widgets.HBox([alicuota_reducida, alicuota_general, alicuota_incrementada]),
    widgets.HBox([impuesto_inmobiliario, impuesto_automotor]),
    tiene_deuda
])

app = widgets.VBox([controles, output])

# --- MOSTRAR LA APLICACIÓN ---
# Ejecutar la simulación una vez al inicio con los valores por defecto
simular_impuestos(
    ingresos_anuales.value, alicuota_reducida.value, alicuota_general.value,
    alicuota_incrementada.value, impuesto_inmobiliario.value,
    impuesto_automotor.value, tiene_deuda.value
)

# Registrar la función para que se actualice con cada cambio
ingresos_anuales.observe(lambda change: simular_impuestos(change.new, alicuota_reducida.value, alicuota_general.value, alicuota_incrementada.value, impuesto_inmobiliario.value, impuesto_automotor.value, tiene_deuda.value), names='value')
alicuota_reducida.observe(lambda change: simular_impuestos(ingresos_anuales.value, change.new, alicuota_general.value, alicuota_incrementada.value, impuesto_inmobiliario.value, impuesto_automotor.value, tiene_deuda.value), names='value')
alicuota_general.observe(lambda change: simular_impuestos(ingresos_anuales.value, alicuota_reducida.value, change.new, alicuota_incrementada.value, impuesto_inmobiliario.value, impuesto_automotor.value, tiene_deuda.value), names='value')
alicuota_incrementada.observe(lambda change: simular_impuestos(ingresos_anuales.value, alicuota_reducida.value, alicuota_general.value, change.new, impuesto_inmobiliario.value, impuesto_automotor.value, tiene_deuda.value), names='value')
impuesto_inmobiliario.observe(lambda change: simular_impuestos(ingresos_anuales.value, alicuota_reducida.value, alicuota_general.value, alicuota_incrementada.value, change.new, impuesto_automotor.value, tiene_deuda.value), names='value')
impuesto_automotor.observe(lambda change: simular_impuestos(ingresos_anuales.value, alicuota_reducida.value, alicuota_general.value, alicuota_incrementada.value, impuesto_inmobiliario.value, change.new, tiene_deuda.value), names='value')
tiene_deuda.observe(lambda change: simular_impuestos(ingresos_anuales.value, alicuota_reducida.value, alicuota_general.value, alicuota_incrementada.value, impuesto_inmobiliario.value, impuesto_automotor.value, change.new), names='value')


display(app)
