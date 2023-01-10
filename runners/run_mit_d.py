import os
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import wfdb

# OUR TOOLS
from ecg_processing.signal_anomalies_detector import countAnomalies, beatsClassification4, detect_arrythmia
from ecg_processing.signal_filtering import movingAverageMean, bandpassFilt, derivateStep, movingAverageMeanpanTompkins
from ecg_processing.signal_peak_detector import AMPT, panPeakDetect
from mit_processing.mit_reader import getAnnotation, countAnnotationAnomalies
from mit_processing.load_annotation import loadAnnotationSampleFromPath, loadAnnotationSampleFromPathD
from mit_processing.mit_analysis import checkNegative, checkPositive
from mit_processing.pan import panTompkins

time_window = 150

def main(path, fs, subpath, pan=False, plot=False):
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
    panTompkinsEcgfromderivate = []

    for f in fileList:
        filename = str(f)
        if filename.endswith('_samples.dat'):
            # print(filename)
            print("---------------")   
            print(f)
            f_list.append(filename)
            record = np.genfromtxt(path + filename[:len(filename)-12] + '_samples' + ".dat", delimiter="")

            if pan == False:
                newEcgFilt = bandpassFilt(record, 4, fs, 15, 5)

                derivateSignal = derivateStep(newEcgFilt)

                squaredEcgfromderivate = np.power(np.abs(derivateSignal), 2)

                panTompkinsEcgfromderivate = movingAverageMeanpanTompkins(squaredEcgfromderivate, fs)  
                start_time = time.time()
                peaks, thres = AMPT(panTompkinsEcgfromderivate, fs)
                print(time.time() - start_time)
                time_list.append(time.time() - start_time)
            else:
                newEcgFilt = bandpassFilt(record, 4, fs, 15, 5)

                derivateSignal = derivateStep(newEcgFilt)

                squaredEcgfromderivate = np.power(np.abs(derivateSignal), 2)

                panTompkinsEcgfromderivate = movingAverageMeanpanTompkins(squaredEcgfromderivate, fs)  
                start_time = time.time()
                # peaks, time_passed = panTompkins(signal, fs)
                #peaks = nk.ecg_findpeaks(panTompkinsEcgfromderivate, sampling_rate=360, method="pantompkins1985")
                #peaks = [i for i in peaks['ECG_R_Peaks']]
                peaks = panPeakDetect(panTompkinsEcgfromderivate, fs)
                print(time.time() - start_time)
                time_list.append(time.time() - start_time)
                        
            beats_annotation = []
                        
            peaks_list.append(len(peaks))

            ###############
            # ANNOTATIONS # 
            ###############

            annotationSample = loadAnnotationSampleFromPathD(path, filename[:len(filename)-12])
            annotationSample = np.divide(annotationSample, 1000)
            annotationSample = np.multiply(annotationSample, 500)

            annotation_peaks_list.append(len(annotationSample))

            fp = checkPositive(annotationSample, peaks, fs, time_window)
            fn = checkNegative(annotationSample, peaks, fs, time_window)  
            
            fp_list.append(len(fp))
            fn_list.append(len(fn))

            ##############
            # ANOMALIES WITH ANTONIO AUGELLO based ALGORITHM
            ##############
                            
            normal_rythm = True
            # print(detect_arrythmia(arr_nni, normal_rythm))
            signal_average_mean_removed = movingAverageMean(record, fs)
            nni = calculateNNI(peaks)

            beatClassificationList, pulse = beatsClassification4(signal_average_mean_removed, nni, peaks, pulse, normal_rythm)
            beat_list = countAnomalies(beatClassificationList, peaks)

            cat_1.append(beat_list['cat_1'])
            cat_2.append(beat_list['cat_2'])
            cat_3.append(beat_list['cat_3'])
            cat_4.append(beat_list['cat_4'])
            cat_5.append(beat_list['cat_5'])
            count = count+1

            if plot == True: # -> Not recoomended in automatic analysis due to the big data lenght
                ECG = np.array(record)
                plt.plot(record, label="ECG")
                # All annotation peaks in plot 
                annotation_plot = [int(i) for i in annotationSample]
                plt.scatter(annotation_plot, ECG[annotation_plot], c = 'k', s = 30, label='MIT Annotations')
                plt.scatter(peaks, ECG[peaks], marker="o", c = 'r', s = 30, label='python Detected Peaks')
                # FP and FN in plot
                #plt.vlines(fp, ymin=np.min(ECG), ymax=np.max(ECG), color="y",linewidth=1, label='Fake +')
                #plt.vlines(fn, ymin=np.min(ECG), ymax=np.max(ECG), color="r", linewidth=1, label='Fake -')
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

    print(my_dict)

    if pan == False:
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
        
        df.to_csv (path + "pan_" + subpath + ".csv", index = False, header=True)
        
        # SAVE CSV FILE ANOMALIES COUNT
        df1 = pd.DataFrame(cat_dict)
        print(df1)
        df1.to_csv (path + "pan_" + subpath + "_" + "anomalies" + ".csv", index = False, header=True)

###############
#     RUN     # 
###############

main(fullPath, fs, subpath, pan=True, plot=False)