from __future__ import annotations

from typing import Dict, Optional, Union

import sympy as sp

from .equation_types import TypedEquation
from .symbols import p, q

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

    def evaluate(self, price_value: ParameterValue, params: Optional[ParameterDict] = None) -> float:
        """
        Evaluate the market function to find the quantity for a given price.

        Args:
            price_value: The price at which to evaluate the quantity.
            params: Optional dictionary of parameter symbols and their numeric values.

        Returns:
            The calculated quantity as a float.

        Raises:
            ValueError: If price_value is negative.
            TypeError: If the result after substitution is not numeric.
        """
        if price_value < 0:
            raise ValueError("Price cannot be negative.")

        # Solve for quantity (q)
        q_expr_list = sp.solve(self.equation.equation, q)
        if not q_expr_list:
            raise ValueError(f"Could not solve equation {self.equation.equation} for quantity (q).")
        q_expr = q_expr_list[0]  # Assume the first solution is the relevant one

        # Substitute price and parameters
        subs_dict = {p: price_value}
        if params:
            subs_dict.update(params)

        # Perform substitution
        evaluated_expr = q_expr.subs(subs_dict)

        # Ensure the result is numeric and return as float
        try:
            # Use evalf() for numerical evaluation, then convert to float
            result = float(evaluated_expr.evalf())
        except (TypeError, AttributeError) as exc:  # Catch AttributeError if evalf() is not available
            # Check if it's already a number (e.g., sympy.Float, sympy.Integer)
            if isinstance(evaluated_expr, (sp.Number, float, int)):
                result = float(evaluated_expr)
            else:
                raise TypeError(
                    f"Evaluation did not result in a numeric value. " f"Expression after substitution: {evaluated_expr}"
                ) from exc

        # Optional: Add check for negative quantity if desired by design
        # if result < 0:
        #     raise ValueError("Quantity cannot be negative.")

        return result
