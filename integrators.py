import numpy as np


def euler_step(q, p, h, dqdt, dpdt):
    """Explicit Euler (non-symplectic baseline)."""
    q = np.asarray(q, dtype=float)
    p = np.asarray(p, dtype=float)
    return q + h * dqdt(q, p), p + h * dpdt(q, p)


def symplectic_euler_step(q, p, h, dqdt, dpdt):
    """
    Semi-implicit / symplectic Euler.
    First update p using q_n, then update q using p_{n+1}.
    """
    q = np.asarray(q, dtype=float)
    p = np.asarray(p, dtype=float)
    p_new = p + h * dpdt(q, p)
    q_new = q + h * dqdt(q, p_new)
    return q_new, p_new


def verlet_step(q, p, h, dqdt, dpdt):
    """
    Velocity-Verlet / Leapfrog style update.
    Works best for separable Hamiltonian systems H(q,p)=T(p)+V(q).
    """
    q = np.asarray(q, dtype=float)
    p = np.asarray(p, dtype=float)

    p_half = p + 0.5 * h * dpdt(q, p)
    q_new = q + h * dqdt(q, p_half)
    p_new = p_half + 0.5 * h * dpdt(q_new, p_half)
    return q_new, p_new


def implicit_midpoint_step(q, p, h, dqdt, dpdt, max_iter=20, tol=1e-12):
    """
    Implicit midpoint method solved by fixed-point iteration.
    Good enough for an educational/demo platform.
    """
    q = np.asarray(q, dtype=float)
    p = np.asarray(p, dtype=float)

    q_new = q.copy()
    p_new = p.copy()

    for _ in range(max_iter):
        q_mid = 0.5 * (q + q_new)
        p_mid = 0.5 * (p + p_new)
        q_next = q + h * dqdt(q_mid, p_mid)
        p_next = p + h * dpdt(q_mid, p_mid)

        err = max(np.linalg.norm(q_next - q_new), np.linalg.norm(p_next - p_new))
        q_new, p_new = q_next, p_next
        if err < tol:
            break

    return q_new, p_new


INTEGRATORS = {
    "Euler": euler_step,
    "Symplectic Euler": symplectic_euler_step,
    "Verlet / Leapfrog": verlet_step,
    "Implicit Midpoint": implicit_midpoint_step,
}
