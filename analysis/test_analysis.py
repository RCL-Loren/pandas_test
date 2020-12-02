from pandas_test.analysis.analysis import load_testing_data

def test_load_testing_data():
	assert load_testing_data("./test_data/test_data_dailytest.csv") == "./test_data/test_data_dailytest.csv"
