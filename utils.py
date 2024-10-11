class Button:
    def __init__(self, x, y, name, onClick):
        self.x = x
        self.y = y
        self.name = name
        self.onClick = onClick

class Signal:
     def __init__(self, amp, phase, analog_freq, sampling_freq, sample_no, func):
        self.amp = amp
        self.phase = phase
        self.analog_freq = analog_freq
        self.sampling_freq = sampling_freq
        self.sample_no = sample_no
        self.func = func
         
#check if all field are entered by the user
#TODO -> check for each constraint [fs range and so on]
def valid_inputs(entries, error_lbl):
    error_lbl.place(x=200, y=700)
    print("display signal btn is pressed")
    for key, value in zip(entries.keys(), entries.values()):
        print(value.get())
        if not value.get() or (key=="Signal Generator" and value.get()=="choose function"):
            return False
    return True

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