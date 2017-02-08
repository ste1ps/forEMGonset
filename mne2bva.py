# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 07:44:47 2016

@author: boris
"""
import os
import numpy as np
import codecs


def writevmrk(fname,events,eventType):
    
    vmrkFilename = fname + '.vmrk'
    f = open(vmrkFilename,'w')
    f.write('Brain Vision Data Exchange Marker File, Version 2.1\n')
    f.write('; Create from mne2bva.py\n')
    f.write('; The channel numbers are related to the channels in the exported file.')
    f.write('\n')
    
    f.write('[Common Infos]\n')
    f.write('Codepage=UTF-8\n')
#    fname = "E:\\AutoDetectTest\\raw\\BVA\\S10"    
    f.write('DataFile='+fname+'.eeg\n')
    f.write('\n')
    
    f.write('[Marker Infos]\n')
    for e in xrange(events.shape[0]):
        if events[e,2] in eventType.keys():
            eType = eventType[events[e,2]]
        else:
            eType = 'Comments'
        if events[e,1] == 768:##### Workaround Gab
            events[e,1] = 0
        else:
            pass
        f.write('Mk'+str(e+1)+'='+ eType +','+str(events[e,2])+\
        ','+ str(events[e,0])+',1,' + str(events[e,1]) +'\n')
    f.write('\n')
    

    f.write('[Marker User Infos]\n')
    f.write('\n')
    
    f.close()
    
    


def writevhdr(fname, raw):
    vhdrFilename = fname + '.vhdr'
    with codecs.open(vhdrFilename, "w", encoding="utf-8") as f:
        #muv = u'µ'   
        f.write('Brain Vision Data Exchange Header File Version 2.0\n')
        f.write('; Create from mne2bva.py\n \n')
        f.write('\n')            
        f.write('[Common Infos]\n')
        f.write('Codepage=UTF-8\n')
        f.write('DataFile='+fname.split('/')[-1]+'.eeg\n')
        f.write('MarkerFile='+fname.split('/')[-1]+'.vmrk\n')
        f.write('DataFormat=BINARY\n')
        f.write('; Data orientation: VECTORIZED=ch1,pt1, ch1,pt2..., MULTIPLEXED=ch1,pt1, ch2,pt1 ...\n')
        f.write('DataOrientation=VECTORIZED\n')
        f.write('DataType=TIMEDOMAIN\n')
        f.write('NumberOfChannels='+str(raw.info['nchan'])+'\n')
        f.write('DataPoints='+str(raw._data.shape[1])+'\n')
        f.write('SamplingInterval='+ str(1000000/raw.info['sfreq']) + '\n')
        f.write('\n')    
        
        f.write('[Binary Infos]\n')
        f.write('BinaryFormat=IEEE_FLOAT_32\n')
        f.write('\n')
        
        f.write('[Channel Infos]\n')
        f.write('; Each entry: Ch<Channel number>=<Name>,<Reference channel name>,\n \
                 ; <Resolution in "Unit">,<Unit>, Future extensions... \n \
                 ; Fields are delimited by commas, some fields might be omitted (empty). \n \
                 ; Commas in channel names are coded as "\1".\n')
        for c in xrange(raw.info['nchan']):
            f.write('ch'+str(c+1)+'='+raw.ch_names[c]+',,,'+'V\n')#a changer
        f.write('\n')
    
        f.write('[Coordinates]\n')    
        f.write('; Each entry: Ch<Channel number>=<Radius>,<Theta>,<Phi>\n')
        for c in xrange(raw.info['nchan']):
            f.write('ch'+str(c+1)+'=0,0,0\n') #FIXME!!
        f.write('\n')
        
        f.close()
    
    

def mne2bva(fname,raw,events,eventType):
    dataFilename = fname + '.eeg'
    
    
    #vhdrFilename = fname + '.vhdr'
    
    # Save eeg file
    f = open(dataFilename,'wb')
    raw32 = raw._data.astype(np.float32)
    f.write(raw32)
    del(raw32)
    f.close()
    
    writevhdr(fname,raw)
    writevmrk(fname,events,eventType)    

