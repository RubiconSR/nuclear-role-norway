# Nuclear Power's Role in the Norwegian Energy System

Analysis of how nuclear power (SMR - Small Modular Reactors) affects electricity prices and the energy mix in Norway towards 2050.

## Overview

This study uses the PowerGAMA power market model to simulate the Nordic electricity system with different levels of nuclear capacity in Norway. The analysis covers a 30-year weather period (1991-2020) to capture variability in hydro inflow, wind, and demand.

## Model and Tools

### PowerGAMA
This analysis is built on [PowerGAMA](https://github.com/powergama/powergama) (Power Grid Model Analysis), an open-source power market simulation tool developed at SINTEF Energy Research.

- **License**: MIT License
- **Developer**: Harald G Svendsen, SINTEF Energy Research
- **Documentation**: [PowerGAMA Documentation](https://powergama.readthedocs.io/)

### NordicNuclearAnalysis
The analysis framework, scenario configurations, and input data are based on [NordicNuclearAnalysis](https://github.com/Zynecut/NordicNuclearAnalysis), which provides:

- Scenario setup scripts (`CASE_2035/`)
- Analysis functions (`functions/`)
- Data processing utilities (`scripts/`)
- Nordic power system baseline data

### Analysis Framework
The analysis scripts in `functions/` extend PowerGAMA with:
- Database query functions for result extraction
- Plotting functions for visualization
- Work functions for scenario setup

## Scenarios

Two demand cases are analyzed:

| Case | Annual Demand | Description |
|------|---------------|-------------|
| **MD** | 208 TWh | Medium demand scenario |
| **IC** | 230 TWh | Industrial/increased consumption scenario |

For each demand case, four nuclear capacity scenarios are simulated:

| Scenario | Nuclear Capacity | Description |
|----------|-----------------|-------------|
| **BL** | 0 GW | Baseline (no nuclear) |
| **SMR1** | 1.5 GW | 5 × 300 MW SMR (one per price zone) |
| **SMR3** | 4.5 GW | 15 × 300 MW SMR |
| **SMR6** | 9.0 GW | 30 × 300 MW SMR |

## Key Results

### Price Impact

| Case | Baseline | SMR6 | Reduction |
|------|----------|------|-----------|
| MD (208 TWh) | 121.6 €/MWh | 88.4 €/MWh | -27% |
| IC (230 TWh) | 146.8 €/MWh | 97.1 €/MWh | -34% |

### Nuclear Capacity Factors

- SMR achieves 90-97% capacity factor
- Higher capacity factor at higher demand (IC > MD)
- Slight decrease with more capacity (price cannibalization)

### Displacement Effects

- Hydro reservoir utilization decreases significantly (acts as backup)
- Gas power is displaced
- Wind and solar largely unaffected

## Repository Structure

```
nuclear-role-norway/
├── CASE_2035/              # Input configurations from base scenarios
│   ├── scenario_BL/        # Baseline scenario setup
│   ├── scenario_FDT/       # FDT scenario setup
│   └── scenario_VDT/       # VDT scenario setup
├── functions/              # Analysis and plotting functions
│   ├── database_functions.py   # Database queries
│   ├── plot_functions.py       # Visualization
│   ├── global_functions.py     # Utility functions
│   └── work_functions.py       # Scenario setup
├── powergama/              # PowerGAMA simulation library
│   ├── GridData.py         # Grid data structures
│   ├── LpProblemPyomo.py   # LP optimization
│   ├── Results.py          # Result handling
│   └── database.py         # SQLite interface
├── scripts/                # Data processing utilities
├── results/                # Simulation results
│   ├── MD/                 # Medium demand (208 TWh)
│   │   ├── plots/
│   │   └── tables/
│   └── IC/                 # Increased consumption (230 TWh)
│       ├── plots/
│       └── tables/
└── README.md
```

## Methodology

- **Model**: PowerGAMA (Power Grid Model Analysis)
- **Solver**: HiGHS (Linear Programming)
- **Time resolution**: Hourly (8760 hours × 30 years = 262,968 timesteps)
- **Simulation period**: 1991-2020 (30 weather years)
- **Geographic scope**: Nordic countries (NO, SE, FI, DK) + interconnections

### SMR Assumptions

| Parameter | Value |
|-----------|-------|
| Unit size | 300 MW |
| Fuel cost | 9.37 €/MWh |
| Availability | 100% (no outages modeled) |
| Location | Distributed across NO1-NO5 |

## Data Sources

- **Demand profiles**: ENTSO-E TYNDP 2022
- **Generation capacity**: TYNDP 2022 projections for 2050
- **Hydro inflow**: Historical data 1991-2020
- **Wind/solar profiles**: Renewables.ninja
- **Fuel costs**: Based on 2050 projections (gas: 137.52 €/MWh incl. CO2)

## Requirements

- Python 3.9+
- PowerGAMA dependencies (pandas, numpy, pyomo)
- HiGHS solver

## Contact

For questions about this analysis, please open an issue in this repository.
