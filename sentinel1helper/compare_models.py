import numpy as np
import pandas as pd
from matplotlib import pyplot as plt



plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['legend.title_fontsize'] = 14

bins = 40
exam_param = 'east_shift'
exam_param_title = 'East Shift [m]'
xlim_param = [-500, 500]

stats_folder = '/home/hog/projects/msc_grond/volume_opti/'
df48w = pd.read_csv(stats_folder + 'export_' + '00048_w_ensemble'+'.tab', sep='\s+')
df48n = pd.read_csv(stats_folder + 'export_' + '00048_n_ensemble'+'.tab', sep='\s+')
print(df48w.head())
print(df48w.columns)
print(df48w.shape)




plt.figure(figsize=[16,9])
plt.hist(df48w[exam_param].values, bins=bins, density=True, histtype='step', color='deepskyblue', alpha=0.9)
plt.hist(df48w[exam_param].values, bins=bins, density=True, color='seagreen', alpha=0.9, label='Wide Modelling Ranges')
plt.hist(df48n[exam_param].values, bins=bins, density=True, histtype='step', color='darkorange', alpha=0.9)

plt.hist(df48n[exam_param].values, bins=bins, density=True, color='lime', alpha=0.65, label='Narrow Modelling Ranges')

plt.xlim(xlim_param)

plt.xlabel(exam_param_title, fontsize=28, fontweight='bold')
plt.ylabel('PDF', fontsize=28, fontweight='bold')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

legend_properties = {'weight':'bold'}
plt.legend(fontsize = 14, title_fontproperties={'weight':'bold'}, title='East Shift Modelled from Whole Time Series')
plt.savefig('eastshift48w48n.png')

df49w = pd.read_csv(stats_folder + 'export_' + '00049_w_ensemble'+'.tab', sep='\s+')

df49n = pd.read_csv(stats_folder + 'export_' + '00049_n_ensemble'+'.tab', sep='\s+')
print(df48w.head())
print(df48w.shape)

#####################################################################
plt.figure(figsize=[16,9])
plt.hist(df49w[exam_param].values, bins=bins, density=True, histtype='step', color='navy', alpha=0.9)
plt.hist(df49w[exam_param].values, bins=bins, density=True, color='mediumblue', alpha=0.9, label='Wide Modelling Ranges')
plt.hist(df49n[exam_param].values, bins=bins, density=True, histtype='step', color='deeppink', alpha=0.9)

plt.hist(df49n[exam_param].values, bins=bins, density=True, color='cornflowerblue', alpha=0.5, label='Narrow Modelling Ranges')

plt.xlim(xlim_param)

plt.xlabel(exam_param_title, fontsize=28, fontweight='bold')
plt.ylabel('PDF', fontsize=28, fontweight='bold')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

legend_properties = {'weight':'bold'}
plt.legend(fontsize = 14, title_fontproperties={'weight':'bold'}, title='East Shift Modelled from 6-Day-Cycle Period')
plt.savefig('eastshift49w49n.png')
###################################################################
plt.figure(figsize=[16,9])
plt.hist(df48w[exam_param].values, bins=bins, density=True, histtype='step', color='deepskyblue', alpha=0.9)
plt.hist(df48w[exam_param].values, bins=bins, density=True, color='seagreen', alpha=0.9, label='Whole Time Series')
plt.hist(df49w[exam_param].values, bins=bins, density=True, histtype='step', color='navy', alpha=0.9)

plt.hist(df49w[exam_param].values, bins=bins, density=True, color='mediumblue', alpha=0.5, label='6 Day Cycling')

plt.xlim(xlim_param)

plt.xlabel(exam_param_title, fontsize=28, fontweight='bold')
plt.ylabel('PDF', fontsize=28, fontweight='bold')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

legend_properties = {'weight':'bold'}
plt.legend(fontsize = 14, title_fontproperties={'weight':'bold'}, title='East Shift Modelled with wide ranges')
plt.savefig('eastshift48w49w.png')





print('happy day')

plt.show()