from __future__ import annotations

import sympy as sp
from typing import Optional, Union, Dict
from .equation_types import TypedEquation
from .symbols import p, q

ParameterValue = Union[float, int]
ParameterDict = Dict[sp.Symbol, ParameterValue]


class MarketFunction:
    """Base class for market functions (supply and demand)."""

    def __init__(self, equation: TypedEquation, function_type: str, parameters: Optional[ParameterDict] = None):
        self.equation = equation
        self.function_type = function_type
        self.parameters = parameters or {}
        self._validate_equation()

    def _validate_equation(self) -> None:
        """Validate that equation contains required symbols and is well-formed."""
        if not isinstance(self.equation, TypedEquation):
            raise ValueError("Equation must be a TypedEquation instance")

        symbols = self.equation.free_symbols
        if not (p in symbols and q in symbols):
            raise ValueError("Equation must contain both price (p) and quantity (q) symbols")

    def evaluate(self, price: float, params: Optional[ParameterDict] = None) -> float:
        """Evaluate the function at a given price point."""
        if price < 0:
            raise ValueError("Price cannot be negative")

        all_params = self.parameters.copy()
        if params:
            all_params.update(params)

        expr = sp.solve(self.equation.equation, q)[0]
        result = float(sp.N(expr.subs({p: price, **all_params})))

        if result < 0:
            raise ValueError("Quantity cannot be negative")

        return result

    def get_slope(self, price: float, params: Optional[ParameterDict] = None) -> float:
        """Calculate the slope at a given price point."""
        expr = sp.solve(self.equation.equation, q)[0]
        derivative = sp.diff(expr, p)

        all_params = self.parameters.copy()
        if params:
            all_params.update(params)

        slope = float(sp.N(derivative.subs({p: price, **all_params})))
        return slope

    def substitute_params(self, params: ParameterDict) -> MarketFunction:
        """Create a new instance with substituted parameters."""
        new_eq = self.equation.subs(params)
        return self.__class__(new_eq, self.function_type, params)
