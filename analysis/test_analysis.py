from pandas_test.analysis.analysis import load_testing_data
import pandas as pd

in_file = "~/src/pandas_test/analysis/test_data/test_data_dailytests.csv"
headers = ["Total", "PCR_Tests", "Antigen_Tests", "Pos_Percent"]

def test_load_testing_data_shape():
	df = load_testing_data(in_file,headers)
	assert df.shape == (3,4)

def test_load_testing_data_columns():
	df = load_testing_data(in_file,headers)
	tmp = list(df.columns)
	assert tmp == headers