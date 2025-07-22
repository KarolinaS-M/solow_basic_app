import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# Title and Introduction
# -------------------------------
st.title("📈 Solow–Swan Growth Model Simulation")
st.write("""
This interactive app simulates the basic **Solow–Swan growth model** without technological progress.
You can adjust the model parameters using the sliders below.
""")

# -------------------------------
# User Inputs
# -------------------------------
st.sidebar.header("Model Parameters")

s = st.sidebar.slider("Savings rate (s)", min_value=0.0, max_value=1.0, value=0.3, step=0.01)
δ = st.sidebar.slider("Depreciation rate (δ)", min_value=0.0, max_value=0.2, value=0.05, step=0.005)
n = st.sidebar.slider("Population growth rate (n)", min_value=0.0, max_value=0.1, value=0.01, step=0.005)
α = st.sidebar.slider("Capital share in output (α)", min_value=0.0, max_value=1.0, value=0.3, step=0.01)
k0 = st.sidebar.slider("Initial capital per worker (k₀)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
T = st.sidebar.slider("Number of periods (T)", min_value=20, max_value=300, value=100, step=10)

# -------------------------------
# Model Calculation
# -------------------------------
k = np.zeros(T)
y = np.zeros(T)
c = np.zeros(T)
i = np.zeros(T)

k[0] = k0

for t in range(T - 1):
    y[t] = k[t]**α
    i[t] = s * y[t]
    c[t] = (1 - s) * y[t]
    k[t + 1] = k[t] + i[t] - δ * k[t] - n * k[t]

# last period values
y[-1] = k[-1]**α
i[-1] = s * y[-1]
c[-1] = (1 - s) * y[-1]

# -------------------------------
# Output Charts
# -------------------------------
st.subheader("Per capita variables over time")

fig1, ax1 = plt.subplots()
ax1.plot(k, label="Capital per worker (k)")
ax1.plot(y, label="Output per worker (y)", linestyle="--")
ax1.plot(c, label="Consumption per worker (c)", linestyle=":")
ax1.plot(i, label="Investment per worker (i)", linestyle="-.")
ax1.set_xlabel("Time")
ax1.set_ylabel("Level")
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)

# -------------------------------
# Steady State Info
# -------------------------------
k_star = (s / (δ + n))**(1 / (1 - α))
y_star = k_star**α
c_star = (1 - s) * y_star

st.subheader("📌 Steady-state values")
st.markdown(f"- Capital per worker (k*): **{k_star:.3f}**")
st.markdown(f"- Output per worker (y*): **{y_star:.3f}**")
st.markdown(f"- Consumption per worker (c*): **{c_star:.3f}**")
