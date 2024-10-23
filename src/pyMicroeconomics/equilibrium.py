"""Market equilibrium solver for various supply and demand curves."""

import logging
from typing import Dict, Optional, Union
import sympy as sp
from .symbols import p, q
from .equation_types import TypedEquation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Type aliases
EquilibriumResult = Dict[str, Union[sp.Expr, str, float, TypedEquation]]
ParameterDict = Dict[sp.Symbol, Union[float, int]]


def market_equilibrium(
    demand_eq: Optional[TypedEquation] = None,
    supply_eq: Optional[TypedEquation] = None,
    parameter_subs: Optional[ParameterDict] = None,
) -> Optional[EquilibriumResult]:
    """
    Solve for market equilibrium given demand and supply equations.

    Args:
        demand_eq: TypedEquation representing the demand curve
        supply_eq: TypedEquation representing the supply curve
        parameter_subs: Dictionary of parameter substitutions for numerical evaluation

    Returns:
        Dictionary containing equilibrium results including:
            - Equilibrium Price
            - Equilibrium Quantity
            - Consumer Surplus
            - Producer Surplus
            - Total Surplus
            - Demand Equation
            - Supply Equation
            - Inverse Demand Function
            - Demand Type
            - Supply Type
        Returns None if no valid equilibrium is found.

    Raises:
        ValueError: If demand or supply equations are missing or invalid
    """
    if demand_eq is None:
        raise ValueError("Please provide a demand equation.")
    if supply_eq is None:
        raise ValueError("Please provide a supply equation.")

    logger.debug("Starting market equilibrium calculation")

    try:
        # Store the types and equations
        demand_type = demand_eq.function_type
        supply_type = supply_eq.function_type
        demand_equation = demand_eq.equation
        supply_equation = supply_eq.equation

        logger.debug("Processing demand type %s and supply type %s", demand_type, supply_type)

        # Apply parameter substitutions if provided
        if parameter_subs:
            demand_equation = demand_equation.subs(parameter_subs)
            supply_equation = supply_equation.subs(parameter_subs)

        # Solve for equilibrium
        try:
            equilibrium = sp.solve([demand_equation, supply_equation], (p, q), dict=True)
            if not equilibrium:
                logger.warning("No equilibrium solution found")
                return None
        except Exception as e:
            logger.error("Error solving equilibrium: %s", str(e))
            return None

        # Get first solution (assuming it's the economically relevant one)
        equilibrium = equilibrium[0]
        price_eq = equilibrium[p]
        quantity_eq = equilibrium[q]

        logger.debug("Found equilibrium - Price: %s, Quantity: %s", price_eq, quantity_eq)

        try:
            # Get expressions for demand and supply
            demand_q = sp.solve(demand_equation, q)[0]
            supply_q = sp.solve(supply_equation, q)[0]

            # Calculate inverse demand function
            try:
                inverse_demand = sp.solve(demand_equation, p)[0].simplify()
            except Exception as e:
                logger.warning("Could not compute inverse demand function: %s", e)
                inverse_demand = None

            # Initialize price bounds
            price_max = sp.oo
            price_min = 0

            # Find price_max where demand_q = 0
            try:
                price_max_solutions = sp.solve(sp.Eq(demand_q, 0), p)
                for sol in price_max_solutions:
                    if isinstance(sol, sp.Expr) and sol.is_real:
                        price_max = min(price_max, sol)
            except Exception as e:
                logger.warning("Could not compute price_max: %s", e)

            # Find price_min where supply_q = 0
            try:
                price_min_solutions = sp.solve(sp.Eq(supply_q, 0), p)
                for sol in price_min_solutions:
                    if isinstance(sol, sp.Expr) and sol.is_real:
                        price_min = max(price_min, sol)
            except Exception as e:
                logger.warning("Could not compute price_min: %s", e)

            # Calculate Consumer Surplus
            try:
                if price_max == sp.oo:
                    cs = sp.oo
                else:
                    cs = sp.integrate(demand_q - quantity_eq, (p, price_eq, price_max))
                    if cs != sp.oo:
                        cs = cs.simplify()
            except Exception as e:
                logger.warning("Could not compute Consumer Surplus: %s", e)
                cs = None

            # Calculate Producer Surplus
            try:
                ps = sp.integrate(quantity_eq - supply_q, (p, price_min, price_eq))
                ps = ps.simplify()
            except Exception as e:
                logger.warning("Could not compute Producer Surplus: %s", e)
                ps = None

            # Calculate Total Surplus
            if cs is not None and ps is not None and cs != sp.oo:
                total_surplus = cs + ps
                total_surplus = total_surplus.simplify()
            else:
                total_surplus = sp.oo if cs == sp.oo else None

            # Compile results
            result: EquilibriumResult = {
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

            logger.debug("Successfully created result dictionary")
            return result

        except Exception as e:
            logger.error("Error calculating surpluses: %s", str(e))
            return None

    except Exception as e:
        logger.error("Error in market_equilibrium: %s", str(e))
        return None


def validate_equilibrium(equilibrium_result: Optional[EquilibriumResult]) -> bool:
    """
    Validate the economic sensibility of equilibrium results.

    Args:
        equilibrium_result: Dictionary containing equilibrium calculations

    Returns:
        bool: True if equilibrium is economically valid, False otherwise
    """
    if equilibrium_result is None:
        return False

    try:
        price_eq = equilibrium_result["Equilibrium Price"]
        quantity_eq = equilibrium_result["Equilibrium Quantity"]

        # Check for positive price and quantity
        if not (isinstance(price_eq, sp.Expr) and isinstance(quantity_eq, sp.Expr)):
            return False

        if price_eq.is_negative or quantity_eq.is_negative:
            return False

        # Check if surpluses are non-negative when finite
        cs = equilibrium_result["Consumer Surplus"]
        ps = equilibrium_result["Producer Surplus"]

        if isinstance(cs, sp.Expr) and cs != sp.oo and cs.is_negative:
            return False
        if isinstance(ps, sp.Expr) and ps != sp.oo and ps.is_negative:
            return False

        return True

    except (KeyError, AttributeError):
        return False
