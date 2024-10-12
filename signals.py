import utils
import math 


def generate_signal(data):
    # amp, phase, analog_freq, sampling_freq, sample_no, func
    # labels_text = ["Amplitude", "Phase Shift", "Analog Frequency", "Sampling Frequency", "Samples Number", "Signal Generator"]

    # if data[3] < 2 * data[2]:
    #     pass    
        # raise ValueError("Sampling frequency must be at least twice the analog frequency to satisfy the Nyquist theorem.")
    t = [i / data[3] for i in range(data[4])]

    signal = []

    if data[5] == "Sine":

        signal = [data[0] * math.sin(2 * math.pi * data[2] * ti + data[1] ) for ti in t]

    elif data[5] == "Cosine":

        signal = [data[0]  * math.cos(2 * math.pi * data[2] * ti + data[1]) for ti in t]

    return utils.ConstructedSignal(data[0] , data[1], data[2], data[3], data[4],data[5], signal)