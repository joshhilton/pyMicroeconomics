# pyMicroeconomics

pyMicroeconomics is a Python package designed for symbolic analysis and visualization of market equilibrium conditions. This package allows you to define various supply and demand curves, calculate market equilibrium points, and visualize these using interactive plots. It integrates several powerful libraries, such as Sympy and Matplotlib, making it a versatile tool for microeconomic analysis.

## Features
- Define different types of supply and demand curves (linear, power, exponential, quadratic).
- Calculate key market metrics, including equilibrium price and quantity.
- Compute consumer surplus, producer surplus, and total surplus.
- Visualize market equilibrium interactively with ipywidgets and Matplotlib.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Installation](#installation)
3. [Usage Examples](#usage-examples)
4. [Documentation](#documentation)
5. [Contributing](#contributing)
6. [License](#license)
7. [Acknowledgments](#acknowledgments)

## Getting Started
To get started with pyMicroeconomics, follow these steps:

### Prerequisites
- Python 3.8 or later
- Jupyter Notebook or JupyterLab for interactive usage

### Installation
To install pyMicroeconomics, use pip:
```bash
pip install pyMicroeconomics
```

This package is intended to be used interactively within Jupyter Notebooks to visualize economic concepts dynamically.

### Setting Up the Environment
You can also use the provided **Dockerfile** and **devcontainer.json** to set up a complete development environment. This is especially useful if you use **Visual Studio Code** or **GitHub Codespaces**. To start developing with pyMicroeconomics, clone the repository and spin up a Docker container:
```bash
git clone https://github.com/joshhilton/pyMicroeconomics.git
cd pyMicroeconomics
docker build -t pymicroeconomics .
docker run -it -v $(pwd):/app pymicroeconomics
```

## Usage Examples
### Example 1: Basic Market Equilibrium
Below is a simple example of finding the market equilibrium using linear supply and demand curves:

```python
import pyMicroeconomics as pm

# Define demand and supply curves
demand = pm.linear_demand()
supply = pm.linear_supply()

# Calculate equilibrium
equilibrium = pm.market_equilibrium(demand, supply)

# Display equilibrium details
pm.display_equilibrium(equilibrium)
pm.plot_equilibrium(equilibrium)
```
This visualization allows users to adjust the parameters interactively and observe changes in real-time.

## Documentation
The complete documentation for pyMicroeconomics, including detailed guides, examples, and the API reference, is available [here](https://github.com/joshhilton/pyMicroeconomics/tree/main/docs).

If you need specific help on running tests or contributing, check out the **Developer Guide** and **Testing Guide** in the `docs/` directory.

## Contributing
We welcome contributions to the project! Please follow these steps to get involved:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

Please refer to the **CONTRIBUTING.md** document for more detailed guidelines.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Built using **SymPy**, **Matplotlib**, and **ipywidgets**.

If you have any questions or need further help, please feel free to open an issue on [GitHub](https://github.com/joshhilton/pyMicroeconomics/issues).

## Badges
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyMicroeconomics)
![Build Status](https://github.com/joshhilton/pyMicroeconomics/workflows/Build/badge.svg)
![License](https://img.shields.io/github/license/joshhilton/pyMicroeconomics)

---
