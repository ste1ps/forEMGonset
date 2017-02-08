# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 16:55:42 2016

@author: boris
"""

def tkeo(array):
    import numpy as np
    if len(array.shape)>1:
        print "only 1D vectors are accepted"
        return np.zeros(array.shape)
    else:
        tmp = np.zeros(array.shape)
        tmp[1:-1] = array[1:-1]**2 -  (array[:-2]*array[2:])
        tmp[0]=tmp[1]
        tmp[-1]=tmp[-2]
        return tmp


def findTimes(timeValue, timeSerie):
    import numpy as np
    return np.abs(timeSerie-timeValue).argmin()

def findT0(t):
    '''
    returns the position of the closest value to 0
    For compatibility reasons, will be delete soon
    '''
    findTimes(0,t)
#    import numpy as np
#    return np.abs(t).argmin()

def hpFilter(data,n=3,sf=2500,cutoff=10):
    from numpy import zeros
    import scipy.signal as sg
    Wn = 2.*cutoff/sf
    b,a = sg.butter(n,Wn,"highpass")
    out = zeros(data.shape)
    out = sg.lfilter(b,a,data)
    return out 
            

def lpFilter(data,n=3,sf=1024,cutoff=150):
    from numpy import zeros
    import scipy.signal as sg
    Wn = 2.*cutoff/sf
    b,a = sg.butter(n,Wn,"lowpass")
    out = zeros(data.shape)
    out = sg.lfilter(b,a,data)
    return out

    
def integratedProfile(data,times):
    '''
    returns the integrated profile, defined as the difference between the 
    empirical cimulative sum of a dataset, and its uniform equivalent 
    (straigth line)
    '''
    import numpy as np
    cs = np.abs(data).cumsum()
    a = cs[-1]/(times[-1]-times[0])
    l = a*times
    d = cs - l
    return d    
    
def getOnsetIntegratedProfile(data,times):
    '''
    From the integrated profile of a signal, return the position of min 
    and max, supposed to correspond to the onset and offset of activity
    '''
    import numpy as np
    ip = integratedProfile(data,times)
#    onset = np.argrelmin(ip)
#    offset = np.argrelmax(ip)
    onset = np.argmin(ip)
    offset = np.argmax(ip)
    return onset,offset

def getGlobalVariance(epochs, times, tmin=None, tmax=None, useTkeo=True):
    import numpy as np
    mBl = []
    stBl =[]
    if tmin == None:
        tmin = 0
    if tmax == None:
        tmax = findTimes(0,times)
    
#    t0 = findT0(times)
    nChan = epochs._data.shape[1]
    nEpochs = epochs._data.shape[0]
    for chan in xrange(nChan):
        if useTkeo:
            tkBl = np.zeros((nEpochs,nChan,tmax-tmin))
            for e in xrange(nEpochs):
                tkBl[e,chan,:] = tkeo(epochs._data[e,chan,tmin:tmax])
            mBl.append(tkBl[:,chan,:].mean())
            stBl.append(tkBl[:,chan,:].std())
        else:
            mBl.append(epochs._data[:,chan,tmin:tmax].mean())
            stBl.append(epochs._data[:,chan,tmin:tmax].std())
            
    return mBl,stBl


def getOnsetVariance(data,times,th=3,mBl=None,stBl = None, useDerivative=False):
    import numpy as np
    t0 = findTimes(0,times)
    data = np.squeeze(data)
    if mBl == None:
        mBl = data[:t0].mean()
    if stBl == None:
        stBl = data[:t0].std()
    tmp = np.where(data[t0:]>(mBl+th*stBl))
    if len(tmp[0]) > 0:
        onset = tmp[0][0] + t0
    else:
        onset = None
    if onset != None:
        tmp = np.where(data[onset:]<(mBl+th*stBl))
        if len(tmp[0]) > 0:
            offset = tmp[0][0] + onset
        else:
            offset = None
    
    
        peak = data.argmax()
        if ( (offset < onset) | (offset < peak) ):
            useDerivative = True
        
        if useDerivative:
            dif = data[1:] - data[:-1]
            mBlDif = dif[:t0].mean()
            stBlDif = dif[:t0].std()
            tmp = np.where(dif[peak:]<(mBlDif - th*stBlDif))
            if len(tmp[0]) > 0:
                offset = tmp[0][-1] + peak
            else:
                offset = None
    else:
        offset = None                
    return onset,offset
