import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

from utils import read_yaml

df = pd.read_csv("data/MD_2024_04_19.csv")
df["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%m-%d")
df.set_index("fecha", inplace=True)


#### DATA GROUPS ####
series = read_yaml("src/settings.yaml")

factors = {str(serie) : ['Global', series[serie]['group']] for serie in series}
factor_multiplicities = {'Global': 2}
factor_orders = {
    'Group 1': 1,
    'Group 2': 1,
    'Group 4': 1,
    'Group 5': 1,
    'Group 6': 1,
    'Group 7': 1,
    'Group 8': 1,
    'Global': 4}

endog_m = df.loc['2000':, :]
print(endog_m['SR17536'])

# Construct the dynamic factor model
model = sm.tsa.DynamicFactorMQ(
    endog_m,
    factors=factors, factor_orders=factor_orders,
    factor_multiplicities=factor_multiplicities)

#print(model.summary())

results = model.fit(disp=10, maxiter=50)
print(results.summary())



with sns.color_palette('deep'):
    fig = results.plot_coefficients_of_determination(method='individual', figsize=(14, 9))
    fig.suptitle(r'$R^2$ - regression on individual factors', fontsize=14, fontweight=600)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()