"""
Load ADV measurements and calculate TKE with plot options
Originally coded in Matlab at Nepf LAb (MIT)
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
from rmspike import  rmspike


def load_input_defs(file_name=SCRIPT_DIR+"input.xlsx"):
    """loads provided input file name as pandas dataframe

    Args:
        file_name (str): name of input file (default is input.xlsx)

    Returns:
        (dict): user input of input.xlsx (or costum file, if provided)
    """
    input_xlsx_df = pd.read_excel(file_name, header=0, index_col=0)
    return {
        "folder name": input_xlsx_df["VALUE"]["Input folder name (HOME/data/)"],
        "profile": PROFILE_KEYS[input_xlsx_df["VALUE"]["ADV direction"]],
        "bulk velocity": input_xlsx_df["VALUE"]["Flow velocity"],
        "bulk depth": input_xlsx_df["VALUE"]["Water depth"],
        "freq": input_xlsx_df["VALUE"]["ADV freq"],
        "characteristic wood length": input_xlsx_df["VALUE"]["Characteristic log length dimension"],
        "despiking method": input_xlsx_df["VALUE"]["Spike detection method"],
        "lambda a": input_xlsx_df["VALUE"]["Despike lambda a"],
        "despike k": input_xlsx_df["VALUE"]["Despike k"],
    }


def read_vna(vna_file_name):
    """Read vna file name as pandas dataframe.

    Args:
        vna_file_name (str): name of a vna file, such as __8_16.5_6_T3.vna

    Returns:
        pd.DataFrame
    """
    col_names = ["skip1", "time (s)", "sample no.", "skip2",
                 "u (m/s)", "v (m/s)", "w1 (m/s)", "w2 (m/s)",
                 "ampl. x (dB)", "ampl. y (dB)", "ampl. z1 (dB)", "ampl. z2 (dB)",
                 "SNR x", "SNR y", "SNR z1", "SNR z2",
                 "corr x", "corr y", "corr z1", "corr z2"]
    return pd.read_csv(vna_file_name,
                       sep="\s+",
                       header=None,
                       names=col_names,
                       usecols=lambda x: x not in ["skip1", "skip2"])


def vna_file_name2coordinates(vna_file_name):
    """Take vna file name and extract x, y, and z coordinates in meters.
    Non-convertible numbers are translated into np.nan with warning.

    Args:
        vna_file_name (str): name of a vna file, such as __8_16.5_6_T3.vna

    Returns:
        list [x, y, z] coordinates
    """
    # replace __ with minus, remove file ending and split coordinates with _
    xyz_list = vna_file_name.replace("__", "-").strip(".vna").split("_")[0:3]
    for i, coord in enumerate(xyz_list):
        try:
            xyz_list[i] = float(coord) / 100.
        except ValueError:
            print("WARNING: Could not convert {0} to coordinate in file {1}".format(
                str(coord), vna_file_name))
            xyz_list[i] = np.nan
    return xyz_list


def get_data_info(folder_name="test-example"):
    """get names of input file names and prepare output matrix according to
    number of files

    Args:
        folder_name (str): name of the test (experiment) to analyze (default is test-example)
        input_file_name (str): name of input file (default is input.xlsx)

    Returns:
        pd.DataFrame with row names corresponding to file names ending on .vna,
        and columns X, Y, Z in meters
    """
    # get vna file names
    vna_file_names = [f for f in os.listdir(
        SCRIPT_DIR + "data/" + folder_name) if f.endswith(".vna")]

    # construct dataframe with x-y-z positions of the probe
    probe_position_df = pd.DataFrame(
        data=[vna_file_name2coordinates(vna_fn) for vna_fn in vna_file_names],
        index=[s.strip(".vna") for s in vna_file_names],
        columns=["x (m)", "y (m)", "z (m)"]
    )

    return {"vna files": vna_file_names, "probe positions": probe_position_df}


def build_stats_summary(vna_stats, experiment_info, profile_type, bulk_velocity, log_length):
    """Re-organize the stats dataset and assign probe coordinates

    Args:
        vna_stats (dict): the result of the flowstat.flowstat function
        experiment_info (dict): the result of the get_data_info function for retrieving probe positions
        profile_type (str): profile orientation as a function of sensor position; the default is lp corresponding to DOWN (ignores w2 measurements)
        bulk_velocity (float): bulk streamwise flow velocity in m/s (from input.xlsx)
        log_length (float): characteristic log length (either diameter or length) in m (from input.xlsx)

    Returns:
        Organized overview pandas.DataFrame with measurement stats, ready for dumping to workbook
    """

    data = [
        experiment_info["probe positions"]["x (m)"],
        experiment_info["probe positions"]["y (m)"],
        experiment_info["probe positions"]["z (m)"],
        vna_stats["u STAT (m/s)"]["average"], vna_stats["u STAT (m/s)"]["stderr"], vna_stats["u STAT (m/s)"]["std"],
        vna_stats["v STAT (m/s)"]["average"], vna_stats["v STAT (m/s)"]["stderr"], vna_stats["v STAT (m/s)"]["std"],
        vna_stats["w STAT (m/s)"]["average"], vna_stats["w STAT (m/s)"]["stderr"], vna_stats["w STAT (m/s)"]["std"],
        vna_stats["TKE (m^2/s^2)"],
        vna_stats["tau_v STAT (m^2/s^2)"]["average"], vna_stats["tau_v STAT (m^2/s^2)"]["stderr"],
        vna_stats["tau_v STAT (m^2/s^2)"]["std"],
        vna_stats["tau_w STAT (m^2/s^2)"]["average"], vna_stats["tau_w STAT (m^2/s^2)"]["stderr"],
        vna_stats["tau_w STAT (m^2/s^2)"]["std"],
    ]

    if not(profile_type == "lp"):
        data.extend(
            [vna_stats["w2 STAT (m/s)"]["average"], vna_stats["w2 STAT (m/s)"]["stderr"],
             vna_stats["w2 STAT (m/s)"]["std"], vna_stats["TKE2 (m^2/s^2)"],
             vna_stats["tau_w2 STAT (m^2/s^2)"]["average"], vna_stats["tau_w2 STAT (m^2/s^2)"]["stderr"],
             vna_stats["tau_w2 STAT (m^2/s^2)"]["std"],
             ]
        )

    column_headers = ["x (m)", "y (m)", "z (m)"]
    for par, stats in vna_stats:
        for stat_type in stats.keys():
            column_headers.append(par.replace("STAT", stat_type))

    # append u_norm, x_norm, TKE_norm and TKE-ad
    data.extend([
        vna_stats["u STAT (m/s)"]["average"] / bulk_velocity,
        experiment_info["probe positions"]["x (m)"] / log_length,
        vna_stats["TKE (m^2/s^2)"] / (bulk_velocity ** 2),
        0.5 * (vna_stats["u STAT (m/s)"]["std"] ** 2 + vna_stats["v STAT (m/s)"]["std"] ** 2) / (bulk_velocity ** 2),
        ]
    )
    column_headers.extend(["u norm. (-)", "x norm. (-)", "TKE norm. (-)", "TKE 2d norm. (-)"])

    return pd.DataFrame(
        data=data,
        columns=column_headers,
        index=experiment_info["vna files"]
    )


def process_vna_files(input_file_name):
    """Main function controlling vna file processing.
    Writes full despiked data series and stats series to xlsx workbooks.

    Args:
        input_file_name (str): name of input file with experiment metrics (default is input.xlsx in script folder)
    """
    experiment_setup = load_input_defs(file_name=input_file_name)
    experiment_meta = get_data_info(experiment_setup["folder name"])
    target_folder = SCRIPT_DIR + "data/" + experiment_setup["folder name"]
    for vna_fn in experiment_meta["vna files"]:
        print(" * loading %s ..." % vna_fn)
        vna_df = read_vna(target_folder + "/" + vna_fn)
        print(" * writing raw data to %s " % str(target_folder + "/%s-raw.xlsx" % vna_fn.split(".vna")[0]))
        vna_df.to_excel(str(target_folder + "/%s-raw.xlsx" % vna_fn.split(".vna")[0]))
        print(" * calculating file stats ...")
        vna_time_series, vna_stats = flowstat(time=vna_df["time (s)"].to_numpy(),
                                              u=vna_df["u (m/s)"].to_numpy(),
                                              v=vna_df["v (m/s)"].to_numpy(),
                                              w1=vna_df["w1 (m/s)"].to_numpy(),
                                              w2=vna_df["w2 (m/s)"].to_numpy(),
                                              profile_type=experiment_setup["profile"]
                                              )
        print(" * writing data stats with spikes to %s " % str(
            target_folder + "/%s-stats-with-spikes.xlsx" % vna_fn.split(".vna")[0]))
        stats4write_df = build_stats_summary(
            vna_stats=vna_stats,
            experiment_info=experiment_meta,
            bulk_velocity=experiment_setup["bulk velocity"],
            profile_type=experiment_setup["profile"],
            log_length=experiment_setup["characteristic wood length"]
        )
        stats4write_df.to_excel(target_folder + "/%s-stats-with-spikes.xlsx" % vna_fn.split(".vna")[0])

        print(" * launching spike removal ...")
        spike_df, vna_df = rmspike(
            vna_df,
            u_stats=vna_stats["u STAT (m/s)"],
            v_stats=vna_stats["v STAT (m/s)"],
            w_stats=vna_stats["w STAT (m/s)"],
            w2_stats=vna_stats["w2 STAT (m/s)"],
            freq=experiment_setup["freq"],
            lambda_a=experiment_setup["Despike lambda a"],
            k=experiment_setup["Despike k"],
            method=experiment_setup["despiking method"],
            profile_type=experiment_setup["profile"]
        )
        print(" * writing spike counts to %s " % str(target_folder + "/%s-spikes.xlsx" % vna_fn.split(".vna")[0]))
        spike_df.to_excel(target_folder + "/%s-spikes.xlsx" % vna_fn.split(".vna")[0])
        print(" * writing de-spiked data to %s " % str(target_folder + "/%s-despiked.xlsx" % vna_fn.split(".vna")[0]))
        spike_df.to_excel(target_folder + "/%s-spikes.xlsx" % vna_fn.split(".vna")[0])

        print(" * re-calculating stats with despiked data ...")
        vna_time_series, vna_stats_despiked = flowstat(time=vna_df["time (s)"].to_numpy(),
                                                       u=vna_df["u (m/s)"].to_numpy(),
                                                       v=vna_df["v (m/s)"].to_numpy(),
                                                       w1=vna_df["w1 (m/s)"].to_numpy(),
                                                       w2=vna_df["w2 (m/s)"].to_numpy(),
                                                       profile_type=experiment_setup["profile"]
                                                       )
        print(" * writing despiked data stats to %s " % str(target_folder + "/%s-stats-despiked.xlsx" % vna_fn.split(".vna")[0]))
        stats4write_df = build_stats_summary(
            vna_stats=vna_stats_despiked,
            experiment_info=experiment_meta,
            bulk_velocity=experiment_setup["bulk velocity"],
            profile_type=experiment_setup["profile"],
            log_length=experiment_setup["characteristic wood length"]
        )
        stats4write_df.to_excel(target_folder + "/%s-stats-despiked.xlsx" % vna_fn.split(".vna")[0])

        print("-- DONE -- ALL TASKS FINISHED --")


if __name__ == '__main__':
    print("LAUNCHING TKE PROFILE ANALYST ...")
    print("Note: vna file name must be xx_yy_zz_tt.vna alike (tt=test number).")
    if len(sys.argv) > 1: # make sure input is provided
        # if true: call with user-specific input file.xlsx
        process_vna_files(input_file_name=str(sys.argv[1]))
    else:
        process_vna_files(input_file_name=SCRIPT_DIR + "input.xlsx")
