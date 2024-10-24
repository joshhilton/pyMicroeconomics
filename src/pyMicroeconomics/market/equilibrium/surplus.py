from __future__ import annotations
import sympy as sp
from typing import Optional, Dict
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
        demand_expr = sp.solve(demand.equation.equation, q)[0]
        supply_expr = sp.solve(supply.equation.equation, q)[0]

        # For consumer surplus, we need to solve for inverse demand (p in terms of q)
        inverse_demand = sp.solve(sp.Eq(q, demand_expr), p)[0]

        # Consumer surplus: integrate from 0 to eq_quantity
        price_area = sp.integrate(inverse_demand, (q, 0, eq_quantity))
        expenditure = sp.Mul(eq_price, eq_quantity)
        cs = sp.Add(price_area, sp.Mul(sp.Integer(-1), expenditure))
        cs = sp.simplify(cs)

        # Producer surplus: integrate from 0 to eq_quantity
        inverse_supply = sp.solve(sp.Eq(q, supply_expr), p)[0]
        revenue = sp.Mul(eq_price, eq_quantity)
        cost_area = sp.integrate(inverse_supply, (q, 0, eq_quantity))
        ps = sp.Add(revenue, sp.Mul(sp.Integer(-1), cost_area))
        ps = sp.simplify(ps)

        # Calculate total surplus
        total = sp.Add(cs, ps)
        total = sp.simplify(total)

        return {
            "Consumer_Surplus": cs,
            "Producer_Surplus": ps,
            "Total_Surplus": total,
        }

    except Exception:
        return {"Consumer_Surplus": None, "Producer_Surplus": None, "Total_Surplus": None}
