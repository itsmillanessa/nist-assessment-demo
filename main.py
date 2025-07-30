# VERSIÓN DE DEBUG - Guarda esto como debug_app.py
import streamlit as st

# Test básico
st.title("🛡️ Test de Fortinet App")
st.write("Si ves esto, Streamlit funciona básicamente.")

# Test de imports
try:
    import pandas as pd
    st.success("✅ Pandas importado correctamente")
except Exception as e:
    st.error(f"❌ Error con Pandas: {e}")

try:
    import plotly.express as px
    import plotly.graph_objects as go
    st.success("✅ Plotly importado correctamente")
except Exception as e:
    st.error(f"❌ Error con Plotly: {e}")

try:
    import numpy as np
    st.success("✅ Numpy importado correctamente")
except Exception as e:
    st.warning(f"⚠️ Numpy no disponible: {e}")
    st.info("La app puede funcionar sin numpy")

# Test de session state
if 'test' not in st.session_state:
    st.session_state.test = "Funciona"

st.write(f"Session State: {st.session_state.test}")

# Test básico de gráfico
try:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], mode='markers'))
    fig.update_layout(title="Test de Gráfico Básico")
    st.plotly_chart(fig)
    st.success("✅ Gráficos Plotly funcionan")
except Exception as e:
    st.error(f"❌ Error con gráficos: {e}")

# Botón de test
if st.button("Test Button"):
    st.balloons()
    st.success("¡Los botones funcionan!")

st.markdown("---")
st.info("Si todo aparece en verde ✅, tu entorno está listo para la app completa.")
