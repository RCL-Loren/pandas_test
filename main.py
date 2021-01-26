from analysis.analysis import load_ncdhhs_data
from analysis.analysis import aggregate_weekly
from analysis.analysis import dataframe_ordinary_least_squares
from analysis.analysis import dataframe_lowess
import matplotlib.pyplot as plt
import pandas as pd

def get_test_vol(show_plot=True):
	test_metrics_file = "./data/TABLE_DAILY_TESTING_METRICS.csv"
	test_metrics_headers = ["Total", "PCR_Tests", "Antigen_Tests", "Pos_Percent"]

	test_metrics_daily_df = load_ncdhhs_data(test_metrics_file,
												test_metrics_headers,
												show_table=False)

	test_metrics_weekly_df = aggregate_weekly(test_metrics_daily_df, 'Total',
												show_table=True)

	test_metrics_lowess_df = dataframe_lowess(test_metrics_weekly_df,
												y_col_name='Total',
												x_col_name='Week',
												frac_in=0.5,
												show_plot=show_plot,
												show_table=False)

	test_metrics_lowess_df.iat[0,2] = test_metrics_lowess_df.iat[0,0]
	print(test_metrics_lowess_df)

	return test_metrics_lowess_df

def get_cases(show_plot=True):
	cases_deaths_file = "./data/TABLE_DAILY_CASE&DEATHS_METRICS.csv"
	cases_deaths_headers = ["Cases", "PCR", "Antigen", "Deaths"]
	cases_deaths_daily_df = load_ncdhhs_data(cases_deaths_file,
												cases_deaths_headers,
												show_table=False)

	cases_weekly_df = aggregate_weekly(cases_deaths_daily_df, 'Cases',
												show_table=False)

	cases_lowess_df = dataframe_lowess(cases_weekly_df,
												y_col_name='Cases',
												x_col_name='Week',
												frac_in= 0.2,
												it_in=0,
												show_plot=show_plot,
												show_table=False)

	cases_lowess_df=cases_lowess_df.drop(cases_lowess_df.index[[0,1]])

	cases_lowess_df['Week'] = range(1,len(cases_lowess_df) + 1)

	print(cases_lowess_df)
	return cases_lowess_df

def case_vol_adj():
	test_vol_smoothed = get_test_vol(show_plot=True)

	raw_cases_smoothed = get_cases(show_plot=True)

	baseline_volume = test_vol_smoothed.iloc[2,0]

	raw_cases_smoothed['Adjusted'] =  raw_cases_smoothed['Cases'] * (baseline_volume / test_vol_smoothed['Total'])

	adj_cases_smoothed = dataframe_lowess(raw_cases_smoothed,
												y_col_name='Adjusted',
												x_col_name='Week',
												frac_in= 0.2,
												it_in=0,
												show_plot=True,
												show_table=False)

	adj_index = adj_cases_smoothed.index
	adj_index.strftime('% B % d, % Y, % r')
	adj_cases_smoothed['DateString'] = adj_index
	print(adj_cases_smoothed)

	fig, ax = plt.subplots()
	plt.xticks(rotation=70)
	#ax.scatter(adj_cases_smoothed['DateString'], adj_cases_smoothed['Adjusted'], color="#778899", label="Test Volume")
	ax.plot(adj_cases_smoothed['DateString'], adj_cases_smoothed['Cases'],".--",color="#4682B4", label="Test Volume")
	ax.plot(adj_cases_smoothed['DateString'], adj_cases_smoothed['LOWESS'],".--",color="blue", label="Test Volume")
	plt.show()

def death_analysis():
	cases_deaths_file = "./data/TABLE_DAILY_CASE&DEATHS_METRICS.csv"
	cases_deaths_headers = ["Cases", "PCR", "Antigen", "Deaths"]
	cases_deaths_daily_df = load_ncdhhs_data(cases_deaths_file,
												cases_deaths_headers,
												show_table=False)

	deaths_weekly_df = aggregate_weekly(cases_deaths_daily_df, 'Deaths',
												show_table=False)

	cases_deaths_daily_df['Week'] = range(1,len(cases_deaths_daily_df) + 1)
	deaths_lowess_df = dataframe_lowess(cases_deaths_daily_df,
												y_col_name='Deaths',
												x_col_name='Week',
												frac_in= 0.1,
												it_in=0,
												show_plot=True,
												show_table=True)

	adj_index = deaths_lowess_df.index
	adj_index.strftime('% B % d, % Y, % r')
	deaths_lowess_df['DateString'] = adj_index

	fig, ax = plt.subplots()
	plt.xticks(rotation=70)
	ax.bar(deaths_lowess_df['DateString'], deaths_lowess_df['Deaths'], color="#778899", label="Test Volume")
	ax.plot(deaths_lowess_df['DateString'], deaths_lowess_df['LOWESS'],".--",color="blue", label="Test Volume")
	plt.show()

def main():
	print(__name__)

	#case_vol_adj()

	death_analysis()




if __name__ == "__main__":
    # execute only if run as a script
    main()