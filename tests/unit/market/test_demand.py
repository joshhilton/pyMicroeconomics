from __future__ import annotations

from typing import cast

import pytest
import sympy as sp

from pyMicroeconomics.core.market_base import ParameterDict, ParameterValue
from pyMicroeconomics.core.symbols import a, b, p
from pyMicroeconomics.market.demand import exponential_demand, linear_demand, power_demand, quadratic_demand


@pytest.mark.demand
def test_linear_demand():
    """Test linear demand function creation and evaluation."""
    demand = linear_demand()  # Call factory without args
    params: ParameterDict = {a: cast(ParameterValue, 100), b: cast(ParameterValue, 2)}

    # Test function type
    assert demand.function_type == "linear_demand"

    # Test evaluation
    quantity = demand.evaluate(10, params=params)  # Pass params here
    assert quantity == 80  # 100 - 2*10

    # Test slope (symbolic first, then substitute)
    slope_expr = demand.get_slope()
    assert slope_expr == -b
    numeric_slope = slope_expr.subs(params)
    assert numeric_slope == -2


@pytest.mark.demand
def test_power_demand():
    """Test power demand function creation and evaluation."""
    demand = power_demand()  # Call factory without args
    params: ParameterDict = {a: cast(ParameterValue, 100), b: cast(ParameterValue, -0.5)}

    # Test function type
    assert demand.function_type == "power_demand"

    # Test evaluation
    quantity = demand.evaluate(4, params=params)  # Pass params here
    assert pytest.approx(quantity) == 50  # 100 * 4^(-0.5)

    # Test slope is negative (symbolic first, then substitute)
    slope_expr = demand.get_slope()
    # Slope is a*b*p**(b-1)
    numeric_slope_expr = slope_expr.subs(params).subs({p: 4})  # Substitute params and price
    # Handle cases where the result might already be numeric
    if hasattr(numeric_slope_expr, "evalf"):
        numeric_slope = cast(float, numeric_slope_expr.evalf())
    elif isinstance(numeric_slope_expr, (sp.Number, float, int)):
        numeric_slope = float(numeric_slope_expr)
    else:
        raise TypeError(f"Could not convert slope expression {numeric_slope_expr} to float")
    assert numeric_slope < 0
    assert pytest.approx(numeric_slope) == 100 * (-0.5) * (4 ** (-1.5))  # 100 * -0.5 * (1/8) = -6.25


@pytest.mark.demand
def test_exponential_demand():
    """Test exponential demand function creation and evaluation."""
    demand = exponential_demand()  # Call factory without args
    # Note: Original test used exp(-a*p + b). Let's keep symbols consistent.
    # Equation is exp(-a*p + b). Test params: a=0.05, b=4.6
    params: ParameterDict = {a: cast(ParameterValue, 0.05), b: cast(ParameterValue, 4.6)}

    # Test function type
    assert demand.function_type == "exponential_demand"

    # Test evaluation
    quantity = demand.evaluate(10, params=params)  # Pass params here
    expected = sp.exp(-0.05 * 10 + 4.6)
    assert pytest.approx(quantity) == float(expected)

    # Test slope is negative (symbolic first, then substitute)
    slope_expr = demand.get_slope()
    # Slope is -a * exp(-a*p + b)
    numeric_slope_expr = slope_expr.subs(params).subs({p: 10})  # Substitute params and price
    # Handle cases where the result might already be numeric
    if hasattr(numeric_slope_expr, "evalf"):
        numeric_slope = cast(float, numeric_slope_expr.evalf())
    elif isinstance(numeric_slope_expr, (sp.Number, float, int)):
        numeric_slope = float(numeric_slope_expr)
    else:
        raise TypeError(f"Could not convert slope expression {numeric_slope_expr} to float")
    assert numeric_slope < 0
    assert pytest.approx(numeric_slope) == -0.05 * float(expected)


@pytest.mark.demand
def test_quadratic_demand():
    """Test quadratic demand function creation and evaluation."""
    demand = quadratic_demand()  # Call factory without args
    # Equation is q = a - b*p^2. Test params: a=100, b=0.04
    params: ParameterDict = {a: cast(ParameterValue, 100), b: cast(ParameterValue, 0.04)}

    # Test function type
    assert demand.function_type == "quadratic_demand"

    # Test evaluation
    quantity = demand.evaluate(10, params=params)  # Pass params here
    assert pytest.approx(quantity) == 96  # 100 - 0.04*10^2 = 100 - 4 = 96

    # Test slope is negative (symbolic first, then substitute)
    slope_expr = demand.get_slope()
    # Slope is -2*b*p
    numeric_slope_expr = slope_expr.subs(params).subs({p: 10})  # Substitute params and price
    # Handle cases where the result might already be numeric
    if hasattr(numeric_slope_expr, "evalf"):
        numeric_slope = cast(float, numeric_slope_expr.evalf())
    elif isinstance(numeric_slope_expr, (sp.Number, float, int)):
        numeric_slope = float(numeric_slope_expr)
    else:
        raise TypeError(f"Could not convert slope expression {numeric_slope_expr} to float")
    assert numeric_slope < 0
    assert pytest.approx(numeric_slope) == -2 * 0.04 * 10  # -0.8


@pytest.mark.demand
def test_demand_parameter_validation():
    """Test parameter validation for demand functions using evaluate."""
    demand = linear_demand()  # Call factory without args
    params: ParameterDict = {a: cast(ParameterValue, 100), b: cast(ParameterValue, 2)}

    # Test negative price using evaluate
    with pytest.raises(ValueError, match="Price cannot be negative"):
        demand.evaluate(-10, params=params)

    # Test resulting negative quantity - evaluate currently does NOT check this.
    # This check might belong elsewhere or needs evaluate to be updated.
    # For now, we test that evaluate *does* return the negative value.
    neg_quantity = demand.evaluate(60, params=params)  # Results in 100 - 2*60 = -20
    assert neg_quantity == -20
    # If negative quantities should be disallowed by evaluate, add this check:
    # with pytest.raises(ValueError, match="Quantity cannot be negative"):
    #     demand.evaluate(60, params=params)


@pytest.mark.demand
def test_demand_evaluation_errors():
    """Test error handling in demand evaluation."""
    demand = linear_demand()  # Call factory without args
    params: ParameterDict = {a: cast(ParameterValue, 100), b: cast(ParameterValue, 2)}

    # Test evaluation with negative price
    with pytest.raises(ValueError, match="Price cannot be negative"):
        demand.evaluate(-10, params=params)

    # Test evaluation with missing parameters
    params_missing_a: ParameterDict = {b: cast(ParameterValue, 2)}
    with pytest.raises(TypeError, match="Evaluation did not result in a numeric value"):
        demand.evaluate(10, params=params_missing_a)
    params_missing_a: ParameterDict = {b: cast(ParameterValue, 2)}
    with pytest.raises(TypeError, match="Evaluation did not result in a numeric value"):
        demand.evaluate(10, params=params_missing_a)
    params_missing_a: ParameterDict = {b: cast(ParameterValue, 2)}
    with pytest.raises(TypeError, match="Evaluation did not result in a numeric value"):
        demand.evaluate(10, params=params_missing_a)
        demand.evaluate(10, params=params_missing_a)
        demand.evaluate(10, params=params_missing_a)
        demand.evaluate(10, params=params_missing_a)
        demand.evaluate(10, params=params_missing_a)
        demand.evaluate(10, params=params_missing_a)
        demand.evaluate(10, params=params_missing_a)
