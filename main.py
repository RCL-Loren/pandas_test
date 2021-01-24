from analysis.analysis import load_ncdhhs_data
from analysis.analysis import aggregate_weekly
from analysis.analysis import dataframe_ordinary_least_squares
from analysis.analysis import dataframe_lowess
import matplotlib.pyplot as plt
import pandas as pd

def main():
	print(__name__)

	test_metrics_file = "./data/TABLE_DAILY_TESTING_METRICS.csv"
	test_metrics_headers = ["Total", "PCR_Tests", "Antigen_Tests", "Pos_Percent"]

	test_metrics_daily_df = load_ncdhhs_data(test_metrics_file, test_metrics_headers)
	test_metrics_weekly_df = aggregate_weekly(test_metrics_daily_df, 'Total')
	test_metrics_lowess_df = dataframe_lowess(test_metrics_weekly_df,
												y_col_name='Total',
												x_col_name='Week',
												showplot=False)

	cases_deaths_file = "./data/TABLE_DAILY_CASE&DEATHS_METRICS.csv"
	cases_deaths_headers = ["Cases", "PCR", "Antigen", "Deaths"]
	cases_deaths_daily_df = load_ncdhhs_data(cases_deaths_file, cases_deaths_headers)
	cases_deaths_weekly_df = aggregate_weekly(cases_deaths_daily_df, 'Cases')
	cases_deaths_lowess_df = dataframe_lowess(cases_deaths_weekly_df,
												y_col_name='Cases',
												x_col_name='Week',
												showplot=False)

	cases_deaths_lowess_df.info()

	#calculate test adjusted cases
	baseline_volume = test_metrics_lowess_df.iloc[3,2]

	cases_deaths_lowess_df['Adjusted Cases'] = (baseline_volume/test_metrics_lowess_df['Total'])*cases_deaths_lowess_df['Cases']

	cases_deaths_adj_lowess_df = dataframe_lowess(cases_deaths_lowess_df,
												y_col_name='Adjusted Cases',
												x_col_name='Week',
												showplot=True)


if __name__ == "__main__":
    # execute only if run as a script
    main()