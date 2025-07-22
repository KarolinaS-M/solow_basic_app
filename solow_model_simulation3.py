
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# === Sidebar inputs ===
st.sidebar.header("Model parameters")
s = st.sidebar.slider("Savings rate (s)", min_value=0.01, max_value=0.99, value=0.18, step=0.01)
delta = st.sidebar.slider("Depreciation rate (δ)", min_value=0.001, max_value=0.2, value=0.03, step=0.001)
n = st.sidebar.slider("Population growth rate (n)", min_value=0.001, max_value=0.1, value=0.01, step=0.001)
alpha = st.sidebar.slider("Capital share (α)", min_value=0.01, max_value=0.99, value=1/3, step=0.01)
k0 = st.sidebar.number_input("Initial capital per worker (k₀)", value=10.0)
L0 = st.sidebar.number_input("Initial labor force (L₀)", value=30.0)
T = 1500  # Fixed number of periods

# === Simulation ===
def simulate_solow(T, s, delta, n, alpha, k0, L0):
    k, L = [k0], [L0]
    y, sy, c = [], [], []
    K, Y, sY, C = [], [], [], []

    for t in range(T):
        kt, Lt = k[t], L[t]
        yt = kt ** alpha
        syt = s * yt
        ct = (1 - s) * yt
        Kt, Yt = kt * Lt, yt * Lt
        sYt, Ct = syt * Lt, ct * Lt

        y.append(yt)
        sy.append(syt)
        c.append(ct)
        K.append(Kt)
        Y.append(Yt)
        sY.append(sYt)
        C.append(Ct)

        if t < T - 1:
            k_next = kt + (s * yt - (n + delta) * kt)
            L_next = Lt * (1 + n)
            k.append(k_next)
            L.append(L_next)

    return pd.DataFrame({
        "Period": np.arange(T),
        "k": k, "y": y, "sy": sy, "c": c,
        "L": L, "K": K, "Y": Y, "sY": sY, "C": C
    })

df = simulate_solow(T, s, delta, n, alpha, k0, L0)

# === Steady-state values ===
k_star = (s / (n + delta)) ** (1 / (1 - alpha))
y_star = k_star ** alpha
sy_star = s * y_star
c_star = (1 - s) * y_star

st.header("Steady-State Values (per capita)")
st.write(f"Capital per worker (k*): {k_star:.4f}")
st.write(f"Output per worker (y*): {y_star:.4f}")
st.write(f"Investment per worker (sy*): {sy_star:.4f}")
st.write(f"Consumption per worker (c*): {c_star:.4f}")

# === Selection ===
option = st.selectbox("Select variable group to plot:", ("Per capita", "Aggregate"))

# === Plotting ===
if option == "Per capita":
    var_map = {"k": "Capital per worker (k)", "y": "Output per worker (y)", 
               "sy": "Investment per worker (sy)", "c": "Consumption per worker (c)"}
    for var, label in var_map.items():
        fig, ax = plt.subplots()
        ax.plot(df["Period"], df[var])
        ax.set_title(label)
        ax.set_xlabel("Period")
        ax.set_ylabel(label)
        ax.grid(True)
        st.pyplot(fig)
else:
    st.subheader("Aggregate variables")
    fig, ax = plt.subplots()
    for var, label in zip(["K", "Y", "sY", "C"], ["K(t)", "Y(t)", "sY(t)", "C(t)"]):
        ax.plot(df["Period"], df[var], label=label)
    ax.set_title("Aggregate Variables Over Time")
    ax.set_xlabel("Period")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
