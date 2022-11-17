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

#Leagues by season

leagues_by_season = pd.read_sql("""SELECT Country.name AS country, 
                                League.name AS League, 
                                season,
                                COUNT(DISTINCT stage) AS number_of_stages,
                                COUNT(DISTINCT HT.team_long_name) AS number_of_teams,
                                avg(home_team_goal) AS avg_home_team_scores,
                                avg(away_team_goal) AS avg_away_team_goals,
                                avg(home_team_goal-away_team_goal) AS avg_goal_diff,
                                avg(home_team_goal+away_team_goal) AS avg_goals,
                                sum(home_team_goal+away_team_goal) AS total_goals
                                FROM Match
                                JOIN Country ON Country.id = Match.country_id
                                JOIN League ON League.id = Match.league_id
                                LEFT JOIN Team AS HT ON HT.team_api_id = Match.home_team_api_id
                                LEFT JOIN Team AS AT on AT.team_api_id = Match.away_team_api_id
                                WHERE country in ('Spain', 'Germany', 'France', 'Italy', 'England')
                                GROUP BY Country.name, League.name, season
                                HAVING COUNT(DISTINCT stage) > 10
                                ORDER BY Country.name, League.name, season DESC;""", conn)
print(leagues_by_season.head())

#Data visualization 
#Average goals per game over time

df = pd.DataFrame(index=np.sort(leagues_by_season['season'].unique()), columns=leagues_by_season['country'].unique())
df.loc[:,'Germany'] = list(leagues_by_season.loc[leagues_by_season['country']=='Germany','avg_goals'])
df.loc[:,'Spain'] = list(leagues_by_season.loc[leagues_by_season['country']=='Spain','avg_goals'])
df.loc[:,'Italy'] = list(leagues_by_season.loc[leagues_by_season['country']=='Italy','avg_goals'])
df.loc[:,'France'] = list(leagues_by_season.loc[leagues_by_season['country']=='France','avg_goals'])
df.loc[:,'England'] = list(leagues_by_season.loc[leagues_by_season['country']=='England','avg_goals'])

df.plot(figsize=(12,5), title='Average goals per game over time')
