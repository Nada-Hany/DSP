import files, math, cmath
from utils import ReadSignal
import numpy as np


staticPath_task1 = './files/task1/'
staticPath_task2 = './files/task2/'
staticPath_task3 = './files/task3/'


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



def QuantizationTest2(file_name,Your_IntervalIndices,Your_EncodedValues,Your_QuantizedValues,Your_SampledError):
    expectedIntervalIndices=[]
    expectedEncodedValues=[]
    expectedQuantizedValues=[]
    expectedSampledError=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==4:
                L=line.split(' ')
                V1=int(L[0])
                V2=str(L[1])
                V3=float(L[2])
                V4=float(L[3])
                expectedIntervalIndices.append(V1)
                expectedEncodedValues.append(V2)
                expectedQuantizedValues.append(V3)
                expectedSampledError.append(V4)
                line = f.readline()
            else:
                break
    if(len(Your_IntervalIndices)!=len(expectedIntervalIndices)
     or len(Your_EncodedValues)!=len(expectedEncodedValues)
      or len(Your_QuantizedValues)!=len(expectedQuantizedValues)
      or len(Your_SampledError)!=len(expectedSampledError)):
        print("QuantizationTest2 Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_IntervalIndices)):
        if(Your_IntervalIndices[i]!=expectedIntervalIndices[i]):
            print("QuantizationTest2 Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(Your_EncodedValues)):
        if(Your_EncodedValues[i]!=expectedEncodedValues[i]):
            print("QuantizationTest2 Test case failed, your EncodedValues have different EncodedValues from the expected one") 
            return
        
    for i in range(len(expectedQuantizedValues)):
        if abs(Your_QuantizedValues[i] - expectedQuantizedValues[i]) < 0.01:
            continue
        else:
            print("QuantizationTest2 Test case failed, your QuantizedValues have different values from the expected one") 
            return
    for i in range(len(expectedSampledError)):
        if abs(Your_SampledError[i] - expectedSampledError[i]) < 0.01:
            continue
        else:
            print("QuantizationTest2 Test case failed, your SampledError have different values from the expected one") 
            return
    print("QuantizationTest2 Test case passed successfully")



def QuantizationTest1(file_name,Your_EncodedValues,Your_QuantizedValues):
    expectedEncodedValues=[]
    expectedQuantizedValues=[]
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
                V2=str(L[0])
                V3=float(L[1])
                expectedEncodedValues.append(V2)
                expectedQuantizedValues.append(V3)
                line = f.readline()
            else:
                break
    if( (len(Your_EncodedValues)!=len(expectedEncodedValues)) or (len(Your_QuantizedValues)!=len(expectedQuantizedValues))):
        print("QuantizationTest1 Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_EncodedValues)):
        if(Your_EncodedValues[i]!=expectedEncodedValues[i]):
            print("QuantizationTest1 Test case failed, your EncodedValues have different EncodedValues from the expected one") 
            return
    for i in range(len(expectedQuantizedValues)):
        if abs(Your_QuantizedValues[i] - expectedQuantizedValues[i]) < 0.01:
            continue
        else:
            print("QuantizationTest1 Test case failed, your QuantizedValues have different values from the expected one") 
            return
    print("QuantizationTest1 Test case passed successfully")



#Use to test the Amplitude of DFT and IDFT
def SignalComapreAmplitude(SignalInput = [] ,SignalOutput= []):
    if len(SignalInput) != len(SignalInput):
        return False
    else:
        print('in compare function ,, difference between actual and generated')
        for i in range(len(SignalInput)):
            print(i, ' -- ', SignalInput[i]-SignalOutput[i])
            if abs(SignalInput[i]-SignalOutput[i])>0.001:
                return False
            elif SignalInput[i]!=SignalOutput[i]:
                return False
        return True

def RoundPhaseShift(P):
    while P<0:
        p+=2*math.pi
    return float(P%(2*math.pi))

#Use to test the PhaseShift of DFT
def SignalComaprePhaseShift(SignalInput = [] ,SignalOutput= []):
    if len(SignalInput) != len(SignalInput):
        return False
    else:
        for i in range(len(SignalInput)):
            A=round(SignalInput[i])
            B=round(SignalOutput[i])
            if abs(A-B)>0.0001:
                return False
            elif A!=B:
                return False
        return True





def getComponents(signal : ReadSignal, inverse = None):

        sign = 1 if inverse else -1
        scale = 1/signal.sampleNo if inverse else 1

        result = []
        components = []
        N = signal.sampleNo
        for k in range(N): 
            sum_real = 0
            sum_imag = 0
            for n in range(N):
                angle = 2 * math.pi * k * n / N
                sum_real += signal.x[n] * math.cos(sign * angle)
                sum_imag += signal.x[n] * math.sin(sign * angle)

            result.append((scale * sum_real, scale * sum_imag))
            amplitudes = [abs(complex(r, i)) for r, i in result]
            phases = [math.atan2(i, r) for r, i in result]
        idft_input = [a * math.cos(p) for a, p in zip(amplitudes, phases)]
        # idft_result = dft_idft(idft_input, inverse=True)
        return amplitudes, phases
  
def compute_dft(data, sample_freq):
    N = len(data)
    freq_comp = []
    for k in range(N):
        real_sum = 0
        img_sum = 0
        for n in range(N):
            angle = -2 * np.pi * k * n / N
            real_sum += data[n] * np.cos(angle)
            img_sum += data[n] * np.sin(angle)
        freq_comp.append(complex(real_sum, img_sum))
    freqs = np.arange(N) * (sample_freq / N)
    amp = np.abs(freq_comp)
    phases = np.angle(freq_comp)
    return freq_comp, freqs, amp, phases




def dft(signal, Fs, inverse):
    indicies = []
    samples = []  
    for x, y in signal:
        indicies.append(x)
        samples.append(y)

    N = len(samples)
    real = np.zeros(N)
    imag = np.zeros(N)
    rev = np.zeros(N)

    if inverse:
        for k in range(N):
            amp = indicies[k]      
            theta = samples[k]    
            real[k] = amp * np.cos(theta)
            imag[k] = amp * np.sin(theta)

    for n in range(N):
        for k in range(N):
            angle = 2 * np.pi * k * n / N if inverse else -2 * np.pi * k * n / N

            if not inverse:
                real[k] += samples[n] * np.cos(angle)
                imag[k] += samples[n] * np.sin(angle)
            
           
            else:
                rev[n] += real[k] * np.cos(angle) - imag[k] * np.sin(angle)

   
    if not inverse:
        amp = np.sqrt(real*2 + imag*2)
        phase = np.arctan2(imag, real)
        fundamental_freq = (2 * np.pi) / (N / Fs)
        frequencies = np.arange(1, N + 1) * fundamental_freq
        return frequencies, amp, phase

    
    else:
       return np.arange(N), rev / N
    


    # elif transform_type == 'IDFT':
    #         amp, phase = self.read_reference_data()
    #         if not amp or not phase:
    #             print("Error: No amplitude or phase data read from the reference file.")
    #             return

    #         sampling_frequency = simpledialog.askfloat("Input", "Enter the sampling frequency in Hz:", minvalue=1.0)
    #         if sampling_frequency is None:
    #             return

    #         amp = np.array(amp)
    #         phase = np.array(phase)

    #         real_part = amp * np.cos(phase)
    #         imaginary_part = amp * np.sin(phase)
    #         complex_spectrum = real_part + 1j * imaginary_part

    #         reconstructed_signal = self.fourier_transform(complex_spectrum, inverse=True)
    #         reconstructed_amplitude = np.round(np.real(reconstructed_signal), decimals=0).tolist()

    #         reference_time, reference_signal = self.read_signals_from_txt_files()
    #         reference_signal = reference_signal[0].tolist()

    #         recon_amplitude_comparison = SignalComapreAmplitude(reconstructed_amplitude, reference_signal)

    #         if recon_amplitude_comparison:
    #             print("Reconstructed Amplitude comparison passed successfully.")
    #         else:
    #             print("Reconstructed Amplitude comparison failed.")
    #         elif transform_type == 'IDFT':
    #         amp, phase = self.read_reference_data()
    #         if not amp or not phase:
    #             print("Error: No amplitude or phase data read from the reference file.")
    #             return

    #         sampling_frequency = simpledialog.askfloat("Input", "Enter the sampling frequency in Hz:", minvalue=1.0)
    #         if sampling_frequency is None:
    #             return

    #         amp = np.array(amp)
    #         phase = np.array(phase)

    #         real_part = amp * np.cos(phase)
    #         imaginary_part = amp * np.sin(phase)
    #         complex_spectrum = real_part + 1j * imaginary_part

    #         reconstructed_signal = self.fourier_transform(complex_spectrum, inverse=True)
    #         reconstructed_amplitude = np.round(np.real(reconstructed_signal), decimals=0).tolist()

    #         reference_time, reference_signal = self.read_signals_from_txt_files()
    #         reference_signal = reference_signal[0].tolist()

    #         recon_amplitude_comparison = SignalComapreAmplitude(reconstructed_amplitude, reference_signal)

    #         if recon_amplitude_comparison:
    #             print("Reconstructed Amplitude comparison passed successfully.")
    #         else:
    #             print("Reconstructed Amplitude comparison failed.")


    #     def fourier_transform(self, signal, inverse=False):
    #         N = len(signal)
    #         k = np.arange(N)
    #         n = np.arange(N)
    #         # Exponential factor
    #         if inverse:
    #             factor = 1 / N
    #             exponent = np.exp(2j * np.pi * k[:, None] * n / N)  # IDFT
    #         else:
    #             factor = 1
    #             exponent = np.exp(-2j * np.pi * k[:, None] * n / N)  # DFT

    #         return factor * np.dot(exponent, signal)  # Compute DFT or IDFT