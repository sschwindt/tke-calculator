.


def rmspik(dataset, f, lambda_a=1.0, k=3.0):
	""" Spike removal and replacement - see Nikora & Goring (1999) and Goring & Nikora (2002).

	Args:
		dataset (numpy.array): matrix-like data array from the measurement file
		f (int): sampling frequency in 1/s (Hz)
		lambda_a (float): multiplier of gravitational acceleration (acceleration threshold)
		k (float): multiplier of velocity stdev (velocity threshold)

	Note:
		Goring & Nikora (2002) suggest lambda_a = 1.0 ~ 1.5 and k = 1.5, but we shall use lambda_a = 1.0 and k = 3 ~ 9.
		SonTek, Nortek, and Lei recommend the SNR and correlation thresholds to be 15 and 70 respectively.
		Though data points have high SNR, the correlation can be low.
	"""


# Time series. In column order: t (s), u (m/s), v (m/s), w1 (m/s), w2 (m/s).
out = [dataset(:, 1), dataset(:, 4:7)];
[row, ~] = size(out);  # Count of recorded samples.
t_0 = out(1, 1);
t = cat(1, out(: , 1)) - t_0; # t (s) starting from 0.
out(: , 1) = t;
u = cat(1, out(: , 2)); v = cat(1, out(: , 3)); w1 = cat(1, out(: , 4)); w2 = cat(1, out(: , 5)); # velocity (m/s)
rawout = [t, u, v, w1, w2];  # Save the time series

# Headers
if side == 1
	hdr_tsr = {'t (s)', 'u (m/s)', 'v (m/s)', 'w (m/s)'};
	rawout(: , 5) = [];
	hdr_spkct = {'u spikes', 'v spikes', 'w spikes'};
else
	hdr_tsr = {'t (s)', 'u (m/s)', 'v (m/s)', 'w1 (m/s)', 'w2 (m/s)'};
	hdr_spkct = {'u spikes', 'v spikes', 'w1 spikes', 'w2 spikes'};
end

# Write raw data to a .csv file.
writecell(hdr_tsr, [name '-Raw.csv']);
dlmwrite([name '-Raw.csv'], rawout, '-append');

# # Plot the raw time series
# rawfig = figure('Name',name,'units','normalized','outerposition',[0 0 1 1]);
# if side == 1
# 	subplot(3,1,1);
# 	u_ser = scatter(t,u,2,'r','filled');
# 	xticks([]);
# 	ylabel('\itu\rm (m/s)');
# 	set(gca,'FontSize',16);
# 	subplot(3,1,2);
# 	v_ser = scatter(t,v,2,'k','filled');
# 	xticks([]);
# 	ylabel('\itv\rm (m/s)');
# 	set(gca,'FontSize',16);
# 	subplot(3,1,3);
# 	w_ser = scatter(t,w1,2,'b','filled');
# 	xticks([0:10:150]);
# 	xlabel('\itt\rm (s)');
# 	ylabel('\itw\rm (m/s)');
# 	set(gca,'FontSize',16);
# else
# 	subplot(4,1,1);
# 	u_ser = scatter(t,u,2,'r','filled');
# 	xticks([]);
# 	ylabel('\itu\rm (m/s)');
# 	set(gca,'FontSize',16);
# 	subplot(4,1,2);
# 	v_ser = scatter(t,v,2,'k','filled');
# 	xticks([]);
# 	ylabel('\itv\rm (m/s)');
# 	set(gca,'FontSize',16);
# 	subplot(4,1,3);
# 	w1_ser = scatter(t,w1,2,'b','filled');
# 	xticks([]);
# 	ylabel('\itw\rm_1 (m/s)');
# 	set(gca,'FontSize',16);
# 	subplot(4,1,4);
# 	w2_ser = scatter(t,w2,2,'m','filled');
# 	xticks([0:10:150]);
# 	xlabel('\itt\rm (s)');
# 	ylabel('\itw\rm_2 (m/s)');
# 	set(gca,'FontSize',16);
# end
# sgt = sgtitle(['Original flow data at (\itx\rm, \ity\rm, \itz\rm) = (' num2str(pos(1)) ...
# ' m, ' num2str(pos(2)) ' m, ' num2str(pos(3)) ' m)']);
# sgt.FontSize = 20;
# print(sprintf('#s-raw.png',name),'-dpng','-r600');

# Low-pass filter
# lpsout(:,1) = t;
# lpsout(:,2:4) = lowpass(rawout(:,2:4),32,200,'ImpulseResponse','iir','Steepness',0.999);
# if side ~= 1
# 	lpsout(:,5) = lowpass(rawout(:,5),32,200,'ImpulseResponse','iir','Steepness',0.999);
# end
# writecell(hdr_tsr, [name '-lowpass.csv']);
# dlmwrite([name '-lowpass.csv'], lpsout, '-append');
# out = lpsout;
# clear lpsout;
# t = out(:,1); u = out(:,2); v = out(:,3); w1 = out(:,4);
# if side ~= 1
# 	w2 = out(:,5);
# end

