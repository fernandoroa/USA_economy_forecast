import pandas as pd

def read_csv_index(csv_file_path: str = 'HstDebt_17900101_20230930.csv', date_column: str = 'Record Date') -> pd.DataFrame:
    """
    Reads a CSV file into a pandas DataFrame, sets a specified date column as the index,
    and adds a 'Year' column extracted from the date index.
    
    Parameters:
    csv_file_path (str): Path to the CSV file to be read.
    date_column (str): Name of the column to be used as the date index. Default is 'Record Date'.
    
    Returns:
    pd.DataFrame: A pandas DataFrame with the date column set as the index and an added 'Year' column.
    """
    try:
        debt_data = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at path {csv_file_path} does not exist.")
    except pd.errors.EmptyDataError:
        raise ValueError(f"The file at path {csv_file_path} is empty.")
    except pd.errors.ParserError:
        raise ValueError(f"The file at path {csv_file_path} could not be parsed.")
    
    if date_column not in debt_data.columns:
        raise ValueError(f"The specified date column '{date_column}' is not in the CSV file.")
    
    debt_df = pd.DataFrame(debt_data)
    try:
        debt_df[date_column] = pd.to_datetime(debt_df[date_column])
    except pd.errors.OutOfBoundsDatetime:
        raise ValueError(f"The date values in column '{date_column}' are out of bounds.")
    except pd.errors.ParserError:
        raise ValueError(f"The date values in column '{date_column}' could not be parsed.")
    
    debt_df.set_index(date_column, inplace=True)
    debt_df['Year'] = debt_df.index.year
    
    selected_columns = ['Year', 'Debt Outstanding Amount']
    debt_df = debt_df[selected_columns]
    debt_df.rename(columns={'Debt Outstanding Amount': 'Debt'}, inplace=True)
    
    return debt_df

