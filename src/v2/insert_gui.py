import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
import tkinter.scrolledtext as tkscrolled
from insert_db import insert_game, OPPONENTS, select_opponent_data



class InsertDataWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Northeastern Huskies Hockey - Insert Game into Database")
        self.file_frame = FileFrame(self)
        self.query_frame = QueryFrame(self)
        
        

        self._pack_frames()
        
    
    def _pack_frames(self):
        self.geometry("800x500")
        self.file_frame.grid(column=0, row=0)
        self.query_frame.grid(column=10, row=0)
        
        

class FileFrame(tk.LabelFrame):
    def __init__(self, container):
        super().__init__(container, text= "Insert Game File")
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
    
class QueryFrame(tk.LabelFrame):
    def __init__(self, container):
        super().__init__(container, text= "View Opponent:")
        self.select_opponent = tk.Label(master=self, text="Select Opponent:")
        self.opponent_box = ttk.Combobox(master=self,state="readonly", values = OPPONENTS, height=5)
        self.log_display = tkscrolled.ScrolledText(master=self, wrap='word')
        self.view_button = tk.Button(master=self, text="View Data", command=self.get_game_data)
        
        self._pack_widgets()
        
    def _pack_widgets(self):
        self.select_opponent.grid(row=0,column=1)
        self.opponent_box.grid(row=1,column=1)
        self.view_button.grid(row=2,column=1)
        self.log_display.grid(row=3, column=1)
        
        
        
        
    def get_game_data(self):
        opponent = self.opponent_box.get()
        
        display_table = select_opponent_data("2023-2024/hockey.db", opponent, "this will be a selector")
        self.log_display.delete("1.0", END)
        self.log_display.insert("1.0", display_table.to_markdown(index=False))
        return display_table
        
        
        
        
if __name__ == '__main__':
    window = InsertDataWindow()
    
    window.mainloop()
    
    