import utils,math
import numpy as np

# time = np.arange(0.0,1,0.001)

def generate_signal(data, error_label):
    # ["Amplitude", "Phase Shift", "Analog Frequency", "Sampling Frequency", "Signal Generator"]

    if data[3] < 2 * data[2]:
        error_label.configure(text="enter a higher analog frequency/lower sampling frequency")
        error_label.place(x=95, y=300)
        return None
        # raise ValueError("Sampling frequency must be at least twice the analog frequency to satisfy the Nyquist theorem.")
   
    # t = [i / data[3] for i in range(data[4])]
    t =  np.arange(0,data[3]) / data[3]
    signal = []

    if data[4] == "Sine":

        signal = [data[0] * math.sin(2 * math.pi * data[2] * ti + data[1] ) for ti in t]

    elif data[4] == "Cosine":

        signal = [data[0]  * math.cos(2 * math.pi * data[2] * ti + data[1]) for ti in t]
    # print(t, "  ----- times")
    return utils.ConstructedSignal(data[0] , data[1], data[2], data[3], int(data[3]),data[4], signal), t