from __future__ import annotations

import sympy as sp
from typing import Optional
from ..core.market_base import MarketFunction, ParameterDict
from ..core.equation_types import TypedEquation
from ..core.symbols import p, q, c, d


def linear_supply(c_param: Optional[float] = None, d_param: Optional[float] = None) -> MarketFunction:
    """Create linear supply curve equation: q = c + d*p

    Args:
        c_param: Intercept parameter (minimum quantity supplied at p=0)
        d_param: Slope parameter (should be positive)

    Returns:
        MarketFunction: Linear supply function

    Examples:
        >>> supply = linear_supply(20, 3)  # q = 20 + 3p
        >>> quantity = supply.evaluate(price=10)  # Evaluate at p = 10
        >>> slope = supply.get_slope(price=10)  # Get slope at p = 10
    """
    params: ParameterDict = {}
    if c_param is not None:
        params[c] = c_param
    if d_param is not None:
        params[d] = d_param

    eq = TypedEquation(sp.Eq(q, c + d * p), "linear_supply")
    return MarketFunction(eq, "linear_supply", params)


def power_supply(c_param: Optional[float] = None, d_param: Optional[float] = None) -> MarketFunction:
    """Create power supply curve equation: q = c*p^d

    This is equivalent to log-log form ln(q) = ln(c) + d*ln(p), common in econometrics.

    Args:
        c_param: Scale parameter (should be positive)
        d_param: Price elasticity of supply (should be positive)

    Returns:
        MarketFunction: Power supply function

    Examples:
        >>> supply = power_supply(1, 1.5)  # q = p^1.5
        >>> quantity = supply.evaluate(price=10)  # Evaluate at p = 10
        >>> slope = supply.get_slope(price=10)  # Get slope at p = 10
    """
    params: ParameterDict = {}
    if c_param is not None:
        params[c] = c_param
    if d_param is not None:
        params[d] = d_param

    eq = TypedEquation(sp.Eq(q, c * p**d), "power_supply")
    return MarketFunction(eq, "power_supply", params)


def exponential_supply(c_param: Optional[float] = None, d_param: Optional[float] = None) -> MarketFunction:
    """Create exponential supply curve equation: q = exp(c*p + d)

    This is equivalent to semi-log form ln(q) = c*p + d, common in econometrics.

    Args:
        c_param: Price sensitivity parameter (should be positive)
        d_param: Scale parameter

    Returns:
        MarketFunction: Exponential supply function

    Examples:
        >>> supply = exponential_supply(0.05, 0)  # q = exp(0.05*p)
        >>> quantity = supply.evaluate(price=10)  # Evaluate at p = 10
        >>> slope = supply.get_slope(price=10)  # Get slope at p = 10
    """
    params: ParameterDict = {}
    if c_param is not None:
        params[c] = c_param
    if d_param is not None:
        params[d] = d_param

    eq = TypedEquation(sp.Eq(q, sp.exp(c * p + d)), "exponential_supply")
    return MarketFunction(eq, "exponential_supply", params)


def quadratic_supply(c_param: Optional[float] = None, d_param: Optional[float] = None) -> MarketFunction:
    """Create quadratic supply curve equation: q = c + d*p^2

    Args:
        c_param: Minimum quantity parameter (quantity at p=0)
        d_param: Price sensitivity parameter (should be positive)

    Returns:
        MarketFunction: Quadratic supply function

    Examples:
        >>> supply = quadratic_supply(0, 0.04)  # q = 0.04*p^2
        >>> quantity = supply.evaluate(price=10)  # Evaluate at p = 10
        >>> slope = supply.get_slope(price=10)  # Get slope at p = 10
    """
    params: ParameterDict = {}
    if c_param is not None:
        params[c] = c_param
    if d_param is not None:
        params[d] = d_param

    eq = TypedEquation(sp.Eq(q, c + d * p**2), "quadratic_supply")
    return MarketFunction(eq, "quadratic_supply", params)
