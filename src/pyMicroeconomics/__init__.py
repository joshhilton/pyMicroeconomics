"""Python Package Template"""

from __future__ import annotations

__version__ = "0.0.6"

from .core.equation_types import TypedEquation
from .core.market_base import MarketFunction
from .market.demand import exponential_demand, linear_demand, power_demand, quadratic_demand

# Update equilibrium import
from .market.equilibrium.main import market_equilibrium
from .market.supply import exponential_supply, linear_supply, power_supply, quadratic_supply
from .visualization.display import display_equilibrium
from .visualization.plotting import plot_equilibrium
