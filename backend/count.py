import numpy as np
from scipy.signal import butter, filtfilt, find_peaks
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def butter_bandpass(low_cut, high_cut, fs, order=5):
    nyquist = 0.5 * fs
    low = low_cut / nyquist
    high = high_cut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, low_cut, high_cut, fs, order=5):
    b,a = butter_bandpass(low_cut, high_cut, fs, order=order)
    y = filtfilt(b, a, data)
    return y


def Count(data, height, distance):

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
        smoothed_y = butter_bandpass_filter(y, 0.5, 10, int(len(y)/(elapsedTime[-1]-elapsedTime[0])))
        smoothed_z = butter_bandpass_filter(z, 0.5, 10, int(len(y)/(elapsedTime[-1]-elapsedTime[0])))

        # plt.plot(elapsedTime, smoothed_y)
        # plt.plot(elapsedTime, smoothed_z)
        # plt.show()

        peaks, _ = find_peaks(smoothed_y, height = height, distance = distance)

        peakTimeStamp = [] 

        if len(peaks) == 0:
            peakTimeStamp = [datetime(1970, 1, 1, 0, 0, 0, 500000)] 
        else:
            for i in range(len(peaks)):
                peakTimeStamp.append(timeStamp[peaks[i]])
    
    return peakTimeStamp