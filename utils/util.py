from blist import sorteddict


def getValueOfClosestKey(*, key: float, dict: sorteddict):
    d = dict
    keys = sorted(list(d.keys()))
    assert len(keys) >= 0

    if len(keys) == 1:
        return d[keys[0]]
    if len(keys) == 2:
        lowIndex = 0
        highIndex = 1
    else:
        highIndex = 0
        while keys[highIndex] < key and highIndex < len(keys)-1:
            print(highIndex)
            highIndex += 1

    lowIndex = highIndex - 1

    lowDistance = abs(keys[lowIndex] - key)
    highDistance = abs(keys[highIndex] - key)

    if lowDistance < highDistance:
        return d[keys[lowIndex]]
    else:
        return d[keys[highIndex]]
