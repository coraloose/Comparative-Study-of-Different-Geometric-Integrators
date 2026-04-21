# Comparative Study of Different Geometric Integrators

This repository contains the implementation developed for my final-year project:

**Comparative Study of Different Geometric Integrators**

The project investigates the long-term numerical behaviour of several integrators for Hamiltonian systems through an interactive visualisation platform built with Streamlit.

## Environment requirements
- Python 3.12
- pip
- Recommended: a virtual environment

## Included benchmark systems
- Simple Harmonic Oscillator
- Pendulum
- Kepler Problem

## Implemented integrators
- Explicit Euler
- Symplectic Euler
- Verlet / Leapfrog
- Implicit Midpoint

## Visual outputs
- Phase portrait / orbit plot
- Energy deviation plot
- Order / accuracy experiment

## Installation
Clone the repository:
```bash
git clone https://github.com/coraloose/Comparative-Study-of-Different-Geometric-Integrators.git
cd Comparative-Study-of-Different-Geometric-Integrators
```

Create a virtual environment:
```bash
py -3.12 -m venv .venv
```

Activate the virtual environment on Windows:
```bash
.venv\Scripts\Activate.ps1
```

Activate the virtual environment on macOS / Linux:
```bash
source .venv/bin/activate
```

Install dependencies:
```bash
pip install numpy streamlit plotly
```

## Run
```bash
streamlit run app.py
```
## Project purpose
The platform is used to compare non-symplectic and geometric integrators on representative Hamiltonian systems. It supports both qualitative and quantitative evaluation through:
- trajectory visualisation
- long-term energy behaviour
- step-size error comparison

## Repository structure
- `app.py` - Streamlit interface
- `systems.py` - benchmark system definitions
- `integrators.py` - numerical integrators
- `utils.py` - simulation and error-estimation utilities


## Notes
- The Implicit Midpoint method is implemented using fixed-point iteration.
- The Kepler problem is included as the most demanding benchmark case in the project.
