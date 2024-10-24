from __future__ import annotations
import sympy as sp
from ..core.market_base import MarketFunction
from ..core.equation_types import TypedEquation
from ..core.symbols import p, q, c, d


def linear_supply() -> MarketFunction:
    """Create linear supply curve equation: q = c + d*p"""
    eq = TypedEquation(sp.Eq(q, c + d * p), "linear_supply")
    return MarketFunction(eq, "linear_supply")


def power_supply() -> MarketFunction:
    """Create power supply curve equation: q = c*p^d"""
    eq = TypedEquation(sp.Eq(q, c * p**d), "power_supply")
    return MarketFunction(eq, "power_supply")


def exponential_supply() -> MarketFunction:
    """Create exponential supply curve equation: q = exp(c*p + d)"""
    eq = TypedEquation(sp.Eq(q, sp.exp(c * p + d)), "exponential_supply")
    return MarketFunction(eq, "exponential_supply")


def quadratic_supply() -> MarketFunction:
    """Create quadratic supply curve equation: q = c + d*p^2"""
    eq = TypedEquation(sp.Eq(q, c + d * p**2), "quadratic_supply")
    return MarketFunction(eq, "quadratic_supply")
