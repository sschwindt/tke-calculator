% Main program for flow analysis

% Initialization
clear; % Clear the memory
clc; % Clear the screen

% 1. Name final file -- needs to be adapted
global testnr; 
global profiletype;
testnr = 'T2_LP_6';
profiletype = 'LP'; %lateral profile; other types: VP for vertical; LP for longitudinal

% 2. Data Indexing
% Read the summary sheet to return "raw", a cell array including numeric and text data, excluding following consecutive empty rows.
% For further process in the load(sprintf()) function, names of the data file cannot be numeric.
[~, txt, raw] = xlsread('Input.xlsx');

[m, ~] = size(txt); % Return row numbers of the cell array txt as m.
data_ct = m - 13; % Quantity of indexed data files.
Stat_sum = NaN(data_ct, 22); % Initialization of matrix Stat_sum in which despiked flow data will be stored.

% Read the (cell) array raw; data index begins at row # 14.
% The following file names (cannot be numeric) and 3D position should be predefined in the summary sheet -
% PRIOR TO the post-processing below.
nc = raw(14:m,1); % All file names of data files (*.vna);
									% *.dat files can be loaded as well, but column indexes should be changed accordingly.
xx = raw(14:m,2); % all x (cm)
yy = raw(14:m,5); % all y (cm)
zz = raw(14:m,6); % all z (cm)

[m, ~]=size(xx); % Return the quantity of data files as m.

% Convert the position cells to arrays (column vectors) for further operation.
xx = cell2mat(xx(1:m)); yy = cell2mat(yy(1:m)); zz = cell2mat(zz(1:m));

% 3. Data processing
global name; % This variable will be called in function rmspike(dataset, f, lambda_a, k).
global side; % Side-looking probe - 1; down-looking probe - 0.
global pos; % 3D position of measurement
for i = 1 : m
   name = nc{i}; % Assign a file name to the variable "name".
   pos = [xx(i), yy(i), zz(i)];
	 % Try-catch-end loop
	 % If the block before catch does not work, the block inside "catch" will be executed.
   try 
   	 RawFlow = load(sprintf('%s.vna',name)); % Load the data file (*.vna) into a matrix - Automatic split.
   catch
   	 continue; % Continue with a new loop for(i).
   end

   % Data #, 3D measurement position
   Stat_sum(i,1) = i; Stat_sum(i,2) = xx(i); Stat_sum(i,3) = yy(i); Stat_sum(i,4) = zz(i); 

   % For *.vna files, the first column is all-zero. Remove this column so that the code can be easily applied to *.dat files.
	 if RawFlow(1,1) == 0 && RawFlow(2,1) == 0
	   RawFlow(:,1) = [];
   end
   if RawFlow(1,7) == 0 && RawFlow(2,7) == 0
   	 side = 1; % Side-looking probes do not report w2.
   else
   	 side = 0; % Down-looking probes will report non-zero w2.
   end
  
   
   % At this stage, the matrix RawFlow is constituted of the following 19 columns:
   % Columns 1 - 3: Time (s), Sample #, (disregard);
   % Columns 4 - 7: Velocity records - u, v, w1, w2 (m/s);
   % Columns 8 - 11: Beam amplitude - x, y, z1, z2 (dB);
   % Columns 12 - 15: Signal to Noise Ratio - x, y, z1, z2;
   % Columns 16 - 19: Correlation (normalized amplitude of the auto-correlation function) - x, y, z1, z2 (%).

   Dat = rmspike(RawFlow, 200, 1.0, 3.0); % Spike detection and removal
   clear RawFlow;
   [TimeS_dsp, Stat_dsp, hdr_final, hdr_stat] = flowstat(Dat); % Time series and statistics of the despiked flow data
   clear Dat;
   writecell(hdr_final, [name '-final.csv']);
   dlmwrite([name '-final.csv'], TimeS_dsp, '-append');
   Stat_sum(i,5:4+size(Stat_dsp,2)) = Stat_dsp; % Collect statistics of the despiked flow data
end
clear TimeS_dsp;
if isnan(Stat_sum(1,17))
	Stat_sum(:,17:22) = [];
end

