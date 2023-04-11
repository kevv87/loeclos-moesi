import tkinter as tk
from tkinter import ttk

from code.ui.graphic_tkinter.graphic_processor import GraphicProcessor

class GUI():
    def creating_processors(self):
        # Create a container for the processors with a scrollbar
        container = tk.Frame(self.root)
        container.pack(side="top", fill="both", expand=True)
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand=scrollbar.set)

        # Pack the scrollbar and canvas
        scrollbar.pack(side="bottom", fill="x")
        canvas.pack(side="top", fill="both", expand=True)

        # Create a Frame to hold the processors
        processors_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=processors_frame, anchor="nw")

        frames = []
        for i in range(4):
            graphic_proc = GraphicProcessor(self.root, i, processors_frame)

        processors_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def creating_memory(self):
        memory_frame = tk.Frame(self.root, borderwidth=2, relief=tk.GROOVE)
        memory_frame.pack(side=tk.TOP, padx=10, pady=10)

        memory_label = tk.Label(memory_frame, text="Main Memory")
        memory_label.pack()

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Loeclos Moesi")

        self.creating_processors()
        self.creating_memory()

        self.root.mainloop()
