from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from spotify_api import SpotifyAPI
import requests
import sqlite3
import os

# pull song suggestions from the spotify_songs_kaggle database

DB_FILEPATH = os.path.join(os.path.dirname(__file__), "spotify_songs_kaggle.db")

connection = sqlite3.connect(DB_FILEPATH)
print("CONNECTION:", connection)

cursor = connection.cursor()
print("CURSOR", cursor)

query = "SELECT * FROM record LIMIT 10;"

#result = cursor.execute(query)
#print("RESULT", result) #> returns cursor object w/o results (need to fetch the results)

result2 = cursor.execute(query).fetchall()
print("RESULT 2", result2)
print("___________________")
test = result2[0]
test = test[0]
# the result should be YG
print(test)