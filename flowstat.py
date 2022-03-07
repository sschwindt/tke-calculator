import numpy as np


def flowstat(t, u, v, w1, w2, side="DOWN"):
    """get data statistics

    Args:
        time (np.array): time in seconds
        u (np.array): streamweise velocity along x-axis (positive in bulk flow direction)
        v (np.array): perpendicular velocity along y-axis
        w1 (np.array): vertical velocity if side is DOWN
        w2 (np.array): vertical velocity if side is not DOWN
        side (str): orientation of the probe (default: DOWN, which mean probe looks like FlowTracker in a river)

    Returns:
        time_series, stat, hdr1, hdr1
    """
    if side == "DOWN":
        w = w1
    else:
        w = w2
   # flow statistics: velocity (m/s), mean (m/s), rms (m/s), stderr (m/s)
   u_stats = {
              "average": np.nanmean(u),
              "std": np.nanstd(u),
              "stderr": np.nanstd(u) / np.sqrt(np.count_nonzero(~np.isnan(u)))
   }

   v_stats = {
              "average": np.nanmean(v),
              "std": np.nanstd(v),
              "stderr": np.nanstd(v) / np.sqrt(np.count_nonzero(~np.isnan(v)))
   }

   w_stats = {
              "average": np.nanmean(w),
              "std": np.nanstd(w),
              "stderr": np.nanstd(w) / np.sqrt(np.count_nonzero(~np.isnan(w)))
   }

   # get k_t1
   k_t1 = 0.5 * (u_stats["std"] ** 2 + v_stats["std"] ** 2 + w_stats["std"] ** 2);  # k_t1 in m^2/s^2

   # calculate Reynolds stress for u and v
   tau_re0 = np.multiply(u - u_stat["average"], v - v_stat["average"])
   tau_re0_stats = {
                    "average": np.nanmean(tau_re0),
                    "std": np.nanstd(tau_re0),
                    "stderr": np.nanstd(tau_re0) / np.sqrt(np.count_nonzero(~np.isnan(tau_re0)))
   }

   # calculate Reynolds stress for u and w1
   tau_re1 = np.multiply(u - u_stat["average"], w - w_stat["average"])
   tau_re1_stats = {
                    "average": np.nanmean(tau_re1),
                    "std": np.nanstd(tau_re1),
                    "stderr": np.nanstd(tau_re1) / np.sqrt(np.count_nonzero(~np.isnan(tau_re1)))
   }


   time_series = pd.DataFrame(data=[t, u, v, w1, tau_re1, tau_re0]) # Time series output
   stats = pd.DataFrame(
                    data=[u_stats, v_stats, w_stats, tau_re0_stats, tau_re1_stats],
                    index=["t (s)", "u (m/s)", "v (m/s)", "w (m/s)", "tau_re0_stats (m^2/s^2)", "tau_re0_stats (m^2/s^2)"],
                    )


   # u_cum = [np.nancumsum(u), np.nancumsum(u)]
   #     for k = 1:length(u_dsp)
   #         u_cum(k,:) = [k, mean(u_dsp(1:k)), std(u_dsp(1:k),1)];
   #     end
   # v_cum = zeros(length(v_dsp),3);
   #     for k = 1:length(v_dsp)
   #         v_cum(k,:) = [k, mean(v_dsp(1:k)), std(v_dsp(1:k),1)];
   #     end
   # w1_cum = zeros(length(w1_dsp),3);
   #     for k = 1:length(w1_dsp)
   #         w1_cum(k,:) = [k, mean(w1_dsp(1:k)), std(w1_dsp(1:k),1)];
   #     end
	# tau_re1_cum = zeros(length(tau_re1_dsp),2);
	# 	for k = 1:length(tau_re1_dsp)
	# 		tau_re1_cum(k,:) = [k, mean(tau_re1_dsp(1:k))];
   #      end
   #  tau_re0_cum = zeros(length(tau_re0_dsp),2);
	# 	for k = 1:length(tau_re0_dsp)
	# 		tau_re0_cum(k,:) = [k, mean(tau_re0_dsp(1:k))];
	# 	end
   return time_series, stats