# # Plot the low-pass filtered time series
# lpsfig = figure('Name',name,'units','normalized','outerposition',[0 0 1 1]);
# if side == 1
# 	subplot(3,1,1);
# 	u_ser = scatter(t,u,2,'r','filled');
# 	xticks([]);
# 	ylabel('\itu\rm (m/s)');
# 	set(gca,'FontSize',16);
# 	subplot(3,1,2);
# 	v_ser = scatter(t,v,2,'k','filled');
# 	xticks([]);
# 	ylabel('\itv\rm (m/s)');
# 	set(gca,'FontSize',16);
# 	subplot(3,1,3);
# 	w_ser = scatter(t,w1,2,'b','filled');
# 	xticks([0:10:150]);
# 	xlabel('\itt\rm (s)');
# 	ylabel('\itw\rm (m/s)');
# 	set(gca,'FontSize',16);
# else
# 	subplot(4,1,1);
# 	u_ser = scatter(t,u,2,'r','filled');
# 	xticks([]);
# 	ylabel('\itu\rm (m/s)');
# 	set(gca,'FontSize',16);
# 	subplot(4,1,2);
# 	v_ser = scatter(t,v,2,'k','filled');
# 	xticks([]);
# 	ylabel('\itv\rm (m/s)');
# 	set(gca,'FontSize',16);
# 	subplot(4,1,3);
# 	w1_ser = scatter(t,w1,2,'b','filled');
# 	xticks([]);
# 	ylabel('\itw\rm_1 (m/s)');
# 	set(gca,'FontSize',16);
# 	subplot(4,1,4);
# 	w2_ser = scatter(t,w2,2,'m','filled');
# 	xticks([0:10:150]);
# 	xlabel('\itt\rm (s)');
# 	ylabel('\itw\rm_2 (m/s)');
# 	set(gca,'FontSize',16);
# end
# sgt = sgtitle(['Low-pass filtered flow data at (\itx\rm, \ity\rm, \itz\rm) = (' num2str(pos(1)) ...
# ' m, ' num2str(pos(2)) ' m, ' num2str(pos(3)) ' m)']);
# sgt.FontSize = 20;
# print(sprintf('#s-lowpass.png',name),'-dpng','-r600');

# Acceleration
# Any operation with NaN will return NaN.
# Hence, only two consecutive data records (i.e. delta t = 1/f) will produce a set of acceleration components.
# x acceleration (m/s^2)
a_x = cat(1, NaN, out(2: row, 2) - out(1: (row-1), 2)) * f;
# y acceleration (m/s^2)
a_y = cat(1, NaN, out(2: row, 3) - out(1: (row-1), 3)) * f;
# z1 acceleration (m/s^2)
a_z1 = cat(1, NaN, out(2: row, 4) - out(1: (row-1), 4)) * f;
if side ~ = 1
	# z2 acceleration (m/s^2)
	a_z2 = cat(1, NaN, out(2: row, 5) - out(1: (row-1), 5)) * f;
end
a_cr = 9.8 * lambda_a;  # Acceleration threshold

# In Goring & Nikora (2002)'s Acceleration Thresholding Method (ATM), the acceleration thresholds are tested at first.
spikeu = 0; spikev = 0; spikew1 = 0;  # Initialization of total counts
	for j = 2: length(u)-1  # Count
	  # NaN values are also included.
	  if (~((a_x(j) > -a_cr) & & (a_x(j) < a_cr)) & & ~isnan(a_x(j)))
		  u(j) = NaN;
		  spikeu = spikeu + 1;
	  end
	  if (~((a_y(j) > -a_cr) & & (a_y(j) < a_cr)) & & ~isnan(a_y(j)))
		  v(j) = NaN;
		  spikev = spikev + 1;
	  end
	  if (~((a_z1(j) > -a_cr) & & (a_z1(j) < a_cr)) & & ~isnan(a_z1(j)))
		  w1(j) = NaN;
		  spikew1 = spikew1 + 1;
	  end
	end
	out = [t, u, v, w1];
	spikevct = [spikeu, spikev, spikew1];
	if side ~ = 1
		spikew2 = 0;
		for j = 2: length(u)-1  # Count
			if (~((a_z2(j) > -a_cr) & & (a_z2(j) < a_cr)) & & ~isnan(a_z2(j)))
		  	w2(j) = NaN;
		  	spikew2 = spikew2 + 1;
	  	end
	  end
	  out = [out, w2];
	  spikevct = [spikevct, spikew2];
	end

