"""Market equilibrium solver for various supply and demand curves."""

import sympy as sp
from .symbols import p, q


def market_equilibrium(demand_eq=None, supply_eq=None, parameter_subs=None):
    """Solve for market equilibrium given demand and supply equations."""
    if demand_eq is None:
        print("Please provide a demand equation.")
        return None
    if supply_eq is None:
        print("Please provide a supply equation.")
        return None

    # print("DEBUG: Starting market_equilibrium")
    # print(f"DEBUG: Demand equation type: {type(demand_eq)}")
    # print(f"DEBUG: Supply equation type: {type(supply_eq)}")
    # print(f"DEBUG: Demand function type: {getattr(demand_eq, 'function_type', None)}")
    # print(f"DEBUG: Supply function type: {getattr(supply_eq, 'function_type', None)}")

    try:
        # Store the types and equations
        demand_type = demand_eq.function_type
        supply_type = supply_eq.function_type
        demand_equation = demand_eq.equation
        supply_equation = supply_eq.equation

        print(f"DEBUG: Successfully extracted types - Demand: {demand_type}, Supply: {supply_type}")

        # Apply parameter substitutions if provided
        if parameter_subs:
            demand_equation = demand_equation.subs(parameter_subs)
            supply_equation = supply_equation.subs(parameter_subs)

        # Solve for equilibrium
        try:
            equilibrium = sp.solve([demand_equation, supply_equation], (p, q), dict=True)
            print(f"DEBUG: Solved equilibrium: {equilibrium}")
        except Exception as e:
            print(f"Error solving equilibrium: {str(e)}")
            return None

        if not equilibrium:
            print("No equilibrium solution found")
            return None

        # Get first solution
        equilibrium = equilibrium[0]
        price_eq = equilibrium[p]
        quantity_eq = equilibrium[q]

        # print(f"DEBUG: Found equilibrium - Price: {price_eq}, Quantity: {quantity_eq}")

        try:
            # Get expressions for demand and supply
            demand_q = sp.solve(demand_equation, q)[0]
            supply_q = sp.solve(supply_equation, q)[0]

            # Calculate inverse demand function
            try:
                inverse_demand = sp.solve(demand_equation, p)[0].simplify()
            except Exception as e:
                print(f"Could not compute inverse demand function: {e}")
                inverse_demand = None

            # Initialize price bounds
            price_max = None
            price_min = None

            # Find price_max where demand_q = 0
            try:
                price_max_solutions = sp.solve(sp.Eq(demand_q, 0), p)
                price_max = sp.oo  # Default if no solution
                for sol in price_max_solutions:
                    if sol.is_real:
                        price_max = min(price_max, sol)
            except Exception as e:
                print(f"Could not compute price_max: {e}")

            # Find price_min where supply_q = 0
            try:
                price_min_solutions = sp.solve(sp.Eq(supply_q, 0), p)
                price_min = 0  # Default if no solution
                for sol in price_min_solutions:
                    if sol.is_real:
                        price_min = max(price_min, sol)
            except Exception as e:
                print(f"Could not compute price_min: {e}")

            # Calculate Consumer Surplus
            try:
                if price_max == sp.oo:
                    cs = sp.oo
                else:
                    cs = sp.integrate(demand_q - quantity_eq, (p, price_max, price_eq))
                if cs != sp.oo:
                    cs = cs.simplify()
            except Exception as e:
                print(f"Could not compute Consumer Surplus: {e}")
                cs = None

            # Calculate Producer Surplus
            try:
                ps = sp.integrate(quantity_eq - supply_q, (p, price_min, price_eq))
                ps = ps.simplify()
            except Exception as e:
                print(f"Could not compute Producer Surplus: {e}")
                ps = None

            # Calculate Total Surplus
            if cs is not None and ps is not None and cs != sp.oo:
                total_surplus = cs + ps
                total_surplus = total_surplus.simplify()
            else:
                total_surplus = sp.oo if cs == sp.oo else None

            result = {
                "Equilibrium Price": price_eq,
                "Equilibrium Quantity": quantity_eq,
                "Consumer Surplus": cs,
                "Producer Surplus": ps,
                "Total Surplus": total_surplus,
                "Demand Equation": demand_equation,
                "Supply Equation": supply_equation,
                "Inverse Demand Function": inverse_demand,
                "Demand Type": demand_type,
                "Supply Type": supply_type,
            }

            # print("DEBUG: Successfully created result dictionary with surplus calculations")
            return result

        except Exception as e:
            print(f"Error calculating surpluses: {str(e)}")
            traceback.print_exc()
            return None

    except Exception as e:
        print(f"Error in market_equilibrium: {str(e)}")
        traceback.print_exc()
        return None
