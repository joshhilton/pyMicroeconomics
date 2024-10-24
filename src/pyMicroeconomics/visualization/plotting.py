"""Module for creating interactive market equilibrium plots with adjustable parameters."""

import traceback
from typing import Optional, Dict, Union, Any
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from ipywidgets import widgets
from IPython.display import display
from ..core.symbols import p, q
from ..market.equilibrium.types import EquilibriumResult


def plot_equilibrium(equilibrium_results: Optional[EquilibriumResult]) -> None:
    """
    Creates interactive plot for market equilibrium with surplus calculations.

    Args:
        equilibrium_results: Dictionary containing equilibrium calculation results
    """
    if equilibrium_results is None:
        print("Please provide valid equilibrium results.")
        return

    demand_eq = equilibrium_results.get("Demand_Equation")
    supply_eq = equilibrium_results.get("Supply_Equation")
    demand_type = equilibrium_results.get("Demand_Type")
    supply_type = equilibrium_results.get("Supply_Type")

    # Get the symbolic surplus calculations
    cs_symbolic = equilibrium_results.get("Consumer_Surplus")
    ps_symbolic = equilibrium_results.get("Producer_Surplus")
    total_surplus_symbolic = equilibrium_results.get("Total_Surplus")

    if demand_eq is None or supply_eq is None:
        print("Equilibrium results do not contain valid demand or supply equations.")
        return

    # Get all symbolic parameters
    all_symbols = demand_eq.free_symbols.union(supply_eq.free_symbols) - {p, q}

    # Define default values based on function type
    demand_defaults: Dict[str, Dict[str, float]] = {
        "linear_demand": {"a": 10.0, "b": 2.0},
        "power_demand": {"a": 10.0, "b": 0.5},
        "exponential_demand": {"a": 0.05, "b": 4.6},
        "quadratic_demand": {"a": 100.0, "b": 0.04},
    }

    supply_defaults: Dict[str, Dict[str, float]] = {
        "linear_supply": {"c": 0.0, "d": 2.0},
        "power_supply": {"c": 1.0, "d": 1.5},
        "exponential_supply": {"c": 0.05, "d": 0.0},
        "quadratic_supply": {"c": 0.0, "d": 0.04},
    }

    default_values: Dict[str, float] = {}
    if demand_type in demand_defaults:
        default_values.update(demand_defaults[demand_type])
    if supply_type in supply_defaults:
        default_values.update(supply_defaults[supply_type])

    param_inputs: Dict[str, widgets.FloatText] = {}
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

    def update(**kwargs: float) -> None:
        """Update plot with new parameter values."""
        try:
            # Create parameter substitutions dictionary
            parameter_subs = {symbol: kwargs[str(symbol)] for symbol in all_symbols}

            # Get expressions for demand and supply
            demand_q_expr = sp.solve(demand_eq, q)[0]
            supply_q_expr = sp.solve(supply_eq, q)[0]

            # Create lambda functions for curves
            demand_func = sp.lambdify(p, demand_q_expr.subs(parameter_subs), modules=["numpy"])
            supply_func = sp.lambdify(p, supply_q_expr.subs(parameter_subs), modules=["numpy"])

            # Get equilibrium values from results and substitute parameters
            eq_price_expr = equilibrium_results.get("Equilibrium_Price")
            eq_quantity_expr = equilibrium_results.get("Equilibrium_Quantity")

            if eq_price_expr is None or eq_quantity_expr is None:
                print("Invalid equilibrium values found.")
                return

            eq_price = float(sp.N(eq_price_expr.subs(parameter_subs)))
            eq_quantity = float(sp.N(eq_quantity_expr.subs(parameter_subs)))

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

            # Initialize surplus values
            cs_text = "N/A"
            ps_text = "N/A"
            total_text = "N/A"

            # Calculate surpluses using symbolic expressions
            try:
                if cs_symbolic is not None:
                    cs = float(sp.N(cs_symbolic.subs(parameter_subs)))
                    if cs > 0:  # Only update text if positive
                        cs_text = f"{cs:.2f}"

                if ps_symbolic is not None:
                    ps = float(sp.N(ps_symbolic.subs(parameter_subs)))
                    if ps > 0:  # Only update text if positive
                        ps_text = f"{ps:.2f}"

                if total_surplus_symbolic is not None:
                    total_surplus = float(sp.N(total_surplus_symbolic.subs(parameter_subs)))
                    if total_surplus > 0:  # Only update text if positive
                        total_text = f"{total_surplus:.2f}"

            except Exception as e:
                print(f"Error calculating surpluses: {str(e)}")
                # Variables retain their "N/A" values if an error occurs

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
            try:
                if cs_text != "N/A":
                    cs_value = float(cs_text)  # Safe to convert since we know it's not "N/A"
                    if cs_value > 0:
                        ax1.fill_between(
                            q_demand_valid[mask_d],
                            p_valid[mask_d],
                            [eq_price] * np.sum(mask_d),
                            alpha=0.3,
                            color="blue",
                            label="Consumer Surplus",
                        )

                if ps_text != "N/A":
                    ps_value = float(ps_text)  # Safe to convert since we know it's not "N/A"
                    if ps_value > 0:
                        ax1.fill_between(
                            q_supply_valid[mask_s],
                            [eq_price] * np.sum(mask_s),
                            p_valid[mask_s],
                            alpha=0.3,
                            color="orange",
                            label="Producer Surplus",
                        )
            except ValueError as e:
                print(f"Error shading surpluses: {str(e)}")

            # Plot formatting
            ax1.set_xlabel("Quantity")
            ax1.set_ylabel("Price")
            ax1.set_ylim(bottom=0)
            ax1.grid(True)

            # Info panel
            ax2 = plt.subplot(gs[1])
            ax2.axis("off")
            ax2.legend(*ax1.get_legend_handles_labels(), loc="upper center", bbox_to_anchor=(0.5, 1))

            # Results text with guaranteed defined variables
            calc_text = (
                f"Equilibrium Values:\n"
                f"─────────────────\n"
                f"Price: {eq_price:.2f}\n"
                f"Quantity: {eq_quantity:.2f}\n\n"
                f"Surplus Calculations:\n"
                f"─────────────────\n"
                f"Consumer Surplus: {cs_text}\n"
                f"Producer Surplus: {ps_text}\n"
                f"Total Surplus: {total_text}\n\n"
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
