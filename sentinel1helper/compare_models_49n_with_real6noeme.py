import numpy as np
import pandas as pd
from matplotlib import pyplot as plt



plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['legend.title_fontsize'] = 14

bins = 40
exam_param = 'volume_change'
exam_param_title = 'Volume Change [$m^3$]'
xlim_param = [-25000, -9000]
image_id2 = exam_param + '49nreal6' + '.png'

legend_title02 = 'Model Generation'

stats_folder = '/home/hog/projects/msc_grond/volume_opti/'

st_mdl2 = pd.read_csv(stats_folder + 'export_' + 'roenne_real6_ensemble'+'.tab', sep='\s+')
nd_mdl2 = pd.read_csv(stats_folder + 'export_' + '00049_n_ensemble'+'.tab', sep='\s+')


##############################################################################################################################


plt.figure(figsize=[16,9])
plt.hist(st_mdl2[exam_param].values, bins=bins, density=True, histtype='step', color='navy', alpha=0.9)
plt.hist(st_mdl2[exam_param].values, bins=bins, density=True, color='mediumblue', alpha=0.9, label='Roenne Real6')
plt.hist(nd_mdl2[exam_param].values, bins=bins, density=True, histtype='step', color='deeppink', alpha=0.9)
plt.hist(nd_mdl2[exam_param].values, bins=bins, density=True, color='cornflowerblue', alpha=0.5, label='00049n')

#plt.axvline(st_mdl2.loc[0][exam_param], ymin=0, ymax=max(st_mdl2[exam_param]), color='navy', label='Best Model Wide Ranges')
plt.axvline(st_mdl2.loc[0][exam_param], ymin=0, ymax=1, color='navy', label='Best Model Roenne Real6')

#plt.axvline(nd_mdl2.loc[0][exam_param], ymin=0, ymax=max(nd_mdl2[exam_param]), color='deeppink', label='Best Model Narrow Ranges')
plt.axvline(nd_mdl2.loc[0][exam_param], ymin=0, ymax=1, color='deeppink', label='Best Model 00049n')

bestr = "< {0:.0f} $m^3$".format(nd_mdl2.loc[0][exam_param])
plt.text(nd_mdl2.loc[0][exam_param]+5, 0.0002, bestr, color='deeppink', fontweight='bold', fontsize=16)
bestl = "{0:.0f} $m^3$ >".format(st_mdl2.loc[0][exam_param])
plt.text(st_mdl2.loc[0][exam_param]-10200, 0.0002, bestl, color='navy', fontweight='bold', fontsize=16)
#plt.xlim(xlim_param)


plt.xlabel(exam_param_title, fontsize=28, fontweight='bold')
plt.ylabel('PDF', fontsize=28, fontweight='bold')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

legend_properties = {'weight':'bold'}
plt.legend(fontsize = 14, title_fontproperties={'weight':'bold'}, title=legend_title02)
plt.savefig(image_id2)


plt.figure()
plt.hist(st_mdl2[exam_param].values, bins=bins, density=True, color='mediumblue', alpha=0.9, label='Roenne Real6')






print('happy day')

plt.show()