writecell(hdr_tsr, [name '-accthres.csv']);
dlmwrite([name '-accthres.csv'], out, '-append');
writecell(hdr_spkct, [name '-spikes.csv']);
dlmwrite([name '-spikes.csv'], spikevct, '-append');

spikeu = 0; spikev = 0; spikew1 = 0; # Initialization of total counts

# Mean, standard deviation, and velocity threshold
# nanmean() and nanstd() are utilized because numerous NaN values exist in the time series after the first stage of despiking.
u_m = nanmean(u); u_s = nanstd(u); u_crl = (u_m - k * u_s); u_cru = (u_m + k * u_s); # For u
v_m = nanmean(v); v_s = nanstd(v); v_crl = (v_m - k * v_s); v_cru = (v_m + k * v_s); # For v
w1_m = nanmean(w1); w1_s = nanstd(w1); w1_crl = (w1_m - k * w1_s); w1_cru = (w1_m + k * w1_s); # For w1

# Flow velocity
	for j = 2:length(u)-1 # Count
	  if (~((u(j) > u_crl) && (u(j) < u_cru)) && ~isnan(u(j)))
		  u(j) =  NaN;
		  spikeu = spikeu + 1;
	  end
	  if (~((v(j) > v_crl) && (v(j) < v_cru)) && ~isnan(v(j)))
		  v(j) = NaN;
		  spikev = spikev + 1;
	  end
	  if (~((w1(j) > w1_crl) && (w1(j) < w1_cru)) && ~isnan(w1(j)))
		  w1(j) = NaN;
		  spikew1 = spikew1 + 1;
	  end
	end
	dspout = [t, u, v, w1];
	spikevct = [spikeu, spikev, spikew1];
	if side ~= 1
		w2_m = nanmean(w2); w2_s = nanstd(w2); w2_crl = (w2_m - k * w2_s); w2_cru = (w2_m + k * w2_s); # For w2
		spikew2 = 0;
		for j = 2:length(u)-1 # Count
			if (~((w2(j) > w2_crl) && (w2(j) < w2_cru)) && ~isnan(w2(j)))
		  	w2(j) = NaN;
		  	spikew2 = spikew2 + 1;
	  	end
	  end
	  dspout = [dspout, w2];
	  spikevct = [spikevct, spikew2];
	end

writecell(hdr_tsr, [name '-velthres.csv']);
dlmwrite([name '-velthres.csv'], dspout, '-append');
dlmwrite([name '-spikes.csv'], spikevct, '-append');

# dspfig = figure('Name',name,'units','normalized','outerposition',[0 0 1 1]);
# if side == 1
# 	subplot(3,1,1);
# 	u_ser = scatter(t,u,2,'r','filled');
# 	xticks([]);
# 	ylabel('\itu\rm (m/s)');
# 	set(gca,'FontSize',16);
# 	subplot(3,1,2);
# 	v_ser = scatter(t,v,2,'k','filled');
# 	xticks([]);
# 	ylabel('\itv\rm (m/s)');
# 	set(gca,'FontSize',16);
# 	subplot(3,1,3);
# 	w_ser = scatter(t,w1,2,'b','filled');
# 	xticks([0:10:150]);
# 	xlabel('\itt\rm (s)');
# 	ylabel('\itw\rm (m/s)');
# 	set(gca,'FontSize',16);
# else
# 	subplot(4,1,1);
# 	u_ser = scatter(t,u,2,'r','filled');
# 	xticks([]);
# 	ylabel('\itu\rm (m/s)');
# 	set(gca,'FontSize',16);
# 	subplot(4,1,2);
# 	v_ser = scatter(t,v,2,'k','filled');
# 	xticks([]);
# 	ylabel('\itv\rm (m/s)');
# 	set(gca,'FontSize',16);
# 	subplot(4,1,3);
# 	w1_ser = scatter(t,w1,2,'b','filled');
# 	xticks([]);
# 	ylabel('\itw\rm_1 (m/s)');
# 	set(gca,'FontSize',16);
# 	subplot(4,1,4);
# 	w2_ser = scatter(t,w2,2,'m','filled');
# 	xticks([0:10:150]);
# 	xlabel('\itt\rm (s)');
# 	ylabel('\itw\rm_2 (m/s)');
# 	set(gca,'FontSize',16);
# end
# sgt = sgtitle(['Despiked flow data at (\itx\rm, \ity\rm, \itz\rm) = (' num2str(pos(1)) ...
# ' m, ' num2str(pos(2)) ' m, ' num2str(pos(3)) ' m)']);
# sgt.FontSize = 20;
# print(sprintf('#s-dsp.png',name),'-dpng','-r600');

close all;

end
