import pytest
import sympy as sp
from pyMicroeconomics.demand import linear_demand
from pyMicroeconomics.supply import linear_supply
from pyMicroeconomics.equilibrium import market_equilibrium


@pytest.mark.market
@pytest.mark.integration
def test_full_market_analysis(unit_test_mocks):
    """Test complete market analysis workflow."""
    # Create demand and supply curves
    demand = linear_demand(a_param=100, b_param=2)
    supply = linear_supply(c_param=20, d_param=3)

    # Calculate equilibrium
    result = market_equilibrium(demand, supply)

    assert result is not None

    # Verify all expected components are present
    expected_keys = [
        "Equilibrium_Price",
        "Equilibrium_Quantity",
        "Consumer_Surplus",
        "Producer_Surplus",
        "Total_Surplus",
        "Demand_Equation",
        "Supply_Equation",
        "Inverse_Demand_Function",
    ]

    for key in expected_keys:
        assert key in result
