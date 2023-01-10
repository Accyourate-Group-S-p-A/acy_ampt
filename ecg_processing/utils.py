def valuesOfIndexes(array, indexes):
    values = []
    for i in indexes:
        values.append(array[i])

    return values


def diffInt(arr):
    diff = []

    i = 0
    while i < len(arr)-1:
        diff.append(arr[i + 1] - arr[i])
        i += 1

    return diff


def is_between(a, x, b):
    return min(a, b) < x < max(a, b)

def mean(num1, num2):
    return num1 + num2 / 2

def floatListDiff(list):
    
    res = []
    for i in range(0, len(list)-1):
        diff = (list[i+1]) - (list[i])
        res.append(diff)

    return res
