import pytest
import sympy as sp
from pyMicroeconomics.core.equation_types import TypedEquation
from pyMicroeconomics.symbols import p, q


def test_typed_equation_creation():
    eq = sp.Eq(q, 10 - 2 * p)
    typed_eq = TypedEquation(eq, "test_type")

    assert typed_eq.equation == eq
    assert typed_eq.function_type == "test_type"


def test_typed_equation_substitution():
    eq = sp.Eq(q, 10 - 2 * p)
    typed_eq = TypedEquation(eq, "test_type")

    # Test substitution
    subbed_eq = typed_eq.subs({p: 2})

    assert isinstance(subbed_eq, TypedEquation)
    assert subbed_eq.function_type == "test_type"
    assert subbed_eq.equation == sp.Eq(q, 6)


def test_free_symbols():
    eq = sp.Eq(q, 10 - 2 * p)
    typed_eq = TypedEquation(eq, "test_type")

    assert typed_eq.free_symbols == {p, q}
