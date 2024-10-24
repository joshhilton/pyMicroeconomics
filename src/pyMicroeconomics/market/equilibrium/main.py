from __future__ import annotations
import sympy as sp
from typing import Optional
from ...core.market_base import MarketFunction
from .types import EquilibriumResult
from .solver import solve_equilibrium
from .surplus import calculate_surpluses


def market_equilibrium(demand: MarketFunction, supply: MarketFunction) -> Optional[EquilibriumResult]:
    """Calculate market equilibrium and associated surpluses."""
    try:
        # Solve for equilibrium
        equilibrium = solve_equilibrium(demand, supply)
        if equilibrium is None:
            return None

        eq_price, eq_quantity, inverse_demand = equilibrium

        # Calculate surpluses
        surpluses = calculate_surpluses(demand, supply, eq_price, eq_quantity)

        # Create result
        result: EquilibriumResult = {
            "Equilibrium_Price": eq_price,
            "Equilibrium_Quantity": eq_quantity,
            "Consumer_Surplus": surpluses["Consumer_Surplus"],
            "Producer_Surplus": surpluses["Producer_Surplus"],
            "Total_Surplus": surpluses["Total_Surplus"],
            "Demand_Equation": demand.equation,
            "Supply_Equation": supply.equation,
            "Inverse_Demand_Function": inverse_demand,  # Now included
            "Demand_Type": demand.function_type,
            "Supply_Type": supply.function_type,
        }

        return result

    except Exception as e:
        raise ValueError(f"Error calculating market equilibrium: {str(e)}")
