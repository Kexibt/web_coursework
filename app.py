import flask
from flask import render_template, request, jsonify, Flask, redirect, url_for, flash
import numpy as np
import traceback
import pickle
import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
 
 
# App definition
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret'

def get_dbm_connection():
    conn = sqlite3.connect('database/database_models.db')
    conn.row_factory = sqlite3.Row
    return conn
 
@app.route('/')
def welcome():
    conn = get_dbm_connection()
    mls = conn.execute('SELECT * FROM models').fetchall()
    conn.close()
    return render_template('index.html', text="Choose your fighter", mls=mls)

def get_ml(ml_id):
    conn = get_dbm_connection()
    ml = conn.execute('SELECT * FROM models WHERE id = ?',
                        (ml_id,)).fetchone()
    conn.close()
    if ml is None:
        abort(404)
    return ml

@app.route('/<int:ml_id>', methods=['POST', 'GET'])
def neural(ml_id):
    ml = get_ml(ml_id)
    model = ml['path']
    with open((model+'.pkl'), 'rb') as f:
        classifier = pickle.load(f)
    with open((model + '_columns.pkl'), 'rb') as f:
        model_columns = pickle.load(f)
    if flask.request.method == 'GET':
        return render_template('ml.html', ml=ml)

    if flask.request.method == 'POST':
        try:
            json_ = request.json
            print(json_)
            query_ = pd.get_dummies(pd.DataFrame(json_))
            query = query_.reindex(columns=model_columns, fill_value=0)
            prediction = list(classifier.predict(query))

            return jsonify({"prediction": prediction})
        except:
            return jsonify({"trace": traceback.format_exc()})

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        database = request.form['database']

        if not title:
            flash('Dude.. You forgot the name')
        else:
            new_ml(title, database)
            return redirect(url_for('welcome'))

    return render_template('create.html', text="Create your own model")

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    ml = get_ml(id)
    conn = get_dbm_connection()
    conn.execute('DELETE FROM models WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(ml['title']))
    return redirect(url_for('welcome'))

if __name__ == "__main__":
   app.run()

def new_ml(title, val_database):
    conn = sqlite3.connect("database/database_models.db")
    cursor = conn.cursor()
    ind = cursor.execute('SELECT max(id) FROM models').fetchone()[0] + 1
    s_model = 'model/model'

    boston_data = sqlite3.connect(('database/' + val_database + '.db'))
    data_ = pd.read_sql_query("SELECT * FROM prices", boston_data)
    data_.isnull().sum()
    X = data_.drop(['PRICE'], axis=1)
    y = data_['PRICE']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

    classifier = RandomForestRegressor()
    classifier.fit(X_train, y_train)

    with open((s_model+str(ind)+'.pkl'), 'wb') as file:
        pickle.dump(classifier, file)

    # saving the columns
    model_columns = list(X.columns)
    with open((s_model+str(ind)+'_columns.pkl'), 'wb') as file:
        pickle.dump(model_columns, file)


    cursor.execute("INSERT INTO models (title, path, database) VALUES (?, ?, ?)",
                   (title, (s_model+str(ind)), val_database)
                   )
    conn.commit()
    conn.close()