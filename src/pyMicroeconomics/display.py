"""Module for displaying market equilibrium results in HTML format."""

import sympy as sp
from IPython.display import display, HTML, Math


def display_equilibrium(equilibrium_results, parameter_subs=None):
    """
    Display the equilibrium results in an HTML table.

    Args:
        equilibrium_results: Dictionary containing equilibrium calculation results
        parameter_subs: Optional dictionary of parameter substitutions for numerical evaluation

    Returns:
        None. Displays HTML table of results.
    """
    if equilibrium_results is None:
        print("No equilibrium data to display.")
        return

    # Create a new dictionary for the formatted results
    formatted_results = {}

    for key, value in equilibrium_results.items():
        if parameter_subs and isinstance(value, (sp.Expr, sp.Equality)):
            # Substitute values
            substituted_value = value.subs(parameter_subs)
            if key in ["DemandEquation", "SupplyEquation"]:
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
            formatted_results[key] = sp.latex(value)

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

    display_order = [
        "Equilibrium Price",
        "Equilibrium Quantity",
        "Consumer Surplus",
        "Producer Surplus",
        "Total Surplus",
        "Demand Equation",
        "Supply Equation",
        "Inverse Demand Function",
    ]

    # Display each row separately to allow Math rendering
    for key in display_order:
        if key in formatted_results:
            value = formatted_results[key]
            # Display row start
            display(
                HTML(
                    f"""
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 12px; text-align: right; width: 40%; font-weight: bold; color: #444;">
                        {key}:
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
