from pandas_test.analysis.analysis import load_ncdhhs_data
import pandas as pd

in_file1 = "~/src/pandas_test/analysis/test_data/TABLE_DAILY_TESTING_METRICS.csv"
headers1 = ["Total", "PCR_Tests", "Antigen_Tests", "Pos_Percent"]

in_file2 = "~/src/pandas_test/analysis/test_data//TABLE_DAILY_CASE&DEATHS_METRICS.csv"
headers2 = ["Cases", "PCR", "Antigen", "Deaths"]

def test_load_testing_data_shape_testing():
	df = load_ncdhhs_data(in_file1,headers1)
	assert df.shape == (275,4)

def test_load_testing_data_columns_testing():
	df = load_ncdhhs_data(in_file1,headers1)
	tmp = list(df.columns)
	assert tmp == headers1

def test_load_testing_data_shape_cases():
	df = load_ncdhhs_data(in_file2,headers2)
	assert df.shape == (326,4)

def test_load_testing_data_columns_cases():
	df = load_ncdhhs_data(in_file2, headers2)
	tmp = list(df.columns)
	assert tmp == headers2
