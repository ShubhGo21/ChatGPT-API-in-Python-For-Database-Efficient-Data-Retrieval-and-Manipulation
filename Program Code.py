"""
Created on Mon Feb 27 09:37:27 2023

@author: shubh
"""
# sqlplus
import tkinter as tk
from tkinter import simpledialog

root = tk.Tk()
root.withdraw()

which = simpledialog.askinteger("Choose database to connect :", "1. SQLplus\n2. MySQL\n3. MongoDB\nChoice number:")

# 1.SQLplus
# 2.MySQL
# 3.MongoDB

DB=which


if DB==1:
    import openai
    import cx_Oracle
    
    
    que = simpledialog.askstring("Enter Your query :", "Please enter your query:")
    col = simpledialog.askstring("Enter table name :", "Please enter the table name:")

    
    openai.api_key = 'Enter_API_KEY'
    completion = openai.Completion.create(
      model="text-davinci-003",
      prompt="{} from {} query for oracle do not use limit".format(que,col),
      max_tokens=75,
      temperature=0
    )
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
        cursor.execute("select * from {}".format(col))
        #cursor.execute(query)

        results = cursor.fetchall()
        column_names = [i[0].lower() for i in cursor.description]
        cursor.close()
        conn.close()
    
        # Create the table widget and populate it with the results
        import sys
        sys.path.append("D:/Mini")
        from giving_class import MyClass
        MyClass.tkint(column_names,results)

        
    elif c.find("select")>=0:
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [i[0].lower() for i in cursor.description]
        cursor.close()
        conn.close()
    
        # Create the table widget and populate it with the results
        import sys
        sys.path.append("D:/Mini")
        from giving_class import MyClass
        MyClass.tkint(column_names,results)

#==========================================================================================
elif DB==2:
#MYSQL 

    import openai
    
    query=str(input("Enter Your query : "))
    
    openai.api_key = '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'
    completion = openai.Completion.create(
      model="text-davinci-003",
      prompt="{} query for mysql".format(query),
      max_tokens=50,
      temperature=0
    )
    
    d=(completion.choices[0]['text'])
    
    print (d)
    
    import mysql.connector
    
    # establish connection
    cnx = mysql.connector.connect(user='root', password='root123',
                                  host='localhost',
                                  database='sakila')
    
    # create a cursor object
    cursor = cnx.cursor()
    
    # execute a query
    query = d
    cursor.execute(query)
    
    results = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]
    
    # fetch results
    for row in cursor:
        print(row)
    
    # close cursor and connection
    cursor.close()
    cnx.close()
    
    ############################ tO GET GUI Output##############################
    import sys
    sys.path.append("D:/Mini")
    from giving_class import MyClass
    MyClass.tkint(column_names,results)

#===========================================================================================
# MongoDB
elif DB==3:
        
    import openai
    import re
    query=str(input("Enter Your query : "))
    col=str(input("Enter Your collection name : "))
    
    openai.api_key = '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'
    completion = openai.Completion.create(
      model="text-davinci-003",
      prompt='mongodb query to {} from collection {} use quotes for attribute and '.format(query, col),
      #prompt="mongodb query for table emp where ename is 'revati jadhav' use quotes for attribute",
      max_tokens=50,
      temperature=0
    )
    
    m=(completion.choices[0]['text'])
    print(m)
    m1 = re.sub(r'(\$lt)', r'"\1"', m)


    #print(type(m)) # getting this input in str form which wil not work directly in pymongo
    # as pymongo needs cursor type which gets executes in it
    
    k=m1.split("(") # i am taking only conditional and projection bracket to use json.loads() which converts it into dict
    k=str(k[1]).split(")")
    k=k[0]
    print(k)
    
    
    import json
    from pymongo import MongoClient
    import pandas as pd
    from tkinter import Tk
    from pandasgui import show
    
    # set up a MongoDB client
    client = MongoClient('mongodb://localhost:27017/')
    
    # get the database
    db = client['test']
    
    # get the collection
    collection = db[col]
    
    z=[json.loads(k)]
    print(type(z))
    
    # perform a query
    if m.find("find")>=1:
        result = list(collection.find(json.loads(k)))
        df = pd.DataFrame(result)
        import sys
        sys.path.append("D:/Mini")
        from mongo_gui import mongo
        mongo.tkint(df)
        
            
    elif m.find("deleteOne")>=1:
        result = collection.delete_one(json.loads(k))
        print(result.deleted_count, "documents deleted.")
        
    elif m.find("delete")>=1:
        result = collection.delete_many(json.loads(k))
        print(result.deleted_count, "documents deleted.")
    
    elif m.find("multi:true")>=1:
        result = collection.update_many([json.loads(k)])
        print(result.updated_count, "documents UPDATED.")
        
    elif m.find("update")>=1:
        print(result.updated_count, "documents UPDATED.")
        
    
        
    elif m.find("aggregate")>=1:
        result = collection.aggregate(json.loads(k))
        
    # print the result    
        
    # close the connection when finished
    client.close()

#================================================================================

