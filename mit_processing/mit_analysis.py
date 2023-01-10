#################
#
# Check Positive
#
#################
def checkPositive(ann, peaks, fs, time_window):
    realPeaks = []
    fakePositive = []
    i = 0
    lenght = 0
    if len(peaks) > len(ann):
        lenght = len(peaks)
        arr = peaks
        arr2 = ann
    else:
        lenght = len(ann)
        arr = ann
        arr2 = peaks

    for i in peaks:
        for n in ann:
            if i+(time_window*fs/1000) > n > i-(time_window*fs/1000):
                realPeaks.append(i)

    for i in peaks:
        if i not in realPeaks:
            fakePositive.append(i)

    #print("Fake +")
    print("fake + :" + str(len(fakePositive)))
    # print(fakePositive)
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

    # [[L5[l2 - 1] * sl1 for sl1, l3 in zip(l1, L3) for l2 in L2 if L4[l2 - 1] == l3] for l1 in L1]

    for i in ann:
        for n in peaks:
            if i+(time_window*fs/1000) > n > i-(time_window*fs/1000): #try with 95
                fakePeaks.append(i)

    for i in ann:
        if i not in fakePeaks:
            fakeNegative.append(i)

    # print("fake -")
    print("fake - :" + str(len(fakeNegative)))
    return fakeNegative