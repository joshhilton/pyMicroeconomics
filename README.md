# Market Equilibrium Analysis

pyMicroeconomics is package for symbolic analysis and visualization of market equilibrium conditions with various supply and demand curve specifications.

## Overview

This package provides tools for:
- Defining different types of supply and demand curves (linear, power, exponential, quadratic)
- Calculating market equilibrium points
- Computing consumer and producer surplus
- Visualizing market equilibrium with interactive plots

## Installation

```bash
pip install pyMicroeconomics
```

## Requirements

- Python 3.x
- SymPy
- NumPy
- Matplotlib
- IPython
- ipywidgets
- SciPy

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
from market_equilibrium import display_equilibrium_results
display_equilibrium_results(results)
```

### Interactive Plotting

```python
from market_equilibrium import plot_market_equilibrium

# Create interactive plot with adjustable parameters
plot_market_equilibrium(results)
```

## Supported Curve Types

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

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built using SymPy
- Visualization powered by Matplotlib and ipywidgets

