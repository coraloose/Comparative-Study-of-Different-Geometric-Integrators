# Geometric Integrators Platform

A Python MVP for your project:

**Visualization-Based Comparative Study of Geometric Integrators**

## Features
- Systems:
  - Simple Harmonic Oscillator
  - Pendulum
  - Two-Body / Kepler Problem (optional extension)
- Integrators:
  - Euler
  - Symplectic Euler
  - Verlet / Leapfrog
  - Implicit Midpoint
- Visual outputs:
  - Phase portrait / orbit
  - Energy deviation
  - Simple order / accuracy experiment

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project relevance
This code supports a project comparing non-symplectic and symplectic integrators on Hamiltonian systems.  
It is suitable as a strong starting point / MVP and can be extended with:
- better implicit solvers (Newton / secant),
- user evaluation,
- more systems,
- export of figures and data,
- improved validation against exact solutions.
