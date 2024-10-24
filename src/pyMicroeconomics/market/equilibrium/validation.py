from __future__ import annotations
import sympy as sp
from typing import Optional, Tuple
from ...core.market_base import MarketFunction
from ...core.symbols import p, q


def validate_market_functions(demand: MarketFunction, supply: MarketFunction) -> Tuple[bool, Optional[str]]:
    """Validate market functions for economic consistency."""
    try:
        # Get derivatives symbolically
        demand_slope = demand.get_slope()
        supply_slope = supply.get_slope()

        # Create a positive test point
        test_p = sp.Symbol("test_p", positive=True)

        # Substitute and evaluate for signs
        demand_eval = sp.simplify(demand_slope.subs(p, test_p))
        supply_eval = sp.simplify(supply_slope.subs(p, test_p))

        # Use sympy's relational operators and assumptions
        demand_cond = sp.simplify(demand_eval <= 0)
        supply_cond = sp.simplify(supply_eval >= 0)

        # Check if the conditions are True under positive value assumption
        if (demand_cond is sp.true or demand_cond.is_nonpositive) and (
            supply_cond is sp.true or supply_cond.is_nonnegative
        ):
            return True, None

        return False, "Invalid slopes for supply and demand curves"

    except Exception as e:
        return False, f"Validation error: {str(e)}"
