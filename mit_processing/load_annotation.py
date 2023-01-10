import wfdb
import numpy as np

def loadSample(path):
    fileList = []
    for filename in os.listdir("/Users/antonioaugello/Desktop/projects/ecg_analisys/data/mit/converted/"):
        fileList.append(filename)
    for f in listFile:
        filename = str(f)
        record = wfdb.rdrecord('mit_regular/' + filename)

        f = open("data/sinus_mit/" + str(filename) + ".txt", "w+")
        for i in record.p_signal:
            f.write(str(i[0]) + "\n")
    return fileList

def loadAnnotationSample(filename):
    #ANNOTATIONS

    # file = filename[:12]
    file = filename[9:-8]
    
    #print(file)

    annotation = wfdb.rdann('/Users/antonioaugello/Desktop/projects/ecg_analisys/data/mit-bih-arrhythmia-database-1.0.0/' + file, 'atr')
    
    # annotation = wfdb.rdann('/Users/antonioaugello/Desktop/projects/ecg_analisys/mit_regular/' + file, 'atr')

    ann = annotation.sample

    return ann

def loadAnnotationSampleFromPath(path, filename):
    #ANNOTATIONS

    file = filename
    
    annotation = wfdb.rdann(path + file, 'atr')
    
    ann = annotation.sample

    return ann

def loadAnnotationSampleFromPathSinus(path, filename, counter, sampfrom, sampTo):
    #ANNOTATIONS

    file = filename
    
    annotation = wfdb.rdann(path + file, 'atr', sampfrom=sampfrom, sampto=sampTo)
    
    ann = annotation.sample

    if sampTo>sampTo-sampfrom:
        ann = [i-((sampTo-sampfrom)*counter) for i in ann]

    return ann


def loadAnnotationSampleFromPathD(path, filename):
    #ANNOTATIONS

    file = filename    
    annotation = np.genfromtxt(path + filename + '_ann_ms' + ".dat", delimiter="")
    
    return annotation