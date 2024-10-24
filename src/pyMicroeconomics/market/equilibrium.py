"""Market equilibrium solver for various supply and demand curves."""

import logging
from typing import Dict, Optional, Union, TypedDict
import sympy as sp
from core.symbols import p, q
from core.equation_types import TypedEquation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Type definitions
ParameterDict = Dict[sp.Symbol, Union[float, int]]


class EquilibriumResult(TypedDict):
    """Type definition for equilibrium calculation results."""

    Equilibrium_Price: sp.Expr
    Equilibrium_Quantity: sp.Expr
    Consumer_Surplus: Optional[sp.Expr]
    Producer_Surplus: Optional[sp.Expr]
    Total_Surplus: Optional[sp.Expr]
    Demand_Equation: sp.Equality
    Supply_Equation: sp.Equality
    Inverse_Demand_Function: Optional[sp.Expr]
    Demand_Type: str
    Supply_Type: str


def market_equilibrium(
    demand_eq: Optional[TypedEquation] = None,
    supply_eq: Optional[TypedEquation] = None,
    parameter_subs: Optional[ParameterDict] = None,
) -> Optional[EquilibriumResult]:
    """Solve for market equilibrium given demand and supply equations."""
    if demand_eq is None or supply_eq is None:
        raise ValueError("Please provide both demand and supply equations.")

    try:
        # Store the types and equations
        demand_type = demand_eq.function_type
        supply_type = supply_eq.function_type
        demand_equation = demand_eq.equation
        supply_equation = supply_eq.equation

        # Apply parameter substitutions if provided
        if parameter_subs:
            demand_equation = demand_equation.subs(parameter_subs)
            supply_equation = supply_equation.subs(parameter_subs)

        # Solve for equilibrium
        equilibrium = sp.solve([demand_equation, supply_equation], (p, q), dict=True)
        if not equilibrium:
            return None

        # Get first solution (assuming it's the economically relevant one)
        equilibrium = equilibrium[0]
        price_eq = equilibrium[p]
        quantity_eq = equilibrium[q]

        # Get expressions for demand and supply
        demand_q = sp.solve(demand_equation, q)[0]
        supply_q = sp.solve(supply_equation, q)[0]

        # Calculate inverse demand function
        try:
            inverse_demand = sp.solve(demand_equation, p)[0].simplify()
        except Exception:
            inverse_demand = None

        # Calculate Consumer Surplus
        try:
            cs = sp.integrate(demand_q - quantity_eq, (p, price_eq, sp.oo))
            cs = cs.simplify() if cs != sp.oo else cs
        except Exception:
            cs = None

        # Calculate Producer Surplus
        try:
            ps = sp.integrate(quantity_eq - supply_q, (p, 0, price_eq))
            ps = ps.simplify()
        except Exception:
            ps = None

        # Calculate Total Surplus
        total_surplus = None
        if cs is not None and ps is not None and cs != sp.oo:
            total_surplus = (cs + ps).simplify()
        elif cs == sp.oo:
            total_surplus = sp.oo

        result: EquilibriumResult = {
            "Equilibrium_Price": price_eq,
            "Equilibrium_Quantity": quantity_eq,
            "Consumer_Surplus": cs,
            "Producer_Surplus": ps,
            "Total_Surplus": total_surplus,
            "Demand_Equation": demand_equation,
            "Supply_Equation": supply_equation,
            "Inverse_Demand_Function": inverse_demand,
            "Demand_Type": demand_type,
            "Supply_Type": supply_type,
        }

        return result

    except Exception as e:
        logger.error("Error in market_equilibrium: %s", str(e))
        return None
