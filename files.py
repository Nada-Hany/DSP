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


def writeOnFile_constructed(signal:ConstructedSignal, filename='output.txt'):
    with open(f"{filename}", "w") as file:
        file.write('0\n')
        file.write('0\n')
        file.write(f'{signal.sample_no}\n')
        for i in range(signal.sample_no):
            tmp = round(signal.y[i], 6)
            file.write(f'{i} {tmp}\n')


def writeOnFile_read(signal:ReadSignal, filename='output.txt'):
    with open(f"{filename}", "w") as file:
        file.write(f"{signal.signalType}\n")
        file.write(f"{signal.isPeriodic}\n")
        file.write(f'{signal.sampleNo}\n')
        for i in range(signal.sampleNo):
            tmp = round(signal.y[i], 6)
            file.write(f'{signal.x[i]} {tmp}\n')

def readStructure(fileName):
    list = []
    file = open(fileName, "r")
    for line in file:
        tmp = line.strip().split()
        if len(tmp) == 1:
            list.append(tmp[0])
        elif len(tmp) == 2:
            list.append([tmp[0],tmp[1]])
        else:
            list.append((tmp[0], tmp[1], tmp[2]))

    return list

def getSignalFromFile(filename):
    list = readStructure(filename)
    samples = []
    x = []
    if list[0] == '0':
        for i in range(3, len(list), 1):
            samples.append(list[i][1])
            x.append(list[i][0])
        return ReadSignal(list[0], list[1], list[2], samples, x)
    else:
        for i in range(3, len(list), 1):
            samples.append([list[i][0],list[i][1], list[i][2]])
        return None

