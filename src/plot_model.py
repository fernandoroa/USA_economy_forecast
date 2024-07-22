import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator

def trillions(x, pos):
    """The two args are the value and tick position"""
    if x == 0:
        return '0'
    return '%1.0f' % (x * 1e-12)

def plot_array(df, forecast_years, fiscal_gap_forecast, fiscal_gap_conf_int, debt_to_gdp_ratio, debt_to_gdp_lower, debt_to_gdp_upper, unsustainable_debt_threshold):
    """
    Plots historical and forecasted fiscal gap and debt-to-GDP ratio.

    Parameters:
    - df (pd.DataFrame): DataFrame containing historical data with 'Year', 'Fiscal_Gap', 'Debt', and 'GDP' columns.
    - forecast_years (array-like): Array-like structure containing the forecasted years.
    - fiscal_gap_forecast (array-like): Forecasted fiscal gap values corresponding to forecast_years.
    - fiscal_gap_conf_int (np.ndarray): 2D array containing the lower and upper bounds of the forecasted fiscal gap confidence intervals.
    - debt_to_gdp_ratio (array-like): Forecasted debt-to-GDP ratio values corresponding to forecast_years.
    - debt_to_gdp_lower (array-like): Lower bounds of the forecasted debt-to-GDP ratio.
    - debt_to_gdp_upper (array-like): Upper bounds of the forecasted debt-to-GDP ratio.
    - unsustainable_debt_threshold (float): The threshold value for unsustainable debt-to-GDP ratio.

    Raises:
    - ValueError: If required columns are missing from the dataframe.

    Example:
    >>> plot_array(df, forecast_years, fiscal_gap_forecast, fiscal_gap_conf_int, debt_to_gdp_ratio, debt_to_gdp_lower, debt_to_gdp_upper, 0.9)
    """

    required_columns = ['Year', 'Fiscal_Gap', 'Debt', 'GDP']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"DataFrame is missing required columns: {missing_columns}")

    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(df['Year'], df['Fiscal_Gap'], label='Fiscal Gap (Historical)', color='blue')
    plt.plot(forecast_years, fiscal_gap_forecast, label='Fiscal Gap (Forecast)', linestyle='--', color='orange')
    plt.fill_between(forecast_years, fiscal_gap_conf_int[:, 0], fiscal_gap_conf_int[:, 1], color='orange', alpha=0.3)
    plt.title('Fiscal Gap Forecast')
    plt.xlabel('Year')
    plt.ylabel('Fiscal Gap (Trillions)')
    plt.legend()
    
    formatter = FuncFormatter(trillions)
    ax1 = plt.gca()
    ax1.yaxis.set_major_formatter(formatter)
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))  # Automatically place a reasonable number of ticks


    plt.subplot(2, 1, 2)
    plt.plot(df['Year'], df['Debt'] / df['GDP'], label='Debt to GDP Ratio (Historical)', color='blue')
    plt.plot(forecast_years, debt_to_gdp_ratio, label='Debt to GDP Ratio (Forecast)', linestyle='--', color='orange')
    plt.fill_between(forecast_years, debt_to_gdp_lower, debt_to_gdp_upper, color='orange', alpha=0.3)
    plt.axhline(y=unsustainable_debt_threshold, color='red', linestyle='--', label='Unsustainable Debt Threshold')
    plt.title('Debt to GDP Ratio Forecast')
    plt.xlabel('Year')
    plt.ylabel('Debt to GDP Ratio')
    plt.legend()

    plt.tight_layout()
   
    plt.show()
