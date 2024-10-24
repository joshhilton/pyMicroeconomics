from typing import Dict, Union

import pytest
import sympy as sp
from sympy.core.symbol import Symbol

from pyMicroeconomics.demand import linear_demand
from pyMicroeconomics.equilibrium import ParameterDict, market_equilibrium
from pyMicroeconomics.supply import linear_supply
from pyMicroeconomics.symbols import a, b, c, d, p, q


@pytest.mark.market
def test_market_equilibrium_linear(unit_test_mocks):
    """Test basic linear equilibrium calculation."""
    demand = linear_demand(a_param=100, b_param=2)
    supply = linear_supply(c_param=20, d_param=3)

    result = market_equilibrium(demand, supply)

    assert result is not None
    assert "Equilibrium_Price" in result
    assert "Equilibrium_Quantity" in result

    price_eq = result["Equilibrium_Price"]
    quantity_eq = result["Equilibrium_Quantity"]

    assert float(sp.N(price_eq)) == pytest.approx(16.0)
    assert float(sp.N(quantity_eq)) == pytest.approx(68.0)


@pytest.mark.market
def test_market_equilibrium_invalid_inputs(unit_test_mocks):
    """Test error handling for invalid inputs."""
    # Test with missing demand
    with pytest.raises(ValueError):
        market_equilibrium(demand_eq=None, supply_eq=linear_supply())

    # Test with missing supply
    with pytest.raises(ValueError):
        market_equilibrium(demand_eq=linear_demand(), supply_eq=None)


@pytest.mark.market
def test_market_equilibrium_with_parameters(unit_test_mocks):
    """Test market equilibrium calculation with parameter substitutions."""
    demand = linear_demand()
    supply = linear_supply()

    # Create properly typed parameter dictionary
    params: ParameterDict = {a: 100.0, b: 2.0, c: 20.0, d: 3.0}  # Using float instead of int

    result = market_equilibrium(demand, supply, parameter_subs=params)

    assert result is not None
    price_eq = result["Equilibrium Price"]
    quantity_eq = result["Equilibrium Quantity"]

    assert float(sp.N(price_eq)) == pytest.approx(16.0)
    assert float(sp.N(quantity_eq)) == pytest.approx(68.0)
