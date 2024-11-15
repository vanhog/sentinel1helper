import numpy as np
import pandas as pd
from matplotlib import pyplot as plt



plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['legend.title_fontsize'] = 14

bins = 40
exam_param = 'volume_change'
exam_param_title = 'Volume Change [$m^3$]'
xlim_param = [-25000, -9000]
image_id1 = exam_param + '48w48n' + '.png'
image_id2 = exam_param + '49w49n' + '.png'
image_id3 = exam_param + '48w49w' + '.png'

legend_title01 = 'Volume Change Modelled from Whole Time Series'
legend_title02 = 'Volume Change Modelled from 6-Day-Cycle Period'
legend_title03 = 'Volume Change Modelled with Wide Ranges'

stats_folder = '/home/hog/projects/msc_grond/volume_opti/'
st_mdl = pd.read_csv(stats_folder + 'export_' + '00048_w_ensemble'+'.tab', sep='\s+')
nd_mdl = pd.read_csv(stats_folder + 'export_' + '00048_n_ensemble'+'.tab', sep='\s+')

st_mdl2 = pd.read_csv(stats_folder + 'export_' + '00049_w_ensemble'+'.tab', sep='\s+')
nd_mdl2 = pd.read_csv(stats_folder + 'export_' + '00049_n_ensemble'+'.tab', sep='\s+')


##############################################################################################################################
plt.figure(figsize=[16,9])
plt.hist(st_mdl[exam_param].values, bins=bins, density=True, histtype='step', color='deepskyblue', alpha=0.9)
plt.hist(st_mdl[exam_param].values, bins=bins, density=True, color='seagreen', alpha=0.9, label='Wide Modelling Ranges')
plt.hist(nd_mdl[exam_param].values, bins=bins, density=True, histtype='step', color='darkorange', alpha=0.9)
plt.hist(nd_mdl[exam_param].values, bins=bins, density=True, color='lime', alpha=0.65, label='Narrow Modelling Ranges')
plt.axvline(st_mdl.loc[0][exam_param], ymin=0, ymax=1, color='deepskyblue', label='Best Model Wide Ranges')
print(st_mdl.loc[0][exam_param])
#plt.axvline(nd_mdl.loc[0][exam_param], ymin=0, ymax=max(nd_mdl[exam_param]), color='darkorange', label='Best Model Narrow Ranges')

plt.axvline(nd_mdl.loc[0][exam_param], ymin=0, ymax=1, color='darkorange', label='Best Model Narrow Ranges')
bestr = "< {0:.0f} $m^3$".format(nd_mdl.loc[0][exam_param])
plt.text(nd_mdl.loc[0][exam_param]+5, 0.00054, bestr, color='orangered', fontweight='bold', fontsize=16)
bestl = "< {0:.0f} $m^3$".format(st_mdl.loc[0][exam_param])
plt.text(st_mdl.loc[0][exam_param]+5, 0.00050, bestl, color='deepskyblue', fontweight='bold', fontsize=16)
plt.xlim(xlim_param)

plt.xlabel(exam_param_title, fontsize=28, fontweight='bold')
plt.ylabel('PDF', fontsize=28, fontweight='bold')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

legend_properties = {'weight':'bold'}
plt.legend(fontsize = 14, title_fontproperties={'weight':'bold'}, title=legend_title01)
plt.savefig(image_id1)



#####################################################################
#22222222222222222222222222222222222222222222222222222222222222222222
plt.figure(figsize=[16,9])
plt.hist(st_mdl2[exam_param].values, bins=bins, density=True, histtype='step', color='navy', alpha=0.9)
plt.hist(st_mdl2[exam_param].values, bins=bins, density=True, color='mediumblue', alpha=0.9, label='Wide Modelling Ranges')
plt.hist(nd_mdl2[exam_param].values, bins=bins, density=True, histtype='step', color='deeppink', alpha=0.9)
plt.hist(nd_mdl2[exam_param].values, bins=bins, density=True, color='cornflowerblue', alpha=0.5, label='Narrow Modelling Ranges')

#plt.axvline(st_mdl2.loc[0][exam_param], ymin=0, ymax=max(st_mdl2[exam_param]), color='navy', label='Best Model Wide Ranges')
plt.axvline(st_mdl2.loc[0][exam_param], ymin=0, ymax=1, color='navy', label='Best Model Wide Ranges')

#plt.axvline(nd_mdl2.loc[0][exam_param], ymin=0, ymax=max(nd_mdl2[exam_param]), color='deeppink', label='Best Model Narrow Ranges')
plt.axvline(nd_mdl2.loc[0][exam_param], ymin=0, ymax=1, color='deeppink', label='Best Model Narrow Ranges')

bestr = "< {0:.0f} $m^3$".format(nd_mdl2.loc[0][exam_param])
plt.text(nd_mdl2.loc[0][exam_param]+100, 0.000595, bestr, color='deeppink', fontweight='bold', fontsize=16)
bestl = "{0:.0f} $m^3$ >".format(st_mdl2.loc[0][exam_param])
plt.text(st_mdl2.loc[0][exam_param]-2000, 0.000595, bestl, color='navy', fontweight='bold', fontsize=16)
plt.xlim(xlim_param)


plt.xlabel(exam_param_title, fontsize=28, fontweight='bold')
plt.ylabel('PDF', fontsize=28, fontweight='bold')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

legend_properties = {'weight':'bold'}
plt.legend(fontsize = 14, title_fontproperties={'weight':'bold'}, title=legend_title02)
plt.savefig(image_id2)






###################################################################
plt.figure(figsize=[16,9])
plt.hist(st_mdl[exam_param].values, bins=bins, density=True, histtype='step', color='deepskyblue', alpha=0.9)
plt.hist(st_mdl[exam_param].values, bins=bins, density=True, color='seagreen', alpha=0.9, label='Whole Time Series')
#plt.axvline(st_mdl.loc[0][exam_param], ymin=0, ymax=max(st_mdl[exam_param]), color='deepskyblue', label='Best Model Whole Time Series')
plt.axvline(st_mdl.loc[0][exam_param], ymin=0, ymax=1, color='deepskyblue', label='Best Model Whole Time Series')

bestr = "< {0:.0f} $m^3$".format(st_mdl.loc[0][exam_param])
plt.text(st_mdl.loc[0][exam_param]+5, 0.0006, bestr, color='deepskyblue', fontweight='bold', fontsize=16)


plt.hist(st_mdl2[exam_param].values, bins=bins, density=True, histtype='step', color='navy', alpha=0.9)
plt.hist(st_mdl2[exam_param].values, bins=bins, density=True, color='mediumblue', alpha=0.5, label='6 Day Cycling')
#plt.axvline(st_mdl2.loc[0][exam_param], ymin=0, ymax=max(st_mdl2[exam_param]), color='navy', label='Best Model 6-Day-Cycling')
plt.axvline(st_mdl2.loc[0][exam_param], ymin=0, ymax=1, color='navy', label='Best Model 6-Day-Cycling')

bestl = "< {0:.0f} $m^3$".format(st_mdl2.loc[0][exam_param])
plt.text(st_mdl2.loc[0][exam_param]+5, 0.0006, bestl, color='navy', fontweight='bold', fontsize=16)

plt.xlim(xlim_param)

plt.xlabel(exam_param_title, fontsize=28, fontweight='bold')
plt.ylabel('PDF', fontsize=28, fontweight='bold')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

legend_properties = {'weight':'bold'}
plt.legend(fontsize = 14, title_fontproperties={'weight':'bold'}, title=legend_title03)
plt.savefig(image_id3)





print('happy day')

plt.show()