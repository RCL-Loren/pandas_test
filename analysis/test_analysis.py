from pandas_test.analysis.analysis import load_ncdhhs_data
from pandas_test.analysis.analysis import aggregate_weekly
import pandas as pd

in_file1 = "./analysis/test_data/TABLE_DAILY_TESTING_METRICS.csv"
headers1 = ["Total", "PCR_Tests", "Antigen_Tests", "Pos_Percent"]

in_file2 = "./analysis/test_data//TABLE_DAILY_CASE&DEATHS_METRICS.csv"
headers2 = ["Cases", "PCR", "Antigen", "Deaths"]

def test_load_testing_data_shape_testing():
	df = load_ncdhhs_data(in_file1,headers1)
	assert df.shape == (326,4)

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

def test_aggregate_weekly():
	df = load_ncdhhs_data(in_file1, headers1)
	df1 = aggregate_weekly(df, 'Total')
	diff = df1.index[1] - df1.index[0]
	assert diff.days == 7