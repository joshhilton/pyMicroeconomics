from __future__ import annotations
import sympy as sp
from typing import Optional, Tuple, Union
from ...core.market_base import MarketFunction
from ...core.symbols import p, q


def solve_equilibrium(
    demand: MarketFunction, supply: MarketFunction
) -> Optional[Tuple[sp.Expr, sp.Expr, Union[sp.Eq, sp.Rel]]]:
    """Solve for market equilibrium price and quantity symbolically."""
    try:
        # Get demand and supply expressions
        demand_expr = sp.solve(demand.equation.equation, q)[0]
        supply_expr = sp.solve(supply.equation.equation, q)[0]

        # Calculate inverse demand function as an equation
        inverse_demand_rhs = sp.solve(sp.Eq(q, demand_expr), p)[0]
        # Don't wrap in Eq(), just return the expression
        inverse_demand = inverse_demand_rhs

        # Create equilibrium equation by setting demand = supply
        eq = sp.Eq(demand_expr, supply_expr)

        # Solve for price
        eq_price = sp.solve(eq, p)[0]

        # Substitute back to get quantity
        eq_quantity = demand_expr.subs(p, eq_price)

        # Simplify expressions
        eq_price = sp.simplify(eq_price)
        eq_quantity = sp.simplify(eq_quantity)

        return eq_price, eq_quantity, inverse_demand

    except Exception as e:
        raise ValueError(f"Error solving equilibrium: {str(e)}")
