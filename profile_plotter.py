# # Summary plots of velocity - longitudinal profile

# Side probe used here, if both add:
# if side == 1
# else

B = 10
h = 15

figure(),
set(gcf, 'Color', 'w', 'Units', 'centimeters', 'Position', [0 0 B h])
subplot(3, 1, 1)
uz = errorbar(Stat_sum(:, 2), Stat_sum(: , 5), Stat_sum(: , 6), 'horizontal', 'o', 'MarkerSize', 8, ...
              'MarkerEdgeColor', 'k', 'MarkerFaceColor', 'k', 'CapSize', 12, 'LineWidth', 0.5, 'Color', 'k')
set(gca, 'FontName', 'Times New Roman', 'FontSize', 11, 'Color', 'k')
# axis([-.5 7 - 0.20 0.20])
xlabel('\fontname{Times New Roman}\itx\rm [m]')
# x-axis label
ylabel('\itu\rm [m/s]')
# y-axis label
ax = gca
ax.Color = 'w'
ax.YColor = 'k'
ax.XColor = 'k'
ax.Layer = 'bottom'
ax.LineWidth = 0.25
ax.XGrid = 'on'
ax.YGrid = 'on'
ax.GridLineStyle = '-'
ax.GridColor = 'k'
ax.GridAlpha = 1
# xticks([-0.5:0.5:7])
# yticks([-0.2 - 0.10 0 0.10 0.2])
# text(0.005, 0.95, '\fontname{Times New Roman}(b) \itx\rm = 1.62 m, \itz\rm = 0.05 m', 'Units', 'Normalized', 'FontSize', 11)

subplot(3, 1, 2)
vz = errorbar(Stat_sum(:, 2), Stat_sum(: , 8), Stat_sum(: , 9), 'horizontal', 'o', 'MarkerSize', 8, ...
              'MarkerEdgeColor', 'k', 'MarkerFaceColor', 'w', 'CapSize', 12, 'LineWidth', 0.5, 'Color', 'k')
set(gca, 'FontName', 'Times New Roman', 'FontSize', 11, 'Color', 'k')
# axis([-0.5 7 - 0.05 0.05])
xlabel('\fontname{Times New Roman}\itx\rm [m]')
# x-axis label
ylabel('\itv\rm [m/s]')
# y-axis label
ax = gca
ax.Color = 'w'
ax.YColor = 'k'
ax.XColor = 'k'
ax.Layer = 'bottom'
ax.LineWidth = 0.25
ax.XGrid = 'on'
ax.YGrid = 'on'
ax.GridLineStyle = '-'
ax.GridColor = 'k'
ax.GridAlpha = 1
# xticks([-0.5:0.5:7])
# yticks([-0.05 - 0.025 0 0.025 0.05])

subplot(3, 1, 3)
wz1 = errorbar(Stat_sum(:, 2), Stat_sum(: , 11), Stat_sum(: , 12), 'horizontal', 'o', 'MarkerSize', 8, ...
               'MarkerEdgeColor', 'k', 'MarkerFaceColor', [0.4 0.4 0.4], 'CapSize', 12, 'LineWidth', 0.5, 'Color', 'k')
set(gca, 'FontName', 'Times New Roman', 'FontSize', 11, 'Color', 'k')
# axis([-0.5 7 - 0.05 0.05])
xlabel('\fontname{Times New Roman}\ity\rm [m]')
# x-axis label
ylabel('\itw\rm [m/s]')
# y-axis label
ax = gca
ax.Color = 'w'
ax.YColor = 'k'
ax.XColor = 'k'
ax.Layer = 'bottom'
ax.LineWidth = 0.25
ax.XGrid = 'on'
ax.YGrid = 'on'
ax.GridLineStyle = '-'
ax.GridColor = 'k'
ax.GridAlpha = 1
# xticks([-0.5:0.5:7])
# yticks([-0.05 - 0.025 0 0.025 0.05])

sgt = sgtitle(['\fontname{Times New Roman}Longitudinal profiles at (\ity\rm, \itz\rm) = (' num2str(pos(2)) ...
               ' m, ' num2str(pos(3)) ' m)'])
sgt.FontSize = 11
#print(sprintf('Velocity_prof.png'), '-dpng', '-r600')
export_fig 'Velocity_prof_LP' - jpg - m5
#saveas(gcf, 'Velocity_prof_LP', 'jpg')

