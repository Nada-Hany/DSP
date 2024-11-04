from tkinter import filedialog


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






    