from __future__ import annotations
from typing import Dict, Optional
import sympy as sp
from ...core.market_base import MarketFunction
from ...core.symbols import p, q


def calculate_surpluses(
    demand: MarketFunction,
    supply: MarketFunction,
    eq_price: sp.Expr,
    eq_quantity: sp.Expr,
) -> Dict[str, Optional[sp.Expr]]:
    """Calculate consumer and producer surplus."""
    try:
        # Get demand and supply expressions
        demand_expr = sp.solve(demand.equation.equation, q)[0]  # q = a - bp
        supply_expr = sp.solve(supply.equation.equation, q)[0]  # q = c + dp

        # Get inverse functions
        inverse_demand = sp.solve(sp.Eq(q, demand_expr), p)[0]  # p = (a-q)/b
        inverse_supply = sp.solve(sp.Eq(q, supply_expr), p)[0]  # p = (q-c)/d

        # Calculate consumer surplus
        cs_integrand = inverse_demand - eq_price
        cs = sp.integrate(cs_integrand, (q, 0, eq_quantity))
        cs = sp.simplify(cs)

        # Calculate producer surplus
        ps_integrand = eq_price - inverse_supply
        ps = sp.integrate(ps_integrand, (q, 0, eq_quantity))
        ps = sp.simplify(ps)

        # Calculate total surplus
        total = cs + ps
        total = sp.simplify(total)

        return {"Consumer_Surplus": cs, "Producer_Surplus": ps, "Total_Surplus": total}

    except Exception as e:
        print(f"Error in surplus calculation: {str(e)}")
        return {"Consumer_Surplus": None, "Producer_Surplus": None, "Total_Surplus": None}
