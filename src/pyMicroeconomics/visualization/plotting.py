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
    """
    Creates interactive plot for market equilibrium with adjustable parameters.

    Args:
        equilibrium_results: Dictionary containing equilibrium calculation results
    """
    if equilibrium_results is None:
        print("Please provide valid equilibrium results.")
        return

    # Get equations and equilibrium values
    demand_eq = equilibrium_results["Demand_Equation"]
    supply_eq = equilibrium_results["Supply_Equation"]
    eq_price = equilibrium_results["Equilibrium_Price"]
    eq_quantity = equilibrium_results["Equilibrium_Quantity"]

    # Get all symbolic parameters
    all_symbols = (demand_eq.free_symbols | supply_eq.free_symbols) - {p, q}

    # Create parameter sliders
    param_inputs = {
        str(symbol): widgets.FloatSlider(
            value=1.0,
            min=0.1,
            max=10.0,
            step=0.1,
            description=str(symbol),
            continuous_update=False,
            description_tooltip=f"Parameter {str(symbol)}",
            layout=Layout(width="500px"),
            style={"description_width": "initial"},
        )
        for symbol in sorted(all_symbols, key=str)
    }

    def update(**kwargs):
        """Update plot with new parameter values."""
        try:
            # Convert kwargs to parameter substitutions
            params = {sp.Symbol(k): v for k, v in kwargs.items()}

            # Get expressions
            demand_expr = sp.solve(demand_eq.equation, q)[0]
            supply_expr = sp.solve(supply_eq.equation, q)[0]

            # Substitute parameters in equilibrium values
            eq_price_val = float(sp.N(eq_price.subs(params)))
            eq_quantity_val = float(sp.N(eq_quantity.subs(params)))

            # Create price range around equilibrium
            p_max = min(eq_price_val * 2, 100)
            p_values = np.linspace(0, p_max, 200)

            # Create lambda functions for curves
            demand_func = sp.lambdify(p, demand_expr.subs(params))
            supply_func = sp.lambdify(p, supply_expr.subs(params))

            # Calculate quantities
            q_demand = demand_func(p_values)
            q_supply = supply_func(p_values)

            # Filter valid points
            valid_demand = (q_demand >= 0) & np.isfinite(q_demand)
            valid_supply = (q_supply >= 0) & np.isfinite(q_supply)

            # Create plot
            plt.close("all")
            fig = plt.figure(figsize=(15, 6))
            gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])

            # Main plot
            ax1 = plt.subplot(gs[0])
            ax1.plot(q_demand[valid_demand], p_values[valid_demand], label="Demand", color="blue")
            ax1.plot(q_supply[valid_supply], p_values[valid_supply], label="Supply", color="orange")
            ax1.plot([eq_quantity_val], [eq_price_val], "ro", label="Equilibrium")

            # Shade surplus areas
            demand_idx = p_values <= eq_price_val
            supply_idx = p_values >= eq_price_val

            if all(valid_demand[demand_idx]) and all(valid_supply[supply_idx]):
                # Consumer surplus
                ax1.fill_betweenx(
                    p_values[demand_idx],
                    q_demand[demand_idx],
                    eq_quantity_val,
                    alpha=0.3,
                    color="blue",
                    label="Consumer Surplus",
                )

                # Producer surplus
                ax1.fill_betweenx(
                    p_values[supply_idx],
                    q_supply[supply_idx],
                    eq_quantity_val,
                    alpha=0.3,
                    color="orange",
                    label="Producer Surplus",
                )

            # Plot formatting
            ax1.set_xlabel("Quantity")
            ax1.set_ylabel("Price")
            ax1.set_title("Market Equilibrium")
            ax1.grid(True)
            ax1.set_ylim(bottom=0)
            ax1.set_xlim(left=0)

            # Info panel
            ax2 = plt.subplot(gs[1])
            ax2.axis("off")

            # Calculate surplus values
            try:
                cs = np.trapezoid(q_demand[demand_idx] - eq_quantity_val, p_values[demand_idx])
                ps = np.trapezoid(eq_quantity_val - q_supply[supply_idx], p_values[supply_idx])
                total_surplus = cs + ps
                surplus_text = (
                    f"Consumer Surplus: {cs:.2f}\n"
                    f"Producer Surplus: {ps:.2f}\n"
                    f"Total Surplus: {total_surplus:.2f}"
                )
            except:
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
