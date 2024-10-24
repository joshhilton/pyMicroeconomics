from __future__ import annotations

import pytest
import sympy as sp
from pyMicroeconomics.market.demand import linear_demand, power_demand, exponential_demand, quadratic_demand
from pyMicroeconomics.core.symbols import p, q


@pytest.mark.demand
def test_linear_demand():
    """Test linear demand function creation and evaluation."""
    demand = linear_demand(100, 2)

    # Test function type
    assert demand.function_type == "linear_demand"

    # Test evaluation
    quantity = demand.evaluate(10)
    assert quantity == 80  # 100 - 2*10

    # Test slope
    slope = demand.get_slope(10)
    assert slope == -2


@pytest.mark.demand
def test_power_demand():
    """Test power demand function creation and evaluation."""
    demand = power_demand(100, -0.5)

    # Test function type
    assert demand.function_type == "power_demand"

    # Test evaluation
    quantity = demand.evaluate(4)
    assert pytest.approx(quantity) == 50  # 100 * 4^(-0.5)

    # Test slope is negative
    slope = demand.get_slope(4)
    assert slope < 0


@pytest.mark.demand
def test_exponential_demand():
    """Test exponential demand function creation and evaluation."""
    demand = exponential_demand(0.05, 4.6)

    # Test function type
    assert demand.function_type == "exponential_demand"

    # Test evaluation
    quantity = demand.evaluate(10)
    expected = sp.exp(-0.05 * 10 + 4.6)
    assert pytest.approx(quantity) == float(expected)

    # Test slope is negative
    slope = demand.get_slope(10)
    assert slope < 0


@pytest.mark.demand
def test_quadratic_demand():
    """Test quadratic demand function creation and evaluation."""
    demand = quadratic_demand(100, 0.04)

    # Test function type
    assert demand.function_type == "quadratic_demand"

    # Test evaluation
    quantity = demand.evaluate(10)
    assert pytest.approx(quantity) == 96  # 100 - 0.04*10^2

    # Test slope is negative
    slope = demand.get_slope(10)
    assert slope < 0


@pytest.mark.demand
def test_demand_parameter_validation():
    """Test parameter validation for demand functions."""
    demand = linear_demand(100, 2)

    # Test negative price
    with pytest.raises(ValueError, match="Price cannot be negative"):
        demand.evaluate(-10)

    # Test resulting negative quantity
    with pytest.raises(ValueError, match="Quantity cannot be negative"):
        demand.evaluate(60)  # Results in -20


@pytest.mark.demand
def test_demand_evaluation_errors():
    """Test error handling in demand evaluation."""
    demand = linear_demand(100, 2)

    # Test evaluation with negative price
    with pytest.raises(ValueError, match="Price cannot be negative"):
        demand.evaluate(-10)
