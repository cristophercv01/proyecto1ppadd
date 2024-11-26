import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Portada
## st.image('fondoadsl.jpg', use_container_width=True)

# Título
st.title('Comparación de Pronóstico de Tendencia vs El Valor Real de las Acciones')

# Intro
st.write("""
    Con esta aplicación logramos comparar datos reales de las acciones con los pronósticos generados por el modelo ARIMA.
    Utiliza los controles para seleccionar las acciones, el rango de fechas y si quieres mostrar los pronósticos. Este trabajo fue hecho por el equipo del Atlético de San Luis de la clase de Programación para Análisis de Datos.
""")

# Lista de acciones
acciones = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']

# accion predeterminada: solo GOOGL
acciones_seleccionadas = st.multiselect('Selecciona las acciones a mostrar:', acciones, default=['GOOGL'])

# fechas predeterminadas: desde el 2023-01-05 hasta el 2024-11-25
fecha_inicio = st.date_input('Fecha de inicio:', value=pd.to_datetime('2023-01-05'))
fecha_fin = st.date_input('Fecha de fin:', value=pd.to_datetime('2024-11-25'))

# csv's
df_real = pd.read_csv('df_real.csv', index_col=0, parse_dates=True)
df_unido = pd.read_csv('df_unido.csv', index_col=0, parse_dates=True)

# Filtrar los datos de df_real y df_unido para las acciones seleccionadas y el rango de fechas
df_real_filtrado = df_real[acciones_seleccionadas]
df_unido_filtrado = df_unido[acciones_seleccionadas]

df_real_filtrado = df_real_filtrado.loc[fecha_inicio:fecha_fin]
df_unido_filtrado = df_unido_filtrado.loc[fecha_inicio:fecha_fin]

# Checkbox
mostrar_pronostico = st.checkbox('Mostrar Pronóstico', value=True)

# Calcular el aumento o disminución
st.subheader("Aumento o disminución del valor de las acciones seleccionadas")
for accion in acciones_seleccionadas:
    valor_inicio = df_real_filtrado[accion].iloc[0]
    valor_fin = df_real_filtrado[accion].iloc[-1]
    cambio = valor_fin - valor_inicio
    porcentaje_cambio = (cambio / valor_inicio) * 100
    st.write(f"**{accion}**: {valor_inicio:.2f} → {valor_fin:.2f} ({cambio:+.2f}, {porcentaje_cambio:+.2f}%)")


# Graficar las series de tiempo de los datos reales y los pronósticos
fig, ax = plt.subplots(figsize=(12, 8))

# Graficar las series reales2
for accion in acciones_seleccionadas:
    ax.plot(df_real_filtrado.index, df_real_filtrado[accion], label=f'Real {accion}')

# Si el checkbox está activado, graficar los pronósticos
if mostrar_pronostico:
    for accion in acciones_seleccionadas:
        ax.plot(df_unido_filtrado.index, df_unido_filtrado[accion], label=f'Pronóstico {accion}', linestyle='--')

#grafica
ax.set_title(f'Comparación de Pronóstico vs Real (Del {fecha_inicio} al {fecha_fin})', fontsize=14)
ax.set_xlabel('Fecha', fontsize=12)
ax.set_ylabel('Precio de las Acciones', fontsize=12)
ax.legend(title="Acciones", fontsize=10)
ax.grid(True, linestyle='--', alpha=0.6)
plt.xticks(rotation=45)  
plt.tight_layout()

#show en streamlit
st.pyplot(fig)
