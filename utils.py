from tkinter import filedialog
import numpy as np
import math 



class Button:
    def __init__(self, x, y, name, onClick):
        self.x = x
        self.y = y
        self.name = name
        self.onClick = onClick

class ConstructedSignal:
     def __init__(self, amp, phase, analog_freq, sampling_freq, sample_no, func, y):
        self.amp = float(amp)
        self.phase = float(phase)
        self.analog_freq = float(analog_freq)
        self.sampling_freq = float(sampling_freq)
        self.sample_no = int(sample_no)
        self.func = func
        self.y = [i for i in y]
        self.x = [i for i in sample_no]

class ReadSignal:
     def __init__(self, signalType, isPeriodic, sampleNo, y, x):
        self.signalType = signalType
        self.isPeriodic = isPeriodic
        self.sampleNo = int(sampleNo)
        self.y = [float(i.rstrip("f")) for i in y]
        self.x = [float(i.rstrip("f")) for i in x]
        self.intervals = []
        self.midpoints = []
        self.error = []
        self.quantization = []
        self.encoded = []


class FilterConfig:
    def __init__(self):
        self.filter_type = None
        self.fs = None
        self.stop_band_attenuation = None
        self.fc = None
        self.f2 = 0
        self.transition_band = None
        self.N = None
        self.deltaF = None
        self.edge = None
        self.window = None

    def read_from_file(self, filename):
        file = open(filename, 'r')
        for line in file:
            key, value = line.strip().split('=')
            key = key.strip()
            value = value.strip()

            if key == "FilterType":
                self.filter_type = value
            elif key == "FS":
                self.fs = int(value)
            elif key == "StopBandAttenuation":
                self.stop_band_attenuation = int(value)
            elif key == "FC":
                self.fc = int(value) 
            elif key == "F1":
                self.fc = int(value) 
            elif key == "F2":
                self.f2 = int(value) 
            elif key == "TransitionBand":
                self.transition_band = int(value)


class ReSampling:
    def __init__(self):
        self.L = None
        self.M = None

    def read_from_file(self, filename):
            file = open(filename, 'r')
            for line in file:
                # print(line.strip().split('='))
                parts = line.strip().split('=')
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()

                    if key == "L (Upsampling Factor)":
                        self.L = int(value)
                    elif key == "M (Downsampling Factor)":
                        self.M = int(value)


#check if all field are entered by the user
#TODO -> check for each constraint [fs range and so on]
def valid_inputs(entries, error_lbl):
    error_lbl.place(x=200, y=700)
    print("display signal btn is pressed")
    for key, value in zip(entries.keys(), entries.values()):
        # print(value.get())
        if not value.get() or (key=="Signal Generator" and value.get()=="choose function"):
            return False
        if key != "Signal Generator" and not is_float(value.get()):
            return False

    return True


# ["Amplitude", "Phase Shift", "Analog Frequency", "Sampling Frequency", "Signal Generator"]
def get_data(entries):
    list = []
    for key, value in zip(entries.keys(), entries.values()):
        if key != 'Signal Generator':
            list.append(float(value.get()))
        else:
            list.append(value.get())
    return list


def is_float(value):
    try:
        float(value)  
        return True  
    except ValueError:
        return False  

def is_int(value):
    try:
        int(value)  
        return True  
    except ValueError:
        return False  
    


def browse_file():
    file = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Text files", "*.txt")]
    )
    if file:
        print(f"Selected file: {file}")
        return file
    return None



def DFT(signal):
    N = signal.sampleNo
    res = []
    for k in range(N):
        realSum = 0
        imagSum = 0
        for n in range(N):
            angle = -2 * np.pi * k * n / N
            realSum += signal.y[n] * np.cos(angle)
            imagSum += signal.y[n] * np.sin(angle)
        res.append(complex(realSum, imagSum))
    return res


def IDFT(signal, freq_domain):
    N = len(freq_domain)
    signal = []
    for n in range(N):
        real = sum(freq_domain[k].real * np.cos(2 * np.pi * k * n / N) - 
                    freq_domain[k].imag * np.sin(2 * np.pi * k * n / N) for k in range(N))
        signal.append(real / N)
    return signal



def calculate_convolution(x1, y1, x2, y2):
    N1 = len(x1)
    N2 = len(x2)

    len_result = N1 + N2 - 1
    result = [0] * len_result
    indices = [0] * len_result

    
    for i in range(N1):
        for j in range(N2):
            indices[i + j] = x1[i] + x2[j]
            result[i + j] += y1[i] * y2[j]

    while result and result[-1] == 0:
        result.pop()
        indices.pop()
        
    return indices, result


# ------------------------- for FIR

def  getHVal(filter, n, fs, f1, f2 = 0):
    fc = f1
    angle = n * 2 * fc * math.pi 
    w1 = 2 * math.pi * f1 
    w2 = 2 * math.pi * f2 
    if filter == 'Low pass':
        return 2 * fc * (np.sin(angle)) / (angle) if n != 0 else 2 * fc
    
    elif filter == "High pass":
        return -2 * fc * (np.sin(angle) / angle) if n != 0 else 1 - 2 * fc
    
    elif filter == "Band pass":
        if n != 0:
            return (2 * f2 * (np.sin(n * w2) / (n * w2))) - (2 * f1 * (np.sin(n * w1) / (n * w1)))
        else:
            return 2 * (f2 - f1)
        
    elif filter == "Band stop":
        if n != 0:
            return (2 * f1 * (np.sin(n * w1) / (n * w1))) - (2 * f2 * (np.sin(n * w2) / (n * w2)))
        else:
            return 1 - 2 * (f2 - f1)


def getWindowVal(window, n, N):
    if window =="rectangular":
        return 1
    elif window == "hanning":
        return 0.5 + 0.5 * np.cos((2 * np.pi * n) / N)
    elif window == "hamming":
        return 0.54 + 0.46 * np.cos((2 * np.pi * n) / N)
    elif window == "blackman":
        return 0.42 + 0.5 * np.cos((2 * np.pi * n) / (N - 1)) + 0.08 * np.cos((4 * np.pi * n) / (N - 1))

    
def getCoeffNumber(window, deltaF):
    if window == "rectangular":
        num = math.ceil(0.9/deltaF)
    elif window == "hanning":
        num = math.ceil(3.1/deltaF)
    elif window == "hamming":
        num = math.ceil(3.3/deltaF) 
    elif window == "blackman":
        num = math.ceil(5.5/deltaF) 
    return num if num % 2 == 1 else num + 1 
 

def getWindowFunction(stopband):
    if stopband <= 21:
        return "rectangular"
    elif stopband <= 44:
        return "hanning"
    elif stopband <= 53:
        return "hamming"
    elif stopband <= 74:
        return "blackman"
    else:
        None