"""Functions for defining various supply curves using sympy equations."""

import sympy as sp
from .symbols import p, q, c, d


def linear_supply(c_param=None, d_param=None):
    """Create linear supply curve equation: q = c + d*p

    Args:
        c_param: Intercept parameter (default: symbolic 'c')
        d_param: Slope parameter (default: symbolic 'd')

    Returns:
        sympy.Eq: Linear supply equation
    """
    if c_param is None:
        c_param = c
    if d_param is None:
        d_param = d
    return sp.Eq(q, c_param + d_param * p)


def power_supply(c_param=None, d_param=None):
    """Create power supply curve equation: q = exp(c)*p**d.
    This is equivalent to log-log form ln(q) = c + d*ln(p), which is common in econometrics.

    Args:
        c_param: Scale parameter (default: symbolic 'c')
        d_param: Supply elasticity of demand (default: symbolic 'd')

    Returns:
        sympy.Eq: Power supply equation
    """
    if c_param is None:
        c_param = c
    if d_param is None:
        d_param = d
    return sp.Eq(q, c_param * p**d_param)


def exponential_supply(c_param=None, d_param=None):
    """Create exponential supply curve equation: q = exp(c*p+d).
    This is equivalent to the semi-log form ln(q) = c*p + d, which is common in econometrics.

    Args:
        c_param: Intercept parameter (default: symbolic 'c')
        d_param: Log coefficient (default: symbolic 'd')

    Returns:
        sympy.Eq: Exponential supply equation
    """
    if c_param is None:
        c_param = c
    if d_param is None:
        d_param = d
    return sp.Eq(q, sp.exp(c_param * p + d_param))


def quadratic_supply(c_param=None, d_param=None):
    """Create quadratic supply curve equation: q = c + d*p^2

    Args:
        c_param: Intercept parameter (default: symbolic 'c')
        d_param: Quadratic coefficient (default: symbolic 'd')

    Returns:
        sympy.Eq: Quadratic supply equation
    """
    if c_param is None:
        c_param = c
    if d_param is None:
        d_param = d
    return sp.Eq(q, c_param + d_param * p**2)
