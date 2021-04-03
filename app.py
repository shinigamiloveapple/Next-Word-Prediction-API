from ML_Prediction import * # Importing all the functions from ML.Prediction.py

from flask import Flask, request

import psycopg2

# Connecting the database 
con = psycopg2.connect(database="postgres", user="postgres", password="admin", host="127.0.0.1")
print("Database opened successfully")

# Creating a cursor to help in execution
cur = con.cursor()

# Function to inserting the data in database
def add_to_sql(entry):
    req_format_q_r=[]
    for query in entry.keys():
        val_i =entry[query]
        temp1 =[]
        for j in range(len(val_i)):
            temp1.append(query)
        req_format_q_r = req_format_q_r+list(zip(temp1,val_i))
    for i in req_format_q_r:
        cur.execute("INSERT INTO REPORT(QUERY,RESULT) VALUES {}".format(i)) #adding data into table REPORT
        con.commit() # apply changes to database
    return True

# creating flask instance
app = Flask(__name__)

# Defining post for our API.
@app.route("/result",methods = ['POST'])
def result():

    # the data the user input, in json format
    extract_json = request.get_json(silent=True,force=True)
    
    """
    quotes in a list
    """
    quotes  = extract_json.get("quotes") #extracting quotes from json feeded
    preds = predict_from_list(quotes) #predicitng the quotes feeded
    add_to_sql(preds) #adding predicitons to the sql table
    return str(preds)


if __name__ == '__main__':
    app.run()