% Create a summary sheet of the profile after despiking
writecell(hdr_stat, [testnr '.csv']);
dlmwrite([testnr '.csv'], Stat_sum, '-append');

%% Summary plots of velocity - longitudinal profile

% Side probe used here, if both add:
% if side == 1
% else

B = 10;
h = 15;

figure(),
set(gcf,'Color','w','Units','centimeters','Position',[0 0 B h]);
subplot(3,1,1);
uz = errorbar(Stat_sum(:,2),Stat_sum(:,5),Stat_sum(:,6),'horizontal','o','MarkerSize',8,...
	'MarkerEdgeColor','k','MarkerFaceColor','k','CapSize',12,'LineWidth',0.5,'Color','k');
set(gca,'FontName','Times New Roman','FontSize',11,'Color','k');
% axis([-.5 7 -0.20 0.20]);
xlabel('\fontname{Times New Roman}\itx\rm [m]');       % x-axis label
ylabel('\itu\rm [m/s]');      % y-axis label
ax = gca;
ax.Color = 'w';
ax.YColor = 'k';
ax.XColor = 'k';
ax.Layer = 'bottom';
ax.LineWidth = 0.25;
ax.XGrid = 'on';
ax.YGrid = 'on';
ax.GridLineStyle = '-';
ax.GridColor = 'k';
ax.GridAlpha = 1;
% xticks([-0.5:0.5:7])
% yticks([-0.2 -0.10 0 0.10 0.2])
% text(0.005,0.95,'\fontname{Times New Roman}(b) \itx\rm = 1.62 m, \itz\rm = 0.05 m','Units','Normalized','FontSize',11)

subplot(3,1,2);
vz = errorbar(Stat_sum(:,2),Stat_sum(:,8),Stat_sum(:,9),'horizontal','o','MarkerSize',8,...
	'MarkerEdgeColor','k','MarkerFaceColor','w','CapSize',12,'LineWidth',0.5,'Color','k');
set(gca,'FontName','Times New Roman','FontSize',11,'Color','k');
% axis([-0.5 7 -0.05 0.05]);
xlabel('\fontname{Times New Roman}\itx\rm [m]');       % x-axis label
ylabel('\itv\rm [m/s]');      % y-axis label
ax = gca;
ax.Color = 'w';
ax.YColor = 'k';
ax.XColor = 'k';
ax.Layer = 'bottom';
ax.LineWidth = 0.25;
ax.XGrid = 'on';
ax.YGrid = 'on';
ax.GridLineStyle = '-';
ax.GridColor = 'k';
ax.GridAlpha = 1;
% xticks([-0.5:0.5:7])
% yticks([-0.05 -0.025 0 0.025 0.05])

subplot(3,1,3);
wz1 = errorbar(Stat_sum(:,2),Stat_sum(:,11),Stat_sum(:,12),'horizontal','o','MarkerSize',8,...
	'MarkerEdgeColor','k','MarkerFaceColor',[0.4 0.4 0.4],'CapSize',12,'LineWidth',0.5,'Color','k');
set(gca,'FontName','Times New Roman','FontSize',11,'Color','k');
% axis([-0.5 7 -0.05 0.05]);
xlabel('\fontname{Times New Roman}\ity\rm [m]');       % x-axis label
ylabel('\itw\rm [m/s]');      % y-axis label
ax = gca;
ax.Color = 'w';
ax.YColor = 'k';
ax.XColor = 'k';
ax.Layer = 'bottom';
ax.LineWidth = 0.25;
ax.XGrid = 'on';
ax.YGrid = 'on';
ax.GridLineStyle = '-';
ax.GridColor = 'k';
ax.GridAlpha = 1;
% xticks([-0.5:0.5:7])
% yticks([-0.05 -0.025 0 0.025 0.05])

sgt = sgtitle(['\fontname{Times New Roman}Longitudinal profiles at (\ity\rm, \itz\rm) = (' num2str(pos(2)) ...
' m, ' num2str(pos(3)) ' m)']);
sgt.FontSize = 11;
%print(sprintf('Velocity_prof.png'),'-dpng','-r600');
export_fig 'Velocity_prof_LP' -jpg -m5
%saveas(gcf,'Velocity_prof_LP','jpg')

