import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.sandbox.regression.predstd import wls_prediction_std

def load_ncdhhs_data(data_filename , headings=[]):
	#NC DHHS has data set to download as UTF16 LE BOM
	df = pd.read_csv(data_filename,
	                             encoding = "utf16",
	                             sep='\t',
	                             thousands=',',
	                             index_col='Date',
	                             parse_dates=True,
	                             ).sort_index(ascending=True, axis=0)

	if len(headings)>0:
		df.columns = headings
	return df


def aggregate_weekly(daily_testing_df, column_name):
	"""Extract a column, resample to weekly, and add an integer reference"""

	# Create new dataframe with only Total Tests and drop rows missing values
	df_test_vol = daily_testing_df[[column_name]]
	df_test_vol = df_test_vol.dropna(axis=0, how='any')

	# Resample and aggregate to weekly
	df_test_vol = df_test_vol.resample('W-MON').sum()

	# Create a sequence of integers to reference as week from start
	df_test_vol['Week'] = range(1,len(df_test_vol) + 1)

	return df_test_vol[:-1]


def dataframe_ordinary_least_squares(dataframe_in, x_col_name, y_col_name):

	x = dataframe_in[x_col_name].to_numpy()
	X =sm.add_constant(x)
	X = np.array(X, dtype=float)
	y = dataframe_in[y_col_name].to_numpy()

	model = sm.OLS(y, X)
	results = model.fit()

	print(results.summary())

	prstd, iv_l, iv_u = wls_prediction_std(results)

	dataframe_in['OLS Values'] = results.fittedvalues
	dataframe_in['Confidence Upper'] = iv_u
	dataframe_in['Confidence Lower'] = iv_l

	fig, ax = plt.subplots()
	ax.scatter(x, y, color="#778899", label="Test Volume")
	ax.plot(x, dataframe_in['OLS Values'],".--",color="#4682B4", label="Ordinary Least Squares Regression")
	ax.plot(x, iv_u,color="#F08080",ls=":")
	ax.plot(x, iv_l,color="#F08080",ls=":")

	plt.show()

def dataframe_lowess(dataframe_in, x_col_name, y_col_name, showplot=False):
	x = dataframe_in[x_col_name].to_numpy()
	y = dataframe_in[y_col_name].to_numpy()

	lowess = sm.nonparametric.lowess

	z = lowess(y, x, return_sorted=False)

	dataframe_in['LOWESS'] = z

	if (showplot == True ):
		fig, ax = plt.subplots()
		ax.scatter(x, y, marker="+",color="#ADD8E6", label="Test Volume")
		ax.plot(x, z,".--",color="#4682B4", label="LOWESS")
		plt.show()

	return dataframe_in



