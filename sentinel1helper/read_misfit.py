#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 12:56:28 2024

@author: sudhaus
"""

import numpy as num
import sys


run_folder = '/home/hog/projects/msc_grond/volume_opti/runs/roenne_real00046_hog.grun'
models = num.fromfile(run_folder + '/harvest/' + 'misfits', dtype='<f8') 

print('happy day')
# nmods = num.shape(models)[0]
# uniqueness = num.shape(num.unique(models))[0]/nmods
# print('Uniqueness of ', run_folder, 'is: \n',uniqueness)