import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
from functions.work_functions import *
from functions.global_functions import *
from functions.database_functions import *
from functions.plot_functions import *
from zoneinfo import ZoneInfo
from powergama.database import Database
import pandas as pd

# === General Configurations ===
SIM_YEAR_START = 1991
SIM_YEAR_END = 2020
CASE_YEAR = 2050
SCENARIO = 'BL'
VERSION = 'v1'
TIMEZONE = ZoneInfo("UTC")

DATE_START = pd.Timestamp(f'{SIM_YEAR_START}-01-01 00:00:00', tz='UTC')
DATE_END = pd.Timestamp(f'{SIM_YEAR_END}-12-31 23:00:00', tz='UTC')

# Get base directory
try:
    BASE_DIR = pathlib.Path(__file__).parent
except NameError:
    BASE_DIR = pathlib.Path().cwd() / f'CASE_{CASE_YEAR}_MD' / f'scenario_{SCENARIO}'

# === File Paths ===
SQL_FILE = BASE_DIR / f"powergama_{SCENARIO}_{VERSION}_{SIM_YEAR_START}_{SIM_YEAR_END}.sqlite"
DATA_PATH = BASE_DIR / 'data'
OUTPUT_PATH = BASE_DIR / 'results'
OUTPUT_PATH_PLOTS = BASE_DIR / 'results' / 'plots'

# Create directories if needed
OUTPUT_PATH_PLOTS.mkdir(parents=True, exist_ok=True)
(OUTPUT_PATH_PLOTS / 'reservoir').mkdir(parents=True, exist_ok=True)

# === Initialize Database and Grid Data ===
print("Loading grid data and database...")
data, time_max_min = setup_grid(VERSION, DATE_START, DATE_END, DATA_PATH, SCENARIO)
database = Database(SQL_FILE)

# Matplotlib config (no LaTeX)
plt.rcParams.update({
    "text.usetex": False,
    "font.family": "serif",
    "font.serif": ['cmr10'],
    "axes.formatter.use_mathtext": True,
    "axes.unicode_minus": False
})

# %% === 1. ZONAL PRICE MATRIX (NO1-NO5) ===
print("\n=== 1. Creating Zonal Price Matrix (NO1-NO5) ===")
zones_NO = ['NO1', 'NO2', 'NO3', 'NO4', 'NO5']
year_range = list(range(SIM_YEAR_START, SIM_YEAR_END + 1))
price_matrix, log = createZonePriceMatrix(data, database, zones_NO, year_range, TIMEZONE, SIM_YEAR_START, SIM_YEAR_END)

plot_config = {
    'save_fig': True,
    'OUTPUT_PATH_PLOTS': OUTPUT_PATH_PLOTS,
    'start': SIM_YEAR_START,
    'end': SIM_YEAR_END,
    'version': VERSION,
    'colormap': "YlOrRd",
    'title': f"Average Zonal Prices - {SCENARIO}",
    'fig_size': (10, 5),
    'dpi': 300,
    'cbar_label': "Price [EUR/MWh]",
    'cbar_xpos': 0.02,
    'bbox_inches': 'tight',
    'rotation_x': 65,
    'rotation_y': 0,
    'ha_x': 'right',
    'va_x': 'top',
    'ha_y': 'right',
    'va_y': 'center',
    'x_label_xShift': 5 / 72,
    'x_label_yShift': 0.01,
    'x_label': 'Weather Year',
}
plotZonePriceMatrix(price_matrix, plot_config)
print(f"Saved: ZonePriceMatrix_{VERSION}_{SIM_YEAR_START}_{SIM_YEAR_END}.pdf")

# %% === 2. ENERGY MIX - STACKED BAR CHART ===
print("\n=== 2. Creating Energy Mix Plot (Norway) ===")
START = {"year": 1991, "month": 1, "day": 1, "hour": 0}
END = {"year": 2020, "month": 12, "day": 31, "hour": 23}
time_period = get_hour_range(SIM_YEAR_START, SIM_YEAR_END, TIMEZONE, START, END)

# Get energy mix data
dfplot = getEnergyMix(data, database, timeMaxMin=time_period, relative=False, variable="energy")

# Filter for Norway only
norway_areas = ['NO']
dfplot_NO = dfplot.loc[dfplot.index.isin(norway_areas)]

# Create stacked bar plot
fig, ax = plt.subplots(figsize=(10, 6))
color_map = {
    "biomass": "#8c564b",
    "fossil_gas": "#d62728",
    "fossil_other": "#333333",
    "hydro": "#1f77b4",
    "nuclear": "#9467bd",
    "ror": "#17becf",
    "solar": "#ff7f0e",
    "wind_off": "#2ca02c",
    "wind_on": "#98df8a",
}

# Convert to TWh
dfplot_TWh = dfplot_NO / 1e6

