"""Module for displaying market equilibrium results in HTML format."""

from typing import Optional, Dict, Union
import sympy as sp
from IPython.display import display, HTML, Math
from core.equation_types import TypedEquation
from market.equilibrium import EquilibriumResult


def display_equilibrium(
    equilibrium_results: Optional[EquilibriumResult],
    parameter_subs: Optional[Dict[sp.Symbol, Union[float, int]]] = None,
) -> None:
    """
    Display the equilibrium results in an HTML table.

    Args:
        equilibrium_results: Dictionary containing equilibrium calculation results
        parameter_subs: Optional dictionary of parameter substitutions for numerical evaluation
    """
    if equilibrium_results is None:
        print("No equilibrium data to display.")
        return

    # Create a new dictionary for the formatted results
    formatted_results = {}

    # Mapping of underscored keys to display labels
    key_labels = {
        "Equilibrium_Price": "Equilibrium Price",
        "Equilibrium_Quantity": "Equilibrium Quantity",
        "Consumer_Surplus": "Consumer Surplus",
        "Producer_Surplus": "Producer Surplus",
        "Total_Surplus": "Total Surplus",
        "Demand_Equation": "Demand Equation",
        "Supply_Equation": "Supply Equation",
        "Inverse_Demand_Function": "Inverse Demand Function",
        "Demand_Type": "Demand Type",
        "Supply_Type": "Supply Type",
    }

    for key, value in equilibrium_results.items():
        if parameter_subs and isinstance(value, (sp.Expr, sp.Equality)):
            # Substitute values
            substituted_value = value.subs(parameter_subs)
            if key in ["Demand_Equation", "Supply_Equation"]:
                formatted_results[key] = sp.latex(substituted_value)
            else:
                # Evaluate numerically
                try:
                    numeric_value = float(sp.N(substituted_value))
                    formatted_results[key] = f"{numeric_value:.2f}"
                except (ValueError, TypeError, AttributeError):
                    # If evaluation fails, keep symbolic
                    formatted_results[key] = sp.latex(substituted_value)
        else:
            formatted_results[key] = sp.latex(value) if isinstance(value, (sp.Expr, sp.Equality)) else str(value)

    # Display header
    display(
        HTML(
            """
    <div style="margin: 20px;">
        <h3 style="text-align: center; margin-bottom: 15px;">Market Equilibrium Results</h3>
        <table style="border-collapse: collapse; width: 100%; margin: auto;">
    """
        )
    )

    # Define display order with new keys
    display_order = [
        "Equilibrium_Price",
        "Equilibrium_Quantity",
        "Consumer_Surplus",
        "Producer_Surplus",
        "Total_Surplus",
        "Demand_Equation",
        "Supply_Equation",
        "Inverse_Demand_Function",
    ]

    # Display each row separately to allow Math rendering
    for key in display_order:
        if key in formatted_results:
            value = formatted_results[key]
            display_label = key_labels.get(key, key)
            # Display row start
            display(
                HTML(
                    f"""
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 12px; text-align: right; width: 40%; font-weight: bold; color: #444;">
                        {display_label}:
                    </td>
                    <td style="padding: 12px; text-align: left;">
            """
                )
            )

            # Display the math content
            display(Math(value))

            # Display row end
            display(HTML("</td></tr>"))

    # Close table
    display(
        HTML(
            """
        </table>
    </div>
    """
        )
    )
