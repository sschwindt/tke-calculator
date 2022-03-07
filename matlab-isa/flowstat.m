% Statistics of flow data
function [TimeSer, Stat, Hdr1, Hdr2] = flowstat (inp)
   global side;
   global name;
   global pos;
   t = inp(:,1); % t (s)
   
   % Flow statistics: velocity (m/s), mean (m/s), rms (m/s), stderr (m/s)
   u = inp(:,2); u_avr = nanmean(u); u_rms = nanstd(u,1); u_dsp = u(~isnan(u));
   u_stderr = std(u_dsp)/(sqrt(length(u_dsp))); 
   v = inp(:,3); v_avr = nanmean(v); v_rms = nanstd(v,1); v_dsp = v(~isnan(v));
   v_stderr = std(v_dsp)/(sqrt(length(v_dsp))); 
   w1 = inp(:,4); w1_avr = nanmean(w1); w1_rms = nanstd(w1,1); w1_dsp = w1(~isnan(w1));
   w1_stderr = std(w1_dsp)/(sqrt(length(w1_dsp))); 
   k_t1 = 0.5 * (u_rms^2 + v_rms^2 + w1_rms^2); % k_t1 in m^2/s^2
   % Reynolds stress with u and v
   tau_re0 = NaN(size(t));
   for k = 1:size(t,1)
       if ~isnan(u(k)) && ~isnan(v(k))
	       if u(k) && v(k)
	           tau_re0(k) = - (u(k)-u_avr)*(v(k)-v_avr);
		   end
	   end
   end
   tau_avr0 = nanmean(tau_re0); tau_re0_dsp = tau_re0(~isnan(tau_re0));
   tau_stderr0 = std(tau_re0_dsp)/(sqrt(length(tau_re0_dsp))); 
   % Reynolds stress with u and w1
   tau_re1 = NaN(size(t));
   for k = 1:size(t,1)
       if ~isnan(u(k)) && ~isnan(w1(k))
	       if u(k) && w1(k)
	           tau_re1(k) = - (u(k)-u_avr)*(w1(k)-w1_avr);
		   end
	   end
   end
   tau_avr1 = nanmean(tau_re1); tau_re1_dsp = tau_re1(~isnan(tau_re1));
   tau_stderr1 = std(tau_re1_dsp)/(sqrt(length(tau_re1_dsp))); 
   TimeSer = [t, u, v, w1, tau_re1, tau_re0]; % Time series output
   Stat = [u_avr, u_stderr, u_rms, v_avr, v_stderr, v_rms, w1_avr, w1_stderr, w1_rms, k_t1, tau_avr1, tau_stderr1, tau_avr0, tau_stderr0]; % Stat output
   % Headers
   Hdr1 = {'t (s)', 'u (m/s)', 'v (m/s)', 'w (m/s)', 'tau_re_w (m^2/s^2)', 'tau_re_v (m^2/s^2)'};
   Hdr2 = {'File #', 'x (m)', 'y (m)', 'z (m)', ...
	 'u_avr (m/s)', 'u_stderr (m/s)', 'u_rms (m/s)', ...
	 'v_avr (m/s)', 'v_stderr (m/s)', 'v_rms (m/s)', ...
	 'w_avr (m/s)', 'w_stderr (m/s)', 'w_rms (m/s)', ...
	 'k_t (m^2/s^2)', 'tau_avr_w (m^2/s^2)', 'tau_stderr_w (m^2/s^2)', 'tau_avr_v (m^2/s^2)', 'tau_stderr_v (m^2/s^2)'};
   u_cum = zeros(length(u_dsp),3);
       for k = 1:length(u_dsp)
           u_cum(k,:) = [k, mean(u_dsp(1:k)), std(u_dsp(1:k),1)];
       end
   v_cum = zeros(length(v_dsp),3);
       for k = 1:length(v_dsp)
           v_cum(k,:) = [k, mean(v_dsp(1:k)), std(v_dsp(1:k),1)];
       end
   w1_cum = zeros(length(w1_dsp),3);
       for k = 1:length(w1_dsp)
           w1_cum(k,:) = [k, mean(w1_dsp(1:k)), std(w1_dsp(1:k),1)];
       end
	tau_re1_cum = zeros(length(tau_re1_dsp),2);
		for k = 1:length(tau_re1_dsp)
			tau_re1_cum(k,:) = [k, mean(tau_re1_dsp(1:k))];
        end
    tau_re0_cum = zeros(length(tau_re0_dsp),2);
		for k = 1:length(tau_re0_dsp)
			tau_re0_cum(k,:) = [k, mean(tau_re0_dsp(1:k))];
		end
       
   if side ~= 1   % Measurements with downlooking probe - not adapted
   	 w2 = inp(:,5); w2_avr = nanmean(w2); w2_rms = nanstd(w2,1); w2_dsp = w2(~isnan(w2));
   	 w2_stderr = std(w2_dsp)/(sqrt(length(w2_dsp))); 
   	 k_t2 = 0.5 * (u_rms^2 + v_rms^2 + w2_rms^2); % k_t2 in cm^2/s^2
   	 % Reynolds stress with u and w2
   	 tau_re2 = NaN(size(t));
   	 for k = 1:size(t,1)
       if ~isnan(u(k)) && ~isnan(w2(k))
	       if u(k) && w2(k)
	           tau_re2(k) = - (u(k)-u_avr)*(w2(k)-w2_avr);
		     end
	     end
     end
     tau_avr2 = nanmean(tau_re2); tau_re2_dsp = tau_re2(~isnan(tau_re2));
     tau_stderr2 = std(tau_re2_dsp)/(sqrt(length(tau_re2_dsp))); 
     TimeSer = [TimeSer, w2, tau_re2]; % Time series output
     Stat = [Stat, w2_avr, w2_stderr, w2_rms, k_t2, tau_avr2, tau_stderr2]; % Stat output
     Hdr1 = {'t (s)', 'u (m/s)', 'v (m/s)', 'w1 (m/s)', 'tau_re1 (m^2/s^2)', 'w2 (m/s)', 'tau_re2 (m^2/s^2)'};
     Hdr2 = {'File #', 'x (m)', 'y (m)', 'z (m)', ...
	   'u_avr (m/s)', 'u_stderr (m/s)', 'u_rms (m/s)', ...
	   'v_avr (m/s)', 'v_stderr (m/s)', 'v_rms (m/s)', ...
	 	 'w1_avr (m/s)', 'w1_stderr (m/s)', 'w1_rms (m/s)', ...
	   'k_t1 (m^2/s^2)', 'tau_avrw1 (m^2/s^2)', 'tau_stderrw1 (m^2/s^2)', ...
       'tau_avrv (m^2/s^2)', 'tau_stderrv (m^2/s^2)', ...
	   'w2_avr (m/s)', 'w2_stderr (m/s)', 'w2_rms (m/s)', ...
	   'k_t2 (m^2/s^2)', 'tau_avrw2 (m^2/s^2)', 'tau_stderrw2 (m^2/s^2)'}; % Header updated
     w2_cum = zeros(length(w2_dsp),3);
       for k = 1:length(w2_dsp)
           w2_cum(k,:) = [k, mean(w2_dsp(1:k)), std(w2_dsp(1:k),1)];
       end
	  tau_re2_cum = zeros(length(tau_re2_dsp),2);
		for k = 1:length(tau_re2_dsp)
			tau_re2_cum(k,:) = [k, mean(tau_re2_dsp(1:k))];
		end
   end
   
   % Making cumulative mean plots
