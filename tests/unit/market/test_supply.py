from __future__ import annotations

from typing import cast

import pytest
import sympy as sp

from pyMicroeconomics.core.market_base import ParameterDict, ParameterValue
from pyMicroeconomics.core.symbols import c, d, p
from pyMicroeconomics.market.supply import exponential_supply, linear_supply, power_supply, quadratic_supply


@pytest.mark.supply
def test_linear_supply():
    """Test linear supply function creation and evaluation."""
    supply = linear_supply()  # Call factory without args
    params: ParameterDict = {c: cast(ParameterValue, 20), d: cast(ParameterValue, 3)}

    # Test function type
    assert supply.function_type == "linear_supply"

    # Test evaluation
    quantity = supply.evaluate(10, params=params)  # Pass params here
    assert quantity == 50  # 20 + 3*10

    # Test slope (symbolic first, then substitute)
    slope_expr = supply.get_slope()
    assert slope_expr == d
    numeric_slope = slope_expr.subs(params)
    assert numeric_slope == 3


@pytest.mark.supply
def test_power_supply():
    """Test power supply function creation and evaluation."""
    supply = power_supply()  # Call factory without args
    params: ParameterDict = {c: cast(ParameterValue, 1), d: cast(ParameterValue, 1.5)}

    # Test function type
    assert supply.function_type == "power_supply"

    # Test evaluation
    quantity = supply.evaluate(4, params=params)  # Pass params here
    assert pytest.approx(quantity) == 8  # 1 * 4^1.5

    # Test slope is positive (symbolic first, then substitute)
    slope_expr = supply.get_slope()
    # Slope is c*d*p**(d-1)
    numeric_slope_expr = slope_expr.subs(params).subs({p: 4})  # Substitute params and price
    # Handle cases where the result might already be numeric
    if hasattr(numeric_slope_expr, "evalf"):
        numeric_slope = cast(float, numeric_slope_expr.evalf())
    elif isinstance(numeric_slope_expr, (sp.Number, float, int)):
        numeric_slope = float(numeric_slope_expr)
    else:
        raise TypeError(f"Could not convert slope expression {numeric_slope_expr} to float")
    assert numeric_slope > 0
    assert pytest.approx(numeric_slope) == 1 * 1.5 * (4**0.5)  # 1.5 * 2 = 3


@pytest.mark.supply
def test_exponential_supply():
    """Test exponential supply function creation and evaluation."""
    supply = exponential_supply()  # Call factory without args
    # Equation is exp(c*p + d). Test params: c=0.05, d=0
    params: ParameterDict = {c: cast(ParameterValue, 0.05), d: cast(ParameterValue, 0)}

    # Test function type
    assert supply.function_type == "exponential_supply"

    # Test evaluation
    quantity = supply.evaluate(10, params=params)  # Pass params here
    expected = sp.exp(0.05 * 10 + 0)
    assert pytest.approx(quantity) == float(expected)

    # Test slope is positive (symbolic first, then substitute)
    slope_expr = supply.get_slope()
    # Slope is c * exp(c*p + d)
    numeric_slope_expr = slope_expr.subs(params).subs({p: 10})  # Substitute params and price
    # Handle cases where the result might already be numeric
    if hasattr(numeric_slope_expr, "evalf"):
        numeric_slope = cast(float, numeric_slope_expr.evalf())
    elif isinstance(numeric_slope_expr, (sp.Number, float, int)):
        numeric_slope = float(numeric_slope_expr)
    else:
        raise TypeError(f"Could not convert slope expression {numeric_slope_expr} to float")
    assert numeric_slope > 0
    assert pytest.approx(numeric_slope) == 0.05 * float(expected)


