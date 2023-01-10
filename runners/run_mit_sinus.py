import os
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import wfdb
from ecgdetectors import panPeakDetect

# OUR TOOLS
from ecg_processing.signal_anomalies_detector import countAnomalies, beatsClassification4, detect_arrythmia
from ecg_processing.signal_filtering import movingAverageMean, bandpassFilt, derivateStep, movingAverageMeanPamTompkins
from ecg_processing.signal_peak_detector import AMPT, panPeakDetect
from ecg_processing.signal_analysis import calculateNNI
from mit_processing.mit_reader import getAnnotation, countAnnotationAnomalies
from mit_processing.load_annotation import loadAnnotationSampleFromPathSinus
from mit_processing.mit_analysis import checkNegative, checkPositive
from mit_processing.pam import panTompkins

time_window = 75

def main(path, fs, subpath, pam=False, plot=False):
    fileList = []
    for filename in os.listdir(path):
        fileList.append(filename)

    fileList.sort()

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
            print("---------------")   
            print(f)
            f_list.append(filename)
            record = wfdb.rdrecord(path + filename[:len(filename)-4], channels=[0])
            signal = record.p_signal
            count_fp=0
            count_fn=0
            time_list_section = 0
            count_ann_peak=0
            
            peak_list = []
            i=1
            count_peaks_iteration = 0
            if pam == False:
                data = wfdb.rdrecord(path + filename[:len(filename)-4], sampfrom=0, sampto=230400, channels=[0])
                signal_average_mean_removed = movingAverageMean(data.p_signal, fs)
                if np.max(signal_average_mean_removed)>1.0:
                    newEcgFilt = bandpassFilt(data.p_signal, 4, fs, 15, 5)
                    derivateSignal = derivateStep(newEcgFilt)
                    squaredEcgfromderivate = np.power(np.abs(derivateSignal), 2)
                    panTompkinsEcgfromderivate = movingAverageMeanPamTompkins(squaredEcgfromderivate, fs) 

                    start_time = time.time()
                    peaks, _ = AMPT(panTompkinsEcgfromderivate, fs)
                    time_list_section = time_list_section + (time.time() - start_time)
                    print(time.time() - start_time)

                    annotationSample = loadAnnotationSampleFromPathSinus(fullPath, filename[:len(filename)-4], counter=count_peaks_iteration, sampfrom=0, sampTo=230400)
                    count_ann_peak = count_ann_peak+len(annotationSample)

                    fp = checkPositive(annotationSample, peaks, fs, time_window)
                    fn = checkNegative(annotationSample, peaks, fs, time_window)  

                    count_fp = count_fp+len(fp)
                    count_fn = count_fn+len(fn)

                    count_peaks_iteration += 1
                    for p in peaks:
                        peak_list.append(p)
            else:
                data = wfdb.rdrecord(path + filename[:len(filename)-4], sampfrom=0, sampto=230400, channels=[0])
                signal_average_mean_removed = movingAverageMean(data.p_signal, fs)
                if np.max(signal_average_mean_removed)>1.0:

                    newEcgFilt = bandpassFilt(data.p_signal, 4, fs, 15, 5)
                    derivateSignal = derivateStep(newEcgFilt)
                    squaredEcgfromderivate = np.power(np.abs(derivateSignal), 2)
                    panTompkinsEcgfromderivate = movingAverageMeanPamTompkins(squaredEcgfromderivate, fs) 

                    #signal_pam = np.ravel(data.p_signal)
                    
                    start_time = time.time()
                    # peaks, time_passed = panTompkins(signal, fs)
                    #peaks = nk.ecg_findpeaks(panTompkinsEcgfromderivate, sampling_rate=360, method="pantompkins1985")
                    #peaks = [i for i in peaks['ECG_R_Peaks']]
                    peaks = panPeakDetect(panTompkinsEcgfromderivate, fs)
                    print(time.time() - start_time)
                    time_list_section = time_list_section + (time.time() - start_time)

                    annotationSample = loadAnnotationSampleFromPathSinus(fullPath, filename[:len(filename)-4], counter=count_peaks_iteration, sampfrom=0, sampTo=230400)
                    count_ann_peak = count_ann_peak+len(annotationSample)

                    fp = checkPositive(annotationSample, peaks, fs, time_window)
                    fn = checkNegative(annotationSample, peaks, fs, time_window)  

                    count_fp = count_fp+len(fp)
                    count_fn = count_fn+len(fn)

                    count_peaks_iteration += 1
                    for p in peaks:
                         peak_list.append(p)
                    i+=1
            
            print("total analysis time :" + str(time_list_section))

            time_list.append(time_list_section)

            annotation_peaks_list.append(count_ann_peak)
                          
            peaks_list.append(len(peak_list))
            print("Peaks loaded, peaks size: " + str(len(peak_list)))

            ###############
            # ANNOTATIONS # 
            ###############
            
            fp_list.append(count_fp)
            fn_list.append(count_fn) 

            print("annotation checked")

            ##############
            # ANOMALIES WITH ANTONIO AUGELLO based ALGORITHM based on Tsipouras
            ##############
            
            normal_rythm = True
            # print(detect_arrythmia(arr_nni, normal_rythm))
            
            #signal_average_mean_removed = movingAverageMean(signal, fs)
            #nni = calculateNNI(peak_list)

            #beatClassificationList, pulse = beatsClassification4(signal_average_mean_removed, nni, peak_list, pulse, normal_rythm)
            #beat_list = countAnomalies(beatClassificationList, peak_list)

            #cat_1.append(beat_list['cat_1'])
            #cat_2.append(beat_list['cat_2'])
            #cat_3.append(beat_list['cat_3'])
            #cat_4.append(beat_list['cat_4'])
            #cat_5.append(beat_list['cat_5'])
            count = count+1

            if plot == True: # -> Not recoomended in automatic analysis due to the big data lenght
                ECG = np.array(signal_pam)
                plt.plot(signal_pam, label="ECG")
                # All annotation peaks in plot 
                plt.scatter(annotationSample, ECG[annotationSample], c = 'k', s = 30, label='MIT Annotations')
                plt.scatter(peak_list, ECG[peak_list], marker="o", c = 'r', s = 30, label='python Detected Peaks')
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

    cat_dict = { 'cat_1':[i for i in cat_1],
                    'cat_2':[i for i in cat_2], 
                    'cat_3 ' : [i for i in cat_3],
                    'cat_4': [i for i in cat_4],
                    'cat_5' : [i for i in cat_5]
                }

    if pam == False:
        # SAVE CSV FILE FULL ANALYSIS
        df = pd.DataFrame(my_dict)
        print(df)
        
        df.to_csv (path + "YouCare_" + subpath + ".csv", index = False, header=True)
        
        # SAVE CSV FILE ANOMALIES COUNT
        df1 = pd.DataFrame(cat_dict)
        print(df1)
        df1.to_csv (path + "YouCare_" + subpath + "_" + "anomalies" + ".csv", index = False, header=True)
    else:
        # SAVE CSV FILE FULL ANALYSIS
        df = pd.DataFrame(my_dict)
        print(df)
        
        df.to_csv (path + "Pam_" + subpath + ".csv", index = False, header=True)
        
        # SAVE CSV FILE ANOMALIES COUNT
        df1 = pd.DataFrame(cat_dict)
        print(df1)
        df1.to_csv (path + "Pam_" + subpath + "_" + "anomalies" + ".csv", index = False, header=True)

###############
#     RUN     # 
###############

main(fullPath, fs, subpath, pam=True, plot=False)