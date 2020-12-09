import flask
from flask import render_template, request, jsonify, Flask
import numpy as np
import traceback
import pickle
import pandas as pd
import sqlite3
 
 
# App definition
app = Flask(__name__, template_folder='templates')
 
# importing models
with open('model/model.pkl', 'rb') as f:
   classifier = pickle.load(f)
 
with open('model/model_columns.pkl', 'rb') as f:
   model_columns = pickle.load(f)

def get_dbm_connection():
    conn = sqlite3.connect('database_models.db')
    conn.row_factory = sqlite3.Row
    return conn
 
@app.route('/')
def welcome():
    conn = get_dbm_connection()
    mls = conn.execute('SELECT * FROM models').fetchall()
    conn.close()
    return render_template('index.html', text="Choose your fighter", mls=mls)

@app.route('/create')
def create():
    return render_template('Create.html', text="Create your own model")

@app.route('/predict', methods=['POST', 'GET'])
def predict():
   if flask.request.method == 'GET':
       return "Prediction page"
 
   if flask.request.method == 'POST':
       try:
           json_ = request.json
           print(json_)
           query_ = pd.get_dummies(pd.DataFrame(json_))
           query = query_.reindex(columns=model_columns, fill_value=0)
           prediction = list(classifier.predict(query))
 
           return jsonify({
               "prediction": str(prediction)
           })
       except:
           return jsonify({
               "trace": traceback.format_exc()
               })


def get_ml(ml_id):
    conn = get_dbm_connection()
    ml = conn.execute('SELECT * FROM models WHERE id = ?',
                        (ml_id,)).fetchone()
    conn.close()
    if ml is None:
        abort(404)
    return ml

@app.route('/<int:ml_id>')
def neural(ml_id):
    ml = get_ml(ml_id)
    return render_template('ml.html', ml=ml)
 
if __name__ == "__main__":
   app.run()