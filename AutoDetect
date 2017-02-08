# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 18:45:55 2016

@author: boris
"""

import sys
import os
sys.path.insert(0, 'F:/MEG_data/script/')
import mne
import numpy as np
import pylab as plt
import emgTools as emg
from mne2bva import mne2bva



def processTrial(n,epochs):
#    th = np.arange(2,4,.01)
    tmp = epochs._data[n,:2,:]
    t=epochs.times
#    tk1 = emg.tkeo(tmp[0,:])
#    tk2 = emg.tkeo(tmp[1,:])
#    tmp1 = emg.lpFilter(tmp[0,:],n=3,sf=epochs.info['sfreq'],cutoff=100)
#    tmp2 = emg.lpFilter(tmp[1,:],n=3,sf=epochs.info['sfreq'],cutoff=100)
    on1Var = []
    on2Var = []
    ip1 = emg.integratedProfile(tmp[0,1024:],t[1024:])
    ip2 = emg.integratedProfile(tmp[1,1024:],t[1024:])
    onVar,OffVar = emg.getOnsetVariance(np.abs(tmp[0,:]),t,th=4,\
        mBl=mBl[0],stBl=stBl[0])
    plt.subplot(2,2,1)
    plt.plot(t,tmp[0,:],'b')
    plt.ylim((tmp.min(),tmp.max()))
    if onVar !=None:
        on1,off1 = emg.getOnsetIntegratedProfile(tmp[0,1024:],t[1024:])
        plt.vlines(t[on1+1024],tmp.min(),tmp.max())

    plt.subplot(2,2,2)
    plt.plot(t[1024:],ip1,'b')
    if onVar !=None:
        plt.vlines(t[on1+1024],ip1.min(),ip1.max())
    onVar,OffVar = emg.getOnsetVariance(np.abs(tmp[1,:]),t,th=4,\
        mBl=mBl[1],stBl=stBl[1])
    plt.subplot(2,2,3)
    plt.plot(t,tmp[1,:],'r')
    plt.ylim((tmp.min(),tmp.max()))
    if onVar !=None:
        on2,off2 = emg.getOnsetIntegratedProfile(tmp[1,1024:],t[1024:])
        plt.vlines(t[on2+1024],tmp.min(),tmp.max())
    plt.subplot(2,2,4)
    plt.plot(t[1024:],ip2,'r')
    if onVar !=None:
        plt.vlines(t[on2+1024],ip2.min(),ip2.max())


pathBDF = u'F:/MEG_data/data/'
pathBVA = u'F:/MEG_data/output/'

list_dir = os.listdir(pathBDF)

for f in list_dir:
    if f[-4:] == 'vhdr':
        nameSubj = f.split('.')[0]
        nameBDF = f
        Trigger = [11,21,31,41]
        #65314
        fname = os.path.join(pathBDF,nameBDF)
    #    raw = mne.io.read_raw_edf(fname,preload=True, verbose=True)
        raw = mne.io.read_raw_brainvision(fname,montage=None, eog=('HEOG_m', 'HEOG_p', 'VEOG_m', 'VEOG_p'),misc='auto', scale=1.0,preload=True, verbose=True)
        raw
        mne.set_bipolar_reference(raw,anode=['EMGg_m','EMGd_m'],\
        cathode=['EMGg_p','EMGd_p'],ch_name=['EMG_L','EMG_R'],\
        copy=False)
#        events = mne.find_events(raw, stim_channel = 'STI 014', min_duration=0.002, mask=2**24-64)
        events = mne.find_events(raw)
        raw.pick_channels(['EMG_L','EMG_R'])
        
        raw.set_channel_types({
            'EMG_L':'emg',
            'EMG_R':'emg',
    #        'EXG5' :'eog',
    #        'EXG6' :'eog',
    #        'Erg1' :'misc',
    #        'Erg2': 'misc',
#             'STI 014': 'stim'
             })
             
#        raw.apply_function(emg.hpFilter(data,n=3,sf=2500,cutoff=10), picks=[0,1])
        raw.apply_function(emg.hpFilter)
        
        epochs = mne.Epochs(raw,events,event_id=Trigger,tmin=-1.3, \
            tmax=1.3,baseline=(None,0))
        epochs.load_data()
        
        nameBVA = pathBVA+nameSubj
        if os.path.isfile(nameBVA+'.vhdr'):
            os.remove(nameBVA+'.vhdr')
            print 'File removed !!'
        
        # 101,202 EMG onsets IP
        # 110,220 EMG onstes variance
        
        mBl,stBl = emg.getGlobalVariance(epochs,epochs.times,useTkeo=False)
        onset=[]
        chan = []
        code = []
        
        print('Detecting onset ...')
        
        for e in xrange(epochs._data.shape[0]):
            for c in xrange(epochs.info['nchan']):
        #        current = np.abs(emg.tkeo(epochs._data[e,c,:]))
        #        current = emg.lpFilter(current,n=6,sf=epochs.info['sfreq'],cutoff=50)
                current = np.abs(epochs._data[e,c,:])
                if epochs.ch_names[c][:3] == 'EMG':
                    onVar,OffVar = emg.getOnsetVariance(current,epochs.times,th=4,\
                    mBl=mBl[c],stBl=stBl[c])
                    if onVar != None:
                        code.append(101*(c+1))
                        onIp,offIp = emg.getOnsetIntegratedProfile(current[1024:],\
                        epochs.times[1024:])
        #                emg.getOnsetIntegratedProfile(tmp[0,1024:],t[1024:])
                        onset.append(onIp+epochs.events[e,0])  #FIXME !!!
                        chan.append(c+1)
        
                if epochs.ch_names[c][:3] == 'Erg':
                    onVar,OffVar = emg.getOnsetVariance(current,epochs.times,th=8,\
                    mBl=mBl[c],stBl=stBl[c])
                    if onVar != None:
                        onVar,OffVar = emg.getOnsetVariance(current,epochs.times,th=4,\
                        mBl=mBl[c],stBl=stBl[c])
                        if onVar != None:
                            onset.append(onVar+epochs.events[e,0]-1024) #FIXME !!!
                            chan.append(c+1)
                            code.append(110*(c+1))
        
        
        newEvent = np.vstack((onset,chan,code))
        newEvent = np.rollaxis(newEvent,1)
        #eventIp = np.vstack((onsetIp,chanIp,codeIp))
        #eventIp = np.rollaxis(eventIp,1)
        
        events = np.vstack((events,newEvent))
        sortedEvents = np.argsort(events[:,0])
        events =  events[sortedEvents,:]
        
        
        raw._data[2:4,:] = raw._data[2:4,:]/100
        
        
        print('Done !')
        # 101,202 EMG onsets IP
        # 110,220 EMG onstes variance
        
    #    eventColor = {100:'r',200:'r',101:'g',202:'g',330:'y',440:'y'}
    #    eventColor.update(dict((el,'b') for el in Trigger))
    #    
    #    eventType = {868:'Response',968:'Response',101:'EMG',202:'EMG',330:'Force',\
    #                440:'Force'}
        eventType = (dict((el,'Stimulus') for el in Trigger))
        
        mne2bva(nameBVA, raw,events,eventType)
        print("Saved for " + f)
