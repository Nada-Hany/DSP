import os 
from utils import ReadSignal

def getFile(path):
    startDir = "C:/"
    found = False
    file_path = ""
    for root, dirs, files in os.walk(startDir):
        if path in files:
            found = True
            file_path = os.path.join(root, path)
            break
    # Open the file if found
    if found:
        return file_path
    return None


def readStructure(fileName):
    list = []
    file = open(fileName, "r")
    for line in file:
        tmp = line.strip().split()
        if len(tmp) == 1:
            list.append(tmp[0])
        else:
            list.append(tmp[1])
    return list

def getSignalFromFile(filename):
    # file = getFile(filename)
    list = readStructure(filename)
    samples = []
    for i in range(4, len(list), 1):
        samples.append(list[i])
    return ReadSignal(list[0], list[1], list[2], samples)



print(getSignalFromFile("signal1.txt").signalType)
print(getSignalFromFile("signal1.txt").isPeriodic)
print(getSignalFromFile("signal1.txt").sampleNo)
print(getSignalFromFile("signal1.txt").sampleList)