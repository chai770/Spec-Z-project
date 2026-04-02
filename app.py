import streamlit as st
import matplotlib.pyplot as plt
from sympy import symbols, Poly
from sympy.ntheory import prime_range

st.set_page_config(page_title="Spec(Z) Visualizer", layout="wide")

st.title("🧮 Number Field Spec(Z) Viewer")
st.sidebar.header("Parameters")

# User Inputs
poly_input = st.sidebar.text_input("Defining Polynomial (e.g., x^2 + 5)", "x^2 + 5")
max_p = st.sidebar.slider("Range of Primes (up to)", 5, 200, 50)
show_labels = st.sidebar.checkbox("Show e and f labels", True)

try:
    x = symbols('x')
    # Clean the input string and create a polynomial
    f_poly = Poly(poly_input.replace('^', '**'), x)
    
    # Setup Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    primes = list(prime_range(max_p))
    
    # Draw the base line representing Spec Z
    ax.axhline(0, color='black', linewidth=1.5, alpha=0.4, zorder=1)
    ax.text(-1, -0.2, "Spec(Z)", fontweight='bold', fontsize=10)

    for i, p in enumerate(primes):
        # The base point for the prime p
        ax.plot(i, 0, 'ko', markersize=3, zorder=2)
        ax.text(i, -0.6, str(p), ha='center', fontsize=9, rotation=45)

        # FACTORIZATION LOGIC:
        # We factor the polynomial f(x) modulo p. 
        # By the Dedekind-Kummer theorem, the factors correspond to 
        # the prime ideals lying above p.
        try:
            # factor_list() returns (constant, [(factor, multiplicity), ...])
            factors = Poly(f_poly, x, domain=f'GF({p})').factor_list()[1]
        except Exception:
            # Fallback for very small primes or edge cases
            factors = []

        num_ideals = len(factors)
        for j, (factor, e) in enumerate(factors):
            # f is the degree of the irreducible factor mod p
            f = factor.degree()
            
            # Spread the points out vertically so the "sheets" don't overlap
            y_pos = (j - (num_ideals - 1) / 2) * 0.8 + 1.5
            
            # VISUAL RULES:
            # e > 1: Ramified (Red)
            # e = 1: Unramified (Blue)
            # size: Larger for higher f (Inertial degree)
            color = 'crimson' if e > 1 else 'royalblue'
            size = 50 + (f * 70)
            
            ax.scatter(i, y_pos, s=size, color=color, edgecolor='white', linewidth=0.7, zorder=3)
            
            if show_labels:
                if e > 1:
                    ax.text(i, y_pos + 0.2, f"e={e}", color='crimson', fontsize=8, ha='center', fontweight='bold')
                if f > 1:
                    ax.text(i, y_pos - 0.35, f"f={f}", color='black', fontsize=8, ha='center')

    # Formatting the visual
    ax.set_ylim(-1.5, 4.5)
    ax.set_xlim(-1, len(primes))
    ax.axis('off')
    
    # Show the plot
    st.pyplot(fig)
    
    st.markdown("""
    ---
    ### How to read this diagram:
    - **Horizontal Axis:** Rational primes $p \in \mathbb{Z}$.
    - **Vertical Points:** Prime ideals $\mathfrak{P}$ in the ring of integers $\mathcal{O}_K$.
    - **Branching (Multiple dots):** The prime **splits**.
    - **Red Dots:** The prime is **ramified** (it 'collides' with itself, $e > 1$).
    - **Dot Size:** Larger dots mean the prime is **inert** or has a larger residue field ($f > 1$).
    """)

except Exception as err:
    st.error(f"Input Error: {err}")
    st.info("Try a simple monic polynomial like 'x^2 + 1' or 'x^3
