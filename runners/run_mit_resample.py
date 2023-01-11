import os
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import wfdb
from scipy.signal import resample, resample_poly

# OUR TOOLS
from ecg_processing.signal_filtering import movingAverageMean, bandpassFilt, derivateStep, movingAverageMeanPanTompkins
from ecg_processing.signal_peak_detector import AMPT, panPeakDetect
from mit_processing.load_annotation import loadAnnotationSampleFromPath, loadAnnotationSampleFromPathSinus
from mit_processing.mit_analysis import checkNegative, checkPositive
from mit_processing.pan import panTompkins

time_window = 150

def main(path, fs, subpath, pan=False, plot=False, pan_to_use=1, resample_ecg=False):

    if pan_to_use==0:
        pan_used = "AMPT"
    if pan_to_use==1:
        pan_used = "PIKUS"

    print()
    print("********")
    print("Starting peak detection analysis on dataset '%s'"%(path))
    print()
    print("Peak detector: %s"%(pan_used))
    print("Sample base sampling frequency: %s"%(fs))
    print("Trace resampled to 200HZ: %s"%(resample_ecg))
    print("Plot enabled: %s"%(plot))
    print("********")
    print()

    signal_sampling = fs
    fileList = []
    for filename in os.listdir(path):
        fileList.append(filename)

    fileList.sort()
    beats_annotation = []

    data_arr = []
    count = 0

    pulse = 0

    peaks_list = []
    fp_list = []
    fn_list = []
    time_list = []
    f_list = []
    annotation_peaks_list=[]
    cat_1 = []
    cat_2 = []
    cat_3 = []
    cat_4 = []
    cat_5 = []
    

    for f in fileList:
        filename = str(f)
        if filename.endswith('.dat'):
            # print(filename)
            print("---------------")
            print(f)
            f_list.append(filename)
            if path == "ECG DBs/B - MIT-BIH NSR & ARRHYTHMIA/B1 - NSR DB 1.0.0/":
                record = wfdb.rdrecord(path + filename[:len(filename)-4], sampfrom=0, sampto=230400, channels=[0])
            else:
                record = wfdb.rdrecord(path + filename[:len(filename)-4], channels=[0])

            not_resampled_signal = [i for i in np.ravel(record.p_signal)]

            if resample_ecg:
                ## HERE TO RESAMPLE
                ecg_resampled = resample(not_resampled_signal, int(len(not_resampled_signal) * 200 / signal_sampling))
                fs = 200
            else:
                ecg_resampled = not_resampled_signal
                fs = signal_sampling
            
            count_peaks_iteration = 0

            if pan == False:
                newEcgFilt = bandpassFilt(ecg_resampled, 4, fs, 15, 5)

                derivateSignal = derivateStep(newEcgFilt)
                squaredEcgfromderivate = np.power(np.abs(derivateSignal), 2)

                panTompkinsEcgfromderivate = movingAverageMeanPanTompkins(squaredEcgfromderivate, fs)  
                
                start_time = time.time()
                peaks, _ = AMPT(panTompkinsEcgfromderivate, fs)
                print(time.time() - start_time)
                time_list.append(time.time() - start_time)

            else:
                # Pikus
                if pan_to_use == 1:
                    peaks, time_time = panTompkins(ecg_resampled, fs)
                    print(time_time)
                    time_list.append(time_time)

                if pan_to_use == 2:
                    newEcgFilt = bandpassFilt(ecg_resampled, 4, fs, 15, 5)

                    derivateSignal = derivateStep(newEcgFilt)
                    squaredEcgfromderivate = np.power(np.abs(derivateSignal), 2)

                    panTompkinsEcgfromderivate = movingAverageMeanPanTompkins(squaredEcgfromderivate, fs)  
                    
                    start_time = time.time()
                    peaks = panPeakDetect(panTompkinsEcgfromderivate, fs)
                    print(time.time() - start_time)
                    time_list.append(time.time() - start_time)

            beats_annotation = []   
            peaks_list.append(len(peaks))

            ###############
            # ANNOTATIONS #
            ###############

            if path == "ECG DBs/B - MIT-BIH NSR & ARRHYTHMIA/B1 - NSR DB 1.0.0/":
                annotationSample = loadAnnotationSampleFromPathSinus(path, filename[:len(filename)-4], counter=count_peaks_iteration, sampfrom=0, sampTo=230400)
            else:
                annotationSample = loadAnnotationSampleFromPath(path, filename[:len(filename)-4])

            if resample_ecg:
                # print(annotationSample)
                annotationSample = [int(i * 200 / signal_sampling) for i in annotationSample]
                
            # print(annotationSample)
            annotation_peaks_list.append(len(annotationSample))
            
            fp = checkPositive(annotationSample, peaks, fs, time_window)
            fn = checkNegative(annotationSample, peaks, fs, time_window)  
            
            fp_list.append(len(fp))
            fn_list.append(len(fn))

            count_peaks_iteration += 1

            if plot == True: # -> Not recoomended in automatic analysis due to the big data lenght
                ECG = np.array(ecg_resampled)
                plt.plot(ecg_resampled, label="Resampled ECG")
                # All annotation peaks in plot 
                plt.scatter(annotationSample, ECG[annotationSample], c = 'k', s = 30, label='MIT Annotations')
                plt.scatter(peaks, ECG[peaks], marker="o", c = 'r', s = 30, label='python Detected Peaks')
                # FP and FN in plot
                plt.vlines(fp, ymin=np.min(ECG), ymax=np.max(ECG), color="y",linewidth=1, label='Fake +')
                plt.vlines(fn, ymin=np.min(ECG), ymax=np.max(ECG), color="r", linewidth=1, label='Fake -')
                plt.legend()
                plt.show()
            print("______________________________")
            print()
            
    my_dict = { 'timing':[i for i in time_list],
                    'file':[i for i in f_list], 
                    'Our Peaks' : [i for i in peaks_list],
                    'Annotation Peaks': [i for i in annotation_peaks_list],
                    'False Positive' : [i for i in fp_list],
                    'False Negative': [i for i in fn_list]
                }

    # checking if the directory results 
    # exist or not.
    if not os.path.exists("results"):
        
        # if the results directory is not present 
        # then create it.
        os.makedirs("results")

    # checking if the directory results 
    # exist or not.
    if not os.path.exists(subpath[:-1]):
        print("NOT EXIST")
        
        # if the results directory is not present 
        # then create it.
        os.makedirs(subpath[:-1])
        
    if pan == False:
        if resample_ecg:
            # SAVE CSV FILE FULL ANALYSIS
            df = pd.DataFrame(my_dict)
            print(df)
            
            df.to_csv (subpath + "YouCare_resampled" + ".csv", index = False, header=True)
        else:
            # SAVE CSV FILE FULL ANALYSIS
            df = pd.DataFrame(my_dict)
            print(df)
            
            df.to_csv (subpath + "YouCare_not_resampled" + ".csv", index = False, header=True)
        
    else:
        if resample_ecg:
            # SAVE CSV FILE FULL ANALYSIS
            df = pd.DataFrame(my_dict)
            print(df)

            df.to_csv(subpath + "pan_resampled_" + str(pan_to_use) + ".csv", index=False, header=True)
        else:
            # SAVE CSV FILE FULL ANALYSIS
            df = pd.DataFrame(my_dict)
            print(df)

            df.to_csv(subpath + "pan_not_resampled_" + str(pan_to_use) + ".csv", index=False, header=True)