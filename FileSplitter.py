import pyaudio
import sys
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.io.wavfile as wav
import subprocess
# install lame
# install bleeding edge scipy (needs new cython)
def openMp3(fname):
    print fname
    oname = 'temp.wav'
    cmd = ['lame','--decode',fname, oname]
    subprocess.call(cmd)
    data = wav.read(oname)
    return data

def plotSplitting(data,wndw=0.1,threshold=10000):
    if len(data[1].shape) == 1:
        signal = data[1]
    else:
        signal = data[1][:,0]
    sampleRate = float(data[0])
    length_s = len(signal)/sampleRate
    sample_period = 1.0/sampleRate
    wndw = int(wndw*sampleRate)
    print "length in seconds {0}s".format(length_s)
    t = np.arange(0,length_s,sample_period)
    vals = [np.abs(float(np.max(signal[s*wndw:s*wndw+wndw]))-float(np.min(signal[s*wndw:s*wndw+wndw]))) for s in range(0,len(signal)/int(wndw))]
    tvals = [float(s*wndw)/sampleRate for s in range(0,len(signal)/int(wndw))]
    plt.plot(t,signal)
    plt.title('bird call analysis')
    plt.xlabel('signal value')
    plt.ylabel('time s.')
    plt.grid()
    for t,v in zip(tvals,vals):
        if( v < threshold ):
            plt.axvline(t, color='green', lw=2, alpha=0.5)
        else:
            plt.axvline(t, color='red', lw=2, alpha=0.5)
    plt.show()

def findIntervals(data,wndw=0.1,threshold=10000,pad=3):
    if len(data[1].shape) == 1:
        signal = data[1]
    else:
        signal = data[1][:,0]
    sampleRate = float(data[0])
    wndw = int(wndw*sampleRate)
    vals = [np.abs(float(np.max(signal[s*wndw:s*wndw+wndw]))-float(np.min(signal[s*wndw:s*wndw+wndw]))) for s in range(0,len(signal)/int(wndw))]
    idxs =  np.where(np.array(vals) > threshold )[0]
    #there are no useful regions
    if( len(idxs) == 0 ):
        return []
    print idxs
    delta = idxs[1:]-idxs[:-1]
    inflect = np.where(np.array(delta)>1)[0]
    #if there are no gaps return the whole region)
    if(len(inflect)==0):
        retval = [(idxs[0]*wndw,idxs[-1]*wndw)]
    retVal = []
    last = idxs[0]
    for split in inflect:
        retVal.append((wndw*(last-pad),wndw*(idxs[split]+pad)))
        last = idxs[split+1]
    retVal.append((wndw*(last-pad),wndw*(idxs[-1]+pad)))
    return retVal

def writeWav(data,rate,fname):
    pass


path = './rawData/Agelaius+phoeniceus/'
count = 0
for fname in os.listdir(path):
    data = openMp3(path+fname)
    plotSplitting(data)
    intervals = findIntervals(data)
    print intervals
    if len(data[1].shape) == 1:
        signal = data[1]
    else:
        signal = data[1][:,0]

    for interval in intervals:
        plt.plot(signal[interval[0]:interval[1]])
        plt.show()
        ofile = 'output{0}.wav'.format(count)
        count+=1
        wav.write(ofile,data[0],signal[interval[0]:interval[1]])
