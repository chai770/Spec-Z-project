import streamlit as st
import matplotlib.pyplot as plt
from sympy import symbols, Poly
from sympy.ntheory import prime_range

# Use a simpler layout to avoid script runner context issues
st.title("🧮 Number Field Spec(Z) Viewer")

# Sidebar
poly_input = st.sidebar.text_input("Defining Polynomial", "x**2 + 5")
max_p = st.sidebar.slider("Range of Primes", 5, 200, 50)
show_labels = st.sidebar.checkbox("Show e and f labels", True)

try:
    x = symbols('x')
    # Use double asterisk for powers and ensure string is clean
    clean_poly = poly_input.replace('^', '**')
    f_poly = Poly(clean_poly, x)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    primes = list(prime_range(max_p))
    
    ax.axhline(0, color='black', linewidth=1.5, alpha=0.4)
    ax.text(-1, -0.2, "Spec(Z)", fontweight='bold')

    for i, p in enumerate(primes):
        ax.plot(i, 0, 'ko', markersize=3)
        ax.text(i, -0.6, str(p), ha='center', fontsize=8, rotation=45)

        try:
            # Dedekind-Kummer factorization
            factors = Poly(f_poly, x, domain=f'GF({p})').factor_list()[1]
        except:
            factors = []

        num_ideals = len(factors)
        for j, (factor, e) in enumerate(factors):
            f = factor.degree()
            y_pos = (j - (num_ideals - 1) / 2) * 0.7 + 1.2
            
            color = 'crimson' if e > 1 else 'royalblue'
            size = 50 + (f * 60)
            
            ax.scatter(i, y_pos, s=size, color=color, edgecolor='white', linewidth=0.5)
            
            if show_labels:
                if e > 1: ax.text(i, y_pos+0.2, f"e={e}", color='crimson', fontsize=7, ha='center')
                if f > 1: ax.text(i, y_pos-0.3, f"f={f}", color='black', fontsize=7, ha='center')

    ax.set_ylim(-1.5, 4.5)
    ax.set_xlim(-1, len(primes))
    ax.axis('off')
    st.pyplot(fig)
    
    # Using individual markdown lines to avoid the "Unterminated String" error
    st.markdown("---")
    st.markdown("**🔵 Blue Points:** Unramified ($e=1$)")
    st.markdown("**🔴 Red Points:** Ramified ($e > 1$)")
    st.markdown("**Size:** Represents Inertial Degree ($f$)")

except Exception as e:
    st.error(f"Error: {e}")
