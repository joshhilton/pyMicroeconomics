import pytest
import sympy as sp
from pyMicroeconomics.demand import linear_demand, power_demand, exponential_demand, quadratic_demand
from pyMicroeconomics.symbols import p, q, a, b


@pytest.mark.demand
def test_linear_demand(unit_test_mocks, sample_market_data):
    """Test linear demand function with default and specific parameters."""
    # Test with default parameters
    eq = linear_demand()
    assert eq.function_type == "linear_demand"
    assert eq.equation == sp.Eq(q, a - b * p)

    # Test with specific parameters from fixture
    a_param = sample_market_data["demand_params"]["a"]
    b_param = sample_market_data["demand_params"]["b"]
    eq = linear_demand(a_param=a_param, b_param=b_param)
    assert eq.equation == sp.Eq(q, 100 - 2 * p)

    # Test substitution at equilibrium price
    result = eq.subs({p: sample_market_data["expected_price"]})
    assert result.equation == sp.Eq(q, sample_market_data["expected_quantity"])


@pytest.mark.demand
def test_power_demand(unit_test_mocks):
    """Test power demand function."""
    # Test with default parameters
    eq = power_demand()
    assert eq.function_type == "power_demand"
    assert eq.equation == sp.Eq(q, a * p**b)

    # Test with specific parameters
    eq = power_demand(a_param=5, b_param=-0.5)
    assert eq.equation == sp.Eq(q, 5 * p ** (-0.5))
