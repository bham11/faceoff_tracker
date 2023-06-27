import tkinter as tk
from tkinter import *
import tkinter.scrolledtext as tkscrolled
from PIL import ImageTk, Image


ROOT = '/Users/brandonhampstead/Documents/NortheasternHockey/faceoff_tracker/src'



class HockeyWindow(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Northeastern Huskies Hockey - Faceoff Tracker")
        self.game_info_frame = GameInfoFrame(self)
        self.faceoff_input_frame = FaceoffInputFrame(self)
        self.rink_frame = RinkFrame(self)
        #    self.stats_frame = stats

        self._pack_frames()
       
       
       
    def _pack_frames(self):
        self.game_info_frame.pack(side='top', ipady=10)
        self.rink_frame.pack(side='left', fill='both', expand=True)
        self.faceoff_input_frame.pack(side='left', fill='both', expand=True)
        # self.stats_frame.pack(side='left', fill='both', expand=True)
       
 

class GameInfoFrame(tk.LabelFrame):
    
    def __init__(self, container):
        super().__init__(container, text= "Options")
        
        self.what_period = tk.StringVar(value="1rst")
        self.first_period = tk.Radiobutton(master=self, text="1rst", value="1rst", variable=self.what_period)
        self.second_period = tk.Radiobutton(master=self, text="2nd", value="2nd", variable=self.what_period)
        self.third_period = tk.Radiobutton(master=self, text="3rd", value="3rd", variable=self.what_period)
        self.ot = tk.Radiobutton(master=self, text="OT", value="OT", variable=self.what_period)
        self.strength = tk.StringVar(value="even")
        self.even = tk.Radiobutton(master=self, text="Even", value="even", variable=self.strength)
        self.pk = tk.Radiobutton(master=self, text="PK", value="pk", variable=self.strength)
        self.pp = tk.Radiobutton(master=self, text="PP", value="pp", variable=self.strength)
        
        self._pack_widgets()
        
    
    def _pack_widgets(self):
        self.first_period.grid(row=0, column=1)
        self.second_period.grid(row=0, column=3)
        self.third_period.grid(row=0, column=5)
        self.ot.grid(row=0, column=7)
        self.even.grid(row=1, column=2)
        self.pp.grid(row=1, column=4)
        self.pk.grid(row=1, column=6)
        
class FaceoffInputFrame(tk.LabelFrame):
    def __init__(self, container):
        super().__init__(container, text="Inputs:")
        
        self.config(width=200)
        self.what_zone = tk.Label(master=self, text="What Zone (1-9)?")
        self.zone = tk.Entry(master=self, width=2)
        self.what_husky = tk.Label(master=self, text="What Husky?")
        self.husky = tk.Entry(master=self, width=2)
        self.what_opp = tk.Label(master=self, text="What Opp?")
        self.opp = tk.Entry(master=self, width=2)
        self.ask_result = tk.Label(master=self, text="Result (W/L)?")
        self.result = tk.Entry(master=self, width=2)
        
        self.clear_entries = tk.Button(master=self, text="Clear", command=self.clear_ents)

        self.log = tkscrolled.ScrolledText(master=self, width=40, wrap='word')
        
        self._pack_widgets()
    
    def clear_ents(self):
        self.zone.delete(0, END)
        self.husky.delete(0, END)
        self.opp.delete(0, END)
        self.result.delete(0, END)
        self.zone.focus()    
    
    def _pack_widgets(self):
        self.what_zone.grid(row=1, column=1)
        self.zone.grid(row=1, column=2)
        self.what_husky.grid(row=2, column=1)
        self.husky.grid(row=2, column=2)
        self.what_opp.grid(row=3, column=1)
        self.opp.grid(row=3, column=2)
        self.ask_result.grid(row=4, column=1)
        self.result.grid(row=4, column=2)
        self.clear_entries.grid(row=5, column=2)
        self.log.grid(row=6, columnspan=5)   


class RinkFrame(tk.LabelFrame):
    def __init__(self, container):
        super().__init__(container, text= "Rink Mappings")
        
        first_third = f'{ROOT}/utils/first_and_third_rink.png'
        second = f'{ROOT}/utils/second_period_rink.png'    
        photo = Image.open(first_third)
        re_sized_photo = photo.resize((500, 200))
        sec_photo = Image.open(second).resize((500, 200))
        self.hockey_rink = ImageTk.PhotoImage(re_sized_photo)
        self.second_rink = ImageTk.PhotoImage(sec_photo)
        
        self.rink_photo = tk.Label(self, image=self.hockey_rink)
        self.second_rink_photo = tk.Label(self, image=self.second_rink)
        
        self._pack_widgets()
        
    def _pack_widgets(self):
        self.rink_photo.pack()
        self.second_rink_photo.pack()