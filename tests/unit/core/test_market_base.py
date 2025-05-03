from __future__ import annotations

from typing import cast

import pytest
import sympy as sp

from pyMicroeconomics.core.equation_types import TypedEquation
from pyMicroeconomics.core.market_base import MarketFunction, ParameterDict, ParameterValue
from pyMicroeconomics.core.symbols import a, b, p, q


def test_market_function_creation():
    """Test basic MarketFunction creation and validation."""
    eq = TypedEquation(sp.Eq(q, a - b * p), "test")
    market_func = MarketFunction(eq, "test_type")

    assert market_func.function_type == "test_type"
    # No parameters stored in the instance anymore
    # assert market_func.parameters == {}


def test_market_function_evaluate_with_parameters():
    """Test MarketFunction evaluate method with parameter values."""
    eq = TypedEquation(sp.Eq(q, a - b * p), "test")
    params: ParameterDict = {a: cast(ParameterValue, 100), b: cast(ParameterValue, 2)}
    market_func = MarketFunction(eq, "test_type")  # No params in constructor

    quantity = market_func.evaluate(10.0, params=params)  # Pass params here
    assert quantity == 80.0  # 100 - 2*10


def test_market_function_slope():
    """Test slope calculation."""
    eq = TypedEquation(sp.Eq(q, a - b * p), "test")
    # Params not needed for symbolic slope
    market_func = MarketFunction(eq, "test_type")  # No params in constructor

    slope_expr = market_func.get_slope()  # Slope is symbolic, no price needed
    assert slope_expr == -b  # The symbolic slope is -b

    # If you want to evaluate the slope with parameters:
    params_for_slope: ParameterDict = {b: cast(ParameterValue, 2)}
    numeric_slope = slope_expr.subs(params_for_slope)
    assert numeric_slope == -2


def test_invalid_equation():
    """Test validation of invalid equations."""
    eq = TypedEquation(sp.Eq(a, b), "test")  # Missing p and q
    with pytest.raises(ValueError, match="Equation must contain both price .* and quantity"):
        MarketFunction(eq, "test_type")


def test_market_function_evaluate_parameter_override():
    """Test evaluating with different parameters than initially assumed (if any)."""
    eq = TypedEquation(sp.Eq(q, a - b * p), "test")
    market_func = MarketFunction(eq, "test_type")

    # Evaluate with one set of parameters
    params1: ParameterDict = {a: cast(ParameterValue, 100), b: cast(ParameterValue, 2)}
    quantity1 = market_func.evaluate(10.0, params1)
    assert quantity1 == 80.0  # 100 - 2*10

    # Evaluate with a different set of parameters
    params2: ParameterDict = {a: cast(ParameterValue, 200), b: cast(ParameterValue, 3)}
    quantity2 = market_func.evaluate(10.0, params2)
    assert quantity2 == 170.0  # 200 - 3*10


def test_market_function_evaluate_float_parameters():
    """Test MarketFunction evaluate method with float parameters."""
    eq = TypedEquation(sp.Eq(q, a - b * p), "test")
    params: ParameterDict = {a: 100.0, b: 2.0}  # float is valid ParameterValue
    market_func = MarketFunction(eq, "test_type")  # No params in constructor

    quantity = market_func.evaluate(10.0, params=params)  # Pass params here
    assert quantity == 80.0


# --- New tests for evaluate ---


def test_evaluate_basic():
    """Test basic evaluation without parameters (if equation allows)."""
    eq = TypedEquation(sp.Eq(q, 50 - 2 * p), "test_no_params")
    market_func = MarketFunction(eq, "test_type")
    quantity = market_func.evaluate(10.0)  # No params needed
    assert quantity == 30.0  # 50 - 2*10


def test_evaluate_negative_price():
    """Test that evaluate raises ValueError for negative price."""
    eq = TypedEquation(sp.Eq(q, a - b * p), "test")
    params: ParameterDict = {a: 100, b: 2}
    market_func = MarketFunction(eq, "test_type")
    with pytest.raises(ValueError, match="Price cannot be negative"):
        market_func.evaluate(-5.0, params=params)


def test_evaluate_non_numeric_result_handling():
    """Test evaluate's error handling if substitution leads to non-numeric result."""
    # This is tricky to trigger naturally if sp.solve works.
    # We might need a more complex or unusual equation form.
    # Example: If 'a' was left unsubstituted.
    eq = TypedEquation(sp.Eq(q, a - b * p), "test")
    params_missing_a: ParameterDict = {b: 2}  # 'a' is missing
    market_func = MarketFunction(eq, "test_type")

    # The evaluate method substitutes and then calls evalf().
    # If a symbol remains, evalf() still returns a symbolic expression,
    # and float() will raise a TypeError.
    with pytest.raises(TypeError, match="Evaluation did not result in a numeric value"):
        market_func.evaluate(10.0, params=params_missing_a)
        market_func.evaluate(10.0, params=params_missing_a)
        market_func.evaluate(10.0, params=params_missing_a)
