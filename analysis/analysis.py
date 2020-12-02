import pandas as pd

def load_testing_data(data_filename , headings):
	df = pd.read_csv(data_filename,
	                             encoding = "utf16",
	                             sep='\t',
	                             thousands=',',
	                             index_col='Date',
	                             parse_dates=True,
	                             ).sort_index(ascending=True, axis=0)
	df.columns = headings

	return df