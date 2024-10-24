#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""
This is a configuration file for pytest containing customizations and fixtures.

In VSCode, Code Coverage is recorded in config.xml. Delete this file to reset reporting.
"""

from __future__ import annotations

from typing import List

import pytest
from _pytest.nodes import Item


def pytest_collection_modifyitems(items: list[Item]):
    for item in items:
        if "spark" in item.nodeid:
            item.add_marker(pytest.mark.spark)
        elif "_int_" in item.nodeid:
            item.add_marker(pytest.mark.integration)


@pytest.fixture
def unit_test_mocks(monkeypatch: None):
    """Include Mocks here to execute all commands offline and fast."""
    pass


@pytest.fixture
def sample_market_data():
    """Fixture providing sample market equilibrium data for testing."""
    return {
        "demand_params": {"a": 100, "b": 2},
        "supply_params": {"c": 20, "d": 3},
        "expected_price": 16.0,
        "expected_quantity": 68.0,
    }


def pytest_configure(config):
    """Add custom markers to pytest configuration."""
    custom_markers = [
        "market: tests for market equilibrium functionality",
        "demand: tests for demand curve functionality",
        "supply: tests for supply curve functionality",
        "visualization: tests for plotting and display functionality",
        "optimization: tests for parameter optimization functionality",
    ]
    for marker in custom_markers:
        config.addinivalue_line("markers", marker)
