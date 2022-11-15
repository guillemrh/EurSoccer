#Practice from https://www.kaggle.com/code/dimarudov/data-analysis-using-sql/notebook
#Imports.

import numpy as np
import pandas as pd
import sqlite3 
import matplotlib.pyplot as plt

path = '../KAGGLE/'
database = path + 'database.sqlite'

#Connection to the DB and see what tables we have 

conn = sqlite3.connect(database)
tables = pd.read_sql("""SELECT * FROM sqlite_master WHERE type='table';""", conn)
print(tables.head())

#List of countries 

countries = pd.read_sql("""SELECT * FROM Country;""", conn)
print(countries.head())