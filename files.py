import os 
from utils import ReadSignal, ConstructedSignal

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


def writeOnFile(signal:ConstructedSignal, filename='output.txt'):
    with open("output.txt", "w") as file:
        file.write(f'{signal.amp}\n')
        file.write('0\n')
        file.write(f'{signal.sample_no}\n')
        for i in range(signal.sample_no):
            file.write(f'{i} {signal.y_values[i]}\n')


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
    # if file:
    #     # read the signal
    # else:
    #     print("file not found")
    #     return
    list = readStructure(filename)
    samples = []
    for i in range(4, len(list), 1):
        samples.append(list[i])
    return ReadSignal(list[0], list[1], list[2], samples)
