import pytest
import sympy as sp
from pyMicroeconomics.supply import linear_supply, power_supply, exponential_supply, quadratic_supply
from pyMicroeconomics.symbols import p, q, c, d


@pytest.mark.supply
def test_linear_supply(unit_test_mocks, sample_market_data):
    """Test linear supply function with default and specific parameters."""
    # Test with default parameters
    eq = linear_supply()
    assert eq.function_type == "linear_supply"
    assert eq.equation == sp.Eq(q, c + d * p)

    # Test with specific parameters from fixture
    c_param = sample_market_data["supply_params"]["c"]
    d_param = sample_market_data["supply_params"]["d"]
    eq = linear_supply(c_param=c_param, d_param=d_param)
    assert eq.equation == sp.Eq(q, 20 + 3 * p)

    # Test substitution at equilibrium price
    result = eq.subs({p: sample_market_data["expected_price"]})
    assert float(sp.N(result.equation.rhs)) == pytest.approx(sample_market_data["expected_quantity"])
