"""Module for displaying market equilibrium results in HTML format."""

import sympy as sp
from IPython.display import display, HTML, Math


def display_equilibrium_results(equilibrium_results, parameter_subs=None):
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
        <table style="border-collapse: collapse; width: auto; margin-top: 10px;">
            <thead>
                <tr style="background-color: #f2f2f2;">
                    <th style="border: 1px solid black; padding: 8px; text-align: left;">Parameter</th>
                    <th style="border: 1px solid black; padding: 8px; text-align: left;">Value</th>
                </tr>
            </thead>
        </table>
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

    # Display each row separately
    for key in display_order:
        if key in formatted_results:
            value = formatted_results[key]
            # Display row start
            display(
                HTML(
                    f"""
                <tr>
                    <td style="border: 1px solid black; padding: 8px; text-align: center; font-size: 18px;">{key}</td>
                    <td style="border: 1px solid black; padding: 8px; text-align: center; font-size: 18px;">
            """
                )
            )

            # Display the math content
            display(Math(value))

            # Display row end
            display(HTML("</td></tr>"))

    # Display table end
    display(HTML("</table>"))
