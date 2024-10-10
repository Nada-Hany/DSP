import tkinter as tk
from tkinter import ttk
from utils import Button


# Input Labels and Fields
labels_text = ["Amplitude", "Phase Shift", "Analog Frequency", "Sampling Frequency", "Samples Number", "Signal Generator"]
entries = {}

# Place labels and entries
positions = [
    (60, 50), (300, 50),  # Row 1
    (60, 120), (300, 120),  # Row 2
    (60, 200), (300, 200) # Row 3
]

#left section for all buttons
def left_section(root):
    left_frame = tk.Frame(root, width=150, height=500, bg="#d3d3d3")
    left_frame.pack(side="left", fill="y")

    generate_signal_btn = Button(20, 40, "Generate Signal")
    buttons = []
    buttons.append(generate_signal_btn)
    for btn in buttons:
        tmp = tk.Button(left_frame, text=f"{btn.name}", bg="#808080", fg="white", width=15, height=2)
        tmp.place(x=btn.x, y=btn.y)
  

#entrying values for generating a signal window
def generate_signal(root):
    right_frame = tk.Frame(root, width=450, height=500, bg="white")
    right_frame.pack(side="right", fill="both", expand=True)

    frame = tk.Frame(right_frame, width=520, height=480, bg="#d3d3d3")  # Darker frame color
    frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame


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
    display_button = tk.Button(frame, text="Display Signal", bg="#808080", fg="white", width=15, height=2)
    display_button.place(x=380, y=400)


def main_window():
    root = tk.Tk()
    root.geometry("700x500")
    root.configure(bg="#d3d3d3")
    root.title("Signal Generator")

    left_section(root)
    generate_signal(root)

    root.mainloop()


main_window()
