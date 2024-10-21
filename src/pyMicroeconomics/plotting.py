"""
Module for creating interactive market equilibrium plots with adjustable parameters.
Provides visualization tools for supply, demand, and economic surplus analysis.
"""

import traceback
from scipy import integrate
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from ipywidgets import widgets
from IPython.display import display
from .symbols import p, q


def plot_market_equilibrium(equilibrium_results):
    """
    Creates interactive plot for market equilibrium with surplus calculations.

    Args:
        equilibrium_results (dict): Dictionary containing equilibrium analysis results

    Returns:
        None: Displays interactive plot widget
    """
    if equilibrium_results is None:
        print("Please provide valid equilibrium results.")
        return

    demand_eq = equilibrium_results.get("Demand Equation")
    supply_eq = equilibrium_results.get("Supply Equation")

    if demand_eq is None or supply_eq is None:
        print("Equilibrium results do not contain valid demand or supply equations.")
        return

    # Get all symbolic parameters from equations
    all_symbols = demand_eq.free_symbols.union(supply_eq.free_symbols) - {p, q}

    # Create text input widgets for each parameter, sorted alphabetically
    param_inputs = {}
    for param in sorted(all_symbols, key=str):
        param_inputs[str(param)] = widgets.FloatText(
            value=1.0, description=str(param), style={"description_width": "initial"}
        )

    def update(**kwargs):
        try:
            # Create parameter substitutions dictionary matching the actual symbols
            parameter_subs = {}
            for k, v in kwargs.items():
                for sym in all_symbols:
                    if str(sym) == k:
                        parameter_subs[sym] = sp.Float(v)
                        break

            # Substitute parameter values into equations
            demand_eq_sub = demand_eq.subs(parameter_subs)
            supply_eq_sub = supply_eq.subs(parameter_subs)

            # Solve for equilibrium with numeric values
            equilibrium = sp.solve([demand_eq_sub, supply_eq_sub], (p, q), dict=True)

            if not equilibrium:
                print("No equilibrium found for these parameter values.")
                return

            equilibrium = equilibrium[0]

            # Get expressions and substitute parameters again
            p_expr = equilibrium[p].subs(parameter_subs)
            q_expr = equilibrium[q].subs(parameter_subs)

            # Convert to float
            p_eq = float(p_expr)
            q_eq = float(q_expr)

            if p_eq <= 0 or q_eq <= 0:
                print("Invalid equilibrium with negative values found.")
                return

            # Solve for q in terms of p
            demand_q_expr = sp.solve(demand_eq_sub, q)[0]
            supply_q_expr = sp.solve(supply_eq_sub, q)[0]

            # Create lambda functions for faster evaluation
            demand_func = sp.lambdify(p, demand_q_expr, modules=["numpy"])
            supply_func = sp.lambdify(p, supply_q_expr, modules=["numpy"])

            # Generate price values around equilibrium
            # Calculate y-intercepts
            demand_y_intercept = float(demand_func(0)) if np.isfinite(demand_func(0)) else None
            supply_y_intercept = float(supply_func(0)) if np.isfinite(supply_func(0)) else None

            # Set price range based on equilibrium and y-intercepts
            p_min = 0
            p_max = (
                max(
                    p_eq * 1.8,
                    demand_y_intercept if demand_y_intercept is not None else 0,
                    supply_y_intercept if supply_y_intercept is not None else 0,
                )
                * 1.2
            )  # Add 20% margin

            p_values = np.linspace(p_min, p_max, 400)

            # Calculate quantities using vectorized operations
            q_demand = demand_func(p_values)
            q_supply = supply_func(p_values)

            # Filter valid points
            valid_points = (q_demand >= 0) & (q_supply >= 0) & np.isfinite(q_demand) & np.isfinite(q_supply)
            p_valid = p_values[valid_points]
            q_demand_valid = q_demand[valid_points]
            q_supply_valid = q_supply[valid_points]

            if len(p_valid) == 0:
                print("No valid points found for plotting.")
                return

            # Create masks for surplus calculations
            mask_d = p_valid >= p_eq
            mask_s = p_valid <= p_eq

            # Calculate surpluses
            consumer_surplus = integrate.trapezoid(
                (p_valid[mask_d] - p_eq) * q_demand_valid[mask_d], dx=(p_max - p_eq) / sum(mask_d)
            )

            producer_surplus = integrate.trapezoid(
                (p_eq - p_valid[mask_s]) * q_supply_valid[mask_s], dx=(p_eq - p_min) / sum(mask_s)
            )

            total_surplus = consumer_surplus + producer_surplus

            # Create figure with GridSpec for plot and info panel
            plt.close("all")  # Close any existing figures
            fig = plt.figure(figsize=(15, 6))
            gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])

            # Create main plot
            ax1 = plt.subplot(gs[0])
            ax1.plot(q_demand_valid, p_valid, label="Demand", color="blue")
            ax1.plot(q_supply_valid, p_valid, label="Supply", color="orange")
            ax1.plot([q_eq], [p_eq], "ro", label="Equilibrium")

            # Add shaded areas for surpluses
            ax1.fill_between(
                q_demand_valid[mask_d],
                p_valid[mask_d],
                [p_eq] * np.sum(mask_d),
                alpha=0.3,
                color="blue",
                label="Consumer Surplus",
            )

            ax1.fill_between(
                q_supply_valid[mask_s],
                [p_eq] * np.sum(mask_s),
                p_valid[mask_s],
                alpha=0.3,
                color="orange",
                label="Producer Surplus",
            )

            ax1.set_xlabel("Quantity")
            ax1.set_ylabel("Price")
            ax1.set_title("Market Equilibrium")
            ax1.set_ylim(bottom=0)
            ax1.grid(True)

            # Create info panel
            ax2 = plt.subplot(gs[1])
            ax2.axis("off")  # Hide axes

            # Add legend to info panel
            ax2.legend(*ax1.get_legend_handles_labels(), loc="upper center", bbox_to_anchor=(0.5, 1))

            # Add calculations text to info panel
            calc_text = (
                f"Equilibrium Values:\n"
                f"─────────────────\n"
                f"Price: {p_eq:.2f}\n"
                f"Quantity: {q_eq:.2f}\n\n"
                f"Surplus Calculations:\n"
                f"─────────────────\n"
                f"Consumer Surplus: {consumer_surplus:.2f}\n"
                f"Producer Surplus: {producer_surplus:.2f}\n"
                f"Total Surplus: {total_surplus:.2f}"
            )

            ax2.text(
                0.1,
                0.7,
                calc_text,
                transform=ax2.transAxes,
                verticalalignment="top",
                fontfamily="monospace",
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.8, edgecolor="gray"),
            )

            # Adjust layout
            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Error in plotting: {str(e)}")
            traceback.print_exc()
            return

    # Create interactive widget with vertical layout
    out = widgets.interactive_output(update, param_inputs)
    display(widgets.VBox([widgets.VBox(list(param_inputs.values())), out]))
