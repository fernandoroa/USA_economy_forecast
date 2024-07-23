## Model Description

The code uses the `auto_arima` function from the `pmdarima` library to fit an ARIMA model to a given time series data. Here's the step-by-step breakdown:

1. **Model Specification**:

   ```python
   model = auto_arima(data[column], seasonal=False, trace=True, error_action='ignore', suppress_warnings=True)
   ```

   - **Data**: `data[column]` is the time series data.
   - **Seasonality**: `seasonal=False` indicates that the model is non-seasonal.
   - **Trace**: `trace=True` enables tracing of the model fitting process.
   - **Error Handling**: `error_action='ignore'` ignores any errors during model fitting.
   - **Warnings**: `suppress_warnings=True` suppresses warnings during model fitting.

2. **Forecasting**:
   ```python
   forecast, conf_int = model.predict(n_periods=n_periods, return_conf_int=True)
   ```
   - **Prediction**: `model.predict(n_periods=n_periods, return_conf_int=True)` generates forecasts for `n_periods` future periods and also provides confidence intervals for the forecasts.

### Mathematical Formulation

To express this process mathematically, consider the following components:

1. **Time Series Data**: $y_t$

   - The observed time series data at time $t$.

2. **ARIMA Model**:

   - ARIMA stands for AutoRegressive Integrated Moving Average.
   - The general form of an ARIMA(p, d, q) model is:

$$
(1 - \sum_{i=1}^p \phi_i B^i)(1 - B)^d y_t = \epsilon_t + \sum_{j=1}^q \theta_j B^j \epsilon_{t-j}
$$

Where:

- $y_t$ is the time series value at time $t$.
- $B$ is the backshift operator, $B y_t = y_{t-1}$.
- $\phi_i$ are the coefficients of the autoregressive (AR) terms.
- $\theta_j$ are the coefficients of the moving average (MA) terms.
- $d$ is the degree of differencing.
- $\epsilon_t$ is white noise.

3. **Model Fitting**:

   - The `auto_arima` function automatically selects the best parameters (p, d, q) based on the given data.
   - It performs the following steps:
     - Differencing the series $(1 - B)^d y_t$ to make it stationary.
     - Identifying the optimal parameters for the AR and MA components through model selection criteria (e.g., AIC, BIC).

4. **Forecasting**:

   - Once the model is fitted, the forecast for the next $n$ periods is given by:

$\hat{y}_{t+h} = \phi_0 + \sum_{i=1}^p \phi_i \hat{y}_{t+h-i} + \sum_{j=1}^q \theta_j \epsilon_{t+h-j}$

- $\hat{y}_{t+h} = \phi_0 + \sum_{i=1}^p \phi_i \hat{y}_{t+h-i} + \sum_{j=1}^q \theta_j \epsilon_{t+h-j}$

$$
\hat{y}_{t+h} = \phi_0 + \sum_{i=1}^p \phi_i \hat{y}_{t+h-i} + \sum_{j=1}^q \theta_j \epsilon_{t+h-j}
$$

`$\hat{y}_{t+h} = \phi_0 + \sum_{i=1}^p \phi_i \hat{y}_{t+h-i} + \sum_{j=1}^q \theta_j \epsilon_{t+h-j}$`

Where:

- $\hat{y}_{t+h}$ is the forecasted value at time $t+h$.
- The confidence interval for the forecast is typically given by:

$\hat{y}_{t+h} \pm z_{\alpha/2} \cdot \sigma_{\hat{y}_{t+h}}$

Where $z_{\alpha/2}$ is the critical value from the normal distribution for the desired confidence level, and $\sigma_{\hat{y}_{t+h}}$ is the standard error of the forecast.

### ARIMA(p, d, q) Model

The ARIMA (AutoRegressive Integrated Moving Average) model is a popular statistical method for analyzing and forecasting time series data. The model is defined by three main parameters: $p$, $d$, and $q$.

#### ARIMA(p, d, q) Components

1. **AutoRegressive (AR) Component - $p$**:

   - **Definition**: The autoregressive component specifies the number of lagged observations (lags) to include in the model.
   - **Notation**: $AR(p)$
   - **Equation**:

$$
y_t = \phi_0 + \sum_{i=1}^p \phi_i y_{t-i} + \epsilon_t
$$

where $y_t$ is the value at time $t$, $\phi_i$ are the coefficients of the lagged values, and $\epsilon_t$ is the error term (white noise).

1. **Integrated (I) Component - $d$**:

   - **Definition**: The integrated component represents the number of differences needed to make the time series stationary.
   - **Notation**: $I(d)$
   - **Differencing**: Differencing is used to remove trends and seasonality from the time series. For example, if $d = 1$, the differenced series is $y_t' = y_t - y_{t-1}$.

2. **Moving Average (MA) Component - $q$**:

   - **Definition**: The moving average component specifies the number of lagged forecast errors to include in the model.
   - **Notation**: $MA(q)$
   - **Equation**:

$$
y_t = \mu + \epsilon_t + \sum_{j=1}^q \theta_j \epsilon_{t-j}
$$

where $\epsilon_t$ is the error term at time $t$, and $\theta_j$ are the coefficients of the lagged error terms.
