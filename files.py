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
    with open(f"{filename}", "w") as file:
        file.write(f'{signal.amp}\n')
        file.write('0\n')
        file.write(f'{signal.sample_no}\n')
        for i in range(signal.sample_no):
            file.write(f'{i} {signal.y_values[i]}\n')

# sample aplitude -> 1st row = 0

# [SignalType] // Time-->0/Freq-->1
# [IsPeriodic] // takes 0 or 1
# [Index SampleAmp] or [Freq Amp PhaseShift]//
# N1 rows follow with Sample Index followed by space followed by Sample Amplitude in 
# case Time domain was specified in the first row in the file,
# or N1 rows follow with frequency followed by space followed by amplitude followed by Phase shift

def readStructure_2(fileName):
    list = []
    file = open(fileName, "r")
    for line in file:
        tmp = line.strip().split()
        if len(tmp) == 1:
            list.append(tmp[0])
        elif len(tmp) == 2:
            list.append(tmp[1])
        else:
            list.append((tmp[0], tmp[1], tmp[2]))

    return list

def getSignalFromFile_2(filename):
    # file = getFile(filename)
    # if file:
    #     # read the signal
    # else:
    #     print("file not found")
    #     return
    list = readStructure_2(filename)
    samples = []
    if list[0] == '0':
        for i in range(3, len(list), 1):
            samples.append(list[i])
        return ReadSignal(list[0], list[1], list[2], samples)
    else:
        for i in range(3, len(list), 1):
            samples.append([list[i][0],list[i][1], list[i][2]])
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
    # if file:
    #     # read the signal
    # else:
    #     print("file not found")
    #     return
    list = readStructure(filename)
    samples = []
    for i in range(3, len(list), 1):
        samples.append(list[i])
    return ReadSignal(list[0], list[1], list[2], samples)
