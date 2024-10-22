#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
"""Python Package Template"""
from __future__ import annotations

__version__ = "0.0.5"

from .equation_types import TypedEquation

from .demand import (
    linear_demand,
    power_demand,
    exponential_demand,
    quadratic_demand,
)

from .supply import (
    linear_supply,
    power_supply,
    exponential_supply,
    quadratic_supply,
)

from .equilibrium import market_equilibrium
from .display import display_equilibrium

# from .optimization import optimize_parameters
from .plotting import plot_equilibrium

if __name__ == "__main__":
    test_market_equilibrium()
