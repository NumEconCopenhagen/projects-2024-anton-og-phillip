import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from scipy.stats import linregress

def import_and_clean_data(fertility_path, gdp_path, inflation_path):
    """
    Imports and cleans data from CSV files.

    Parameters:
    fertility_path (str): Path to the fertility data CSV file.
    gdp_path (str): Path to the GDP data CSV file.
    inflation_path (str): Path to the inflation data CSV file.

    Returns:
    pd.DataFrame: Cleaned and merged data.
    """
    # Read data from CSV files
    FERT = pd.read_csv(fertility_path, delimiter=';')
    GDP = pd.read_csv(gdp_path, delimiter=';')
    INF = pd.read_csv(inflation_path, delimiter=';')

    FERT.drop(range(0, 17), inplace=True)
    Fertility = FERT['Fertility'].values
    Puncturation = [i.replace(',', '.') for i in Fertility]
    Fertilityrate = list(map(float, Puncturation))
    FERT = FERT.reset_index(drop=True)
    FERT = pd.concat([FERT, pd.DataFrame(Puncturation, columns=['Fertilityrate'])], axis=1)
    FERT = FERT.drop(columns=['Fertility'])

    GDproduct = GDP['Real GDP'].values
    Puncturation = [i.replace(',', '.') for i in GDproduct]
    GrossDP = list(map(float, Puncturation))
    GDP = GDP.reset_index(drop=True)
    GDP = pd.concat([GDP, pd.DataFrame(Puncturation, columns=['GrossDP'])], axis=1)
    GDP = GDP.drop(columns=['Real GDP'])

    Inflation = INF['Inflation'].values
    Puncturation = [i.replace(',', '.') for i in Inflation]
    Inflationrate = list(map(float, Puncturation))
    INF = INF.reset_index(drop=True)
    INF = pd.concat([INF, pd.DataFrame(Puncturation, columns=['Inflationrate'])], axis=1)
    INF = INF.drop(columns=['Inflation'])

    # Merge datasets
    Alldata = pd.merge(FERT, GDP, on='Year', how='outer')
    Alldata = pd.merge(Alldata, INF, on='Year', how='outer')
    
    # Convert columns to numeric
    Alldata['Year'] = pd.to_numeric(Alldata['Year'], errors='coerce')
    Alldata['GrossDP'] = pd.to_numeric(Alldata['GrossDP'], errors='coerce')
    Alldata['Inflationrate'] = pd.to_numeric(Alldata['Inflationrate'], errors='coerce')
    Alldata['Fertilityrate'] = pd.to_numeric(Alldata['Fertilityrate'], errors='coerce')

    # Drop rows with NaN values
    Alldata.dropna(inplace=True)

    # Sort the DataFrame by the 'Year' column
    Alldata.sort_values(by='Year', inplace=True)

    return Alldata

def create_plots(Alldata):
    """
    Creates and displays plots for the dataset.

    Parameters:
    Alldata (pd.DataFrame): The dataset.
    """
    # Plot GrossDP
    plt.figure(figsize=(10, 4))
    plt.plot(Alldata['Year'], Alldata['GrossDP'], marker='o', color='blue')
    plt.ylabel('Real GDP (Mia. kr.)')
    plt.title('Real GDP Over Time For Denmark')
    plt.xticks(Alldata['Year'].unique())  # Set x-ticks to unique years
    plt.xlabel('Year')
    plt.grid(True)  # Add gridlines
    plt.tight_layout()
    plt.show()

    # Plot Inflationrate
    plt.figure(figsize=(10, 4))
    plt.plot(Alldata['Year'], Alldata['Inflationrate'], marker='o', color='green')
    plt.ylabel('Inflationrate (Percent)')
    plt.title('Inflation Rate Over Time For Denmark')
    plt.xticks(Alldata['Year'].unique())  # Set x-ticks to unique years
    plt.xlabel('Year')
    plt.grid(True)  # Add gridlines
    plt.tight_layout()
    plt.show()

    # Plot Fertilityrate
    plt.figure(figsize=(10, 4))
    plt.plot(Alldata['Year'], Alldata['Fertilityrate'], marker='o', color='orange')
    plt.ylabel('Fertilityrate (Babies pr. 1000 woman)')
    plt.title('Fertility Rate Over Time For Denmark')
    plt.xticks(Alldata['Year'].unique())  # Set x-ticks to unique years
    plt.xlabel('Year')
    plt.grid(True)  # Add gridlines
    plt.tight_layout()
    plt.show()

