import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
from functions.work_functions import *
from functions.global_functions import *
from functions.database_functions import *
from zoneinfo import ZoneInfo
from powergama.database import Database


# === General Configurations ===
SIM_YEAR_START = 1991
SIM_YEAR_END = 2020
CASE_YEAR = 2050
SCENARIO = 'SMR1'
VERSION = 'v1'
TIMEZONE = ZoneInfo("UTC")

DATE_START = pd.Timestamp(f'{SIM_YEAR_START}-01-01 00:00:00', tz='UTC')
DATE_END = pd.Timestamp(f'{SIM_YEAR_END}-12-31 23:00:00', tz='UTC')

# Get base directory dynamically
try:
    BASE_DIR = pathlib.Path(__file__).parent
except NameError:
    BASE_DIR = pathlib.Path().cwd()
    BASE_DIR = BASE_DIR / f'CASE_{CASE_YEAR}_MD' / f'scenario_{SCENARIO}'

# === File Paths ===
SQL_FILE = BASE_DIR / f"powergama_{SCENARIO}_{VERSION}_{SIM_YEAR_START}_{SIM_YEAR_END}.sqlite"
DATA_PATH = BASE_DIR / 'data'
OUTPUT_PATH = BASE_DIR / 'results'
OUTPUT_PATH_PLOTS = BASE_DIR / 'results' / 'plots'

# === Initialize Database and Grid Data ===
data, time_max_min = setup_grid(VERSION, DATE_START, DATE_END, DATA_PATH, SCENARIO)
database = Database(SQL_FILE)

plt.rcParams.update({
    "text.usetex": False,
    "font.family": "serif",
    "font.serif": ['cmr10'],
    "axes.formatter.use_mathtext": True,
    "axes.unicode_minus": False
})


# %% === ZONAL PRICE MAP ===
zones = ['NO1', 'NO2', 'NO3', 'NO4', 'NO5']
year_range = list(range(SIM_YEAR_START, SIM_YEAR_END + 1))
price_matrix, log = createZonePriceMatrix(data, database, zones, year_range, TIMEZONE, SIM_YEAR_START, SIM_YEAR_END)
# Plot Zonal Price Matrix
colormap = "YlOrRd"
title_map = None
plot_config = {
    'save_fig': True,
    'OUTPUT_PATH_PLOTS': OUTPUT_PATH_PLOTS,
    'start': SIM_YEAR_START,
    'end': SIM_YEAR_END,
    'version': VERSION,
    'colormap': colormap,
    'title': title_map,
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


# %% === GET ENERGY MIX ===
START = {"year": 1991, "month": 1, "day": 1, "hour": 0}
END = {"year": 2020, "month": 12, "day": 31, "hour": 23}
time_period = get_hour_range(SIM_YEAR_START, SIM_YEAR_END, TIMEZONE, START, END)
variable_type = "energy"
dfplot = plotEnergyMix(data=data, database=database, areas=['NO'],
                       timeMaxMin=time_period, variable=variable_type).fillna(0)
plt.savefig(OUTPUT_PATH_PLOTS / f'EnergyMix_{SCENARIO}_{VERSION}.pdf', dpi=300, bbox_inches='tight')
plt.close()


# %% === PLOT ZONAL PRICES (DURATION CURVE) ===
START = {"year": 1991, "month": 1, "day": 1, "hour": 0}
END = {"year": 2020, "month": 12, "day": 31, "hour": 23}
plot_config = {
    'zones': ['NO1', 'NO2', 'NO3', 'NO4', 'NO5'],
    "plot_by_year": False,
    "duration_curve": True,
    "save_fig": True,
    "interval": 1,
    "tex_font": False
}
time_ZP = get_hour_range(SIM_YEAR_START, SIM_YEAR_END, TIMEZONE, START, END)
calcPlot_ZonalPrices_FromDB(data, database, time_ZP, OUTPUT_PATH_PLOTS, DATE_START, plot_config)


# %% === PLOT STORAGE FILLING FOR AREAS ===
START = {"year": 1991, "month": 1, "day": 1, "hour": 0}
END = {"year": 2020, "month": 12, "day": 31, "hour": 23}
plot_config = {
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
    'title': None,
}
time_SF = get_hour_range(SIM_YEAR_START, SIM_YEAR_END, TIMEZONE, START, END)
OUTPUT_PATH_PLOTS_RESERVOIR = OUTPUT_PATH_PLOTS / 'reservoir'
plot_SF_Areas_FromDB(data, database, time_SF, OUTPUT_PATH_PLOTS_RESERVOIR, DATE_START, plot_config, START, END)
