from flask import Flask, render_template,jsonify
import json
from sqlalchemy import create_engine
import psycopg2
import pandas as pd
import numpy as np
import tablib
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

engine = create_engine('postgresql://postgres:1234@localhost:5432/peliculas_db')

data = pd.read_csv("./Resources/ActoresDirectoresPelis.csv")
pelis = np.asarray(data['Title'])
actores = np.asarray(data['Actors'])
directores = np.asarray(data['Director'])


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
        password='1234'
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

#@app.route("/api/list/<genres>")
#def genre():
 #   try:
  #      connection = psycopg2.connect(
   #     database='peliculas_db',
    #    user='postgres',
     #   host='localhost',
      #  password='1234')

       # query=""

        #'''SELECT Title, Genre FROM movie_data
        #WHERE Genre LIKE '%Action%'''
            
    #except (Exception, psycopg2.Error) as error :
     #   print ('Error while fetching data from PostgreSQL', error)
        #return render_template("dashboard.html", pelis = pelis)
        #return render_template("dashboard.html", resultado=resultado)
    #return jsonify({
     #   "": 
    #});

#@app.route("/api/random/<descriptions>")
#def descript():
 #   try:
  #      connection = psycopg2.connect(
   #     database='peliculas_db',
    #    user='postgres',
     #   host='localhost',
      #  password='1234')

       # query= "SELECT Title AS Movie, to_char(worldwide, '$999,999,999,999') AS BoxOffice, Metascore AS Metascore, Genre AS Genre, Plot as Plot, Runtime AS Runtime FROM movie_data WHERE Title LIKE '%Avatar%'"
            
    #except (Exception, psycopg2.Error) as error :
     #   print ('Error while fetching data from PostgreSQL', error)
        #return render_template("dashboard.html", pelis = pelis)
        #return render_template("dashboard.html", resultado=resultado)
    #return jsonify({
     #   "": 
    #})
        
########################################################################################
# ENDPOINT to get random movie lists  

########################################################################################
#ENDPOINT that filters data for movies and give all teh information about it.

###########################################################################################

################################################# POST method example

#@app.route("/auto2", methods = ["POST"])
#def auto2():
    #Lo que nos llega es un json
 #   miJSON = request.json

  #  keyWord = miJSON["searchString"]










   # miJSON = jsonify({
    #    "peliculas":[]
    #})

    #return miJSON



################################################# POST method example
 
def searchInArrays(string):
    if string in pelis:
        return 1
    if string in actores:
        return 2
    if string in directores:
        return 3

if __name__ == "__main__":
    app.run(debug = True)