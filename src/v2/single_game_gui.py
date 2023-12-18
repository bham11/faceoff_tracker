import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
import tkinter.scrolledtext as tkscrolled


class GameViewerWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Northeastern Huskies Hockey - View Game")
        
        

        self._pack_frames()
        
    
    def _pack_frames(self):
        self.geometry("1050x500")
        self.file_frame.grid(column=0, row=0, ipadx=10, sticky=NW)
        self.query_frame.grid(column=15, row=0)