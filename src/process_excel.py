import pandas as pd

def quarter_to_date(quarter_str: str) -> pd.Timestamp:
    """
    Converts a quarter string (e.g., 'Q1 '20') to a pandas Timestamp representing the first day of that quarter.
    
    Parameters:
    quarter_str (str): The quarter string to convert.
    
    Returns:
    pd.Timestamp: A pandas Timestamp representing the first day of the quarter.
    """
    try:
        parts = quarter_str.split(' ')
        quarter = int(parts[0][1])
        year = int(parts[1].replace("'", "20"))
        month = 3 * quarter - 2
        return pd.Timestamp(year=year, month=month, day=1)
    except Exception as e:
        raise ValueError(f"Error converting quarter string '{quarter_str}': {e}")

def year_to_date(year_str: str) -> pd.Timestamp:
    """
    Converts a year string (e.g., "'20") to a pandas Timestamp representing the first day of that year.
    
    Parameters:
    year_str (str): The year string to convert.
    
    Returns:
    pd.Timestamp: A pandas Timestamp representing the first day of the year.
    """
    try:
        year = int(year_str.replace("'", "20"))
        return pd.Timestamp(year=year, month=1, day=1)
    except Exception as e:
        raise ValueError(f"Error converting year string '{year_str}': {e}")

def drop_column_if_exists(data_df: pd.DataFrame, column_name: str):
    """
    Drops a column from a DataFrame if it exists.

    Parameters:
    data_df (pd.DataFrame): The DataFrame from which to drop the column.
    column_name (str): The name of the column to drop.
    """
    try:
        if column_name in data_df.columns:
            data_df.drop(columns=[column_name], inplace=True)
            print(f"Column '{column_name}' dropped successfully.")
        else:
            print(f"Column '{column_name}' does not exist in the DataFrame.")
    except Exception as e:
        raise ValueError(f"Error dropping column '{column_name}': {e}")

def read_excel(file_path: str, 
               sheet_name: str = 'Data', 
               header: int = None, 
               usecols: str = 'B:C', 
               skiprows: int = 5, 
               date_type: str = 'year', 
               multiplier: float = 1_000_000_000,
               value_name: str = 'Value') -> pd.DataFrame:
    """
    Reads economic data from an Excel file and returns a DataFrame with processed values.
    
    Parameters:
    file_path (str): Path to the Excel file to be read.
    sheet_name (str): Name of the sheet to read data from. Default is 'Data'.
    header (int): Row (0-indexed) to use for the column labels. Default is None.
    usecols (str): Columns to read from the sheet. Default is 'B:C'.
    skiprows (int): Number of rows to skip at the beginning. Default is 5.
    date_type (str): Type of date conversion to apply ('year' or 'quarter'). Default is 'year'.
    multiplier (float): Multiplier to apply to the data values. Default is 1 billion (1_000_000_000).
    value_name (str): The name to assign to the value column. Default is 'Value'.
    
    Returns:
    pd.DataFrame: A DataFrame with processed data.
    """
    try:
        temp_df = pd.read_excel(file_path, sheet_name=sheet_name, header=header, usecols=usecols, skiprows=skiprows)
        
        temp_df.dropna(subset=[temp_df.columns[0]], inplace=True)
        
        nrows = temp_df.shape[0]
        
        data_df = pd.read_excel(file_path, sheet_name=sheet_name, header=header, usecols=usecols, skiprows=skiprows, nrows=nrows)
        data_df.columns = ['Date', value_name]
        
        if pd.api.types.is_integer_dtype(data_df['Date']):
            data_df['Date'] = data_df['Date'].apply(lambda x: pd.Timestamp(year=x, month=1, day=1))
            data_df['Year'] = data_df['Date'].dt.year
        else:
            data_df = data_df[~data_df['Date'].str.contains('\*', na=False)]
            if date_type == 'quarter':
                data_df['Date'] = data_df['Date'].apply(quarter_to_date)
                data_df['Year'] = data_df['Date'].dt.year
                data_df = data_df.groupby('Year')[value_name].sum().reset_index()
            elif date_type == 'year':
                data_df['Date'] = data_df['Date'].apply(year_to_date)
                data_df['Year'] = data_df['Date'].dt.year
            else:
                raise ValueError("Invalid date_type. Must be either 'year' or 'quarter'.")
        
        data_df[value_name] *= multiplier
        
        drop_column_if_exists(data_df, "Date")
        
        return data_df
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except ValueError as ve:
        raise ValueError(f"Value error: {ve}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")
