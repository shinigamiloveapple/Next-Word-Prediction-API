from ML_Prediction import *

from flask import Flask, request

import psycopg2

con = psycopg2.connect(database="postgres", user="postgres", password="admin", host="127.0.0.1")
print("Database opened successfully")

cur = con.cursor()

def add_to_sql(a):
    req_format_q_r=[]
    for query in a.keys():
        val_i =a[query]
        temp1 =[]
        for j in range(len(val_i)):
            temp1.append(query)
        req_format_q_r = req_format_q_r+list(zip(temp1,val_i))
    for i in req_format_q_r:
        cur.execute("INSERT INTO REPORT(QUERY,RESULT) VALUES {}".format(i))
        con.commit()
    return True

app = Flask(__name__)

@app.route("/result",methods = ['POST'])
def result():
    extract_json = request.get_json(silent=True,force=True)
    
    """
    quotes in a list
    """
    quotes  = extract_json.get("quotes")
    preds = predict_from_list(quotes)
    add_to_sql(preds)
    return str(preds)


if __name__ == '__main__':
    app.run()