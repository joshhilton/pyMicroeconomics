"""
Module for creating interactive market equilibrium plots with adjustable parameters.
Provides visualization tools for supply, demand, and economic surplus analysis.
"""

import traceback
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from ipywidgets import widgets
from IPython.display import display
from .symbols import p, q


def plot_equilibrium(equilibrium_results):
    """
    Creates interactive plot for market equilibrium with surplus calculations.
    """
    if equilibrium_results is None:
        print("Please provide valid equilibrium results.")
        return

    demand_eq = equilibrium_results.get("Demand Equation")
    supply_eq = equilibrium_results.get("Supply Equation")
    demand_type = equilibrium_results.get("Demand Type")
    supply_type = equilibrium_results.get("Supply Type")

    # Get the symbolic surplus calculations
    cs_symbolic = equilibrium_results.get("Consumer Surplus")
    ps_symbolic = equilibrium_results.get("Producer Surplus")
    total_surplus_symbolic = equilibrium_results.get("Total Surplus")

    if demand_eq is None or supply_eq is None:
        print("Equilibrium results do not contain valid demand or supply equations.")
        return

    # Get all symbolic parameters
    all_symbols = demand_eq.free_symbols.union(supply_eq.free_symbols) - {p, q}

    # Define default values based on function type
    demand_defaults = {
        "linear_demand": {"a": 10.0, "b": 2.0},
        "power_demand": {"a": 10.0, "b": 0.5},
        "exponential_demand": {"a": 0.05, "b": 4.6},
        "quadratic_demand": {"a": 100.0, "b": 0.04},
    }

    supply_defaults = {
        "linear_supply": {"c": 0.0, "d": 2.0},
        "power_supply": {"c": 1.0, "d": 1.5},
        "exponential_supply": {"c": 0.05, "d": 0.0},
        "quadratic_supply": {"c": 0.0, "d": 0.04},
    }

    default_values = {}
    if demand_type in demand_defaults:
        default_values.update(demand_defaults[demand_type])
    if supply_type in supply_defaults:
        default_values.update(supply_defaults[supply_type])

    param_inputs = {}
    for symbol in sorted(all_symbols, key=str):
        param_letter = str(symbol)
        default_value = default_values.get(param_letter)
        if default_value is None:
            print(f"Warning: No default value found for parameter {param_letter}, using 1.0")
            default_value = 1.0
        param_inputs[param_letter] = widgets.FloatText(
            value=default_value,
            description=param_letter,
            style={"description_width": "initial"},
        )

    def update(**kwargs):
        try:
            # Create parameter substitutions dictionary
            parameter_subs = {symbol: kwargs[str(symbol)] for symbol in all_symbols}

            # Get expressions for demand and supply
            demand_q_expr = sp.solve(demand_eq, q)[0]
            supply_q_expr = sp.solve(supply_eq, q)[0]

            # Create lambda functions for curves
            demand_func = sp.lambdify(p, demand_q_expr.subs(parameter_subs), modules=["numpy"])
            supply_func = sp.lambdify(p, supply_q_expr.subs(parameter_subs), modules=["numpy"])

            # Get equilibrium values
            eq_price = float(sp.N(equilibrium_results["Equilibrium Price"].subs(parameter_subs)))
            eq_quantity = float(sp.N(equilibrium_results["Equilibrium Quantity"].subs(parameter_subs)))

            if eq_price <= 0 or eq_quantity <= 0:
                print("Invalid equilibrium with negative values found.")
                return

            # Calculate plot range
            p_max = min(eq_price * 2, 1000)
            p_min = 0
            p_values = np.linspace(p_min, p_max, 400)

            # Calculate quantities
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

            # Calculate surpluses using symbolic expressions
            try:
                cs = float(sp.N(cs_symbolic.subs(parameter_subs)))
                ps = float(sp.N(ps_symbolic.subs(parameter_subs)))
                total_surplus = float(sp.N(total_surplus_symbolic.subs(parameter_subs)))
            except Exception as e:
                print(f"Error calculating surpluses: {str(e)}")
                cs = None
                ps = None
                total_surplus = None

            # Create plot
            plt.close("all")
            fig = plt.figure(figsize=(15, 6))
            gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])

            # Main plot
            ax1 = plt.subplot(gs[0])

            # Plot the curves
            ax1.plot(q_demand_valid, p_valid, label="Demand", color="blue")
            ax1.plot(q_supply_valid, p_valid, label="Supply", color="orange")
            ax1.plot([eq_quantity], [eq_price], "ro", label="Equilibrium")

            # Create masks for surplus shading
            mask_d = p_valid >= eq_price
            mask_s = p_valid <= eq_price

            # Shade surplus areas if they are valid
            if cs is not None and cs > 0:
                ax1.fill_between(
                    q_demand_valid[mask_d],
                    p_valid[mask_d],
                    [eq_price] * np.sum(mask_d),
                    alpha=0.3,
                    color="blue",
                    label="Consumer Surplus",
                )

            if ps is not None and ps > 0:
                ax1.fill_between(
                    q_supply_valid[mask_s],
                    [eq_price] * np.sum(mask_s),
                    p_valid[mask_s],
                    alpha=0.3,
                    color="orange",
                    label="Producer Surplus",
                )

            # Plot formatting
            ax1.set_xlabel("Quantity")
            ax1.set_ylabel("Price")
            ax1.set_ylim(bottom=0)
            ax1.grid(True)

            # Info panel
            ax2 = plt.subplot(gs[1])
            ax2.axis("off")
            ax2.legend(*ax1.get_legend_handles_labels(), loc="upper center", bbox_to_anchor=(0.5, 1))

            # Results text
            calc_text = (
                f"Equilibrium Values:\n"
                f"─────────────────\n"
                f"Price: {eq_price:.2f}\n"
                f"Quantity: {eq_quantity:.2f}\n\n"
                f"Surplus Calculations:\n"
                f"─────────────────\n"
                f"Consumer Surplus: {f'{cs:.2f}' if cs is not None else 'N/A'}\n"
                f"Producer Surplus: {f'{ps:.2f}' if ps is not None else 'N/A'}\n"
                f"Total Surplus: {f'{total_surplus:.2f}' if total_surplus is not None else 'N/A'}\n\n"
                f"Function Types:\n"
                f"─────────────────\n"
                f"Demand: {demand_type}\n"
                f"Supply: {supply_type}"
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

            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Error in plotting: {str(e)}")
            traceback.print_exc()
            return

    # Create interactive widget
    out = widgets.interactive_output(update, param_inputs)
    display(widgets.VBox([widgets.HTML("<h3>Adjust Parameters:</h3>"), widgets.VBox(list(param_inputs.values())), out]))
