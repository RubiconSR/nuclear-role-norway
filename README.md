# Nuclear Power's Role in the Norwegian Energy System

Analysis of how nuclear power (SMR - Small Modular Reactors) affects electricity prices and the energy mix in Norway towards 2050.

## Overview

This study uses the PowerGAMA power market model to simulate the Nordic electricity system with different levels of nuclear capacity in Norway. The analysis covers a 30-year weather period (1991-2020) to capture variability in hydro inflow, wind, and demand.

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
results/
├── MD/                     # Medium demand case (208 TWh)
│   ├── plots/              # All visualizations
│   └── tables/             # Data tables (CSV and TXT)
└── IC/                     # Increased consumption case (230 TWh)
    ├── plots/
    └── tables/
```

## Methodology

- **Model**: PowerGAMA (Power Grid Model Analysis)
- **Time resolution**: Hourly
- **Simulation period**: 1991-2020 (30 weather years)
- **Geographic scope**: Nordic countries + interconnections

## Data Sources

- Demand profiles: ENTSO-E
- Generation capacity: TYNDP 2022 projections for 2050
- Hydro inflow: Historical data 1991-2020
- Wind/solar profiles: Renewables.ninja

## Contact

For questions about this analysis, please open an issue in this repository.
