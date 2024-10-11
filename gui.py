import tkinter as tk
from tkinter import ttk
from utils import Button
from utils import Signal
import utils
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Input Labels and Fields
labels_text = ["Amplitude", "Phase Shift", "Analog Frequency", "Sampling Frequency", "Samples Number", "Signal Generator"]
entries = {}

# Place labels and entries
positions = [
    (60, 50), (300, 50),  # Row 1
    (60, 120), (300, 120),  # Row 2
    (60, 200), (300, 200) # Row 3
]

def to_generate_signal(rightFrame):
    frame = right_frame(rightFrame)
    generate_signal_input(frame)
    print("to_generate_signal btn triggered")

#left section for all buttons - right section for displaying 
def sections(root):
    left_frame = tk.Frame(root, width=150, height=500, bg="#d3d3d3")
    left_frame.pack(side="left", fill="y")
    left_frame.pack_propagate(False)

    right_frame = tk.Frame(root, width=450, height=500, bg="white", highlightbackground='black', highlightthickness=2)
    right_frame.pack(side="right", fill="both", expand=True)
    right_frame.pack_propagate(False)

    generate_signal_btn = Button(20, 40, "Generate Signal", lambda:to_generate_signal(right_frame))
    buttons = []
    buttons.append(generate_signal_btn)
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
        old_frame.destroy()
        frame = right_frame(root)
        # test = tk.Label(frame, text="in graph window")
        # test.place(x=200,y=300)

        # dummy graph
        fig = Figure(figsize=(5, 2), dpi=100)
        plot = fig.add_subplot(1, 1, 1)
        # Sample data for discrete points
        x = [1, 2, 3, 4, 5]
        y = [2, 3, 5, 7, 11]

        plot.scatter(x, y, color="blue", marker="x")  # Discrete points with circular markers
        plot.set_xlabel("X-axis")
        plot.set_ylabel("Y-axis")
        plot.set_title("Discrete Points Plot")

        # Embed the figure into the Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        fig = Figure(figsize=(5, 2), dpi=100)
        plot = fig.add_subplot(1, 1, 1)
        plot.plot([1, 2, 3, 4, 5], [1, 4, 2, 5, 3])  # Example data

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
