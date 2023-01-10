import os
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import wfdb
from scipy.signal import resample, resample_poly

# OUR TOOLS
from ecg_processing.signal_filtering import movingAverageMean, bandpassFilt, derivateStep, movingAverageMeanPamTompkins
from ecg_processing.signal_peak_detector import AMPT, panPeakDetect
from mit_processing.load_annotation import loadAnnotationSampleFromPath
from mit_processing.mit_analysis import checkNegative, checkPositive
from mit_processing.pam import panTompkins

time_window = 150

def main(path, fs, subpath, pam=False, plot=False, pam_to_use=1, resample_ecg=False):
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
            record = wfdb.rdrecord(path + filename[:len(filename)-4], channels=[0])

            not_resampled_signal = [i for i in np.ravel(record.p_signal)]

            if resample_ecg:
                ## HERE TO RESAMPLE
                ecg_resampled = resample(not_resampled_signal, int(len(not_resampled_signal) * 200 / 360))
                fs = 200
            else:
                ecg_resampled = not_resampled_signal
                fs = 360
            
            if pam == False:
                newEcgFilt = bandpassFilt(ecg_resampled, 4, fs, 15, 5)

                derivateSignal = derivateStep(newEcgFilt)
                squaredEcgfromderivate = np.power(np.abs(derivateSignal), 2)

                panTompkinsEcgfromderivate = movingAverageMeanPamTompkins(squaredEcgfromderivate, fs)  
                
                start_time = time.time()
                peaks, _ = AMPT(panTompkinsEcgfromderivate, fs)
                print(time.time() - start_time)
                time_list.append(time.time() - start_time)

            else:
                if pam_to_use == 1:
                    peaks, time_time = panTompkins(ecg_resampled, fs)
                    print(time_time)
                    time_list.append(time_time)

                if pam_to_use == 2:
                    newEcgFilt = bandpassFilt(ecg_resampled, 4, fs, 15, 5)

                    derivateSignal = derivateStep(newEcgFilt)
                    squaredEcgfromderivate = np.power(np.abs(derivateSignal), 2)

                    panTompkinsEcgfromderivate = movingAverageMeanPamTompkins(squaredEcgfromderivate, fs)  
                    
                    start_time = time.time()
                    peaks = panPeakDetect(panTompkinsEcgfromderivate, fs)
                    print(time.time() - start_time)
                    time_list.append(time.time() - start_time)

            beats_annotation = []   
            peaks_list.append(len(peaks))

            ###############
            # ANNOTATIONS #
            ###############

            annotationSample = loadAnnotationSampleFromPath(path, filename[:len(filename)-4])

            if resample_ecg:
                # print(annotationSample)
                annotationSample = [int(i * 200 / 360) for i in annotationSample]
                
            # print(annotationSample)
            annotation_peaks_list.append(len(annotationSample))
            
            fp = checkPositive(annotationSample, peaks, fs, time_window)
            fn = checkNegative(annotationSample, peaks, fs, time_window)  
            
            fp_list.append(len(fp))
            fn_list.append(len(fn))

            if plot == True: # -> Not recoomended in automatic analysis due to the big data lenght
                ECG = np.array(ecg_resampled)
                plt.plot(ecg_resampled, label="Resampled ECG")
                # All annotation peaks in plot 
                plt.scatter(annotationSample, ECG[annotationSample], c = 'k', s = 30, label='MIT Annotations')
                plt.scatter(peaks, ECG[peaks], marker="o", c = 'r', s = 30, label='python Detected Peaks')
                # FP and FN in plot
                # plt.vlines(fp, ymin=np.min(ECG), ymax=np.max(ECG), color="y",linewidth=1, label='Fake +')
                # plt.vlines(fn, ymin=np.min(ECG), ymax=np.max(ECG), color="r", linewidth=1, label='Fake -')
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

    if pam == False:
        # SAVE CSV FILE FULL ANALYSIS
        df = pd.DataFrame(my_dict)
        print(df)
        
        df.to_csv (subpath + "YouCare_resampled" + ".csv", index = False, header=True)
        
    else:
        # SAVE CSV FILE FULL ANALYSIS
        df = pd.DataFrame(my_dict)
        print(df)
        
        df.to_csv (subpath + "Pam_resampled_" + str(pam_to_use) + ".csv", index = False, header=True)