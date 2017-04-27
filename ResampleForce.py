# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 17:20:54 2017

@author: boris
"""
import os
import numpy as np
import mne

resample = False

sbj_types={'sb1':'dm','sb2':'dm','sb3':'dm','sb4':'dm','sb5':'dm','sb6':'bv','sb7':'bv','sb8':'bv',
           'sb9':'bv','sb10':'bv','sb11':'bv','sb12':'bv','sb15':'dm','sb16':'dm','sb17':'dm',
           'sb18':'dm','sb19':'dm'}


for s in sbj_types.keys():
    if s == 'sb12':
        nBlock = 5
    else:
        nBlock = 4
    if sbj_types[s] == 'dm':
        sfreqEMG = 1024
    if sbj_types[s] == 'bv':
        sfreqEMG = 2500
        
    for run in xrange(nBlock):
        megDir = './' + s +  '/MEG/' + str(run+1) + '/'
        os.chdir(megDir)
        meg = mne.io.read_raw_bti('c,rfDC',preload=True)
        eventsMeg = mne.find_events(meg)
        meg.pick_channels(['EXT 001','EXT 002'])
        print('resampling...')
        force, eventsForce = meg.resample(sfreqEMG,events=eventsMeg)
        print('Done!')
        forceFname = s + 'b' + str(run+1) + 'ResampledForce_raw.fif'
        eventNames = s + 'b' + str(run+1) + 'ResampledEvents'
#        print(forceFname)
#        print(eventNames)
        force.save(forceFname)
        np.save(eventNames)

        os.chdir('./../../../')