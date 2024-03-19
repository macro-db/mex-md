import pandas as pd
import matplotlib.pyplot as plt

# Set the maximum number of rows to display
pd.options.display.max_rows = None

# Read the CSV file into a DataFrame
df = pd.read_csv('data/sliced_2024_03_19.csv')

df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d')
df.set_index('fecha', inplace=True)

# Display the DataFrame information to see if there are any missing values (NaNs)
print("Number of NaNs in each column:")
print(sum(df.isna().sum()<5))

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