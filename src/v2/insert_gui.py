import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from insert_db import insert_game, OPPONENTS



class InsertDataWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Northeastern Huskies Hockey - Insert Game into Database")
        self.file_frame = FileFrame(self)
        
        

        self._pack_frames()
        
    
    def _pack_frames(self):
        self.geometry("500x500")
        self.file_frame.grid(column=0, row=0, rowspan=100)
        
        

class FileFrame(tk.LabelFrame):
    def __init__(self, container):
        super().__init__(container, text= "Select Game File")
        self.opponent_box = ttk.Combobox(master=self,state="readonly", values = OPPONENTS, height=5)
        self.select_opponent = tk.Label(master=self, text="Select Opponent:")
        self.scrollbar = Scrollbar(master=self, orient=HORIZONTAL)
        self.display_file_name = tk.Entry(master=self, xscrollcommand=self.scrollbar.set)
        self.game_file_name = tk.Button(master=self, text="Select Game", command=self.get_filename)
        self.send_button = tk.Button(master=self, text="Insert Data", command=self.send_game_data)
        
        
        
        
        self._pack_widgets()
        
    def get_filename(self):
        value = filedialog.askopenfilename()
        self.display_file_name.delete(0, END)
        self.display_file_name.insert(0, value)
        self.display_file_name.config(state=DISABLED)
        
    def send_game_data(self):
        game_log = self.display_file_name.get()
        if game_log.endswith(".csv"):
            insert_game("2023-2024/hockey.db", self.opponent_box.get(), game_log)
        
    def _pack_widgets(self):
        self.select_opponent.grid(row=1,column=0)
        self.opponent_box.grid(row=11, column=0)
        self.display_file_name.grid(row=30, column=0,)
        self.scrollbar.grid(row=32, column=0)
        self.scrollbar.config(command=self.display_file_name.xview)
        self.game_file_name.grid(row=34, column=0)
        self.send_button.grid(row=36, column=0)
        
if __name__ == '__main__':
    window = InsertDataWindow()
    
    window.mainloop()
    
    