"""Market equilibrium solver for various supply and demand curves."""

import sympy as sp
from .symbols import p, q


def market_equilibrium(demand_eq=None, supply_eq=None, parameter_subs=None):
    """
    Solve for market equilibrium given demand and supply equations.

    Args:
        demand_eq: Sympy equation for demand curve
        supply_eq: Sympy equation for supply curve
        parameter_subs: Dict of parameter substitutions

    Returns:
        Dict containing equilibrium price, quantity, surpluses, equations,
        and inverse demand function if it exists.
        None if solution cannot be found.
    """
    if demand_eq is None:
        print("Please provide a demand equation.")
        return None
    if supply_eq is None:
        print("Please provide a supply equation.")
        return None

    # Apply parameter substitutions if provided
    if parameter_subs:
        demand_eq = demand_eq.subs(parameter_subs)
        supply_eq = supply_eq.subs(parameter_subs)

    # Solve for equilibrium
    try:
        equilibrium = sp.solve([demand_eq, supply_eq], (p, q), dict=True)
    except Exception as e:
        print(f"An error occurred while solving for equilibrium: {e}")
        return None

    if not equilibrium:
        print("A symbolic solution for the equilibrium could not be found.")
        return None

    # Assuming the first solution is the desired one
    equilibrium = equilibrium[0]
    price_eq = equilibrium.get(p, None).simplify()
    quantity_eq = equilibrium.get(q, None).simplify()

    if price_eq is None or quantity_eq is None:
        print("Equilibrium price or quantity could not be determined.")
        return None

    # Demand and Supply Functions solved for q in terms of p
    try:
        demand_q = sp.solve(demand_eq, q)[0]
        supply_q = sp.solve(supply_eq, q)[0]
    except Exception as e:
        print(f"An error occurred while solving for q in terms of p: {e}")
        return None

    # Calculate inverse demand function (p in terms of q)
    try:
        inverse_demand_expr = sp.solve(demand_eq, p)[0].simplify()
        inverse_demand = sp.Eq(p, inverse_demand_expr)
    except Exception as e:
        inverse_demand = None
        print(f"Could not compute inverse demand function: {e}")

    # Initialize price bounds
    price_max = None
    price_min = None

    # Attempt to find price_max where demand_q = 0
    try:
        price_max_solutions = sp.solve(sp.Eq(demand_q, 0), p)
        price_max = sp.oo  # Default if no solution
        for sol in price_max_solutions:
            if sol.is_real:
                price_max = min(price_max, sol)
    except Exception as e:
        print(f"An error occurred while solving for price_max: {e}")

    # Attempt to find price_min where supply_q = 0
    try:
        price_min_solutions = sp.solve(sp.Eq(supply_q, 0), p)
        price_min = 0  # Default if no solution
        for sol in price_min_solutions:
            if sol.is_real:
                price_min = max(price_min, sol)
    except Exception as e:
        print(f"An error occurred while solving for price_min: {e}")

    # Calculate Consumer Surplus
    try:
        if price_max == sp.oo:
            cs = sp.oo
        else:
            cs = sp.integrate(demand_q - quantity_eq, (p, price_eq, price_max)).simplify()
    except Exception as e:
        cs = None
        print(f"Could not compute Consumer Surplus: {e}")

    # Calculate Producer Surplus
    try:
        ps = sp.integrate(quantity_eq - supply_q, (p, price_min, price_eq)).simplify()
    except Exception as e:
        ps = None
        print(f"Could not compute Producer Surplus: {e}")

    # Handle None case for total surplus
    total_surplus = None if cs is None or ps is None else sp.simplify(cs + ps)

    return {
        "Equilibrium Price": price_eq,
        "Equilibrium Quantity": quantity_eq,
        "Consumer Surplus": cs,
        "Producer Surplus": ps,
        "Total Surplus": total_surplus,
        "Demand Equation": demand_eq,
        "Supply Equation": supply_eq,
        "Inverse Demand Function": inverse_demand,
    }
