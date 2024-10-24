from __future__ import annotations

import sympy as sp
from typing import Optional, Dict
from ...core.market_base import MarketFunction, ParameterDict
from ...core.symbols import p, q


def calculate_surpluses(
    demand: MarketFunction,
    supply: MarketFunction,
    eq_price: float,
    eq_quantity: float,
    params: Optional[ParameterDict] = None,
) -> Dict[str, Optional[float]]:
    """Calculate consumer and producer surplus."""
    try:
        # Get demand and supply expressions
        demand_expr = sp.solve(demand.equation.equation, q)[0]
        supply_expr = sp.solve(supply.equation.equation, q)[0]

        # Calculate consumer surplus
        cs = sp.integrate(demand_expr - eq_quantity, (p, eq_price, sp.oo))
        cs_value = float(sp.N(cs))

        # Calculate producer surplus
        ps = sp.integrate(eq_quantity - supply_expr, (p, 0, eq_price))
        ps_value = float(sp.N(ps))

        return {
            "Consumer_Surplus": cs_value if cs_value != sp.oo else None,
            "Producer_Surplus": ps_value,
            "Total_Surplus": cs_value + ps_value if cs_value != sp.oo else None,
        }

    except Exception:
        return {"Consumer_Surplus": None, "Producer_Surplus": None, "Total_Surplus": None}
