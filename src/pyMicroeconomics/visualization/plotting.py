"""Module for creating interactive market equilibrium plots with adjustable parameters."""

from typing import Optional
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from ipywidgets import widgets, Layout
from IPython.display import display, HTML
from ..core.symbols import p, q
from ..market.equilibrium.types import EquilibriumResult


def plot_equilibrium(equilibrium_results: Optional[EquilibriumResult]) -> None:
    if equilibrium_results is None:
        print("Please provide valid equilibrium results.")
        return

    # Import the actual symbol objects being used in the equations
    from ..core.symbols import a, b, c, d, p, q

    # Get equations and equilibrium values
    demand_eq = equilibrium_results["Demand_Equation"]
    supply_eq = equilibrium_results["Supply_Equation"]
    eq_price = equilibrium_results["Equilibrium_Price"]
    eq_quantity = equilibrium_results["Equilibrium_Quantity"]

    # Define default parameters using the imported symbols
    default_params = {a: 10.0, b: 2.0, c: 0.0, d: 3.0}

    # Get all symbolic parameters
    all_symbols = (demand_eq.free_symbols | supply_eq.free_symbols) - {p, q}

    # Create parameter sliders
    param_inputs = {}
    for symbol in sorted(all_symbols, key=str):
        default_value = default_params[symbol]
        param_inputs[str(symbol)] = widgets.FloatSlider(
            value=default_value,
            min=0.0,
            max=default_value * 2,
            step=0.1,
            description=str(symbol),
            continuous_update=False,
            description_tooltip=f"Parameter {str(symbol)}",
            layout=Layout(width="500px"),
            style={"description_width": "initial"},
        )

    # Create symbol mapping
    symbol_map = {"a": a, "b": b, "c": c, "d": d}

    def update(**kwargs):
        """Update plot with new parameter values."""
        try:
            # Convert string keys to actual symbols
            params = {symbol_map[k]: v for k, v in kwargs.items()}

            # Get expressions
            demand_expr = sp.solve(demand_eq.equation, q)[0]
            supply_expr = sp.solve(supply_eq.equation, q)[0]

            # Substitute parameters into expressions
            eq_price_num = eq_price.subs(params)
            eq_quantity_num = eq_quantity.subs(params)

            # Convert to float
            eq_price_val = float(sp.N(eq_price_num))
            eq_quantity_val = float(sp.N(eq_quantity_num))

            # Substitute parameters into expressions
            demand_expr_num = demand_expr.subs(params)
            supply_expr_num = supply_expr.subs(params)

            # Create lambda functions
            demand_func = sp.lambdify(p, demand_expr_num)
            supply_func = sp.lambdify(p, supply_expr_num)

            # Create plot
            plt.close("all")
            fig = plt.figure(figsize=(15, 6))
            gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])

            # Main plot
            ax1 = plt.subplot(gs[0])

            # Create price range for curves and shading
            p_values = np.linspace(0, eq_price_val * 2, 200)

            # Calculate demand and supply curves
            q_demand = demand_func(p_values)
            q_supply = supply_func(p_values)

            # Plot the curves
            ax1.plot(q_demand, p_values, label="Demand", color="blue")
            ax1.plot(q_supply, p_values, label="Supply", color="orange")

            # Create shading for Consumer Surplus
            # Only use points up to equilibrium price
            mask = p_values <= eq_price_val
            p_shade = p_values[mask]
            q_demand_shade = q_demand[mask]

            # Create polygon vertices for consumer surplus
            x_cs = np.concatenate(
                [
                    [eq_quantity_val],  # Start at equilibrium quantity
                    q_demand_shade,  # Follow demand curve
                    [eq_quantity_val],  # Back to equilibrium quantity
                ]
            )
            y_cs = np.concatenate(
                [
                    [eq_price_val],  # Start at equilibrium price
                    p_shade,  # Follow prices
                    [p_shade[-1]],  # Back to lowest price
                ]
            )
            ax1.fill(x_cs, y_cs, alpha=0.3, color="blue", label="Consumer Surplus")

            # Create shading for Producer Surplus
            q_supply_shade = q_supply[mask]

            # Create polygon vertices for producer surplus
            x_ps = np.concatenate(
                [
                    [eq_quantity_val],  # Start at equilibrium quantity
                    q_supply_shade,  # Follow supply curve
                    [eq_quantity_val],  # Back to equilibrium quantity
                ]
            )
            y_ps = np.concatenate(
                [
                    [eq_price_val],  # Start at equilibrium price
                    p_shade,  # Follow prices
                    [p_shade[-1]],  # Back to lowest price
                ]
            )
            ax1.fill(x_ps, y_ps, alpha=0.3, color="orange", label="Producer Surplus")

            # Plot equilibrium point
            ax1.plot([eq_quantity_val], [eq_price_val], "ro", label="Equilibrium")

            # Plot formatting
            ax1.legend()
            ax1.set_xlabel("Quantity")
            ax1.set_ylabel("Price")
            ax1.set_title("Market Equilibrium")
            ax1.grid(True)
            ax1.set_ylim(bottom=0)
            ax1.set_xlim(left=0)

            # Info panel
            ax2 = plt.subplot(gs[1])
            ax2.axis("off")

            # Calculate surpluses
            try:
                # Consumer Surplus
                mask = p_values <= eq_price_val
                p_cs = p_values[mask]
                q_cs = q_demand[mask]
                cs = np.trapz(q_cs - eq_quantity_val, p_cs)

                # Producer Surplus
                q_ps = q_supply[mask]
                ps = np.trapz(eq_quantity_val - q_ps, p_cs)

                total_surplus = cs + ps
                surplus_text = (
                    f"Consumer Surplus: {abs(cs):.2f}\n"
                    f"Producer Surplus: {abs(ps):.2f}\n"
                    f"Total Surplus: {total_surplus:.2f}"
                )
            except Exception as e:
                print(f"Error calculating surplus: {str(e)}")
                surplus_text = "Surplus calculation error"

            # Results text
            results_text = (
                f"Equilibrium Values:\n"
                f"─────────────────\n"
                f"Price: {eq_price_val:.2f}\n"
                f"Quantity: {eq_quantity_val:.2f}\n\n"
                f"Surplus Values:\n"
                f"─────────────────\n"
                f"{surplus_text}\n\n"
                f"Function Types:\n"
                f"─────────────────\n"
                f"Demand: {equilibrium_results['Demand_Type']}\n"
                f"Supply: {equilibrium_results['Supply_Type']}"
            )

            ax2.text(
                0.1,
                0.9,
                results_text,
                transform=ax2.transAxes,
                verticalalignment="top",
                fontfamily="monospace",
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.8, edgecolor="gray"),
            )

            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Error in plotting: {str(e)}")
            return

    # Create widget layout
    widgets_box = widgets.VBox(
        [
            widgets.HTML("<h3>Adjust Parameters:</h3>"),
            widgets.VBox(list(param_inputs.values()), layout=Layout(padding="10px")),
        ]
    )

    # Create interactive widget
    out = widgets.interactive_output(update, param_inputs)
    display(widgets.VBox([widgets_box, out]))
