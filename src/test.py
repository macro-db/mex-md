import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set the maximum number of rows to display
pd.options.display.max_rows = None

# Read the CSV file into a DataFrame
df = pd.read_csv("data/MD_2024_04_02.csv")

df["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%m-%d")
df.set_index("fecha", inplace=True)


# Function to plot NaN values
def plot_nan_locations(df_group, group_name):
    plt.figure(figsize=(10, 5))
    plt.title(f"NaN Locations in Group {group_name}")

    # Plot NaN locations for each column in the group
    for col in df_group.columns:
        plt.plot(df_group.index, df_group[col].isna(), label=col)

    plt.xlabel("Date")
    plt.ylabel("NaN Value")
    plt.yticks([0, 1], ["Data", "NaN"])
    plt.legend()
    plt.tight_layout()
    plt.show()


df_1 = df[
    [
        "SR17536",
        "SR17537",
        "SR17538",
        "SR17539",
        "SR17540",
        "737219",
        "737226",
        "737233",
        "737268",
        "SR16967",
    ]
]
df_2 = df[
    [
        "444884",
        "SL136",
        "SL137",
        "SL138",
        "SL11136",
        "SL11137",
        "SL11138",
        "SL11139",
        "SL2829",
        "SL2830",
        "SL5113",
        "SL5114",
        "SL11298",
        "SL11295",
        "SL11439",
        "SL11453",
        "SL11432",
        "SL11426",
    ]
]
df_4 = df[
    [
        "SR17449",
        "SR17450",
        "SR17451",
        "SR17452",
        "SR17453",
        "SR16882",
        "SR16894",
        "SR16906",
        "SR16918",
        "SR2761",
        "SR2768",
        "SR2775",
        "SR2782",
    ]
]
df_5 = df[
    ["SF311408", "SF311418", "SF311433", "SF311438", "SF29652", "SF235719", "SF235716"]
]
df_6 = df[
    [
        "SF61745",
        "SF282",
        "SF3338",
        "SF3270",
        "SF3367",
        "SF17990",
        "SF18608",
        "SF30057",
        "SF57805",
        "SF57771",
        "SF57923",
        "SF229267",
        "SR28",
    ]
]
df_7 = df[
    [
        "SP12754",
        "SP12755",
        "SP12753",
        "673095",
        "673096",
        "673097",
        "673098",
        "673099",
        "673100",
        "SP1",
        "SP74625",
        "SP74626",
        "SP66540",
        "SP74627",
        "SP74628",
        "SP66542",
        "SP56339",
        "SP74629",
        "SP74630",
        "SP56337",
        "SP56385",
        "SP56386",
        "SP74631",
        "SP56373",
        "SP74640",
    ]
]
df_8 = df[["SF117754", "SF4782", "SF4774", "SF4801"]]


def plot_nan_locations_heatmap(df_group, group_name):
    plt.figure(figsize=(10, 5))
    plt.title(f"NaN Locations in Group {group_name}")

    # Create a DataFrame indicating NaN locations (1 for NaN, 0 for data)
    nan_locations = df_group.isna().astype(int)

    # Plot heatmap
    sns.heatmap(
        nan_locations.T,
        cmap=["green", "red"],
        cbar=False,
        linewidths=0.5,
        linecolor="black",
    )

    plt.xlabel("Date")
    plt.ylabel("Series")
    plt.tight_layout()
    plt.savefig(f"src/group{group_name}")


plot_nan_locations_heatmap(df_1, "1")
plot_nan_locations_heatmap(df_2, "2")
plot_nan_locations_heatmap(df_4, "4")
plot_nan_locations_heatmap(df_5, "5")
plot_nan_locations_heatmap(df_6, "6")
plot_nan_locations_heatmap(df_7, "7")
plot_nan_locations_heatmap(df_8, "8")

"""
# Plot each series
for column in df.columns:
    # Count NaNs in the column
    na_count = df[column].isna().sum()

    
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df[column])
    plt.title(f"{column} (NaNs: {na_count})")
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.grid(True)
    plt.show()
"""
