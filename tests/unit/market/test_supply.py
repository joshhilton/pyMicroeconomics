from __future__ import annotations

import pytest
import sympy as sp
from pyMicroeconomics.market.supply import linear_supply, power_supply, exponential_supply, quadratic_supply
from pyMicroeconomics.core.symbols import p, q


@pytest.mark.supply
def test_linear_supply():
    """Test linear supply function creation and evaluation."""
    supply = linear_supply(20, 3)

    # Test function type
    assert supply.function_type == "linear_supply"

    # Test evaluation
    quantity = supply.evaluate(10)
    assert quantity == 50  # 20 + 3*10

    # Test slope
    slope = supply.get_slope(10)
    assert slope == 3


@pytest.mark.supply
def test_power_supply():
    """Test power supply function creation and evaluation."""
    supply = power_supply(1, 1.5)

    # Test function type
    assert supply.function_type == "power_supply"

    # Test evaluation
    quantity = supply.evaluate(4)
    assert pytest.approx(quantity) == 8  # 4^1.5

    # Test slope is positive
    slope = supply.get_slope(4)
    assert slope > 0


@pytest.mark.supply
def test_exponential_supply():
    """Test exponential supply function creation and evaluation."""
    supply = exponential_supply(0.05, 0)

    # Test function type
    assert supply.function_type == "exponential_supply"

    # Test evaluation
    quantity = supply.evaluate(10)
    expected = sp.exp(0.05 * 10)
    assert pytest.approx(quantity) == float(expected)

    # Test slope is positive
    slope = supply.get_slope(10)
    assert slope > 0


@pytest.mark.supply
def test_quadratic_supply():
    """Test quadratic supply function creation and evaluation."""
    supply = quadratic_supply(0, 0.04)

    # Test function type
    assert supply.function_type == "quadratic_supply"

    # Test evaluation
    quantity = supply.evaluate(10)
    assert pytest.approx(quantity) == 4  # 0.04*10^2

    # Test slope is positive
    slope = supply.get_slope(10)
    assert slope > 0


@pytest.mark.supply
def test_supply_parameter_validation():
    """Test parameter validation for supply functions."""
    supply = linear_supply(20, 3)

    # Test negative price
    with pytest.raises(ValueError, match="Price cannot be negative"):
        supply.evaluate(-10)


@pytest.mark.supply
def test_supply_evaluation_errors():
    """Test error handling in supply evaluation."""
    supply = linear_supply(20, 3)

    # Test evaluation with negative price
    with pytest.raises(ValueError, match="Price cannot be negative"):
        supply.evaluate(-10)