%% Summary plots of k_t and Reynolds stress
% Side probe used here, if both add:
% if side == 1
% else

B = 10;
h = 15;

figure(),
set(gcf,'Color','w','Units','centimeters','Position',[0 0 B h]);
subplot(3,1,1);
kte = plot(Stat_sum(:,2),Stat_sum(:,14),'o',...
                'LineWidth',0.75,...
                'MarkerEdgeColor','k',...
                'MarkerFaceColor','k',...
                'MarkerSize',8);
set(gca,'FontName','Times New Roman','FontSize',11,'Color','k');
% axis([-.5 7 0 0.01]);
xlabel('\fontname{Times New Roman}\itx\rm [m]');       % x-axis label
ylabel('\itk_t\rm [m^2/s^2]');      % y-axis label
ax = gca;
ax.Color = 'w';
ax.YColor = 'k';
ax.XColor = 'k';
ax.Layer = 'bottom';
ax.LineWidth = 0.25;
ax.XGrid = 'on';
ax.YGrid = 'on';
ax.GridLineStyle = '-';
ax.GridColor = 'k';
ax.GridAlpha = 1;
% xticks([-0.5:0.5:7])
% yticks([0 0.0025 0.005 0.0075 0.01])
% text(0.005,0.95,'\fontname{Times New Roman}(b) \itx\rm = 1.62 m, \itz\rm = 0.05 m','Units','Normalized','FontSize',11)

subplot(3,1,2);
tauw = errorbar(Stat_sum(:,2),Stat_sum(:,15),Stat_sum(:,16),'horizontal','o','MarkerSize',8,...
	'MarkerEdgeColor','k','MarkerFaceColor','w','CapSize',12,'LineWidth',0.5,'Color','k');
set(gca,'FontName','Times New Roman','FontSize',11,'Color','k');
% axis([-0.5 7 -0.001 0.001]);
xlabel('\fontname{Times New Roman}\itx\rm [m]');       % x-axis label
ylabel('\itu''w''\rm [m^2/s^2]');      % y-axis label
ax = gca;
ax.Color = 'w';
ax.YColor = 'k';
ax.XColor = 'k';
ax.Layer = 'bottom';
ax.LineWidth = 0.25;
ax.XGrid = 'on';
ax.YGrid = 'on';
ax.GridLineStyle = '-';
ax.GridColor = 'k';
ax.GridAlpha = 1;
% xticks([-0.5:0.5:7])
% yticks([-0.001 -0.0005 0 0.0005 0.001])

subplot(3,1,3);
tauv = errorbar(Stat_sum(:,2),Stat_sum(:,17),Stat_sum(:,18),'horizontal','o','MarkerSize',8,...
	'MarkerEdgeColor','k','MarkerFaceColor',[0.4 0.4 0.4],'CapSize',12,'LineWidth',0.5,'Color','k');
set(gca,'FontName','Times New Roman','FontSize',11,'Color','k');
% axis([-0.5 7 -0.001 0.001]);
xlabel('\fontname{Times New Roman}\itx\rm [m]');       % x-axis label
ylabel('\itu''v''\rm [m^2/s^2]');      % y-axis label
ax = gca;
ax.Color = 'w';
ax.YColor = 'k';
ax.XColor = 'k';
ax.Layer = 'bottom';
ax.LineWidth = 0.25;
ax.XGrid = 'on';
ax.YGrid = 'on';
ax.GridLineStyle = '-';
ax.GridColor = 'k';
ax.GridAlpha = 1;
% xticks([-0.5:0.5:7])
% yticks([-0.001 -0.0005 0 0.0005 0.001])

sgt = sgtitle(['\fontname{Times New Roman}TKE and RS profiles at (\ity\rm, \itz\rm) = (' num2str(pos(2)) ...
' m, ' num2str(pos(3)) ' m)']);
sgt.FontSize = 11;
%print(sprintf('Velocity_prof.png'),'-dpng','-r600');
export_fig 'TKE_stress_LP' -jpg -m5
%saveas(gcf,'TKE_stress_LP','jpg')

%%
close all;