def descriptive_statistics(Alldata):
    """
    Prints descriptive statistics for the dataset.

    Parameters:
    Alldata (pd.DataFrame): The dataset.
    """
    avg_gdp = Alldata['GrossDP'].mean()
    max_gdp = Alldata['GrossDP'].max()
    min_gdp = Alldata['GrossDP'].min()
    avg_fertility = Alldata['Fertilityrate'].mean()
    avg_inflation = Alldata['Inflationrate'].mean()

    print("Average GDP:", avg_gdp)
    print("Maximum GDP:", max_gdp)
    print("Minimum GDP:", min_gdp)
    print("Average Fertility Rate:", avg_fertility)
    print("Average Inflation Rate:", avg_inflation)

def correlations(Alldata):
    """
    Computes and prints correlations between key variables in the dataset.

    Parameters:
    Alldata (pd.DataFrame): The dataset.
    """
    correlation_gdp_inflation = Alldata['GrossDP'].corr(Alldata['Inflationrate'])
    correlation_gdp_fertility = Alldata['Fertilityrate'].corr(Alldata['GrossDP'])
    correlation_inflation_fertility = Alldata['Inflationrate'].corr(Alldata['Fertilityrate'])

    print("Correlation between GDP and Inflation Rate:", correlation_gdp_inflation)
    print("Correlation coefficient between Fertilityrate and Real GDP:", correlation_gdp_fertility)
    print("Correlation coefficient between Inflationrate and Fertilityrate:", correlation_inflation_fertility)

def interactive_plot(Alldata):
    """
    Creates an interactive plot to explore relationships in the data.

    Parameters:
    Alldata (pd.DataFrame): The dataset.
    """
    fig = px.scatter(Alldata, x='Inflationrate', y='GrossDP', size='Fertilityrate', hover_name='Year', title='Interactive Plot of Inflation vs Real GDP')
    fig.show()

def visualize_tables(Alldata):
    """
    Visualizes tables in the dataset using plots.

    Parameters:
    Alldata (pd.DataFrame): The dataset.
    """
    # Visualizing GDP Growth
    Alldata['GDP_growth'] = Alldata['GrossDP'].pct_change() * 100  # Calculate percentage change for GDP growth
    gdp_growth_data = Alldata.dropna(subset=['GDP_growth'])  # Drop rows with NaN values in GDP_growth
    filtered_data = Alldata[Alldata['Year']>2003]

    plt.figure(figsize=(14, 6))
    plt.bar(gdp_growth_data['Year'], gdp_growth_data['GDP_growth'], color='blue')
    plt.xlabel('Year')
    plt.ylabel('GDP Growth Rate (%)')
    plt.xticks(filtered_data['Year'].unique())  # Set x-ticks to unique years
    plt.title('Annual GDP Growth Rate')
    plt.show()

    # Visualizing Fertility Rate per Woman
    Alldata['Fertilityrate_per_woman'] = (Alldata['Fertilityrate'] / 1000).round(2)
    plt.figure(figsize=(14, 6))
    plt.plot(Alldata['Year'], Alldata['Fertilityrate_per_woman'], marker='o', color='orange')
    plt.xlabel('Year')
    plt.xticks(Alldata['Year'].unique())  # Set x-ticks to unique years
    plt.ylabel('Fertility Rate (Babies per Woman)')
    plt.title('Fertility Rate per Woman Over Time')
    plt.show()

def trend_analysis(Alldata):
    """
    Performs trend analysis on the dataset and prints the results.

    Parameters:
    Alldata (pd.DataFrame): The dataset.
    """
    slope, intercept, r_value, p_value, std_err = linregress(Alldata['Year'], Alldata['GrossDP'])
    print(f"Trend Analysis for GDP: Slope={slope}, Intercept={intercept}, R-squared={r_value**2}")

    slope, intercept, r_value, p_value, std_err = linregress(Alldata['Year'], Alldata['Inflationrate'])
    print(f"Trend Analysis for Inflation: Slope={slope}, Intercept={intercept}, R-squared={r_value**2}")

    slope, intercept, r_value, p_value, std_err = linregress(Alldata['Year'], Alldata['Fertilityrate'])
    print(f"Trend Analysis for Fertility Rate: Slope={slope}, Intercept={intercept}, R-squared={r_value**2}")