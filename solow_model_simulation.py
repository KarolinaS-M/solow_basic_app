
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# === Model parameters ===
T = 1500  # number of periods
s = 0.18  # savings rate
delta = 0.03  # depreciation rate
n = 0.01  # population growth rate
alpha = 1/3  # capital share in output
k0 = 10.0  # initial capital per worker
L0 = 30.0  # initial labor force

# === Solow-Swan simulation function ===
def simulate_solow(T, s, delta, n, alpha, k0, L0):
    k = [k0]
    L = [L0]
    y = []
    sy = []
    c = []
    K = []
    Y = []
    sY = []
    C = []

    for t in range(T):
        kt = k[t]
        Lt = L[t]
        yt = kt ** alpha
        syt = s * yt
        ct = (1 - s) * yt
        Kt = kt * Lt
        Yt = yt * Lt
        sYt = syt * Lt
        Ct = ct * Lt

        y.append(yt)
        sy.append(syt)
        c.append(ct)
        K.append(Kt)
        Y.append(Yt)
        sY.append(sYt)
        C.append(Ct)

        if t < T - 1:
            k_next = kt + (s * yt - (n + delta) * kt)  # Euler step
            L_next = Lt * (1 + n)
            k.append(k_next)
            L.append(L_next)

    return pd.DataFrame({
        "Period": np.arange(T),
        "k": k,
        "y": y,
        "sy": sy,
        "c": c,
        "L": L,
        "K": K,
        "Y": Y,
        "sY": sY,
        "C": C
    })

# === Compute simulation and steady state values ===
df = simulate_solow(T, s, delta, n, alpha, k0, L0)
k_star = (s / (n + delta)) ** (1 / (1 - alpha))
y_star = k_star ** alpha
sy_star = s * y_star
c_star = (1 - s) * y_star

print("=== Steady State Values ===")
print(f"k*  = {k_star:.4f}")
print(f"y*  = {y_star:.4f}")
print(f"sy* = {sy_star:.4f}")
print(f"c*  = {c_star:.4f}")

# === Plot per capita variables (separate plots) ===
for var, label in zip(["k", "y", "sy", "c"], ["k(t)", "y(t)", "sy(t)", "c(t)"]):
    plt.figure(figsize=(8, 4))
    plt.plot(df["Period"], df[var], label=label)
    plt.title(f"{label} over time")
    plt.xlabel("Period")
    plt.ylabel(label)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# === Plot aggregated variables (one figure) ===
plt.figure(figsize=(10, 5))
for var, label in zip(["K", "Y", "sY", "C"], ["K(t)", "Y(t)", "sY(t)", "C(t)"]):
    plt.plot(df["Period"], df[var], label=label)
plt.title("Aggregated variables over time")
plt.xlabel("Period")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
