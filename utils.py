import numpy as np
from integrators import INTEGRATORS


def simulate(system, method_name, q0, p0, h, steps):
    """
    Run a trajectory and return time series.
    Shapes:
      - scalar systems -> q_hist, p_hist are 1D arrays
      - vector systems -> q_hist, p_hist are 2D arrays [step, dim]
    """
    stepper = INTEGRATORS[method_name]
    q = np.array(q0, dtype=float)
    p = np.array(p0, dtype=float)

    q_hist = [q.copy()]
    p_hist = [p.copy()]
    e_hist = [float(system.energy(q, p))]
    t_hist = [0.0]

    for i in range(steps):
        q, p = stepper(q, p, h, system.dqdt, system.dpdt)
        q_hist.append(q.copy())
        p_hist.append(p.copy())
        e_hist.append(float(system.energy(q, p)))
        t_hist.append((i + 1) * h)

    return (
        np.array(t_hist),
        np.array(q_hist),
        np.array(p_hist),
        np.array(e_hist),
    )


def final_error_against_reference(system, method_name, q0, p0, h, tfinal, refinement=20):
    """
    Estimate global error by comparing with a very fine reference solution.
    """
    coarse_steps = int(round(tfinal / h))
    if coarse_steps < 1:
        raise ValueError("Need at least one time step.")

    h_ref = h / refinement
    ref_steps = coarse_steps * refinement

    _, q_c, p_c, _ = simulate(system, method_name, q0, p0, h, coarse_steps)
    _, q_r, p_r, _ = simulate(system, method_name, q0, p0, h_ref, ref_steps)

    q_err = np.linalg.norm(np.asarray(q_c[-1]) - np.asarray(q_r[-1]))
    p_err = np.linalg.norm(np.asarray(p_c[-1]) - np.asarray(p_r[-1]))
    return float(np.sqrt(q_err**2 + p_err**2))


def estimate_order(system, method_name, q0, p0, tfinal, h_values):
    """
    Return errors for a range of h values.
    A log-log slope of about 1 suggests first order, about 2 suggests second order.
    """
    errors = []
    for h in h_values:
        errors.append(final_error_against_reference(system, method_name, q0, p0, h, tfinal))
    return np.array(h_values, dtype=float), np.array(errors, dtype=float)
