from __future__ import annotations

from typing import TypedDict, Optional, Union
import sympy as sp
from ...core.equation_types import TypedEquation


class EquilibriumResult(TypedDict):
    """Type definition for equilibrium calculation results."""

    Equilibrium_Price: sp.Expr
    Equilibrium_Quantity: sp.Expr
    Consumer_Surplus: Optional[sp.Expr]
    Producer_Surplus: Optional[sp.Expr]
    Total_Surplus: Optional[sp.Expr]
    Demand_Equation: TypedEquation
    Supply_Equation: TypedEquation
    Inverse_Demand_Function: Union[sp.Eq, sp.Rel]  # Updated type
    Demand_Type: str
    Supply_Type: str
