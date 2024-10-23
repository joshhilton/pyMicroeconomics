"""
Module for defining typed equation classes that combine SymPy equations with metadata.

This module provides the TypedEquation class which wraps SymPy equations with additional
type information, allowing for better tracking and handling of different equation types
in economic analysis (e.g., demand curves, supply curves).
"""


class TypedEquation:
    def __init__(self, equation, function_type):
        self.equation = equation
        self.function_type = function_type

    def subs(self, *args, **kwargs):
        """Preserve type information when substituting values"""
        return TypedEquation(self.equation.subs(*args, **kwargs), self.function_type)

    @property
    def free_symbols(self):
        """Pass through to underlying equation's free_symbols"""
        return self.equation.free_symbols
