from __future__ import annotations
import sympy as sp
from .equation_types import TypedEquation
from .symbols import p, q
from typing import Dict, Union, Any

ParameterValue = Union[float, int]
ParameterDict = Dict[sp.Symbol, ParameterValue]


class MarketFunction:
    """Base class for market functions (supply and demand)."""

    def __init__(self, equation: TypedEquation, function_type: str):
        self.equation = equation
        self.function_type = function_type
        self._validate_equation()

    def _validate_equation(self) -> None:
        """Validate that equation contains required symbols."""
        if not isinstance(self.equation, TypedEquation):
            raise ValueError("Equation must be a TypedEquation instance")
        symbols = self.equation.free_symbols
        if not (p in symbols and q in symbols):
            raise ValueError("Equation must contain both price (p) and quantity (q) symbols")

    def get_slope(self) -> sp.Expr:
        """Get symbolic slope of the function."""
        expr = sp.solve(self.equation.equation, q)[0]
        return sp.diff(expr, p)
