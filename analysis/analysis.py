import pandas as pd

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
