import numpy as np
from scipy.signal import find_peaks

def Count(data):

    timeStamp = []
    x = []
    y = []
    z = []
    elapsedTime = []

    if type(data) == list:
        for i in range(len(data)):
            timeStamp.append(data[i][0])
            x.append(data[i][1])
            y.append(data[i][2])
            z.append(data[i][3])
            elapsedTime.append(data[i][4])
        peaks, _ = find_peaks(y)

        peakTimeStamp = []

        for i in range(len(peaks)):
            peakTimeStamp.append(timeStamp[peaks[i]])
    
    return peakTimeStamp