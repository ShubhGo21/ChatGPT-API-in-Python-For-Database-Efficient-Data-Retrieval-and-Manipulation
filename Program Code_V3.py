# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 11:05:40 2023

@author: shubh
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 09:46:40 2023

@author: shubh
"""
# MongoDB work pending

import re
import sys
import json
import openai
import pymongo
import cx_Oracle
import mysql.connector
from pymongo import MongoClient

import tkinter as tk
from tkinter import *
from tkinter import simpledialog
sys.path.append("D:/Mini")


class Application(tk.Frame):
    label_font = ("Times New Roman", 14)
    button_font = ("Times New Roman", 12)
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("400x150")  # set the window size to 400x200 pixels
        self.master.title("Database Connector")  # set the title of the window
        self.pack()
        self.create_widgets()
        self.DB = None
        
       
        
    def create_widgets(self):
        self.label_frame = tk.Frame(self)
        self.label_frame.pack(side="top")
        
        import sys
        sys.path.append("D:/Mini")
        
        self.label_image = tk.PhotoImage(file=r"D:/Mini/dbs.png")
        self.label_image = self.label_image.subsample(12)
        self.label = tk.Label(self.label_frame, text="Choose database to connect:", font=self.label_font,
                              compound="bottom", image=self.label_image)
        self.label.pack(side="left")
    
        self.selected_DB = tk.IntVar()
        self.selected_DB.set(1)
        
        self.label_image1 = tk.PhotoImage(file=r"D:/Mini/oracle.png")
        self.label_image1 = self.label_image1.subsample(14)
        self.SQLplus_button = tk.Radiobutton(self, text="Oracle",compound="bottom", image=self.label_image1, variable=self.selected_DB, value=1, font=self.button_font)
        self.SQLplus_button.pack(side="left")
        
        self.label_image2 = tk.PhotoImage(file=r"D:/Mini/mysql.png")
        self.label_image2 = self.label_image2.subsample(10)
        self.MySQL_button = tk.Radiobutton(self, text="MySQL",compound="bottom", image=self.label_image2, variable=self.selected_DB, value=2, font=self.button_font)
        self.MySQL_button.pack(side="left")
    
        self.label_image3 = tk.PhotoImage(file=r"D:/Mini/mongo2.png")
        self.label_image3 = self.label_image3.subsample(18)
        self.MongoDB_button = tk.Radiobutton(self, text="Mongo",compound="bottom", image=self.label_image3, variable=self.selected_DB, value=3, font=self.button_font)
        self.MongoDB_button.pack(side="left")
    
        self.run_button = tk.Button(self, text="Run",fg="green", command=self.run_selected_DB, font=self.button_font)
        self.run_button.pack(side="bottom")
    
        self.quit = tk.Button(self, text="Quit", fg="red", command=self.master.destroy, font=self.button_font)
        self.quit.pack(side="bottom")

        
    def run_selected_DB(self):
        selected_db = self.selected_DB.get()
        if selected_db == 1:
            self.SQLplus()
        elif selected_db == 2:
            self.MySQL()
        elif selected_db == 3:
            self.MongoDB()


    def SQLplus(self):
        self.DB = 1
        self.label["text"] = "Selected SQLplus"
        self.query = simpledialog.askstring("Enter Your query :", "Please enter your query:")
        self.col = simpledialog.askstring("Enter table name :", "Please enter the table name:")
        
        openai.api_key = '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'
        completion = openai.Completion.create(
          model="text-davinci-003",
          prompt="{} from {} query for oracle do not use limit".format(self.query, self.col),
          max_tokens=75,
          temperature=0)
        
        d=(completion.choices[0]['text'])
        print(d)
        # Establish a connection to the Oracle database
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='XE')
        conn = cx_Oracle.connect(user='system', password='shubh123', dsn=dsn_tns)
        
        # Execute a query and fetch the results
        b=d.split(";") #sometime output repeats after ; hence using split and then its [0]th index at below line
        query = '{}'.format(b[0])
        
        #query="select * from emp"
        c=query.lower()
        cursor = conn.cursor()
        
        if c.find("update")>=0 or c.find("alter")>=0 or c.find("insert")>=0:
            cursor.execute(query)
            # Commit the changes
            conn.commit()
            print("Updated..")
            cursor.execute("select * from {}".format(self.col))
            results = cursor.fetchall()
            column_names = [i[0].lower() for i in cursor.description]
            cursor.close()
            conn.close()
            Application.tkint(column_names, results)
            
        elif c.find("select")>=0:
            cursor.execute(query)
            results = cursor.fetchall()
            column_names = [i[0].lower() for i in cursor.description]
            cursor.close()
            conn.close()
            Application.tkint(column_names,results)
        
        
    def MySQL(self):
        self.DB = 2
        self.label["text"] = "Selected MySQL"
        query = simpledialog.askstring("Enter Your query :", "Please enter your query:")
        table_name = simpledialog.askstring("Enter table name :", "Please enter the table name:")
        openai.api_key = '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'
        completion = openai.Completion.create(
            model="text-davinci-003",
            prompt="{} from {} table query for mysql".format(query, table_name),
            max_tokens=75,
            temperature=0
        )
        d=(completion.choices[0]['text'])
        c=d.lower()
        print(c)
        
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root123",
            database="sakila")
        
        cursor = conn.cursor()
        if c.find("update")>=0 or c.find("alter")>=0 or c.find("insert")>=0:
            cursor.execute(d)
            # Commit the changes
            conn.commit()
            print("Updated..")
            cursor.execute("select * from {}".format(table_name))
            results = cursor.fetchall()
            column_names = [i[0].lower() for i in cursor.description]
            cursor.close()
            conn.close()
            Application.tkint(column_names, results)
            
        elif c.find("select")>=0:
            cursor.execute(d)
            column_names = [i[0].lower() for i in cursor.description]
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            Application.tkint(column_names, results)
            
            
    def MongoDB(self):
        import re
        import pandas as pd
        self.DB = 3
        self.label["text"] = "Selected MongoDB"
        query = simpledialog.askstring("Enter Your query :", "Please enter your query:")
        col_name = simpledialog.askstring("Enter Collection Name :", "Please enter collection name:")
        openai.api_key = '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'
        
        completion = openai.Completion.create(
            model="text-davinci-003",
            prompt="query is {} from collection {} for mongodb keep quotes for keys".format(query,col_name),
            max_tokens=75,
            temperature=0)
        
        m1 = completion.choices[0]['text']
        d = re.sub(r":\s*\{\s*(\$lt|\$gt)\s*:\s*(\d+)\s*\}\s*", r': {"\1": \2}', m1)
        print(d)
        m1=d.split(',')
        m1=m1[0]
        k=m1.split("(") # i am taking only conditional and projection bracket to use json.loads() which converts it into dict
        k=str(k[1]).split(")")
        k=k[0]
        
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db_name = simpledialog.askstring("Enter Database Name :", "Please enter database name:")
        db = client[db_name]
        col = db[col_name]
               
        if d.find("find")>=1:
            result = list(col.find(json.loads(k)))
            df = pd.DataFrame(result)
            import sys
            sys.path.append("D:/Mini")
            from mongo_gui import mongo
            mongo.tkint(df)

        else:
            print("Invalid query type")

    @staticmethod
    def tkint(column_names, results):
        from tkinter import ttk
        root = tk.Tk()
        root.title("Query Result")
        table = ttk.Treeview(root)
        table["columns"] = column_names
        table["show"] = "headings"
        for col in column_names:
            table.heading(col, text=col.title(), anchor=tk.CENTER)
            table.column(col, anchor=tk.CENTER)
        for row in results:
            table.insert("", "end", values=row)
        table.pack()
        root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
