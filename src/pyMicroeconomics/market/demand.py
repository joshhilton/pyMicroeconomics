from __future__ import annotations

import sympy as sp
from typing import Optional
from ..core.market_base import MarketFunction, ParameterDict
from ..core.equation_types import TypedEquation
from ..core.symbols import p, q, a, b


def linear_demand(a_param: Optional[float] = None, b_param: Optional[float] = None) -> MarketFunction:
    """Create linear demand curve equation: q = a - b*p

    Args:
        a_param: Intercept parameter (maximum willingness to pay)
        b_param: Slope parameter (price sensitivity)

    Returns:
        MarketFunction: Linear demand function with equation q = a - b*p

    Examples:
        >>> demand = linear_demand(100, 2)  # q = 100 - 2p
        >>> quantity = demand.evaluate(price=10)  # Evaluate at p = 10
        >>> slope = demand.get_slope(price=10)  # Get slope at p = 10
    """
    params: ParameterDict = {}
    if a_param is not None:
        params[a] = a_param
    if b_param is not None:
        params[b] = b_param

    eq = TypedEquation(sp.Eq(q, a - b * p), "linear_demand")
    return MarketFunction(eq, "linear_demand", params)


def power_demand(a_param: Optional[float] = None, b_param: Optional[float] = None) -> MarketFunction:
    """Create power (constant elasticity) demand curve equation: q = a*p^b

    Args:
        a_param: Scale parameter
        b_param: Price elasticity of demand (should be negative)

    Returns:
        MarketFunction: Power demand function with equation q = a*p^b

    Examples:
        >>> demand = power_demand(100, -0.5)  # q = 100*p^(-0.5)
        >>> quantity = demand.evaluate(price=10)  # Evaluate at p = 10
        >>> slope = demand.get_slope(price=10)  # Get slope at p = 10
    """
    params: ParameterDict = {}
    if a_param is not None:
        params[a] = a_param
    if b_param is not None:
        params[b] = b_param

    eq = TypedEquation(sp.Eq(q, a * p**b), "power_demand")
    return MarketFunction(eq, "power_demand", params)


def exponential_demand(a_param: Optional[float] = None, b_param: Optional[float] = None) -> MarketFunction:
    """Create exponential demand curve equation: q = exp(-a*p + b)

    This is equivalent to the semi-log form ln(q) = -a*p + b, common in econometrics.

    Args:
        a_param: Price sensitivity parameter (should be positive)
        b_param: Scale parameter (determines maximum quantity at p=0)

    Returns:
        MarketFunction: Exponential demand function

    Examples:
        >>> demand = exponential_demand(0.05, 4.6)  # q = exp(-0.05*p + 4.6)
        >>> quantity = demand.evaluate(price=10)  # Evaluate at p = 10
        >>> slope = demand.get_slope(price=10)  # Get slope at p = 10
    """
    params: ParameterDict = {}
    if a_param is not None:
        params[a] = a_param
    if b_param is not None:
        params[b] = b_param

    eq = TypedEquation(sp.Eq(q, sp.exp(-a * p + b)), "exponential_demand")
    return MarketFunction(eq, "exponential_demand", params)


def quadratic_demand(a_param: Optional[float] = None, b_param: Optional[float] = None) -> MarketFunction:
    """Create quadratic demand curve equation: q = a - b*p^2

    Args:
        a_param: Maximum quantity parameter (quantity at p=0)
        b_param: Price sensitivity parameter (should be positive)

    Returns:
        MarketFunction: Quadratic demand function

    Examples:
        >>> demand = quadratic_demand(100, 0.04)  # q = 100 - 0.04*p^2
        >>> quantity = demand.evaluate(price=10)  # Evaluate at p = 10
        >>> slope = demand.get_slope(price=10)  # Get slope at p = 10
    """
    params: ParameterDict = {}
    if a_param is not None:
        params[a] = a_param
    if b_param is not None:
        params[b] = b_param

    eq = TypedEquation(sp.Eq(q, a - b * p**2), "quadratic_demand")
    return MarketFunction(eq, "quadratic_demand", params)

