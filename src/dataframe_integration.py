import pandas as pd

def integrate_dataframes(revenue_df, yearly_exp, debt_df, gdp_data, fill_forward_debt=True):
    """
    Integrates multiple economic dataframes into a single dataframe.

    This function merges revenue, yearly expenditure, debt, and GDP data into a single dataframe,
    computes the fiscal gap (expenditure minus revenue), and optionally fills forward missing debt values.

    Parameters:
    - revenue_df (pd.DataFrame): DataFrame containing 'Year' and 'revenue' columns.
    - yearly_exp (pd.DataFrame): DataFrame containing 'Year' and 'expenditure' columns.
    - debt_df (pd.DataFrame): DataFrame containing 'Year' and 'Debt' columns.
    - gdp_data (pd.DataFrame): DataFrame containing 'Year' and other relevant GDP columns.
    - fill_forward_debt (bool, optional): If True, fills forward missing debt values. Defaults to True.

    Returns:
    - pd.DataFrame: A merged dataframe with fiscal gap and optionally forward-filled debt values.

    Raises:
    - ValueError: If any required columns are missing from the input dataframes.

    Example:
    >>> result = integrate_dataframes(revenue_df, yearly_exp, debt_df, gdp_data)
    """
    required_columns = {
        'revenue_df': ['Year', 'revenue'],
        'yearly_exp': ['Year', 'expenditure'],
        'debt_df': ['Year', 'Debt'],
        'gdp_data': ['Year']
    }

    for df_name, columns in required_columns.items():
        df = locals()[df_name]
        if not all(col in df.columns for col in columns):
            missing_cols = [col for col in columns if col not in df.columns]
            raise ValueError(f"{df_name} is missing required columns: {missing_cols}")

    economic_data = pd.merge(revenue_df, yearly_exp, on='Year', how='inner')

    economic_data = economic_data.assign(Fiscal_Gap=lambda df: df['expenditure'] - df['revenue'])

    economic_data = economic_data.merge(debt_df[['Debt', 'Year']], on='Year', how='left')
    if fill_forward_debt:
        economic_data = economic_data.assign(Debt=lambda df: df["Debt"].ffill())

    economic_data = economic_data.merge(gdp_data, on='Year', how='left')

    economic_data = economic_data.set_index('Year').reset_index()

    return economic_data
