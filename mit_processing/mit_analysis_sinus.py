#################
#
# Check Positive
#
#################
def checkPositive(ann, peaks, fs, time_window):
    realPeaks = []
    fakePositive = []

    i = 1
    while i < len(peaks):
        if i % 1000==0:
            peaks_chunk = peaks[i-1000:i]
            ann_chunk = ann[i-1000:i]
            for p in peaks_chunk:
                for n in ann_chunk:
                    if p+((time_window*fs)/1000) > n > p-((time_window*fs)/1000):
                        realPeaks.append(p)
        i += 1
    peaks_chunk = peaks[len(peaks)-i%1000:len(peaks)]
    ann_chunk = ann[len(peaks)-i%1000:len(peaks)]
    for p in peaks_chunk:
        for n in ann_chunk:
            if p+((time_window*fs)/1000) > n > p-((time_window*fs)/1000):
                realPeaks.append(p)
        
    print("size of realPeaks: " + str(len(realPeaks)))
    
    for i in peaks:
        if i not in realPeaks:
            fakePositive.append(i)

    print("fake + :" + str(len(fakePositive)))
    return fakePositive

#################
#
# Check Negative
#
#################
# start from annotation and subtract number of real annotation from the presents
def checkNegative(ann, peaks, fs, time_window):
    fakePeaks = []
    fakeNegative = []

    i = 1
    while i < len(ann):
        if i % 1000==0:
            peaks_chunk = peaks[i-1000:i]
            ann_chunk = ann[i-1000:i]
            for p in ann_chunk:
                for n in peaks_chunk:
                    if p+((time_window*fs)/1000) > n > p-((time_window*fs)/1000):
                        fakePeaks.append(p)
        i += 1
    peaks_chunk = peaks[len(peaks)-i%1000:len(peaks)]
    ann_chunk = ann[len(peaks)-i%1000:len(peaks)]
    for p in ann_chunk:
        for n in peaks_chunk:
            if p+((time_window*fs)/1000) > n > p-((time_window*fs)/1000):
                fakePeaks.append(p)
    
    print("size of fakePeaks: " + str(len(fakePeaks)))

    for i in ann:
        if i not in fakePeaks:
            fakeNegative.append(i)

    print("fake - :" + str(len(fakeNegative)))
    return fakeNegative