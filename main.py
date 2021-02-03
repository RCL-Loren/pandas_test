from analysis.analysis import load_ncdhhs_data
from analysis.analysis import aggregate_weekly
from analysis.analysis import dataframe_ordinary_least_squares
from analysis.analysis import dataframe_lowess
from analysis.ftstyle import FtStyle
import matplotlib.pyplot as plt
import pandas as pd

def get_test_vol(show_plot=False):
	test_metrics_file = "./data/TABLE_DAILY_TESTING_METRICS.csv"
	test_metrics_headers = ["Total", "PCR_Tests", "Antigen_Tests", "Pos_Percent"]

	test_metrics_daily_df = load_ncdhhs_data(test_metrics_file,
												test_metrics_headers,
												show_table=False)

	test_metrics_weekly_df = aggregate_weekly(test_metrics_daily_df, 'Total',
												show_table=False)

	test_metrics_lowess_df = dataframe_lowess(test_metrics_weekly_df,
												y_col_name='Total',
												x_col_name='Week',
												frac_in=0.5,
												show_plot=show_plot,
												show_table=False)

	test_metrics_lowess_df.iat[0,2] = test_metrics_lowess_df.iat[0,0]

	adj_index = test_metrics_lowess_df.index
	adj_index.strftime('% B % d, % Y, % r')
	test_metrics_lowess_df['DateString'] = adj_index

	return test_metrics_lowess_df

def get_cases(show_plot=False):
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

	adj_index = cases_lowess_df.index
	adj_index.strftime('% B % d, % Y, % r')
	cases_lowess_df['DateString'] = adj_index

	return cases_lowess_df

def case_vol_adj():
	test_vol_smoothed = get_test_vol(show_plot=False)

	raw_cases_smoothed = get_cases(show_plot=False)

	baseline_volume = test_vol_smoothed.iloc[2,0]

	raw_cases_smoothed['Adjusted'] =  raw_cases_smoothed['Cases'] * (baseline_volume / test_vol_smoothed['Total'])

	adj_cases_smoothed = dataframe_lowess(raw_cases_smoothed,
												y_col_name='Adjusted',
												x_col_name='Week',
												frac_in= 0.2,
												it_in=0,
												show_plot=False,
												show_table=False)

	adj_index = adj_cases_smoothed.index
	adj_index.strftime('% B % d, % Y, % r')
	adj_cases_smoothed['DateString'] = adj_index

	return adj_cases_smoothed

def plot_test_vol(vol_df):
	style = FtStyle()
	fig, ax = style.set_plt_rc(plt).subplots()
	plt.xticks(rotation=70)
	ax.scatter(vol_df['DateString'], vol_df['Total'], marker="+", color="#778899", label="Test Volume")
	ax.plot(vol_df['DateString'], vol_df['LOWESS'],".--",color="#7D062E", label="Test Volume (LOWESS)")
	

	left = -0.06
	ax.text(0.0, 1.07, 'NC DHHS Aggregate Weekly COVID-19 Total Test Volume',
				ha='left', va='center', transform=ax.transAxes, color="k")

	ax.legend(loc='lower right');
	ax.xaxis.set_label_coords(0.5, -0.2)
	ax.yaxis.set_label_coords(-0.15, 0.5)
	ax.set_ylabel("Test Volume")

	plt.savefig("testvolume.png", dpi=300)

	plt.show()

def plot_raw_adj_cases(adj_cases_df, cases_df):
	style = FtStyle()
	fig, ax = style.set_plt_rc(plt).subplots()
	plt.xticks(rotation=70)
	ax.plot(cases_df['DateString'], cases_df['LOWESS'], marker="+", color="#778899", label="Raw Cases")
	ax.plot(adj_cases_df['DateString'], adj_cases_df['LOWESS'],".--",color="#7D062E", label="Volume Adjusted Cases")
	

	left = -0.06
	ax.text(0.0, 1.07, 'NC DHHS Raw vs. Volume Adjusted Case Count',
				ha='left', va='center', transform=ax.transAxes, color="k")

	ax.legend(loc='upper left');
	ax.xaxis.set_label_coords(0.5, -0.2)
	ax.yaxis.set_label_coords(-0.15, 0.5)
	ax.set_ylabel("Cases")

	plt.savefig("cases.png", dpi=300)

	plt.show()

def plot_adj_cases(adj_cases_df):
	style = FtStyle()
	fig, ax = style.set_plt_rc(plt).subplots()
	plt.xticks(rotation=70)
	ax.scatter(adj_cases_df['DateString'], adj_cases_df['Adjusted'], marker="+", color="#778899", label="Volume Adjusted Cases")
	ax.plot(adj_cases_df['DateString'], adj_cases_df['LOWESS'],".--",color="#7D062E", label="Volume Adjusted Cases (LOWESS)")
	

	left = -0.06
	ax.text(0.0, 1.07, 'NC DHHS Volume Adjusted Case Count',
				ha='left', va='center', transform=ax.transAxes, color="k")

	ax.legend(loc='lower right');
	ax.xaxis.set_label_coords(0.5, -0.2)
	ax.yaxis.set_label_coords(-0.15, 0.5)
	ax.set_ylabel("Volume Adjusted Cases")

	ax.annotate('Testing\nRamp',
            xy=(0.24,0.42), xycoords='figure fraction',
            xytext=(0.3, 0.3), textcoords='figure fraction',size=8,
            arrowprops=dict(arrowstyle="->"))

	ax.annotate('Respiratory\nVirus\nSeason',
            xy=(0.825,0.62), xycoords='figure fraction',
            xytext=(0.6, 0.8), textcoords='figure fraction',size=8,
            arrowprops=dict(arrowstyle="->"))

	ax.annotate('Infection\nIntercept',
            xy=(0.27,0.55), xycoords='figure fraction',
            xytext=(0.18, 0.68), textcoords='figure fraction',size=8,
            arrowprops=dict(arrowstyle="->"))

	plt.savefig("adjcases.png", dpi=300)

	plt.show()	

def main():
	print(__name__)

	#plot_test_vol(get_test_vol())

	#plot_raw_adj_cases(case_vol_adj(), get_cases())

	plot_adj_cases(case_vol_adj())








if __name__ == "__main__":
    # execute only if run as a script
    main()