from pmdarima import auto_arima

def forecast_time_series(data, column, n_periods):
    """
    Forecast future values for a given time series using auto ARIMA.
    
    Parameters:
        data (pd.DataFrame): The data containing the time series.
        column (str): The column name of the time series to forecast.
        n_periods (int): Number of periods to forecast.
    
    Returns:
        forecast (np.ndarray): The forecasted values.
        conf_int (np.ndarray): The confidence intervals for the forecasted values.
    """
    model = auto_arima(data[column], seasonal=False, trace=True, error_action='ignore', suppress_warnings=True)
    forecast, conf_int = model.predict(n_periods=n_periods, return_conf_int=True)
    return forecast, conf_int
