import numpy as np
import pandas as pd
col_names = ["skip1", "time (s)", "sample no.", "skip2",
                 "u (m/s)", "v (m/s)", "w1 (m/s)", "w2 (m/s)",
                 "ampl. x (dB)", "ampl. y (dB)", "ampl. z1 (dB)", "ampl. z2 (dB)",
                 "SNR x", "SNR y", "SNR z1", "SNR z2",
                 "corr x", "corr y", "corr z1", "corr z2"]
vna_df =  pd.read_csv("/home/schwindt/github/tke-calculator/data/test-example/__8_16.5_6_T3.vna",
                       sep="\s+",
                       header=None,
                       names=col_names,
                       usecols=lambda x: x not in ["skip1", "skip2"])

u = vna_df["u (m/s)"].to_numpy()
u_stats = {
    "average": np.nanmean(u),
    "std": np.nanstd(u),
    "stderr": np.nanstd(u) / np.sqrt(np.count_nonzero(~np.isnan(u)))
}
k=1.5
u_crl = u_stats["average"] - k * u_stats["std"]
u_cru = u_stats["average"] + k * u_stats["std"]

a_cr = 9.81 * 1.0
a_x = (vna_df["u (m/s)"].shift(-1) - vna_df["u (m/s)"])*200
spikeu = np.nansum(np.where(~((a_x > -a_cr) & (a_x < a_cr)) & ~np.isnan(a_x), 1, 0))
spikeu_vel = np.nansum(np.where(~((vna_df["u (m/s)"] > u_crl) & (vna_df["u (m/s)"] < u_cru)) & ~np.isnan(vna_df["u (m/s)"]), 1, 0))
print(spikeu)
print(spikeu_vel)
print(vna_df["u (m/s)"].head(20))


vna_df["u (m/s)"] = np.where(
			~((vna_df["u (m/s)"] > u_crl) & (vna_df["u (m/s)"] < u_cru)) & ~np.isnan(vna_df["u (m/s)"]),
			np.nan, vna_df["u (m/s)"]
			)


# freq = 200
# a_cr = 9.81 * 1.0
a_x = (vna_df["u (m/s)"].shift(-1) - vna_df["u (m/s)"]).shift(1)*1
print(a_x.head())
print(vna_df["u (m/s)"].head())
# a_y = vna_df["v (m/s)"].shift(-1) - vna_df["v (m/s)"] * freq
# a_z = vna_df["w1 (m/s)"].shift(-1) - vna_df["w1 (m/s)"] * freq
# print(a_x.head())
spikeu = np.nansum(np.where(~((a_x > -a_cr) & (a_x < a_cr)) & ~np.isnan(a_x), 1, 0))
spikeu_vel = np.nansum(np.where(~((vna_df["u (m/s)"] > u_crl) & (vna_df["u (m/s)"] < u_cru)) & ~np.isnan(vna_df["u (m/s)"]), 1, 0))
#spikeu=a_x.loc[not((a_x > -a_cr) & (a_x < a_cr)) & not(np.isnan(a_x)), '<= 53'] = '1'

# spikevct = [1,2,3]
# spikevct_vel = [234,243,432]
# hdr_spkct = ["u spikes", "v spikes", "w spikes"]
# spike_df = pd.DataFrame(data=[spikevct, spikevct_vel],
# 						columns=hdr_spkct,
# 						index=["acceleration" ,"velocity"])
print(a_x.size)
print(vna_df["u (m/s)"].size)
# print(spikeu_vel)
