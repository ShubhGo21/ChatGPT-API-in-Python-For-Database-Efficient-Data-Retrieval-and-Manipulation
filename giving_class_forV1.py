# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:09:01 2023

@author: shubh
"""

class MyClass:
    def __init__(self):
        self=self
    def tkint(column_names,results):
        import tkinter as tk
        from tkinter import ttk
        
        app = tk.Tk()
        table = ttk.Treeview(app, columns=column_names, show='headings')

        # Configure columns
        for col in column_names:
            table.heading(col, text=col)
            table.column(col, width=100)
            table.tag_configure(col, anchor='center')
        
        # Insert data rows
        for i, row in enumerate(results):
            table.insert('', 'end', values=row)
            
        # Add Treeview to layout
        table.pack()
        
        
        # Start event loop
        app.mainloop()
        





