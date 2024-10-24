from __future__ import annotations

import sympy as sp
from typing import Optional, Tuple
from ...core.market_base import MarketFunction, ParameterDict
from ...core.symbols import p, q


def validate_market_functions(
    demand: MarketFunction, supply: MarketFunction, params: Optional[ParameterDict] = None
) -> Tuple[bool, Optional[str]]:
    """Validate market functions for economic consistency."""
    try:
        # Check slopes at a test price point
        test_price = 1.0
        demand_slope = demand.get_slope(test_price, params)
        supply_slope = supply.get_slope(test_price, params)

        if demand_slope >= 0:
            return False, "Demand curve must have negative slope"
        if supply_slope <= 0:
            return False, "Supply curve must have positive slope"

        return True, None

    except Exception as e:
        return False, f"Validation error: {str(e)}"
