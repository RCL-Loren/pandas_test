from analysis.analysis import load_ncdhhs_data
from analysis.analysis import aggregate_weekly
from analysis.analysis import dataframe_lowess
from analysis.ftstyle import FtStyle
import matplotlib.pyplot as plt
import seaborn as sns



def get_hospital_metrics(show_plot=False, col_select="Hospitalizations"):
	hospital_metrics_file = "./data/HOSPITAL_METRICS_STATE.csv"
	hospital_metrics_headers = ["Hospitalizations", "ICU", "Suspected", "Confirmed"]

	hospital_metrics_daily_df = load_ncdhhs_data(hospital_metrics_file,
												hospital_metrics_headers,
												show_table=False)

	# Drop all rows with NaN
	hospital_metrics_daily_df = hospital_metrics_daily_df.dropna(axis=0, how='any')

	# Create a sequence of integers to reference as week from start
	hospital_metrics_daily_df['Day'] = range(1,len(hospital_metrics_daily_df) + 1)	

	hospital_metrics_daily_lowess_df = dataframe_lowess(hospital_metrics_daily_df,
												y_col_name=col_select,
												x_col_name='Day',
												frac_in=0.1,
												show_plot=show_plot,
												show_table=False)

	adj_index = hospital_metrics_daily_lowess_df.index
	adj_index.strftime('% B % d, % Y, % r')
	hospital_metrics_daily_lowess_df['DateString'] = adj_index

	return hospital_metrics_daily_lowess_df

def get_hospital_stats(show_plot=False, col_select = 'Inpatient_Beds_Used'):
	hospital_stats_file = "./data/HOSPITAL_BEDS_VENTILATORS.csv"
	hospital_stats_headers = ["Vents_Used", "Vents_Avail","ICU_Beds_Used", 
								"ICU_Beds_Empty_Staffed", "Inpatient_Beds_Used", 
								"Inpatient_Beds_Empty_Staffed"]	

	hospital_stats_daily_df = load_ncdhhs_data(hospital_stats_file,
												hospital_stats_headers,
												show_table=False)

	# Drop all rows with NaN
	hospital_stats_daily_df = hospital_stats_daily_df.dropna(axis=0, how='any')

	# Create a sequence of integers to reference as week from start
	hospital_stats_daily_df['Day'] = range(1,len(hospital_stats_daily_df) + 1)

	# Add in unstaffed - this is probably not quite right - but close	
	hospital_stats_daily_df["ICU_Unstaffed"] = 1039
	hospital_stats_daily_df["Inpatient_Beds_Unstaffed"] = 4295


	hospital_stats_daily_lowess_df = dataframe_lowess(hospital_stats_daily_df,
												y_col_name= col_select,
												x_col_name='Day',
												frac_in=0.3,
												show_plot=show_plot,
												show_table=False)
	adj_index = hospital_stats_daily_lowess_df.index
	adj_index.strftime('% B % d, % Y, % r')
	hospital_stats_daily_lowess_df['DateString'] = adj_index

	return hospital_stats_daily_lowess_df

def plot_hospitalizations():
	hospitalized_df = get_hospital_metrics(show_plot=False, 
											col_select="Hospitalizations")

	style = FtStyle()
	fig, ax = style.set_plt_rc(plt).subplots()
	plt.xticks(rotation=70)
	ax.scatter(hospitalized_df['DateString'], hospitalized_df['Hospitalizations'], marker="+", color="LightGrey", label="Hospitalizations")
	ax.plot(hospitalized_df['DateString'], hospitalized_df['LOWESS'],"--",color="#7D062E", label="Hospitalizations (LOWESS)")
	

	left = -0.06
	ax.text(0.0, 1.07, 'NC DHHS Daily Hospitalizations',
				ha='left', va='center', transform=ax.transAxes, color="k")

	ax.legend(loc='lower right');
	ax.xaxis.set_label_coords(0.5, -0.2)
	ax.yaxis.set_label_coords(-0.15, 0.5)
	ax.set_ylabel("Hospitalizations")

	plt.savefig("Hospitalizations.png", dpi=300)

	plt.show()

def plot_bed_context():
	hospitalized_df = get_hospital_metrics(show_plot=False, 
											col_select="Hospitalizations")
	beds_in_use = get_hospital_stats(show_plot=False, 
											col_select='Inpatient_Beds_Used')
	beds_empty = get_hospital_stats(show_plot=False,
											col_select='Inpatient_Beds_Empty_Staffed')
	beds_unstaffed = get_hospital_stats(show_plot=False,
											col_select='Inpatient_Beds_Unstaffed')

	style = FtStyle()
	#pal = sns.color_palette("deep")
	pal = ["#716962", "#A2BC5D", "#E95D8C", "#2ecc71"]
	fig, ax = style.set_plt_rc(plt).subplots()
	plt.xticks(rotation=70)

	ax.plot(hospitalized_df['DateString'], hospitalized_df['LOWESS'],".--",color="#7D062E", label="COVID19 Inpatients")
	ax.stackplot(beds_in_use['DateString'], 
					beds_in_use['LOWESS'], 
					beds_empty['LOWESS'],
					beds_unstaffed['LOWESS'],
					labels=['Beds In Use','Empty Staffed Beds','Empty Unstaffed Beds'],
					colors=pal,
					alpha=0.4)	

	left = -0.06
	ax.text(0.0, 1.07, 'NC DHHS COVID19 Hospitalizations vs. Bed Census',
				ha='left', va='center', transform=ax.transAxes, color="k")

	ax.legend(loc='upper left');
	ax.xaxis.set_label_coords(0.5, -0.2)
	ax.yaxis.set_label_coords(-0.15, 0.5)
	ax.set_ylabel("Beds")

	plt.savefig("InpatientBeds.png", dpi=300)
	plt.show()

def plot_ICU_context():
	ICU_df = get_hospital_metrics(show_plot=False, 
											col_select="ICU")
	ICU_in_use = get_hospital_stats(show_plot=False, 
											col_select='ICU_Beds_Used')
	ICU_empty = get_hospital_stats(show_plot=False,
											col_select='ICU_Beds_Empty_Staffed')
	ICU_unstaffed = get_hospital_stats(show_plot=False,
											col_select='ICU_Unstaffed')

	style = FtStyle()
	#pal = sns.color_palette("deep")
	pal = ["#716962", "#A2BC5D", "#E95D8C", "#2ecc71"]
	fig, ax = style.set_plt_rc(plt).subplots()
	plt.xticks(rotation=70)

	ax.plot(ICU_df['DateString'], ICU_df['LOWESS'],".--",color="#7D062E", label="COVID19 ICU Patients")
	ax.stackplot(ICU_in_use['DateString'], 
					ICU_in_use['LOWESS'], 
					ICU_empty['LOWESS'],
					ICU_unstaffed['LOWESS'],
					labels=['ICU Beds In Use','ICU Empty Staffed Beds','ICU Empty Unstaffed Beds'],
					colors=pal,
					alpha=0.4)	

	left = -0.06
	ax.text(0.0, 1.07, 'NC DHHS COVID19 ICU vs. ICU Bed Census',
				ha='left', va='center', transform=ax.transAxes, color="k")

	ax.legend(loc='upper left');
	ax.xaxis.set_label_coords(0.5, -0.2)
	ax.yaxis.set_label_coords(-0.15, 0.5)
	ax.set_ylabel("Beds")

	plt.savefig("ICUBeds.png", dpi=300)
	plt.show()


if __name__ == "__main__":
	# execute only if run as a script
	#plot_hospitalizations()
	#plot_bed_context()
	plot_ICU_context()


