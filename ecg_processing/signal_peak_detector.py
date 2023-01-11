import numpy as np
import time

def diffInt(arr, val=None):
    diff = []

    i = 0
    while i < len(arr)-1:
        if val == None:
            diff.append(arr[i + 1] - arr[i])
            i += 1
        else: 
            diff.append((arr[i + 1] - arr[i])/val)
            i += 1

    return diff

def AMPT(signal, fs):
    """
    Accyourate Modified Pan Tompkins, a modified and faster Pan Tompkins based algorhythm.

    Pan, Jiapu, and Willis J. Tompkins. "A real-time QRS detection algorithm." 
    IEEE transactions on biomedical engineering 3 (1985): 230-236.

    ARGS:
    - signal: filtered signal;
    - fs: sampling frequency;

    RETURNS:
    - signalPeaks: detected peaks excluding the first peak;
    - thrheshold_list: the threshold list detected while analyzing the signal;
    """

    signalPeaks = [0] # Initialize list to store detected peaks

    SPKI = 0.0 # Running average of signal values at peaks
    NPKI = 0.0 # Running average of signal values not at peaks

    thresholdI1 = 0.0 # Initial threshold value
    thresholdI2 = 0.0 # Initial threshold value

    RRMissed = 0 # Number of missed RR intervals
    index = 0

    peaks = []  # Initialize list to store identified peaks in the signal
    thrheshold_list = []  # Initialize list to store threshold values

    for i in range(len(signal)):
        # Identify local maxima (peaks) in the signal
        if i > 0 and i < len(signal)-1:
            if signal[i-1] < signal[i] and signal[i+1] < signal[i]:
                peaks.append(i)

    i = 1
    while i < len(peaks)-2:
        # Check if an RR interval has been missed
        if len(signalPeaks)>2 and RRMissed>0:
            if peaks[i]- signalPeaks[-1]>RRMissed:
                
                RRMissedPrev = RRMissed
                RRMissed = 0.0
                thresholdI2 = 0.25*thresholdI1
                x = peaks.index(signalPeaks[-1])
                y = peaks.index(peaks[i])
                z = x
                while z < y:
                    if z!=0:
                        # Check if peak is above the threshold value and is a local maxima
                        if signal[peaks[z]] > thresholdI2 and signal[peaks[z]] > signal[peaks[z-1]] and signal[peaks[z]] > signal[peaks[z+1]]:
                            if peaks[z]-signalPeaks[-1]>0.2*fs:
                                signalPeaks.append(peaks[z])
                                SPKI = 0.125*signal[peaks[i]] + 0.875*SPKI
                            else:
                                NPKI = 0.125*signal[peaks[i]] + 0.875*NPKI
                    z+=1
                    
        # Check if peak is above the threshold value and is a local maxima
        if signal[peaks[i]] > thresholdI1 and signal[peaks[i]] > signal[peaks[i-1]] and signal[peaks[i]] > signal[peaks[i+1]]:
            # Check if the peak is a valid QRS complex
            if peaks[i] - signalPeaks[-1] > 0.36*fs: # Total PQRST Interval 
                signalPeaks.append(peaks[i]) # Signal Peak
                SPKI = 0.125*signal[peaks[i]] + 0.875*SPKI

            # T Wave Discrimination
            if peaks[i] - signalPeaks[-1] >0.2*fs and peaks[i] - signalPeaks[-1] < 0.36*fs and signal[peaks[i]] > 0.5*signal[signalPeaks[-1]]:
                signalPeaks.append(peaks[i]) # Signal Peak
                SPKI = 0.125*signal[peaks[i]] + 0.875*SPKI
        else:
            # Update noise thresholds
            NPKI = 0.125*signal[peaks[i]] + 0.875*NPKI 

        # Update signal thresholds
        thresholdI1 = NPKI + 0.25*(SPKI - NPKI)
        thrheshold_list.append(NPKI)

        # Check for missing peaks
        if len(signalPeaks)>8:
            array=signalPeaks[len(
                            signalPeaks) - 9: len(signalPeaks) - 2]

            RR=diffInt(array)

            RRAve=sum(RR)/len(RR)
            RRMissed= (1.66 * RRAve)

        i += 1
    i = 1
    
    # Check for too close peaks to filter the real peak
    while i < len(signalPeaks)-1:
        if signalPeaks[i]-signalPeaks[i-1] < fs/1000*fs:
            if signal[signalPeaks[i]]>signal[signalPeaks[i-1]]:
                signalPeaks.pop(i-1)
            else:
                signalPeaks.pop(i)
        i+=1 

    return signalPeaks[1:], thrheshold_list


def panPeakDetect(detection, fs):
    min_distance = int(0.25*fs)

    signal_peaks = [0]
    noise_peaks = []

    SPKI = 0.0
    NPKI = 0.0

    threshold_I1 = 0.0
    threshold_I2 = 0.0

    RR_missed = 0
    index = 0
    indexes = []

    missed_peaks = []
    peaks = []

    for i in range(len(detection)):

        if i>0 and i<len(detection)-1:
            if detection[i-1]<detection[i] and detection[i+1]<detection[i]:
                peak = i
                peaks.append(i)

                if detection[peak]>threshold_I1 and (peak-signal_peaks[-1])>0.3*fs:
                        
                    signal_peaks.append(peak)
                    indexes.append(index)
                    SPKI = 0.125*detection[signal_peaks[-1]] + 0.875*SPKI
                    if RR_missed!=0:
                        if signal_peaks[-1]-signal_peaks[-2]>RR_missed:
                            missed_section_peaks = peaks[indexes[-2]+1:indexes[-1]]
                            missed_section_peaks2 = []
                            for missed_peak in missed_section_peaks:
                                if missed_peak-signal_peaks[-2]>min_distance and signal_peaks[-1]-missed_peak>min_distance and detection[missed_peak]>threshold_I2:
                                    missed_section_peaks2.append(missed_peak)

                            if len(missed_section_peaks2)>0:           
                                missed_peak = missed_section_peaks2[np.argmax(missed_section_peaks2)]
                                missed_peaks.append(missed_peak)
                                signal_peaks.append(signal_peaks[-1])
                                signal_peaks[-2] = missed_peak   

                else:
                    noise_peaks.append(peak)
                    NPKI = 0.125*detection[noise_peaks[-1]] + 0.875*NPKI

                threshold_I1 = NPKI + 0.25*(SPKI-NPKI)
                threshold_I2 = 0.5*threshold_I1

                if len(signal_peaks)>8:
                    RR = np.diff(signal_peaks[-9:])
                    RR_ave = int(np.mean(RR))
                    RR_missed = int(1.66*RR_ave)

                index = index+1      
    
    signal_peaks.pop(0)

    return signal_peaks