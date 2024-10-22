"""Functions for defining various demand curves using sympy equations."""

import sympy as sp
from .symbols import p, q, a, b
from .equation_types import TypedEquation


def linear_demand(a_param=None, b_param=None):
    """Create linear demand curve equation: q = a - b*p"""
    if a_param is None:
        a_param = a
    if b_param is None:
        b_param = b
    eq = sp.Eq(q, a_param - b_param * p)
    return TypedEquation(eq, "linear_demand")


def power_demand(a_param=None, b_param=None):
    """Create power demand curve equation: q = a*p^b"""
    if a_param is None:
        a_param = a
    if b_param is None:
        b_param = b
    eq = sp.Eq(q, a_param * p**b_param)
    return TypedEquation(eq, "power_demand")


def exponential_demand(a_param=None, b_param=None):
    """Create exponential demand curve equation: q = exp(-a*p+b).
    This is equivalent to the semi-log form ln(q) = -a*p + b, which is common in econometrics.

    Args:
        a_param: Intercept parameter (default: symbolic 'a')
        b_param: Log coefficient (default: symbolic 'b')

    Returns:
        sympy.Eq: Exponential demand equation
    """
    if a_param is None:
        a_param = a
    if b_param is None:
        b_param = b
    eq = sp.Eq(q, sp.exp(-a_param * p + b_param))
    return TypedEquation(eq, "exponential_demand")


def quadratic_demand(a_param=None, b_param=None):
    """Create quadratic demand curve equation: q = a - b*p^2

    Args:
        a_param: Intercept parameter (default: symbolic 'a')
        b_param: Quadratic coefficient (default: symbolic 'b')

    Returns:
        sympy.Eq: Quadratic demand equation
    """
    if a_param is None:
        a_param = a
    if b_param is None:
        b_param = b
    eq = sp.Eq(q, a_param - b_param * p**2)
    return TypedEquation(eq, "quadratic_demand")
