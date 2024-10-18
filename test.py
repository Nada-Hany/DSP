import files

staticPath_task1 = './files/task1/'
staticPath_task2 = './files/task2/'

def SignalSamplesAreEqual(file_name,indices,samples):
    expected_indices=[]
    expected_samples=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
                
    if len(expected_samples)!=len(samples):
        print("Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(expected_samples)):
        if abs(samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Test case failed, your signal have different values from the expected one") 
            return
    print("Test case passed successfully")

signal = files.getSignalFromFile(f'{staticPath_task1}CosOutput.txt')
# print(signal.sampleList)
# ind = [i for i in range(0, len(signal.sampleList))]
# # print(ind)
# samples = []
# for i in range(len(signal.sampleList)):
#     samples.append(float(signal.sampleList[i]))

SignalSamplesAreEqual(f'{staticPath_task1}cos_output.txt',signal.x, signal.y)