# Plot stacked bars
dfplot_TWh.plot(kind='bar', stacked=True, ax=ax, color=[color_map.get(c, '#888888') for c in dfplot_TWh.columns])
ax.set_ylabel('Energy Production [TWh]')
ax.set_xlabel('Area')
ax.set_title(f'Energy Mix - {SCENARIO} (30-year average)')
ax.legend(title='Generator Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT_PATH_PLOTS / f'EnergyMix_{SCENARIO}_{VERSION}.pdf', dpi=300, bbox_inches='tight')
plt.close()
print(f"Saved: EnergyMix_{SCENARIO}_{VERSION}.pdf")

# %% === 3. PRICE DURATION CURVE (NO1-NO5) ===
print("\n=== 3. Creating Price Duration Curve ===")
START = {"year": 1991, "month": 1, "day": 1, "hour": 0}
END = {"year": 2020, "month": 12, "day": 31, "hour": 23}
time_ZP = get_hour_range(SIM_YEAR_START, SIM_YEAR_END, TIMEZONE, START, END)

plot_config_dc = {
    'zones': ['NO1', 'NO2', 'NO3', 'NO4', 'NO5'],
    "plot_by_year": False,
    "duration_curve": True,
    "save_fig": True,
    "interval": 1,
    "tex_font": False
}
calcPlot_ZonalPrices_FromDB(data, database, time_ZP, OUTPUT_PATH_PLOTS, DATE_START, plot_config_dc)
print("Saved: Price duration curve plots")

# %% === 4. RESERVOIR FILLING (NORWAY) ===
print("\n=== 4. Creating Reservoir Filling Plot (Norway) ===")
START = {"year": 1991, "month": 1, "day": 1, "hour": 0}
END = {"year": 2020, "month": 12, "day": 31, "hour": 23}
time_SF = get_hour_range(SIM_YEAR_START, SIM_YEAR_END, TIMEZONE, START, END)

OUTPUT_PATH_PLOTS_RESERVOIR = OUTPUT_PATH_PLOTS / 'reservoir'

plot_config_sf = {
    'areas': ['NO'],
    'relative': True,
    "plot_by_year": True,
    "duration_curve": False,
    "save_fig": True,
    "interval": 1,
    'empty_threshold': 1e-6,
    'include_legend': False,
    'fig_size': (12, 6),
    'tex_font': False,
    'title': f'Reservoir Filling - Norway - {SCENARIO}',
}
plot_SF_Areas_FromDB(data, database, time_SF, OUTPUT_PATH_PLOTS_RESERVOIR, DATE_START, plot_config_sf, START, END)
print("Saved: Reservoir filling plots to reservoir/")

# %% === 5. CAPACITY FACTOR TABLE ===
print("\n=== 5. Capacity Factors for Norway ===")

# Get Norwegian generators
norway_nodes = data.node[data.node['area'] == 'NO']['id'].tolist()
norway_gen_idx = data.generator[data.generator['node'].isin(norway_nodes)].index.tolist()

gen_output = database.getResultGeneratorPowerSum(time_period)
gen_pmax = data.generator['pmax']
gen_info = data.generator[['node', 'type', 'pmax']].copy()
gen_info['production'] = gen_output
gen_info_norway = gen_info[gen_info.index.isin(norway_gen_idx)]

capacity_by_type = gen_info_norway.groupby('type')['pmax'].sum()
production_by_type = gen_info_norway.groupby('type')['production'].sum()

total_hours = 8766.4 * 30
capacity_factor = production_by_type / (capacity_by_type * total_hours)

cf_results = pd.DataFrame({
    'Type': capacity_by_type.index,
    'Installed_MW': capacity_by_type.values,
    'Production_TWh': production_by_type.values / 1e6,
    'Capacity_Factor': capacity_factor.values
}).sort_values('Capacity_Factor', ascending=False)

print("\n" + "=" * 70)
print(f"CAPACITY FACTORS FOR NORWAY - {SCENARIO}")
print("=" * 70)
print(f"{'Type':<15} {'Installed (MW)':>12} {'Prod (TWh)':>12} {'Cap Factor':>12}")
print("-" * 70)
for _, row in cf_results.iterrows():
    cf_pct = row['Capacity_Factor'] * 100 if not pd.isna(row['Capacity_Factor']) else 0
    print(f"{row['Type']:<15} {row['Installed_MW']:>12,.0f} {row['Production_TWh']:>12,.1f} {cf_pct:>11.1f}%")
print("=" * 70)

cf_results.to_csv(OUTPUT_PATH / 'data_files' / f'capacity_factors_{SCENARIO}.csv', index=False)

# === Summary ===
print("\n" + "=" * 70)
print(f"ALL PLOTS SAVED TO: {OUTPUT_PATH_PLOTS}")
print("=" * 70)
print("Files generated:")
print(f"  - ZonePriceMatrix_{VERSION}_{SIM_YEAR_START}_{SIM_YEAR_END}.pdf")
print(f"  - EnergyMix_{SCENARIO}_{VERSION}.pdf")
print("  - Price duration curve plots")
print("  - reservoir/*.pdf (reservoir filling)")
print("=" * 70)
