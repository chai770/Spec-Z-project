import streamlit as st
import matplotlib.pyplot as plt
from sympy import symbols, Poly, NumberField, prime_range
import numpy as np

st.set_page_config(page_title="Spec(Z) Visualizer", layout="wide")

st.title("🧮 Number Field Ramification Viewer")
st.sidebar.header("Parameters")

# User Inputs
poly_input = st.sidebar.text_input("Defining Polynomial (in x)", "x^2 + 5")
max_p = st.sidebar.slider("Range of Primes (up to)", 5, 200, 50)
show_labels = st.sidebar.checkbox("Show e and f labels", True)

try:
    x = symbols('x')
    f_poly = Poly(poly_input, x)
    
    # Setup Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    primes = list(prime_range(max_p))
    
    # Draw Spec Z line
    ax.axhline(0, color='black', linewidth=1.5, alpha=0.4)
    ax.text(-1, -0.2, "Spec(Z)", fontweight='bold')

    for i, p in enumerate(primes):
        # Base Prime Point
        ax.plot(i, 0, 'ko', markersize=3)
        ax.text(i, -0.5, str(p), ha='center', fontsize=8, rotation=45)

        # Factorization via Dedekind-Kummer (Poly mod p)
        factors = Poly(f_poly, x, domain=f'GF({p})').factor_list()[1]
        
        num_ideals = len(factors)
        for j, (factor, e) in enumerate(factors):
            f = factor.degree()
            # Vertical spread
            y_pos = (j - (num_ideals - 1) / 2) * 0.7 + 1.2
            
            # Visuals: Red for ramification, Blue for split/inert
            color = 'crimson' if e > 1 else 'royalblue'
            size = 40 + (f * 60)
            
            ax.scatter(i, y_pos, s=size, color=color, edgecolor='white', linewidth=0.5, zorder=3)
            
            if show_labels:
                if e > 1: ax.text(i, y_pos+0.15, f"e={e}", color='crimson', fontsize=7, ha='center')
                if f > 1: ax.text(i, y_pos-0.25, f"f={f}", color='black', fontsize=7, ha='center')

    ax.set_ylim(-1, 4)
    ax.set_xlim(-1, len(primes))
    ax.axis('off')
    st.pyplot(fig)
    
    st.caption("🔵 Blue: Unramified | 🔴 Red: Ramified | Size: Inertial degree (f)")

except Exception as err:
    st.error(f"Mathematical Error: {err}")
    st.info("Ensure the polynomial is monic and irreducible for best results (e.g., x^3 - 2).")
