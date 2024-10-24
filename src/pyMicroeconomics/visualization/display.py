"""Module for displaying market equilibrium results in HTML format."""

from typing import Optional, Dict, Union
import sympy as sp
from IPython.display import display, HTML, Math
from ..core.equation_types import TypedEquation
from ..market.equilibrium.types import EquilibriumResult


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

    # Mapping of underscored keys to display labels
    key_labels: Dict[str, str] = {
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

    formatted_results: Dict[str, str] = {}

    for key, value in equilibrium_results.items():
        # Handle symbolic expressions
        if isinstance(value, sp.Expr):
            if key == "Inverse_Demand_Function":
                # Add the "p = " prefix for inverse demand function
                formatted_results[key] = f"p = {sp.latex(value)}"
            elif parameter_subs:
                try:
                    # Try numerical substitution
                    numeric_value = sp.N(value.subs(parameter_subs))
                    formatted_results[key] = f"{numeric_value:.2f}"
                except:
                    # If substitution fails, show symbolic form
                    formatted_results[key] = sp.latex(value)
            else:
                # Show symbolic form
                formatted_results[key] = sp.latex(value)

        # Handle TypedEquation objects
        elif isinstance(value, TypedEquation):
            if parameter_subs:
                try:
                    # Try numerical substitution in equation
                    subbed_eq = value.equation.subs(parameter_subs)
                    formatted_results[key] = sp.latex(subbed_eq)
                except:
                    # If substitution fails, show symbolic form
                    formatted_results[key] = sp.latex(value.equation)
            else:
                # Show symbolic form
                formatted_results[key] = sp.latex(value.equation)

        # Handle other types (strings, None)
        else:
            formatted_results[key] = str(value)

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

    # Define display order
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

    # Display each row
    for key in display_order:
        if key in formatted_results:
            value = formatted_results[key]
            display_label = key_labels.get(key, key)

            # Skip None values
            if value == "None":
                continue

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

    # Add function types at the bottom
    for key in ["Demand_Type", "Supply_Type"]:
        if key in formatted_results:
            display_label = key_labels.get(key, key)
            value = formatted_results[key]
            display(
                HTML(
                    f"""
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 12px; text-align: right; width: 40%; font-weight: bold; color: #444;">
                        {display_label}:
                    </td>
                    <td style="padding: 12px; text-align: left;">
                        {value}
                    </td>
                </tr>
                """
                )
            )

    # Close table
    display(
        HTML(
            """
            </table>
        </div>
        """
        )
    )
