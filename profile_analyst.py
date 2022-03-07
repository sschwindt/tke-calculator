"""
Load ADV measurements and calculate TKE with plot options
Originally coded in Matlab at MIT
Re-written in Python by Sebastian Schwindt (2022)
"""

# import relevant standard Python libraries
import sys
import os
# import particular Python libraries
try:
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(e.__class__.__name__ + ": " + e.message)
	raise ImportError("Could not import numpy and pandas. {0}".format(e))
# import global variable names from config
from config import *
from flowstat import flowstat


def load_input_data(file_name=SCRIPT_DIR+"input.xlsx"):
	"""loads provided input file name as pandas dataframe

	Args:
	    file_name (str): name of input file (default is input.xlsx)

	Returns:
		dict(pd.DataFrame(file_name))
	"""
	return pd.read_excel(filename, header=0, index_col=0).to_dict()


def vna_fil_name2coordinates(vna_file_name):
	"""Take vna file name and extract x, y, and z coordinates in meters.
	Non-convertible numbers are translated into np.nan with warning.

	Args:
		vna_file_name (str): name of a vna file, such as __8_16.5_6_T3.vna

	Returns:
		tuple (x, y, z) coordinates
	"""
	# replace __ with minus, remove file ending and split coordinates with _
	xyz_list = vna_file_name.replace("__", "-").strip(".vna").split("_")[0:2]
	for i, coord in enumerate(xyz_list):
		try:
			xyz_list[i] = np.float(coord)
		except ValueError:
			print("WARNING: Could not convert {0} to coordinate in file {1}".format(
			    str(coord), vna_file_name))
			xyz_list[i] = np.nan
	return xyz_list


def get_data_info(folder_name="test-example", input_file_name=SCRIPT_DIR+"input.xlsx"):
	"""get names of input file names and prepare output matrix according to
	number of files

	Args:
		folder_name (str): name of the test (experiment) to analyze (default is test-example)
		input_file_name (str): name of input file (default is input.xlsx)

	Returns:
		pd.DataFrame with row names corresponding to file names ending on .vna,
		and columns X, Xdiff, Xreal, Y, Z
	"""
	# get disctionary of input data -- get pars e.g. with exp_setup["Date"]
	exp_setup = load_input_data(input_file_name)["VALUE"]
	# get vna file names
	vna_file_names = [f for f in os.listdir(
	    SCRIPT_DIR + "data/" + folder_name) if f.endswith(".vna")]

	# initiate stat_sum dataframe for storing de-spiked flow data
	stats_sum_df = pd.DataFrame(
		data=np.ones((vna_file_names.__len__(), 22)) * np.nan,  # UNCLEAR: why 22?
		index=[s.strip(".vna") for s in vna_file_names],
	)

	# construct dataframe with x-y-z positions of the probe
	probe_position_df = pd.DataFrame(
		data=[vna_fil_name2coordinates(vna_fn) for vna_fn in vna_file_names],
		index=[s.strip(".vna") for s in vna_file_names],
	)


# Read the(cell) array raw
data index begins at row  # 14.
# The following file names(cannot be numeric) and 3D position should be predefined in the summary sheet -
# PRIOR TO the post-processing below.
nc = raw(14: m, 1);  # All file names of data files(*.vna)
								# *.dat files can be loaded as well, but column indexes should be changed accordingly.
xx = raw(14: m, 2)
# all x(cm)
yy = raw(14: m, 5)
# all y(cm)
zz = raw(14: m, 6)
# all z(cm)

[m, ~] = size(xx)
# Return the quantity of data files as m.

# Convert the position cells to arrays(column vectors) for further operation.
xx = cell2mat(xx(1: m)); yy = cell2mat(yy(1: m)); zz = cell2mat(zz(1: m))


# 3D position of measurement
for i = 1:
									m
   name = nc{i}; # Assign a file name to the variable "name".
   pos = [xx(i), yy(i), zz(i)]
 # Try-catch-end loop
	 # If the block before catch does not work, the block inside "catch" will be executed.
   try
   	 RawFlow = load(sprintf('#s.vna',name))
   	 # Load the data file (*.vna) into a matrix - Automatic split.
   catch
   	 continue
   	 # Continue with a new loop for(i).
   end

   # Data  # , 3D measurement position
   Stat_sum(i,1) = i; Stat_sum(i,2) = xx(i); Stat_sum(i,3) = yy(i); Stat_sum(i,4) = zz(i)

   # For * .vna files, the first column is all-zero. Remove this column so that the code can be easily applied to *.dat files.
	 if RawFlow(1,1) == 0 & & RawFlow(2,1) == 0
	   RawFlow(: ,1) = [];
   end
   if RawFlow(1,7) == 0 & & RawFlow(2,7) == 0
   	 side = 1
   	 # Side-looking probes do not report w2.
   else
   	 side = 0
   	 # Down-looking probes will report non-zero w2.
   end

   # At this stage, the matrix RawFlow is constituted of the following 19 columns:
   # Columns 1 - 3: Time (s), Sample  # , (disregard);
   # Columns 4 - 7: Velocity records - u, v, w1, w2 (m/s)
   # Columns 8 - 11: Beam amplitude - x, y, z1, z2 (dB)
   # Columns 12 - 15: Signal to Noise Ratio - x, y, z1, z2
   # Columns 16 - 19: Correlation (normalized amplitude of the auto-correlation function) - x, y, z1, z2 ( #).

   Dat = rmspike(RawFlow, 200, 1.0, 3.0)
   # Spike detection and removal
   clear RawFlow
   [TimeS_dsp, Stat_dsp, hdr_final, hdr_stat] = flowstat(Dat)
   # Time series and statistics of the despiked flow data
   clear Dat
   writecell(hdr_final, [name '-final.csv'])
   dlmwrite([name '-final.csv'], TimeS_dsp, '-append')
   Stat_sum(i,5:4+size(Stat_dsp,2)) = Stat_dsp
   # Collect statistics of the despiked flow data
end
clear TimeS_dsp
if isnan(Stat_sum(1, 17))
	Stat_sum(: ,17:22) = [];
end

# Create a summary sheet of the profile after despiking
writecell(hdr_stat, [testnr '.csv'])
dlmwrite([testnr '.csv'], Stat_sum, '-append')

if (__name__ == '__main__'):
	print("Note: vna file name must be xx_yy_zz_tt.vna alike (tt=test number).")
	test_no = 'T2_LP_6'
	profiletype = 'LP' 	 # lateral profile; other types: VP for vertical; LP for longitudinal

    if len(sys.argv) > 1: # make sure input is provided
        # if true: call the dialogue function with the input argument
        dialogue(int(sys.argv[1]))
	# 2. Data Indexing
	# Read the summary sheet to return "raw", a cell array including numeric and text data, excluding following consecutive empty rows.
	# For further process in the load(sprintf()) function, names of the data file cannot be numeric.
	measurements_df = load_input_data()
