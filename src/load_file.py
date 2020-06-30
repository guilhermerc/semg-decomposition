#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from scipy.io import loadmat

mat_file = loadmat('samples/LAE_QEO_cut.mat')
# Check LAE_QEO_cut_tree.md for file structure description

emg_struct = mat_file['QEO_cut'][0][0]['EMG'][0][0]
trial_structs = [emg_struct['Trial1'][0][0], emg_struct['Trial2'][0][0]]
time = emg_struct['Time']

print(trial_structs[0]['TA'].shape)
print(trial_structs[0]['GM'].shape)
print(trial_structs[1]['GL'].shape)
print(trial_structs[1]['SO'].shape)
print(time.shape)

print('\n', trial_structs[1]['SO'][60][8000])
