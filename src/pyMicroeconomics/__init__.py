"""Python Package Template"""

from __future__ import annotations

__version__ = "0.0.5"

from .core.equation_types import TypedEquation
from .core.market_base import MarketFunction

from .market.demand import (
    linear_demand,
    power_demand,
    exponential_demand,
    quadratic_demand,
)

from .market.supply import (
    linear_supply,
    power_supply,
    exponential_supply,
    quadratic_supply,
)

# Update equilibrium import
from .market.equilibrium.main import market_equilibrium
from .visualization.display import display_equilibrium
from .visualization.plotting import plot_equilibrium
