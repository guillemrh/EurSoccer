#Practice from https://www.kaggle.com/code/dimarudov/data-analysis-using-sql/notebook
#Imports.

import numpy as np
import pandas as pd
import sqlite3 
import matplotlib.pyplot as plt

path = '../EurSoccer/'
database = path + 'database.sqlite'

#Connection to the DB and see what tables we have 

conn = sqlite3.connect(database)
tables = pd.read_sql("""SELECT * FROM sqlite_master WHERE type='table';""", conn)
print(tables.head())

#List of countries 

countries = pd.read_sql("""SELECT * FROM Country;""", conn)
print(countries.head())

#List of leagues for countries (use of JOIN)

leagues = pd.read_sql("""SELECT League.name AS League, Country.name AS Country FROM League JOIN Country ON Country.id = League.Country_id;""", conn)
print(leagues.head())

#List of teams ordered by their name (asc)

teams = pd.read_sql("""SELECT * FROM Team ORDER BY team_long_name ASC LIMIT 10;""", conn)
print(teams.head())