@pytest.mark.supply
def test_quadratic_supply():
    """Test quadratic supply function creation and evaluation."""
    supply = quadratic_supply()  # Call factory without args
    # Equation is q = c + d*p^2. Test params: c=0, d=0.04
    params: ParameterDict = {c: cast(ParameterValue, 0), d: cast(ParameterValue, 0.04)}

    # Test function type
    assert supply.function_type == "quadratic_supply"

    # Test evaluation
    quantity = supply.evaluate(10, params=params)  # Pass params here
    assert pytest.approx(quantity) == 4  # 0 + 0.04*10^2 = 4

    # Test slope is positive (symbolic first, then substitute)
    slope_expr = supply.get_slope()
    # Slope is 2*d*p
    numeric_slope_expr = slope_expr.subs(params).subs({p: 10})  # Substitute params and price
    # Handle cases where the result might already be numeric
    if hasattr(numeric_slope_expr, "evalf"):
        numeric_slope = cast(float, numeric_slope_expr.evalf())
    elif isinstance(numeric_slope_expr, (sp.Number, float, int)):
        numeric_slope = float(numeric_slope_expr)
    else:
        raise TypeError(f"Could not convert slope expression {numeric_slope_expr} to float")
    assert numeric_slope > 0
    assert pytest.approx(numeric_slope) == 2 * 0.04 * 10  # 0.8


@pytest.mark.supply
def test_supply_parameter_validation():
    """Test parameter validation for supply functions using evaluate."""
    supply = linear_supply()  # Call factory without args
    params: ParameterDict = {c: cast(ParameterValue, 20), d: cast(ParameterValue, 3)}

    # Test negative price using evaluate
    with pytest.raises(ValueError, match="Price cannot be negative"):
        supply.evaluate(-10, params=params)

    # Add test for missing parameters
    params_missing_c: ParameterDict = {d: cast(ParameterValue, 3)}
    with pytest.raises(TypeError, match="Evaluation did not result in a numeric value"):
        supply.evaluate(10, params=params_missing_c)


@pytest.mark.supply
def test_supply_evaluation_errors():
    """Test error handling in supply evaluation."""
    supply = linear_supply()  # Call factory without args
    params: ParameterDict = {c: cast(ParameterValue, 20), d: cast(ParameterValue, 3)}

    # Test evaluation with negative price
    with pytest.raises(ValueError, match="Price cannot be negative"):
        supply.evaluate(-10, params=params)

    # Test evaluation with missing parameters (redundant with above, but keeps structure)
    params_missing_d: ParameterDict = {c: cast(ParameterValue, 20)}
    with pytest.raises(TypeError, match="Evaluation did not result in a numeric value"):
        supply.evaluate(10, params=params_missing_d)
    params_missing_d: ParameterDict = {c: cast(ParameterValue, 20)}
    with pytest.raises(TypeError, match="Evaluation did not result in a numeric value"):
        supply.evaluate(10, params=params_missing_d)
    params_missing_d: ParameterDict = {c: cast(ParameterValue, 20)}
    with pytest.raises(TypeError, match="Evaluation did not result in a numeric value"):
        supply.evaluate(10, params=params_missing_d)
    params_missing_d: ParameterDict = {c: cast(ParameterValue, 20)}
    with pytest.raises(TypeError, match="Evaluation did not result in a numeric value"):
        supply.evaluate(10, params=params_missing_d)
    params_missing_d: ParameterDict = {c: cast(ParameterValue, 20)}
    with pytest.raises(TypeError, match="Evaluation did not result in a numeric value"):
        supply.evaluate(10, params=params_missing_d)
    params_missing_d: ParameterDict = {c: cast(ParameterValue, 20)}
    with pytest.raises(TypeError, match="Evaluation did not result in a numeric value"):
        supply.evaluate(10, params=params_missing_d)
    params_missing_d: ParameterDict = {c: cast(ParameterValue, 20)}
    with pytest.raises(TypeError, match="Evaluation did not result in a numeric value"):
        supply.evaluate(10, params=params_missing_d)
        supply.evaluate(10, params=params_missing_d)
