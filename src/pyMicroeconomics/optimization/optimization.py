"""
Module for optimizing economic parameters to maximize total surplus in market equilibrium models.
"""

import sympy as sp
import numpy as np
import scipy.optimize as opt
from ..core.symbols import p, q


def optimize_parameters(equilibrium_results):
    """
    Optimizes parameters to maximize total surplus.

    Args:
        equilibrium_results (dict): Dictionary containing demand and supply equations

    Returns:
        tuple: (optimal_values, param_ranges) where optimal_values is a dictionary of
        optimal parameter values and param_ranges contains feasible ranges for each parameter

    Raises:
        Exception: If no valid parameter values can be found
    """
    demand_eq = equilibrium_results["Demand Equation"]
    supply_eq = equilibrium_results["Supply Equation"]
    params = list((demand_eq.free_symbols | supply_eq.free_symbols) - {p, q})

    def evaluate_surplus(param_values):
        param_dict = dict(zip(params, param_values))
        demand_eq_num = demand_eq.subs(param_dict)
        supply_eq_num = supply_eq.subs(param_dict)

        try:
            # Get equilibrium point
            eq = sp.solve([demand_eq_num, supply_eq_num], (p, q), dict=True)
            if not eq:
                return float("inf")

            p_eq = float(sp.N(eq[0][p]))
            q_eq = float(sp.N(eq[0][q]))

            if p_eq <= 0 or q_eq <= 0:
                return float("inf")

            # Get demand and supply functions
            demand_q = sp.solve(demand_eq_num, q)[0]
            supply_q = sp.solve(supply_eq_num, q)[0]

            # Test if demand slope is negative and supply slope is positive
            # at equilibrium point
            try:
                demand_slope = float(sp.N(sp.diff(demand_q, p).subs(p, p_eq)))
                supply_slope = float(sp.N(sp.diff(supply_q, p).subs(p, p_eq)))
                if demand_slope >= 0 or supply_slope <= 0:
                    return float("inf")
            except (ValueError, TypeError):
                return float("inf")

            # Calculate surpluses using numerical integration
            try:
                p_max = p_eq * 2
                p_points = np.linspace(0, p_max, 1000)
                dp = p_points[1] - p_points[0]

                # Calculate demand quantities
                q_demand = [float(sp.N(demand_q.subs(p, pi))) for pi in p_points if pi >= p_eq]

                # Calculate supply quantities
                q_supply = [float(sp.N(supply_q.subs(p, pi))) for pi in p_points if pi <= p_eq]

                # Consumer surplus
                cs = sum((qd - q_eq) * dp for qd in q_demand)

                # Producer surplus
                ps = sum((q_eq - qs) * dp for qs in q_supply)

                total_surplus = cs + ps
                if total_surplus <= 0:
                    return float("inf")

                return -total_surplus  # Negative for maximization

            except (ValueError, TypeError):
                return float("inf")

        except (ValueError, TypeError):
            return float("inf")

    # Try multiple starting points
    best_result = None
    best_value = float("inf")

    # Initial guesses based on parameter names
    initial_guesses = []
    for scale in [0.1, 1.0, 10.0]:
        guess = []
        for param in params:
            if str(param) in ["a", "c"]:  # Intercepts
                guess.append(scale * 100)
            elif str(param) in ["b", "d"]:  # Slopes
                guess.append(scale)
            else:
                guess.append(scale * 10)
        initial_guesses.append(guess)

    for x0 in initial_guesses:
        try:
            # Set bounds based on parameter types
            bounds = []
            for param in params:
                if str(param) in ["a", "c"]:  # Intercepts
                    bounds.append((1.0, 1000.0))
                elif str(param) in ["b", "d"]:  # Slopes
                    bounds.append((0.01, 10.0))
                else:
                    bounds.append((0.01, 100.0))

            result = opt.minimize(
                evaluate_surplus,
                x0,
                bounds=bounds,
                method="Nelder-Mead",
                options={"maxiter": 10000},
            )

            if result.fun < best_value:
                best_result = result
                best_value = result.fun

        except Exception:
            print("Optimization attempt failed")
            continue

    if best_result is None or best_result.fun == float("inf"):
        raise Exception("Could not find valid parameter values")

    # Get optimal values
    optimal_values = dict(zip(params, best_result.x))

    # Find feasible ranges around optimal values
    param_ranges = {}
    for param in params:
        opt_val = optimal_values[param]

        # Set range based on parameter type and optimal value
        if str(param) in ["a", "c"]:  # Intercepts
            param_ranges[param] = (max(1.0, opt_val * 0.5), opt_val * 2.0)
        elif str(param) in ["b", "d"]:  # Slopes
            param_ranges[param] = (max(0.01, opt_val * 0.5), min(10.0, opt_val * 2.0))
        else:
            param_ranges[param] = (max(0.01, opt_val * 0.5), min(100.0, opt_val * 2.0))

    return optimal_values, param_ranges
