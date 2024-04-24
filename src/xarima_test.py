import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from df_utils import *


# Function to remove leading and trailing NaNs from a series
def remove_leading_trailing_nans(series):
    start_index = series.first_valid_index()
    end_index = series.last_valid_index()
    return series.loc[start_index:end_index]


# Apply the function to each series in the DataFrame
# cleaned_df = df.apply(remove_leading_trailing_nans)

series = read_yaml("src/settings.yaml")


# Read the CSV file into a DataFrame
df = pd.read_csv("data/MD_2024_04_16.csv")

df["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%m-%d")
df.set_index("fecha", inplace=True)

df2 = pd.DataFrame(index=df.index.copy())

for column in df:
    try:
        id = int(column)
    except Exception:
        id = column

    if series[id]["sa"] == 0:
        serie = remove_leading_trailing_nans(df[column])
        max = 10 * np.max(np.abs(serie))
        print(max)
        serie.fillna(max, inplace=True)

        # Plot the series
        """
        plt.figure(figsize=(10, 6))
        plt.plot(serie)
        plt.title(column)
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.grid(True)
        plt.show()
        """
        res = sm.tsa.x13_arima_analysis(serie, x12path="x13as", outlier=True)

        if res:
            # Create a grid of plots for the series
            fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

            # Plot res.trend
            axes[0, 0].plot(res.observed)
            axes[0, 0].set_title("Observed")
            axes[0, 0].set_xlabel("Date")
            axes[0, 0].set_ylabel("Value")
            axes[0, 0].grid(True)

            # Plot res.stat
            axes[0, 1].plot(res.trend)
            axes[0, 1].set_title("Trend")
            axes[0, 1].set_xlabel("Date")
            axes[0, 1].set_ylabel("Value")
            axes[0, 1].grid(True)

            # Plot res.prueba
            axes[1, 0].plot(res.seasadj)
            axes[1, 0].set_title("seasadj")
            axes[1, 0].set_xlabel("Date")
            axes[1, 0].set_ylabel("Value")
            axes[1, 0].grid(True)

            # Plot res.prueba2
            axes[1, 1].plot(res.irregular)
            axes[1, 1].set_title("Irregular")
            axes[1, 1].set_xlabel("Date")
            axes[1, 1].set_ylabel("Value")
            axes[1, 1].grid(True)

            # Adjust layout and display the plot
            plt.tight_layout()
            plt.show()
