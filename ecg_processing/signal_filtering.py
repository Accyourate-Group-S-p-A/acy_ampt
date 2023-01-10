import numpy as np
import math
from scipy import signal

def movingAverageMean(data, size):

    newData = []
    for i in data:
        newData.append(i)
    
    i = 0
    moving_averages = []

    size=25

    while i < len(newData)-size+1:
        this_window = data[i: i+size]
        window_average = np.sum(this_window) / size

        val = newData[i]-window_average
        moving_averages.append(val)

        i += 1

    # moving_averages = np.nan_to_num(moving_averages, nan=0.0)
    return moving_averages


def movingAverageMeanPamTompkins(data, fs):
    newData = []
    for i in data:
        newData.append(i)

    size = int(0.15*fs)  # PREV 150
    #size = 150
    i = 0
    moving_averages = []
    window_average_list = []

    while i < len(newData)-size+1:
        this_window = data[i: i+size]
        window_average = np.sum(this_window) / size
        window_average_list.append(window_average)

        i += 1

    # moving_averages = np.nan_to_num(moving_averages, nan=0.0)

    return window_average_list


def bandpassFilt(sample, n, samplingRate, freq_1, freq_2):
    sampletoFilt = []

    for i in sample:
        sampletoFilt.append(i)

    n = int(n / 4)

    a = math.cos(math.pi*(freq_1+freq_2)/samplingRate) / \
        math.cos(math.pi*(freq_1-freq_2)/samplingRate)
    a2 = a * a

    b = math.tan(math.pi * (freq_1 - freq_2) / samplingRate)
    b2 = b * b

    A = []
    d1 = []
    d2 = []
    d3 = []
    d4 = []

    for i in range(0, n+1):
        A.append(0.0)
        d1.append(0.0)
        d2.append(0.0)
        d3.append(0.0)
        d4.append(0.0)

    for i in range(0, n+1):

        r = math.sin(math.pi * (2.0*(i) + 1.0) / (4.0 * (n)))
        s = b2 + 2.0*b*r + 1.0

        A[i] = (b2 / s)

        d1[i] = (4.0 * a * (1.0 + b*r) / s)

        d2[i] = (2.0 * (b2 - 2.0*a2 - 1.0) / s)
        d3[i] = 4.0 * a * (1.0 - b*r) / s
        d4[i] = (-(b2 - 2.0*b*r + 1.0) / s)

    w0 = []
    w1 = []
    w2 = []
    w3 = []
    w4 = []

    for i in range(0, n+1):
        w0.append(0.0)
        w1.append(0.0)
        w2.append(0.0)
        w3.append(0.0)
        w4.append(0.0)

    for x in range(0, len(sampletoFilt)-1):
        for i in range(0, n+1):

            w0[i] = (d1[i]*w1[i] + d2[i]*w2[i] + d3[i] *
                     w3[i] + d4[i]*w4[i] + sampletoFilt[x])

            sampletoFilt[x] = A[i] * (w0[i] - 2.0*w2[i] + w4[i])

            w4[i] = w3[i]
            w3[i] = w2[i]
            w2[i] = w1[i]
            w1[i] = w0[i]

    return sampletoFilt

def sliceForIndex(signal):

    data = []
    resultData = []
    resultdata = []

    for i in signal:
        data.append(i)

    i = 1
    while i <= len(signal):
        if i % 2500 == 0:
            movinaveragedata = movingAverageMean(data[i-2500:i], 250)
            resultdata = artifactRemoval(movinaveragedata)

            for x in resultdata:
                resultData.append(x)
        i += 1

    return resultData


def derivateStep(data):
    derivate = []

    for i in range(1, len(data)-2):
        derivate.append(
            (1/8*360) * ((-data[i-2]-2*data[i-1])+2*data[i+1]+data[i+2]))

    return derivate


def newfilter(ECG, fs):
    if type(ECG) == list or type(ECG) is np.ndarray:
        ECG = np.array(ECG)             
        
    #Initialize
    RRAVERAGE1 = []
    RRAVERAGE2 = []
    IWF_signal_peaks = []
    IWF_noise_peaks = []
    noise_peaks = []
    ECG_bp_peaks = np.array([])
    ECG_bp_signal_peaks = []
    ECG_bp_noise_peaks = []
    final_R_locs = []
    T_wave_found = 0      
    
    #LOW PASS FILTERING
    #Transfer function: H(z)=(1-z^-6)^2/(1-z^-1)^2
    a = np.array([1, -2, 1])
    b = np.array([1, 0, 0, 0, 0, 0, -2, 0, 0, 0, 0, 0, 1])   
        
    impulse = np.repeat(0., len(b)); impulse[0] = 1.    
    impulse_response = signal.lfilter(b,a,impulse)
    
    #convolve ECG signal with impulse response
    ECG_lp = np.convolve(impulse_response, ECG)
    ECG_lp = ECG_lp / (max(abs(ECG_lp)))
    delay = 12 #full convolution
    
    #HIGH PASS FILTERING
    #Transfer function: H(z)=(-1+32z^-16+z^-32)/(1+z^-1)
    a = np.array([1, -1])           
    b = np.array([-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 32, -32, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, -1])
                  
    impulse = np.repeat(0., len(b)); impulse[0] = 1.    
    impulse_response = signal.lfilter(b,a,impulse)
    
    ECG_lp_hp = np.convolve(impulse_response, ECG_lp)
    ECG_lp_hp = ECG_lp_hp/(max(abs(ECG_lp_hp)))
    delay = delay + 32 
    
    #BAND PASS FILTER 
    nyq = fs / 2        
    lowCut = 5 / nyq  #cut off frequencies are normalized from 0 to 1, where 1 is the Nyquist frequency
    highCut = 15 / nyq
    order = 5
    b,a = signal.butter(order, [lowCut, highCut], btype = 'bandpass')
    ECG_bp = signal.lfilter(b, a, ECG_lp_hp)
    
    #DIFFERENTIATION
    #Transfer function: H(z)=(1/8T)(-z^-2-2z^-1+2z^1+z^2)
    T = 1/fs
    b = np.array([-1, -2, 0, 2, 1]) * (1 / (8 * T))
    a = 1
    #Note impulse response of the filter with a = [1] is b
    ECG_deriv = np.convolve(ECG_bp, b)
    delay = delay + 4 
    
    #SQUARING FUNCTION
    ECG_squared = ECG_deriv ** 2
    
    #MOVING INTEGRATION WAVEFORM 
    N = int(np.ceil(0.150 * fs)) 
    ECG_movavg = np.convolve(ECG_squared,(1 / N) * np.ones((1, N))[0])
        
    return ECG_movavg