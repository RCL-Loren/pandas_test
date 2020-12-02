import pandas as pd

def load_ncdhhs_data(data_filename , headings):
	#NC DHHS has data set to download as UTF16 LE BOM
	df = pd.read_csv(data_filename,
	                             encoding = "utf16",
	                             sep='\t',
	                             thousands=',',
	                             index_col='Date',
	                             parse_dates=True,
	                             ).sort_index(ascending=True, axis=0)
	df.columns = headings
	return df

