import utils,math
import numpy as np

# time = np.arange(0.0,1,0.001)

def generate_signal(data, error_label):
    # amp, phase, analog_freq, sampling_freq, sample_no, func
    # labels_text = ["Amplitude", "Phase Shift", "Analog Frequency", "Sampling Frequency", "Samples Number", "Signal Generator"]

    if data[3] < 2 * data[2]:
        error_label.configure(text="enter a higher analog frequency/lower sampling frequency")
        error_label.place(x=95, y=300)
        return None
        # raise ValueError("Sampling frequency must be at least twice the analog frequency to satisfy the Nyquist theorem.")
    t = [i / data[3] for i in range(data[4])]

    signal = []

    if data[5] == "Sine":

        signal = [data[0] * math.sin(2 * math.pi * data[2] * ti + data[1] ) for ti in t]

    elif data[5] == "Cosine":

        signal = [data[0]  * math.cos(2 * math.pi * data[2] * ti + data[1]) for ti in t]

    return utils.ConstructedSignal(data[0] , data[1], data[2], data[3], data[4],data[5], signal)