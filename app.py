"""Aplicación Streamlit que simula lanzamientos de una moneda."""

import time  # ✔ Import estándar primero
import pandas as pd  # ✔ Luego los de terceros
import scipy.stats
import streamlit as st

# Estas son variables de estado que se conservan entre ejecuciones
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(
        columns=['no', 'iteraciones', 'media']
    )

st.header('🎲 Lanzar una moneda (experimentos acumulados)')

# Mostrar gráfico base
line_chart = st.line_chart([0.5])  # ✔ Renombrado para evitar conflicto de nombre

def toss_coin(n):
    """Simula el lanzamiento de una moneda n veces y grafica la media acumulada."""
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    total_lanzamientos = 0
    total_caras = 0
    media = 0

    for resultado in trial_outcomes:
        total_lanzamientos += 1
        if resultado == 1:
            total_caras += 1
        media = total_caras / total_lanzamientos
        line_chart.add_rows([media])
        time.sleep(0.05)

    return media

# Interfaz
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)

col1, col2 = st.columns(2)

with col1:
    start_button = st.button('🚀 Ejecutar experimento')

with col2:
    reset_button = st.button('🧹 Reiniciar historial')

# Ejecutar experimento
if start_button:
    st.write(
        f'📊 Ejecutando experimento #{st.session_state["experiment_no"] + 1} '
        f'con {number_of_trials} lanzamientos...'
    )
    resultado_media = toss_coin(number_of_trials)

    # Guardar resultados
    st.session_state['experiment_no'] += 1
    nuevo_resultado = pd.DataFrame(
        [[st.session_state['experiment_no'], number_of_trials, resultado_media]],
        columns=['no', 'iteraciones', 'media']
    )

    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        nuevo_resultado
    ], axis=0).reset_index(drop=True)

# Reiniciar historial
if reset_button:
    st.session_state['experiment_no'] = 0
    st.session_state['df_experiment_results'] = pd.DataFrame(
        columns=['no', 'iteraciones', 'media']
    )
    st.success("✅ Historial reiniciado correctamente..")

# Mostrar resultados
st.write(st.session_state['df_experiment_results'])

