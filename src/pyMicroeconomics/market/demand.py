from __future__ import annotations
import sympy as sp
from ..core.market_base import MarketFunction
from ..core.equation_types import TypedEquation
from ..core.symbols import p, q, a, b


def linear_demand() -> MarketFunction:
    """Create linear demand curve equation: q = a - b*p"""
    eq = TypedEquation(sp.Eq(q, a - b * p), "linear_demand")
    return MarketFunction(eq, "linear_demand")


def power_demand() -> MarketFunction:
    """Create power demand curve equation: q = a*p^b"""
    eq = TypedEquation(sp.Eq(q, a * p**b), "power_demand")
    return MarketFunction(eq, "power_demand")


def exponential_demand() -> MarketFunction:
    """Create exponential demand curve equation: q = exp(-a*p + b)"""
    eq = TypedEquation(sp.Eq(q, sp.exp(-a * p + b)), "exponential_demand")
    return MarketFunction(eq, "exponential_demand")


def quadratic_demand() -> MarketFunction:
    """Create quadratic demand curve equation: q = a - b*p^2"""
    eq = TypedEquation(sp.Eq(q, a - b * p**2), "quadratic_demand")
    return MarketFunction(eq, "quadratic_demand")
