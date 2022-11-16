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

#List of matches of Spanish league ordered by date

matches = pd.read_sql("""SELECT Match.id, Country.name AS Country, League.name AS League, season, stage, date, HT.team_long_name AS home_team, AT.team_long_name AS away_team, home_team_goal, away_team_goal
                      FROM Match 
                      JOIN Country ON Country.id = Match.Country_id
                      JOIN League ON League.id = Match.league_id
                      LEFT JOIN Team AS HT on HT.team_api_id = Match.home_team_api_id
                      LEFT JOIN Team AS AT on AT.team_api_id = Match.away_team_api_id
                      WHERE Country = 'Spain' 
                      ORDER BY date
                      LIMIT 10;""", conn)
print(matches.head())

#FCBarcelona games for 2008/2009 season
bcn = pd.read_sql("""SELECT Match.id, Country.name AS Country, League.name AS League, season, stage, date, HT.team_long_name AS home_team, AT.team_long_name AS away_team, home_team_goal, away_team_goal
                      FROM Match 
                      JOIN Country ON Country.id = Match.Country_id
                      JOIN League ON League.id = Match.league_id
                      LEFT JOIN Team AS HT on HT.team_api_id = Match.home_team_api_id
                      LEFT JOIN Team AS AT on AT.team_api_id = Match.away_team_api_id
                      WHERE Country = 'Spain' AND (home_team='FC Barcelona' OR away_team='FC Barcelona')
                      ORDER BY date;""", conn)
print(bcn.head())