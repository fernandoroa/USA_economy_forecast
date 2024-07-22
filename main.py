from src.dataframe_integration import integrate_dataframes
from src.process_excel import read_excel
from src.process_debt_csv import read_csv_index
from src.model import forecast_time_series
from src.plot_model import plot_array

def main():
    gdp_data = read_excel('data/statistic_id188105_us-annual-gdp-1990-2023.xlsx', 
                          date_type='year', 
                          multiplier=1_000_000_000, 
                          value_name = 'GDP')

    revenue_data = read_excel('data/statistic_id200405_us-government---total-receipts-2000-2029.xlsx', 
                              date_type='year', 
                              multiplier=1_000_000_000_000, 
                              value_name = 'revenue')

    expenditure_data = read_excel('data/statistic_id215503_us-government-annual-expenditure-2009-2024-by-quarter.xlsx', 
                  date_type= 'quarter', 
                  multiplier=1_000_000_000_000, 
                  value_name = 'expenditure')

    debt_data = read_csv_index("data/HstDebt_17900101_20230930.csv", "Record Date")

    all_data_df = integrate_dataframes(revenue_data, expenditure_data, debt_data, gdp_data)
    
    fiscal_gap_forecast, fiscal_gap_conf_int = forecast_time_series(all_data_df, "Fiscal_Gap", n_periods = 10)
    
    gdp_forecast, conf_int_gdp = forecast_time_series(all_data_df, "GDP", n_periods = 10)
    
    debt_forecast, conf_int_debt = forecast_time_series(all_data_df, "Debt", n_periods = 10)
    
    debt_to_gdp_ratio = debt_forecast / gdp_forecast

    debt_to_gdp_lower = conf_int_debt[:, 0] / conf_int_gdp[:, 1]
    debt_to_gdp_upper = conf_int_debt[:, 1] / conf_int_gdp[:, 0]

    unsustainable_debt_threshold = 1.0
     
    forecast_years = list(range(all_data_df['Year'].iloc[-1] + 1, all_data_df['Year'].iloc[-1] + 11))

    plot_array(all_data_df, forecast_years, 
               fiscal_gap_forecast, fiscal_gap_conf_int, 
               debt_to_gdp_ratio, debt_to_gdp_lower, debt_to_gdp_upper, 
               unsustainable_debt_threshold)

if __name__ == "__main__":
    main()
