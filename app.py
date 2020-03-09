from flask import Flask, render_template,jsonify
import json
from sqlalchemy import create_engine
import psycopg2
import pandas as pd
import numpy as np
import os
import pickle
import random

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
engine = create_engine('postgresql://postgres:ximepss030311@localhost:5432/peliculas_db')
data = pd.read_csv("./Resources/ActoresDirectoresPelis.csv")
actores = np.asarray(data['List'])
data2 = pd.read_csv("./Resources/movies.csv")
pelis1 = pd.DataFrame(data2["Title"])
actores1 = pd.DataFrame(data2["Actors"])
directores1 = pd.DataFrame(data2["Director"])
baselimp = pd.read_csv("./Resources/baselimpia.csv")

pickle_in = open("./Resources/modelProject3","rb")
modeldef = pickle.load(pickle_in)

@app.route("/table")
def table():
    #dataset = tablib.Dataset()
   # with open(os.path.join(os.path.dirname(__file__),'./Resources/movies.csv'), encoding = 'UTF-8') as f:
    #    dataset.csv = f.read()
    x = pd.read_csv("./Resources/ActoresDirectoresPelis.csv")
    return x.to_json(force_ascii = False)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/pred/<arreglop>", methods=["POST"])
def predict(arreglop):
    sp = arreglop.split(",")
    datos = pd.read_csv("./Resources/baselimpia.csv")
    datos.drop(columns = ['Title'], inplace = True)
    print(datos.dtypes)
    rating = baselimp['imdbRating'].sample().values[0]
    if rating>6 :
        ex_noex = 1
    else:
        ex_noex = 0
    x_rec = [baselimp['Worldwide'].sample().values[0],baselimp['Year'].sample().values[0],baselimp['Country'].sample().values[0],sp[1],sp[0],baselimp['Production'].sample().values[0],baselimp['Rated'].sample().values[0],baselimp['Runtime'].sample().values[0],rating,sp[2],ex_noex]
    datos.append(x_rec)
    X = pd.get_dummies(datos,columns=["Country","Actores","Directores","Production","Rated","Genre"])
    x = X[[col for col in X.columns if col!= "Ex_NoEx"]].values
    x_new = x[-1]
    ynew= modeldef.predict(x_new.reshape(1,-1))
    ynew = str(ynew[0])
    resultado = ynew
    return jsonify({
        "resultado": resultado
    })


@app.route("/calculator")
def calcu():
    return render_template("mcalculator.html")

@app.route("/random")
def random():
    return render_template("random.html")

@app.route("/dashboard")
def dash():
    return render_template("dashboard.html")

@app.route("/api/movies/<search>", methods = ["POST"])
def info(search):
    try:
        print(search)
        connection = psycopg2.connect(
        database='peliculas_db',
        user='postgres',
        host='localhost',
        password='ximepss030311'
        )
        flag = searchInArrays(search)
        query = ""
        
        print(flag)
        if flag == 1:
            query = "SELECT * FROM movie_data WHERE Title LIKE \'%"+search+"%\'"
        if flag == 3:
            query  = "SELECT COUNT(title) AS Movie, AVG(imdbrating) AS imdbR, AVG(Metascore) AS Mscore, to_char(SUM(worldwide), '$999,999,999,999') AS WW, mode() WITHIN GROUP (ORDER BY rated) AS modal_value, mode() WITHIN GROUP (ORDER BY genre) AS genreV, mode() WITHIN GROUP (ORDER BY production) AS prodV, AVG(Runtime) AS RunT FROM movie_data WHERE Director LIKE \'%"+search+"%\'"
        if flag == 2:
            query = "SELECT COUNT(title) AS Movie, AVG(imdbrating) AS imdbR, AVG(Metascore) AS Mscore, to_char(SUM(worldwide), '$999,999,999,999') AS WW, mode() WITHIN GROUP (ORDER BY rated) AS modal_value, mode() WITHIN GROUP (ORDER BY genre) AS genreV, mode() WITHIN GROUP (ORDER BY production) AS prodV, AVG(Runtime) AS RunT FROM movie_data WHERE Actors LIKE \'%"+search+"%\'"
        print(query)
        cursor = connection.cursor()
    #      postgreSQL_select_Query = 'SELECT * FROM movie_data'
        cursor.execute(query)
        resultado = cursor.fetchall()
        for x in resultado:
            print(x)
        # COMO VOY A SABER SI ME SEARCH ES IGUAL A PELICULA O ACTOR O DIRECTOR??
        # SE ME OCURRE JUNTAR LOS RESULTADOS DE LOS 3 QUERIES...Y YA
    # CON ESE RESULTADO LO MANDO A TEMPLATE 
        # RESULTADO = PELIS, DIRECTOR, ACTOR
    except (Exception, psycopg2.Error) as error :
        print ('Error while fetching data from PostgreSQL', error)
        #return render_template("dashboard.html", pelis = pelis)
        #return render_template("dashboard.html", resultado=resultado)
    return jsonify({
        "resultado": resultado,
        "flag": flag
    })
################################################# POST method example
 
def searchInArrays(string):
    if pelis1.Title.str.count(string).sum() >= 1:
        return 1
    if actores1.Actors.str.count(string).sum() > directores1.Director.str.count(string).sum():
        return 2
    if actores1.Actors.str.count(string).sum() <= directores1.Director.str.count(string).sum():
        return 3

if __name__ == "__main__":
    app.run(debug = True)




