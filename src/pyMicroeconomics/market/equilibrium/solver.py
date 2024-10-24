from __future__ import annotations

import sympy as sp
from typing import Optional, Tuple
from ...core.market_base import MarketFunction, ParameterDict
from ...core.symbols import p, q
from .types import EquilibriumResult
from .validation import validate_market_functions


def solve_equilibrium(
    demand: MarketFunction, supply: MarketFunction, params: Optional[ParameterDict] = None
) -> Optional[Tuple[float, float]]:
    """Solve for market equilibrium price and quantity."""
    try:
        # Validate inputs
        is_valid, error_msg = validate_market_functions(demand, supply, params)
        if not is_valid:
            raise ValueError(error_msg)

        # Get equations
        demand_eq = demand.equation.equation
        supply_eq = supply.equation.equation

        # Solve system of equations
        solution = sp.solve([demand_eq, supply_eq], (p, q))

        if not solution:
            return None

        # Get first solution and convert to float
        eq_price = float(sp.N(solution[0][0]))
        eq_quantity = float(sp.N(solution[0][1]))

        return eq_price, eq_quantity

    except Exception as e:
        raise ValueError(f"Error solving equilibrium: {str(e)}")