% cumavr = figure('Name',name,'units','normalized','outerposition',[0 0 1 1]);
% if side == 1
% 	subplot(3,1,1);
% 	u_mean_cum = scatter(u_cum(:,1),u_cum(:,2),2,'r','filled');
% 	xticks([]);
% 	ylabel('$\bar{u}$ (m/s)','Interpreter','Latex');
% 	set(gca,'FontSize',11);
% 	subplot(3,1,2);
% 	v_mean_cum = scatter(v_cum(:,1),v_cum(:,2),2,'k','filled');
% 	xticks([]);
% 	ylabel('$\bar{v}$ (m/s)','Interpreter','Latex');
% 	set(gca,'FontSize',11);
% 	subplot(3,1,3);
% 	w_mean_cum = scatter(w1_cum(:,1),w1_cum(:,2),2,'b','filled');
% 	xticks([0:2e3:3e4]);
% 	xlabel('Count of sample points');
% 	ylabel('$\bar{w}$ (m/s)','Interpreter','Latex');
% 	set(gca,'FontSize',11);
% else
% 	subplot(4,1,1);
% 	u_mean_cum = scatter(u_cum(:,1),u_cum(:,2),2,'r','filled');
% 	xticks([]);
% 	ylabel('$\bar{u}$ (cm/s)','Interpreter','Latex');
% 	set(gca,'FontSize',11);
% 	subplot(4,1,2);
% 	v_mean_cum = scatter(v_cum(:,1),v_cum(:,2),2,'k','filled');
% 	xticks([]);
% 	ylabel('$\bar{v}$ (m/s)','Interpreter','Latex');
% 	set(gca,'FontSize',11);
% 	subplot(4,1,3);
% 	w1_mean_cum = scatter(w1_cum(:,1),w1_cum(:,2),2,'b','filled');
% 	xticks([]);
% 	ylabel('$\bar{w}_{1}$ (m/s)','Interpreter','Latex');
% 	set(gca,'FontSize',11);
% 	subplot(4,1,4);
% 	w2_mean_cum = scatter(w2_cum(:,1),w2_cum(:,2),2,'m','filled');
% 	%xticks([0:2e3:3e4]);
% 	xlabel('Count of sample points');
% 	ylabel('$\bar{w}_{2}$ (m/s)','Interpreter','Latex');
% 	set(gca,'FontSize',11);
% end
% sgt1 = sgtitle(['Cumulative temporal means at (\itx\rm, \ity\rm, \itz\rm) = (' num2str(pos(1)) ...
% ' m, ' num2str(pos(2)) ' m, ' num2str(pos(3)) ' m)']);
% sgt1.FontSize = 11;
% print(sprintf('%s-cum_mean.png',name),'-dpng','-r600');
% 
% % Making cumulative rms plots
% cumrms = figure('Name',name,'units','normalized','outerposition',[0 0 1 1]);
% if side == 1
% 	subplot(3,1,1);
% 	u_mean_cum = scatter(u_cum(:,1),u_cum(:,3),2,'r','filled');
% 	xticks([]);
% 	ylabel('\itu\rm_{rms} (m/s)');
% 	set(gca,'FontSize',11);
% 	subplot(3,1,2);
% 	v_mean_cum = scatter(v_cum(:,1),v_cum(:,3),2,'k','filled');
% 	xticks([]);
% 	ylabel('\itv\rm_{rms} (m/s)');
% 	set(gca,'FontSize',11);
% 	subplot(3,1,3);
% 	w_mean_cum = scatter(w1_cum(:,1),w1_cum(:,3),2,'b','filled');
% 	%xticks([0:2e3:3e4]);
% 	xlabel('Count of sample points');
% 	ylabel('\itw\rm_{rms} (m/s)');
% 	set(gca,'FontSize',11);
% else
% 	subplot(4,1,1);
% 	u_mean_cum = scatter(u_cum(:,1),u_cum(:,3),2,'r','filled');
% 	xticks([]);
% 	ylabel('\itu\rm_{rms} (m/s)');
% 	set(gca,'FontSize',11);
% 	subplot(4,1,2);
% 	v_mean_cum = scatter(v_cum(:,1),v_cum(:,3),2,'k','filled');
% 	xticks([]);
% 	ylabel('\itv\rm_{rms} (m/s)');
% 	set(gca,'FontSize',11);
% 	subplot(4,1,3);
% 	w1_mean_cum = scatter(w1_cum(:,1),w1_cum(:,3),2,'b','filled');
% 	xticks([]);
% 	ylabel('\itw\rm_{1,rms} (m/s)');
% 	set(gca,'FontSize',11);
% 	subplot(4,1,4);
% 	w2_mean_cum = scatter(w2_cum(:,1),w2_cum(:,3),2,'m','filled');
% 	%xticks([0:2e3:3e4]);
% 	xlabel('Count of sample points');
% 	ylabel('\itw\rm_{2,rms} (m/s)');
% 	set(gca,'FontSize',11);
% end
% % 
% sgt2 = sgtitle(['Cumulative root-mean-square errors at (\itx\rm, \ity\rm, \itz\rm) = (' num2str(pos(1)) ...
% ' m, ' num2str(pos(2)) ' m, ' num2str(pos(3)) ' m)']);
% sgt2.FontSize = 11;
% print(sprintf('%s-cum_rms.png',name),'-dpng','-r600');
% 
% % Making cumulative tau_re plot
% cumre = figure('Name',name,'units','normalized','outerposition',[0 0 1 1]);
% if side == 1
% 	subplot(1,1,1);
% 	tau_mean_cum = scatter(tau_re1_cum(:,1),tau_re1_cum(:,2),2,'k','filled');
% 	%xticks([0:2e3:3e4]);
% 	xlabel('Count of sample points');
% 	ylabel('$-\bar{u''w''} (m^2/s^2)$','Interpreter','Latex');
% 	set(gca,'FontSize',11);
% else
% 	subplot(3,1,1);
% 	tau1_mean_cum = scatter(tau_re1_cum(:,1),tau_re1_cum(:,2),2,'k','filled');
% 	xticks([]);
% 	ylabel('$-\bar{u''w''_1} (m^2/s^2)$','Interpreter','Latex');
% 	set(gca,'FontSize',11);
% 	subplot(3,1,2);
% 	tau2_mean_cum = scatter(tau_re2_cum(:,1),tau_re2_cum(:,2),2,'k','filled');
% 	%xticks([0:2e3:3e4]);
% 	xlabel('Count of sample points');
% 	ylabel('$-\bar{u''w''_2} (m^2/s^2)$','Interpreter','Latex');
% 	set(gca,'FontSize',11);
% 	subplot(3,1,3);
% 	tau0_mean_cum = scatter(tau_re0_cum(:,1),tau_re0_cum(:,2),2,'k','filled');
% 	%xticks([0:2e3:3e4]);
% 	xlabel('Count of sample points');
% 	ylabel('$-\bar{u''v''} (m^2/s^2)$','Interpreter','Latex');
% 	set(gca,'FontSize',11);
% end
% sgt3 = sgtitle(['Cumulative temporal mean of Reynolds stress at (\itx\rm, \ity\rm, \itz\rm) = (' num2str(pos(1)) ...
% ' m, ' num2str(pos(2)) ' m, ' num2str(pos(3)) ' m)']);
% sgt2.FontSize = 11;
% print(sprintf('%s-cum_rs.png',name),'-dpng','-r600'); %adapt plot type?

close all;
end