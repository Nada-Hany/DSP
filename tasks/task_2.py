from blinker import Signal
import guiHelpers
import tkinter as tk
from utils import Button
import utils, files, test
from tkinter import ttk
import numpy as np
from utils import ReadSignal
from guiHelpers import Graph
from tkinter import filedialog

staticPath= './files/task2/constructed'
testPath = './files/task2/'


class Task2:
    def __init__(self, root, main):
        self.root =root
        self.left_section, self.right_section = self.sections()
        self.add_signals_frame = guiHelpers.right_frame(self.right_section)
        self.subtract_signals_frame = guiHelpers.right_frame(self.right_section)
        self.multiply_signals_frame = guiHelpers.right_frame(self.right_section)
        self.square_signals_frame = guiHelpers.right_frame(self.right_section)
        self.normalization_frame = guiHelpers.right_frame(self.right_section)
        self.accumulation_frame = guiHelpers.right_frame(self.right_section)
        self.signal_1 = None
        self.signal_2 = None
        self.main = main
        self.signals=[]
        self.baseSignals = []
        self.graph = Graph()
        
    def destroyFrames(self):
        self.add_signals_frame.destroy()
        self.subtract_signals_frame.destroy()
        self.multiply_signals_frame.destroy()
        self.square_signals_frame.destroy()
        self.normalization_frame.destroy()
        self.accumulation_frame.destroy()

    def goBack(self):

        print("in go back func")
        self.add_signals_frame.destroy()
        self.subtract_signals_frame.destroy()
        self.multiply_signals_frame.destroy()
        self.square_signals_frame.destroy()
        self.normalization_frame.destroy()
        self.square_signals_frame.destroy()
        self.right_section.destroy()
        self.left_section.destroy()
        # main.main_window()
        self.main.main_window()
        del self


    #left section for all buttons - right section for displaying 
    def sections(self):
        left_frame, right_frame = guiHelpers.sections(self.root)
       
        btn_x = guiHelpers.btn_x

        back_btn = tk.Button(left_frame, text="back",compound=tk.CENTER, command= lambda:self.goBack(), width=3, height=1, borderwidth=0)
        back_btn.place(x= btn_x, y=guiHelpers.back_btn_y)
        
        add_signal_btn = Button(btn_x, 20, "Add Signals", lambda:self.to_add_signals())
        subtract_signal_btn = Button(btn_x, 70, "Subtract Signals", lambda:self.to_subtract_signals())
        multiply_signal_btn = Button(btn_x, 120, "Multiply Signals", lambda:self.get_multiplication_number())
        square_signal_btn = Button(btn_x, 170, "Square Signals", lambda:self.to_square_signals())
        normalization_btn = Button(btn_x, 220, "Normalize", lambda:self.get_normalize_ratio())
        accumulation_btn = Button(btn_x, 270, "Accumulation", lambda:self.to_accumulation())
        read_signal_btn = Button(btn_x, 320, "read signals", lambda:self.select_files()) 
        
        buttons = []
        buttons.append(add_signal_btn)
        buttons.append(subtract_signal_btn)
        buttons.append(multiply_signal_btn)
        buttons.append(square_signal_btn)
        buttons.append(normalization_btn)
        buttons.append(accumulation_btn)
        buttons.append(read_signal_btn)
        for btn in buttons:
            tmp = tk.Button(left_frame, text=f"{btn.name}", bg="#808080", fg="white", width=15, height=2, command=btn.onClick)
            tmp.place(x=btn.x, y=btn.y)
        
        return  left_frame, right_frame
    

    def to_add_signals(self):
        self.signals = self.baseSignals
        print("in add signals")
        self.destroyFrames()
        self.add_signals_frame= guiHelpers.right_frame(self.right_section)
        nosignal=tk.Label(self.right_section, text="please read a signal first")
        signal= (len(self.signals)>1)

        # variable signal -> datatype == boolean 
        if signal:
            nosignal.destroy()
            # key -> index , value -> y value
            dict = {}
            for signal in self.signals:
                for i in range(signal.sampleNo):
                    if(signal.x[i] not in dict):
                        dict[signal.x[i]] = signal.y[i]
                    else:
                        dict[signal.x[i]] += signal.y[i]

            x = list(dict.keys())
            y = list(dict.values())
        
            signal = ReadSignal(0, self.signals[0].isPeriodic, len(x), y, x)
            self.graph.clear()
            self.graph.discreteGraph(self.add_signals_frame, [signal])
            self.graph.continousGraph(self.add_signals_frame, [signal])
            print("signal-1 + signal-2")
            test.SignalSamplesAreEqual(f'{testPath}Signal1+signal2.txt', x, y)
            print("signal-1 + signal-3")
            test.SignalSamplesAreEqual(f'{testPath}signal1+signal3.txt', x, y)
            # files.writeOnFile_read(signal, f"{staticPath}added_signals.txt")
        else:
            nosignal.place(x=200,y=200)  # Show message if no signal is loaded
        print("No signal loaded to add.")
            

    
    def to_subtract_signals(self):
        self.signals = self.baseSignals
        print("in subtract signals")
        self.destroyFrames()
        self.subtract_signals_frame = guiHelpers.right_frame(self.right_section)
        nosignal=tk.Label(self.right_section, text="please read a signal first")
        signal= (len(self.signals)>1)
        # variable signal -> datatype == boolean 
        if signal:
            nosignal.destroy()
            # key -> index , value -> y value

            dict = {}
            for signal in self.signals:
                for i in range(signal.sampleNo):
                    if(signal.x[i] not in dict):
                        dict[signal.x[i]] = signal.y[i]
                    else:
                        dict[signal.x[i]] = abs(dict[signal.x[i]] - signal.y[i])

            x = list(dict.keys())
            y = list(dict.values())
        
            signal = ReadSignal(0, self.signals[0].isPeriodic, len(x), y, x)
            self.graph.clear()
            self.graph.discreteGraph(self.subtract_signals_frame, [signal])
            self.graph.continousGraph(self.subtract_signals_frame, [signal])
            print("signal-1 - signal-2")
            test.SignalSamplesAreEqual(f'{testPath}signal1-signal2.txt', x, y)
            print("signal-1 - signal-3")
            test.SignalSamplesAreEqual(f'{testPath}signal1-signal3.txt', x, y)
            # files.writeOnFile_read(signal, f"{staticPath}subtracted_signals.txt")
        else:
             nosignal.place(x=200,y=200)  # Show message if no signal is loaded
    
    def to_multiply_signals(self, number):
        self.signals = self.baseSignals
        print("in multiply signals")
        self.destroyFrames()
        self.multiply_signals_frame = guiHelpers.right_frame(self.right_section)
        y = self.signals[0].y 
        print(y)
        self.signals[0].y  = [(int(number) * i) for i in y]
        # y_ = []
        # for i in range(len(y)):
        #     y_.append(number * y[i])\
        self.graph.clear()
        self.graph.discreteGraph(self.multiply_signals_frame, self.signals)
        self.graph.continousGraph(self.multiply_signals_frame, self.signals)

        print("signal-1 * 5")
        test.SignalSamplesAreEqual(f'{testPath}MultiplySignalByConstant-Signal1 - by 5.txt', self.signals[0].x, y)
        print("signal-2 * 10")
        test.SignalSamplesAreEqual(f'{testPath}MultiplySignalByConstant-signal2 - by 10.txt', self.signals[0].x, y)
        files.writeOnFile_read(self.signals[0], f"{staticPath}multipled_signal.txt")

    def get_multiplication_number(self):
        print("in get number for multiplication")
        nosignal=tk.Label(self.right_section, text="please read a signal first")
        if (len(self.signals) >= 1):
            self.destroyFrames()
            nosignal.destroy()
            self.multiply_signals_frame = guiHelpers.right_frame(self.right_section)

            entry = tk.Entry(self.multiply_signals_frame)
            entry.place(x=200, y=200)

            back_btn = tk.Button(self.multiply_signals_frame, text="construct signal", bg="#808080", fg="white", width=15, height=2, command=lambda:self.checkNumber(entry))
            back_btn.place(x= 200, y=300)
         
        else:
            nosignal.place(x=200,y=200)


    def checkNumber(self, entry):
        check = entry.get()
        validNumber=tk.Label(self.multiply_signals_frame, text="please enter a number")
        if(utils.is_float(check)):
            validNumber.destroy()
            self.to_multiply_signals(check)
        else:
            validNumber.place(x=200, y=100)

    def to_square_signals(self):
        self.signals = self.baseSignals
        print("in square signals")
        self.destroyFrames()
        self.square_signals_frame = guiHelpers.right_frame(self.right_section)
        nosignal = tk.Label(self.right_section, text="please read a signal first or read only one")

        signal = (len(self.signals)==1)
        
        if signal:
            # Square the y values using a built-in map function
            y=self.signals[0].y
            y = list(map(lambda i: i ** 2, y))
            self.graph.clear()
            self.graph.discreteGraph(self.square_signals_frame, self.signals)
            self.graph.continousGraph(self.square_signals_frame, self.signals)
            print("signal-1 square")
            test.SignalSamplesAreEqual(f'{testPath}Output squaring signal 1.txt', self.signals[0].x, y)
            # files.writeOnFile_read(self.signals[0], f"{staticPath}squared_signal.txt")
        else:
            # Show message if no signal is loaded
            nosignal.place(x=170, y=200)

    
    def get_normalize_ratio(self):
        print("in get normalization ratio")
        self.destroyFrames()
        nosignal=tk.Label(self.right_section, text="please read a signal first")
        if (len(self.signals) == 1):
            self.destroyFrames()
            nosignal.destroy()
            self.normalization_frame = guiHelpers.right_frame(self.right_section)

            combo = ttk.Combobox(self.normalization_frame, values=["[-1,1]", "[0,1]"], state="readonly", width=27)
            combo.set("choose range")
            combo.place(x=180, y=200)

            back_btn = tk.Button(self.normalization_frame, text="construct signal", bg="#808080", fg="white", width=15, height=2, command=lambda:self.check_ratio(combo))
            back_btn.place(x= 200, y=300)
         
        else:
            nosignal.place(x=200,y=200)
        
    def check_ratio(self, entry):
        val = entry.get()
        validRange =tk.Label(self.normalization_frame, text="please select a range")
        if val != 'choose range':
            if val == '[-1,1]':
                self.to_normalization('1')
            else:
                self.to_normalization('2')
        else:
            validRange.place(x=200, y=100)


    def to_normalization(self, range):
        self.signals = self.baseSignals
        print("in normalization")
    
        self.destroyFrames()
        self.normalization_frame = guiHelpers.right_frame(self.right_section)
        noSignalError = tk.Label(self.right_section, text="please read a signal first")
        # range of normalization [-1,1]
        if(range == '1'):
            new_min, new_max = -1, 1
        else:
            new_min, new_max = 0, 1
        signal = (len(self.signals)==1)
        if signal:
            y = self.signals[0].y
            noSignalError.destroy()
            y_min, y_max = np.min(y), np.max(y)
            y = (y - y_min) / (y_max - y_min) * (new_max - new_min) + new_min

            self.signals[0].x = np.arange(1, len(y) + 1)
            self.graph.clear()
            self.graph.discreteGraph(self.normalization_frame, self.signals)
            self.graph.continousGraph(self.normalization_frame, self.signals)
            print("signal-1 normalization from -1 to 1")
            test.SignalSamplesAreEqual(f'{testPath}normalize of signal 1 (from -1 to 1)-- output.txt', self.signals[0].x, y)
            print("signal-2 normalization from 0 to 1")
            test.SignalSamplesAreEqual(f'{testPath}normlize signal 2 (from 0 to 1 )-- output.txt', self.signals[0].x, y)
          
            # files.writeOnFile_read(signal, f"{staticPath}normalization.txt")

        else:
            noSignalError.place(x=200,y=200)
            
    def to_accumulation(self):
        self.signals = self.baseSignals
        self.destroyFrames()
        self.accumulation_frame = guiHelpers.right_frame(self.right_section)
        noSignalError = tk.Label(self.right_section, text="please read a signal first")

        signal = (len(self.signals)==1)
        if signal:
            noSignalError.destroy()
            accumulation = []
            accumulation.append(0)
            for i in range(1, len(self.signals[0].y)):
                tmp = i + accumulation[i-1]
                accumulation.append(tmp)
            self.graph.clear()
            self.graph.discreteGraph(self.accumulation_frame, self.signals)
            self.graph.continousGraph(self.accumulation_frame, self.signals)
            self.signals[0].y = accumulation
            print("signal-1 accumulation")
            test.SignalSamplesAreEqual(f'{testPath}output accumulation for signal1.txt', self.signals[0].x, self.signals[0].y)
            # files.writeOnFile_read(self.signals[0], f"{staticPath}accumulation.txt")

        else:
            noSignalError.place(x=200,y=200)
    
    def select_files(self):
        # Open file dialog to select multiple text files
        file_paths = filedialog.askopenfilenames(
            title="Select Text Files",
            filetypes=[("Text Files", "*.txt")],
            multiple=True
        )
        
        for file in file_paths:
            self.signals.append(files.getSignalFromFile(file))
        
        self.baseSignals = self.signals
