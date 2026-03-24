import numpy as np
import plotly.graph_objects as go
import streamlit as st

from systems import SYSTEMS
from utils import simulate, estimate_order


st.set_page_config(page_title="Geometric Integrators Platform", layout="wide")
st.title("Visualization-Based Comparative Study of Geometric Integrators")

st.markdown(
    """
This app compares **Euler**, **Symplectic Euler**, **Verlet / Leapfrog**, and
**Implicit Midpoint** on simple Hamiltonian systems.

Recommended systems for your project:
- Simple Harmonic Oscillator
- Pendulum
- (Optional) Two-Body / Kepler Problem
"""
)

system_name = st.sidebar.selectbox("System", list(SYSTEMS.keys()))
method = st.sidebar.selectbox(
    "Integrator",
    ["Euler", "Symplectic Euler", "Verlet / Leapfrog", "Implicit Midpoint"],
)
h = st.sidebar.slider("Step size h", 0.001, 0.2, 0.05, 0.001)
tfinal = st.sidebar.slider("Final time", 1.0, 100.0, 20.0, 1.0)

system = SYSTEMS[system_name]()

if system_name == "Simple Harmonic Oscillator":
    q0 = st.sidebar.number_input("q0", value=1.0, format="%.4f")
    p0 = st.sidebar.number_input("p0", value=0.0, format="%.4f")
elif system_name == "Pendulum":
    q0 = st.sidebar.number_input("theta0", value=1.0, format="%.4f")
    p0 = st.sidebar.number_input("p0", value=0.0, format="%.4f")
else:
    qx = st.sidebar.number_input("q0_x", value=1.0, format="%.4f")
    qy = st.sidebar.number_input("q0_y", value=0.0, format="%.4f")
    px = st.sidebar.number_input("p0_x", value=0.0, format="%.4f")
    py = st.sidebar.number_input("p0_y", value=1.0, format="%.4f")
    q0 = np.array([qx, qy], dtype=float)
    p0 = np.array([px, py], dtype=float)

steps = int(round(tfinal / h))

t, q_hist, p_hist, e_hist = simulate(system, method, q0, p0, h, steps)
energy_dev = e_hist - e_hist[0]

if system_name in ("Simple Harmonic Oscillator", "Pendulum"):
    q_label, p_label = system.state_labels()
    col1, col2 = st.columns(2)

    with col1:
        fig_phase = go.Figure()
        fig_phase.add_trace(go.Scatter(x=q_hist, y=p_hist, mode="lines", name=method))
        fig_phase.update_layout(
            title="Phase Portrait",
            xaxis_title=q_label,
            yaxis_title=p_label,
        )
        st.plotly_chart(fig_phase, use_container_width=True)

    with col2:
        fig_e = go.Figure()
        fig_e.add_trace(go.Scatter(x=t, y=energy_dev, mode="lines", name="ΔE"))
        fig_e.update_layout(
            title="Energy Deviation",
            xaxis_title="time",
            yaxis_title="E(t) - E(0)",
        )
        st.plotly_chart(fig_e, use_container_width=True)

else:
    col1, col2 = st.columns(2)

    with col1:
        fig_orbit = go.Figure()
        fig_orbit.add_trace(go.Scatter(x=q_hist[:, 0], y=q_hist[:, 1], mode="lines", name=method))
        fig_orbit.update_layout(
            title="Orbit",
            xaxis_title="x",
            yaxis_title="y",
            yaxis_scaleanchor="x",
            yaxis_scaleratio=1,
        )
        st.plotly_chart(fig_orbit, use_container_width=True)

    with col2:
        fig_e = go.Figure()
        fig_e.add_trace(go.Scatter(x=t, y=energy_dev, mode="lines", name="ΔE"))
        fig_e.update_layout(
            title="Energy Deviation",
            xaxis_title="time",
            yaxis_title="E(t) - E(0)",
        )
        st.plotly_chart(fig_e, use_container_width=True)

st.subheader("Order / Accuracy Experiment")
st.write(
    "This estimates the convergence order by comparing final states against a finer reference solution."
)

if st.button("Run order test"):
    h_values = [0.2, 0.1, 0.05, 0.025]
    h_vals, errs = estimate_order(system, method, q0, p0, min(10.0, tfinal), h_values)

    fig_order = go.Figure()
    fig_order.add_trace(go.Scatter(x=h_vals, y=errs, mode="lines+markers", name="Error"))
    fig_order.update_layout(
        title="Error vs Step Size",
        xaxis_title="h",
        yaxis_title="Final state error",
    )
    st.plotly_chart(fig_order, use_container_width=True)

    st.dataframe({"h": h_vals, "error": errs})

st.info(
    "Expected behaviour: Euler usually shows energy drift. Symplectic Euler and Verlet should "
    "keep the energy error bounded on Hamiltonian systems."
)
