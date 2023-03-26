# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 22:20:24 2023

@author: shubh
"""

class mongo:
    import sys
    import pymongo
    import pandas as pd
    from tkinter import Tk, Label, Frame, Scrollbar, Text, Button
    root = Tk()  
    
    def __init__(self):
        self=self
    def tkint(df):
        import sys
        import pymongo
        import pandas as pd
        from tkinter import Tk, Label, Frame, Scrollbar, Text, Button
        
        
        df=df.drop(['_id'],axis=1)
        
        # Create a Tkinter window
        root = Tk()
        root.title('NoSQL Output in GUI')
        
        # Create a Frame to hold the DataFrame
        frame = Frame(root)
        frame.pack()

        # Create a Label for the DataFrame
        df_label = Label(frame, text='Query Result:')
        
        df_label.pack()
        
        # Create a Text widget for the DataFrame
        df_text = Text(frame, height=40, width=200)
        
        # Create a Scrollbar for the Text widget
        scrollbar = Scrollbar(frame, command=df_text.yview)
        df_text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        df_text.pack(side='left', fill='both', expand=True)
        
        # Insert the DataFrame into the Text widget
        df_text.insert('1.0', df.to_string())
        
        # Run the Tkinter event loop
        root.mainloop()
        root.destroy()
        sys.exit()
        '''
    def close_window():
        import sys
        from tkinter import Tk, Label, Frame, Scrollbar, Text, Button

        root = Tk()        
        root.destroy()
        sys.exit()

        # Create a button to close the window
    close_button = Button(root, text='Close', command=close_window)
    close_button.pack()
        '''

