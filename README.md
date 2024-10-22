# Overview

pyMicroeconomics is package for symbolic analysis and visualization of market equilibrium conditions with various supply and demand curve specifications. This is a wrapper of several packages such as Sympy and Matplotlib. When used interactively, it allows you to build a market equilibrium in an iterative way, starting from the demand and supply functions.

Uses:
- Define different types of supply and demand curves (linear, power, exponential, quadratic)
- Calculate market equilibrium points
- Compute consumer and producer surplus
- Visualize market equilibrium with interactive plots

## Installation

```bash
pip install pyMicroeconomics
```

This package is designed to be used interactively in a Jupyter Notebook.

## Usage Examples

### Basic Market Equilibrium Analysis

```python
from market_equilibrium import linear_demand, linear_supply, market_equilibrium

# Create demand and supply equations
demand = linear_demand()
supply = linear_supply(c_param=20, d_param=3)   # q = 20 + 3p

# Calculate equilibrium
results = market_equilibrium(demand, supply)

# Display results
from market_equilibrium import display_equilibrium
display_equilibrium(results)
```

### Interactive Plotting

```python
from market_equilibrium import plot_equilibrium

# Create interactive plot with adjustable parameters
plot_equilibrium(results)
```

## Example Functions

### Demand Curves
- Linear: $q = a - b p$
- Power: $q = exp(a)*p^b$
- Exponential: $q = exp(ap + b)$
- Quadratic: $q = a - b p^2$

### Supply Curves
- Linear: $q = c + d p$
- Power: $q = exp(c) * p^d$
- Exponential: $q = exp(c*p + d)$
- Quadratic: $q = c + d p^2$

## Contributing

Contributions are welcome! Please submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built using SymPy
- Visualization powered by Matplotlib and ipywidgets