# # Summary plots of k_t and Reynolds stress
# Side probe used here, if both add:
# if side == 1
# else

B = 10
h = 15

figure(),
set(gcf, 'Color', 'w', 'Units', 'centimeters', 'Position', [0 0 B h])
subplot(3, 1, 1)
kte = plot(Stat_sum(:, 2), Stat_sum(: , 14), 'o', ...
           'LineWidth', 0.75, ...
           'MarkerEdgeColor', 'k', ...
           'MarkerFaceColor', 'k', ...
           'MarkerSize', 8)
set(gca, 'FontName', 'Times New Roman', 'FontSize', 11, 'Color', 'k')
# axis([-.5 7 0 0.01])
xlabel('\fontname{Times New Roman}\itx\rm [m]')
# x-axis label
ylabel('\itk_t\rm [m^2/s^2]')
# y-axis label
ax = gca
ax.Color = 'w'
ax.YColor = 'k'
ax.XColor = 'k'
ax.Layer = 'bottom'
ax.LineWidth = 0.25
ax.XGrid = 'on'
ax.YGrid = 'on'
ax.GridLineStyle = '-'
ax.GridColor = 'k'
ax.GridAlpha = 1
# xticks([-0.5:0.5:7])
# yticks([0 0.0025 0.005 0.0075 0.01])
# text(0.005, 0.95, '\fontname{Times New Roman}(b) \itx\rm = 1.62 m, \itz\rm = 0.05 m', 'Units', 'Normalized', 'FontSize', 11)

subplot(3, 1, 2)
tauw = errorbar(Stat_sum(:, 2), Stat_sum(: , 15), Stat_sum(: , 16), 'horizontal', 'o', 'MarkerSize', 8, ...
                'MarkerEdgeColor', 'k', 'MarkerFaceColor', 'w', 'CapSize', 12, 'LineWidth', 0.5, 'Color', 'k')
set(gca, 'FontName', 'Times New Roman', 'FontSize', 11, 'Color', 'k')
# axis([-0.5 7 - 0.001 0.001])
xlabel('\fontname{Times New Roman}\itx\rm [m]')
# x-axis label
ylabel('\itu''w''\rm [m^2/s^2]')
# y-axis label
ax = gca
ax.Color = 'w'
ax.YColor = 'k'
ax.XColor = 'k'
ax.Layer = 'bottom'
ax.LineWidth = 0.25
ax.XGrid = 'on'
ax.YGrid = 'on'
ax.GridLineStyle = '-'
ax.GridColor = 'k'
ax.GridAlpha = 1
# xticks([-0.5:0.5:7])
# yticks([-0.001 - 0.0005 0 0.0005 0.001])

subplot(3, 1, 3)
tauv = errorbar(Stat_sum(:, 2), Stat_sum(: , 17), Stat_sum(: , 18), 'horizontal', 'o', 'MarkerSize', 8, ...
                'MarkerEdgeColor', 'k', 'MarkerFaceColor', [0.4 0.4 0.4], 'CapSize', 12, 'LineWidth', 0.5, 'Color', 'k')
set(gca, 'FontName', 'Times New Roman', 'FontSize', 11, 'Color', 'k')
# axis([-0.5 7 - 0.001 0.001])
xlabel('\fontname{Times New Roman}\itx\rm [m]')
# x-axis label
ylabel('\itu''v''\rm [m^2/s^2]')
# y-axis label
ax = gca
ax.Color = 'w'
ax.YColor = 'k'
ax.XColor = 'k'
ax.Layer = 'bottom'
ax.LineWidth = 0.25
ax.XGrid = 'on'
ax.YGrid = 'on'
ax.GridLineStyle = '-'
ax.GridColor = 'k'
ax.GridAlpha = 1
# xticks([-0.5:0.5:7])
# yticks([-0.001 - 0.0005 0 0.0005 0.001])

sgt = sgtitle(['\fontname{Times New Roman}TKE and RS profiles at (\ity\rm, \itz\rm) = (' num2str(pos(2)) ...
               ' m, ' num2str(pos(3)) ' m)'])
sgt.FontSize = 11
#print(sprintf('Velocity_prof.png'), '-dpng', '-r600')
export_fig 'TKE_stress_LP' - jpg - m5
#saveas(gcf, 'TKE_stress_LP', 'jpg')

##
close all
