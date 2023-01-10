def countAnnotationAnomalies(annotation):
    beatClassificationList_annotation = annotation.symbol

    cat1_arr = ["N", "P", "f", "p", "Q", "|", "+", "s", "t", "~", "L", "R"]
    cat2_arr = ["A", "a", "J", "S"]
    cat3_arr = ["V", "F"]
    cat4_arr = ["e", "j", "n", "E"]
    cat5_arr = ["[, !, ]"]

    cat1_arr_count = 0
    cat2_arr_count = 0
    cat3_arr_count = 0
    cat4_arr_count = 0
    cat5_arr_count = 0

    for i in beatClassificationList_annotation:
        if i in cat1_arr:
            cat1_arr_count +=1
        if i in cat2_arr:
            cat2_arr_count +=1
        if i in cat3_arr:
            cat3_arr_count +=1
        if i in cat4_arr:
            cat4_arr_count +=1
        if i in cat5_arr:
            cat5_arr_count +=1


    print("tot cat 1: " + str(cat1_arr_count))
    print("tot cat 2: " + str(cat2_arr_count))
    print("tot cat 3: " + str(cat3_arr_count))
    print("tot cat 4: " + str(cat4_arr_count))
    print("tot cat 5: " + str(cat5_arr_count))


def getAnnotation(beatClassificationList_annotation, peaks):
    print()
    print()
    print()
    for index, val in enumerate(beatClassificationList_annotation): 
        if val != "N":
            print(peaks[index])
            print(val)

