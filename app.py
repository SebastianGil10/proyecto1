import pandas as pd
import scipy.stats
import streamlit as st
import time

# Inicializar variables de sesión
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

st.header('🎲 Lanzar una moneda (experimentos acumulados)')

# Mostrar gráfico base
chart = st.line_chart([0.5])

# Función que simula los lanzamientos
def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)
    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05)

    return mean

# Interfaz
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)

col1, col2 = st.columns(2)

with col1:
    start_button = st.button('🚀 Ejecutar experimento')

with col2:
    reset_button = st.button('🧹 Reiniciar historial')

# Ejecutar experimento
if start_button:
    st.write(f'📊 Ejecutando experimento #{st.session_state["experiment_no"] + 1} con {number_of_trials} lanzamientos...')
    mean = toss_coin(number_of_trials)

    # Guardar resultados
    st.session_state['experiment_no'] += 1
    nuevo_resultado = pd.DataFrame([[
        st.session_state['experiment_no'],
        number_of_trials,
        mean
    ]], columns=['no', 'iteraciones', 'media'])

    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        nuevo_resultado
    ], axis=0).reset_index(drop=True)

# Reiniciar historial
if reset_button:
    st.session_state['experiment_no'] = 0
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])
    st.success("✅ Historial reiniciado correctamente.")
