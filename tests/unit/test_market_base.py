from __future__ import annotations

import pytest
import sympy as sp
from typing import Dict, cast
from pyMicroeconomics.core.market_base import MarketFunction, ParameterValue, ParameterDict
from pyMicroeconomics.core.equation_types import TypedEquation
from pyMicroeconomics.core.symbols import p, q, a, b


def test_market_function_creation():
    """Test basic MarketFunction creation and validation."""
    eq = TypedEquation(sp.Eq(q, a - b * p), "test")
    market_func = MarketFunction(eq, "test_type")

    assert market_func.function_type == "test_type"
    assert market_func.parameters == {}


def test_market_function_with_parameters():
    """Test MarketFunction with parameter values."""
    eq = TypedEquation(sp.Eq(q, a - b * p), "test")
    params: ParameterDict = {a: cast(ParameterValue, 100), b: cast(ParameterValue, 2)}
    market_func = MarketFunction(eq, "test_type", params)

    quantity = market_func.evaluate(10.0)
    assert quantity == 80.0  # 100 - 2*10


def test_market_function_slope():
    """Test slope calculation."""
    eq = TypedEquation(sp.Eq(q, a - b * p), "test")
    params: ParameterDict = {a: cast(ParameterValue, 100), b: cast(ParameterValue, 2)}
    market_func = MarketFunction(eq, "test_type", params)

    slope = market_func.get_slope(10.0)
    assert slope == -2.0


def test_invalid_equation():
    """Test validation of invalid equations."""
    eq = TypedEquation(sp.Eq(a, b), "test")  # Missing p and q
    with pytest.raises(ValueError):
        MarketFunction(eq, "test_type")


def test_market_function_parameter_update():
    """Test updating parameters after creation."""
    eq = TypedEquation(sp.Eq(q, a - b * p), "test")
    initial_params: ParameterDict = {a: cast(ParameterValue, 100), b: cast(ParameterValue, 2)}
    market_func = MarketFunction(eq, "test_type", initial_params)

    new_params: ParameterDict = {a: cast(ParameterValue, 200), b: cast(ParameterValue, 3)}
    quantity = market_func.evaluate(10.0, new_params)
    assert quantity == 170.0  # 200 - 3*10


def test_market_function_float_parameters():
    """Test MarketFunction with float parameters."""
    eq = TypedEquation(sp.Eq(q, a - b * p), "test")
    params: ParameterDict = {a: 100.0, b: 2.0}  # float is valid ParameterValue
    market_func = MarketFunction(eq, "test_type", params)

    quantity = market_func.evaluate(10.0)
    assert quantity == 80.0
