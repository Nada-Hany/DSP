import guiHelpers, files, utils, test
import tkinter as tk
from tkinter import ttk
from utils import Button
from tkinter import filedialog
import math 


staticPath = './files/task3/'

class Task3:

    def __init__(self, root, main):
        self.root =root
        self.left_section, self.right_section = self.sections()
        self.quantization_frame = guiHelpers.right_frame(self.right_section)
        self.method_comboBox = ttk.Combobox(self.left_section, values=["Bits", "Levels"], state="readonly", width=15)
        self.value_box = tk.Entry(self.left_section, width=18)
        self.signals = []
        self.baseSignals = []
        self.main = main
    
    def sections(self):
        
        left_frame, right_frame = guiHelpers.sections(self.root)
       
        btn_x = guiHelpers.btn_x
        
        back_btn = tk.Button(left_frame, text="back",compound=tk.CENTER, command= lambda:self.goBack(), width=3, height=1, borderwidth=0)
        back_btn.place(x= btn_x, y=guiHelpers.back_btn_y)


        read_signal_btn = Button(btn_x, 40, "Read Signal", lambda:self.select_files())
        get_method_btn = Button(btn_x, 120, "Select Method", lambda:self.to_select_method())
        gte_quantization = Button(btn_x, 200, "Get Quantization", lambda:self.show_quantization())
           
        buttons = []
        buttons.append(read_signal_btn)
        buttons.append(get_method_btn)
        buttons.append(gte_quantization)
        for btn in buttons:
            tmp = tk.Button(left_frame, text=f"{btn.name}", bg="#808080", fg="white", width=15, height=2, command=btn.onClick)
            tmp.place(x=btn.x, y=btn.y)
            
        return  left_frame, right_frame


    def destory_all(self):
        self.quantization_frame.destroy()

    
    def show_quantization(self):
        self.destory_all()
        self.quantization_frame = guiHelpers.right_frame(self.right_section)
        noSignalError = tk.Label(self.right_section, text="please read a signal first")
        noMethodError = tk.Label(self.right_section, text="please select a method first")
        print(self.method_comboBox.get())
        if self.method_comboBox.get() == 'choose method' or self.value_box.get()=='':
            noMethodError.place(x=200,y=200)
            return
        if not utils.is_int(self.value_box.get()):
            noMethodError.place(x=200,y=200)
            return
        
        if len(self.signals) == 1:

            style = ttk.Style()
            style.configure("Treeview", rowheight=40)  # Set row height (in pixels)
            self.get_quantization_value()
            # Define columns

            if self.method_comboBox.get() == 'Levels':
                columns = ("index", "encoded", "quantization", "error")
            else:
                columns = ("encoded", "quantization")


            signal = self.signals[0]

            # Create Treeview widget with defined row height
            tree = ttk.Treeview(self.quantization_frame, columns=columns, show="headings", style="Treeview")
            tree.pack(fill=tk.BOTH, expand=True)

            data = []

            if self.method_comboBox.get() == 'Levels':
                for i in range(signal.sampleNo):
                    data.append((signal.intervals[i], signal.encoded[i], signal.quantization[i], signal.error[i]))
                tree.heading("index", text="index")
                tree.heading("encoded", text="encoded")
                tree.heading("quantization", text="quantization")
                tree.heading("error", text="error")

                tree.column("index", anchor=tk.CENTER, width=80)
                tree.column("encoded", anchor=tk.CENTER, width=100)
                tree.column("quantization", anchor=tk.CENTER, width=120)
                tree.column("error", anchor=tk.CENTER, width=80)
            else:
                for i in range(signal.sampleNo):
                    data.append((signal.encoded[i], signal.quantization[i]))

                tree.heading("encoded", text="encoded")
                tree.heading("quantization", text="quantization")

                tree.column("encoded", anchor=tk.CENTER, width=120)
                tree.column("quantization", anchor=tk.CENTER, width=120)

            # Configure row colors
            tree.tag_configure("oddrow", background="lightgrey")
            tree.tag_configure("evenrow", background="darkgrey")

            # Add some example data (optional) with alternating colors
        
            # Insert data into the table with alternating row colors
            for index, row in enumerate(data):
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                tree.insert("", tk.END, values=row, tags=(tag,))
        else:
            noSignalError.place(x=200,y=200)

    def get_quantization_value(self):
        signal = self.signals[0]
        minValue = min(signal.y)
        maxValue = max(signal.y)

        levels = 0
        if(self.method_comboBox.get() == 'Levels'):
            levels =  int(self.value_box.get())
        else:
            levels = int(pow(2, int(self.value_box.get())))

        delta = (maxValue - minValue) / levels

        ranges = []
        start = minValue
        end = start + delta
        i = 0
        flag = True
        # calculating range intervals and their midpoints
        while flag:
            ranges.append([round(start, 2), round(end, 2)])
            self.signals[0].midpoints.append(round(((start+end)/2), 3))
            start = end
            end += delta
            if round(start, 3) >= maxValue:
                break
            i+=1

        # getting which interval each sample belong to 
        for sample in range(signal.sampleNo):
            for rang in ranges:
                if signal.y[sample] >= rang[0] and signal.y[sample] <= rang[1]:
                    signal.intervals.append(ranges.index(rang))
                    break
        
        # calculating quantization value and error
        signal.quantization = list(map(lambda x : round(signal.midpoints[x], 4), signal.intervals))
        for i in range(signal.sampleNo):
            signal.error.append(round(signal.midpoints[signal.intervals[i]] - signal.y[i], 3))
        
        # setting the encoded binary 
        bits_required = math.floor(math.log2(levels + 1))
        signal.encoded = list(map(lambda x : bin(x)[2:].zfill(bits_required), signal.intervals))
        
        signal.intervals = list(map(lambda x: x+1, signal.intervals))

        self.signals[0] = signal

        print("test case 1")
        test.QuantizationTest1(f'{staticPath}Quan1_Out.txt', signal.encoded ,signal.quantization)

        print("test case 2")
        test.QuantizationTest2(f'{staticPath}Quan2_Out.txt', signal.intervals, signal.encoded, signal.quantization, signal.error)



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

    
    def to_select_method(self):
        self.method_comboBox.set("choose method")
        self.method_comboBox.place(x=guiHelpers.btn_x, y=250)
        self.value_box.place(x=guiHelpers.btn_x, y=280)


    def goBack(self):
        print("in go back func")
        self.quantization_frame.destroy()
        self.right_section.destroy()
        self.left_section.destroy()
        self.main.main_window()
        del self

