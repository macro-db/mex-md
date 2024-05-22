import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, kpss

from utils import remove_leading_trailing_nans, transform, read_yaml

df = pd.read_csv("data/DEBUG_2024_05_09.csv")
df["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%m-%d")
df.set_index("fecha", inplace=True)


settings = read_yaml("src/settings.yaml")


print("######### ADF TESTS #########")
for column in df.columns:
    try:
        id = int(column)
    except Exception:
        id = column

    # Perform the Augmented Dickey-Fuller test
    serie = remove_leading_trailing_nans(df[column])
    result = adfuller(serie.fillna(0))

    plt.figure(figsize=(10, 6))
    plt.plot(serie)
    plt.title(column)
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.grid(True)
    plt.show()

    # Extract and print the results
    print(f"ADF Statistic for {column}: {result[0]}")
    print(f"p-value: {result[1]}")
    print("Critical Values:")
    for key, value in result[4].items():
        print(f"\t{key}: {value}")
    print("-" * 40)

"""
print("######### KPSS TESTS #########")
for column in df.columns:
    # Perform the KPSS test
    serie = remove_leading_trailing_nans(df[column])
    result_kpss = kpss(serie)

    # Extract and print the results
    print(f"KPSS Statistic for {column}: {result_kpss[0]}")
    print(f"p-value: {result_kpss[1]}")
    print("Critical Values:")
    for key, value in result_kpss[3].items():
        print(f"\t{key}: {value}")
    print("-" * 40)
"""
