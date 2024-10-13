import tkinter as tk
from tkinter import ttk

from utils import Button
from utils import ConstructedSignal
import utils, signals, files
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.interpolate import  make_interp_spline


# Input Labels and Fields
labels_text = ["Amplitude", "Phase Shift", "Analog Frequency", "Sampling Frequency", "Signal Generator"]
entries = {}

# Place labels and entries
positions = [
    (60, 50), (300, 50),  # Row 1
    (60, 120), (300, 120),  # Row 2
    (60, 200) # Row 3
]



def to_generate_signal(rightFrame):
    frame = right_frame(rightFrame)
    generate_signal_input(frame)
    print("to_generate_signal btn triggered")

def display_read_signal(root):
    file  = utils.browse_file()
    frame = right_frame(root)
    if file:
        #TODO display graph and construct signal 
        signal = files.getSignalFromFile(file)
        fig = Figure(figsize=(5, 2.1), dpi=100)
        plot = fig.add_subplot(1, 1, 1)

        # Sample data for discrete points
        y = [float(i) for i in signal.sampleList]
        x = [i for i in range(0, len(y))]
        
        # drawing y value for each point
        for i in range(len(x)):
            # plot.text(x[i], y[i], f'{y[i]}', fontsize=9, ha='right', va='bottom')
            plot.plot([i, i], [0, y[i]], 'b-') 

        plot.scatter(x, y, color="blue", marker="x")  # Discrete points with circular markers
        plot.grid(True)
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # continous ----
        fig = Figure(figsize=(5, 2.1), dpi=100)
        plot = fig.add_subplot(1, 1, 1)

        
        x_y_Spline = make_interp_spline(x=x, y=y)
        x_quad = np.linspace(min(x), max(x), 500)
        y_quad = x_y_Spline(x_quad)


        plot.plot(x_quad, y_quad)
        plot.grid(True)
        plot.set_xlabel("time")
        plot.set_ylabel("signal")
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)


        
    print("in read file func")

def to_read_file(rightFrame):
    frame = right_frame(rightFrame)
    get_file = tk.Button(frame, text="Select File", bg="#808080", fg="white", width=15, height=2, command=lambda:display_read_signal(frame))
    get_file.place(x=380, y=400)
    print("in read file func")

#left section for all buttons - right section for displaying 
def sections(root):
    left_frame = tk.Frame(root, width=150, height=500, bg="#d3d3d3")
    left_frame.pack(side="left", fill="y")
    left_frame.pack_propagate(False)

    right_frame = tk.Frame(root, width=450, height=500, bg="white")
    right_frame.pack(side="right", fill="both", expand=True)
    right_frame.pack_propagate(False)
    btn_x = 20
    generate_signal_btn = Button(btn_x, 40, "Generate Signal", lambda:to_generate_signal(right_frame))
    read_file_btn = Button(btn_x, 120, "Read File", lambda:to_read_file(right_frame))
    buttons = []
    buttons.append(generate_signal_btn)
    buttons.append(read_file_btn)
    for btn in buttons:
        tmp = tk.Button(left_frame, text=f"{btn.name}", bg="#808080", fg="white", width=15, height=2, command=btn.onClick)
        tmp.place(x=btn.x, y=btn.y)
    
    return right_frame
  

def right_frame(root):
    frame = tk.Frame(root, width=520, height=480, bg="#d3d3d3")  # Darker frame color
    frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

    return frame

def display_graph(error_lbl, old_frame, root):
    error_lbl.place(x=900, y=300)
    #valid inputs -> construct signal obj and go to displaying the graphs
    if(utils.valid_inputs(entries, error_lbl)):
        signal_data = utils.get_data(entries) 
        signal, time = signals.generate_signal(signal_data, error_lbl)
        if signal:
            print(signal.func)
            if signal.func=='Sine':
                files.writeOnFile(signal, 'sin_output.txt')
            else:
                files.writeOnFile(signal, 'cos_output.txt')

            old_frame.destroy()
            frame = right_frame(root)
  
            fig = Figure(figsize=(5, 2), dpi=100)
            plot = fig.add_subplot(1, 1, 1)
    
            plot.scatter(time, signal.y_values, color="blue", marker="x")  # Discrete points with circular markers
            plot.set_xlabel("time")
            plot.set_ylabel("signal")
            plot.grid(True)
            # plot.set_xlim(0, 1)
            # Embed the figure into the Tkinter canvas
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            x_y_Spline = make_interp_spline(x=time, y=signal.y_values)
            x_quad = np.linspace(time.min(), time.max(), 500)
            y_quad = x_y_Spline(x_quad)

            fig = Figure(figsize=(5, 2), dpi=100)
            plot = fig.add_subplot(1, 1, 1)
            plot.grid(True)
            plot.plot(x_quad, y_quad)  
            plot.set_xlabel("time")
            plot.set_ylabel("signal")

            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

            print("in display graphs")
    else:
        error_lbl.place(x=200, y=300)


def generate_signal_input(root):
    
    frame = right_frame(root)
    #label for trigerring errors 
    error_label = tk.Label(frame, text="enter a valid input")
    # error_label.place(x=200,y=300)
    for i, (text, pos) in enumerate(zip(labels_text, positions)):
        label = tk.Label(frame, text=text.lower(), bg="#d3d3d3")
        label.place(x=pos[0], y=pos[1])
        
        if text == "Signal Generator":
            combo = ttk.Combobox(frame, values=["Sine", "Cosine"], state="readonly", width=27)
            combo.set("choose function")
            combo.place(x=pos[0], y=pos[1]+30)
            entries[text] = combo
        else:
            entry = tk.Entry(frame, width=30)
            entry.place(x=pos[0], y=pos[1]+30)
            entries[text] = entry

    # Display Signal Button
    display_button = tk.Button(frame, text="Display Signal", bg="#808080", fg="white", width=15, height=2, command=lambda:display_graph(error_label, frame, root))
    display_button.place(x=380, y=400)


def main_window():
    root = tk.Tk()
    root.geometry("700x500")
    root.configure(bg="#d3d3d3")
    root.title("Signal Generator")

    right_frame = sections(root)
    generate_signal_input(right_frame)

    root.mainloop()


main_window()
