from __future__ import print_function
import time
import cfbd
from cfbd.rest import ApiException
from pprint import pprint
import pandas as pd
import numpy as np
import config
import seaborn as sns
import matplotlib.pyplot as plt


def get_cfbd_api():

    # Configure API key authorization: ApiKeyAuth
    configuration = cfbd.Configuration()
    configuration.api_key['Authorization'] = config.cfbd_api_key
    configuration.api_key_prefix['Authorization'] = 'Bearer'

    # create an instance of the API class (Teams)
    teams_api = cfbd.TeamsApi(cfbd.ApiClient(configuration))

    # create list of all schools
    teams = teams_api.get_fbs_teams()
    team_names = [t.school for t in teams]

    # create an instance of the API class (Conferences)
    conferences_api = cfbd.ConferencesApi(cfbd.ApiClient(configuration))

    # create a list of all conferences
    conferences = conferences_api.get_conferences()


def betting_line_accuracy():

    # Configure API key authorization: ApiKeyAuth
    configuration = cfbd.Configuration()
    configuration.api_key['Authorization'] = config.cfbd_api_key
    configuration.api_key_prefix['Authorization'] = 'Bearer'

    # create an instance of the API class (Betting Lines)
    betting_lines_api = cfbd.BettingApi(cfbd.ApiClient(configuration))

    # create list of betting lines
    # at some point you need to do an average of the different lines or something
    year = 2021
    betting_lines = betting_lines_api.get_lines(year=year)

    df = pd.DataFrame.from_records([dict(home_team=b.home_team, home_score=b.home_score, away_team=b.away_team,
                                    away_score=b.away_score, line=b.lines) for b in betting_lines])
    df['line'] = df['line'].apply(lambda x: 'NaN' if x == [] else x[0])
    df = df[(df['line'] != 'NaN')]
    df['spread'] = df['line'].apply(lambda x: x.spread)
    df = df[(df['spread'].notnull())]   # does null mean no favorite, 0 line?
    df['spread'] = pd.to_numeric(df['spread'], errors='coerce')
    df['line'] = df['line'].apply(lambda x: x.formatted_spread)
    df['point_differential'] = abs(df['home_score'] - df['away_score'])
    df['winning_team'] = np.where(df['home_score'] > df['away_score'], df['home_team'], df['away_team'])
    df['line_winning_team'] = df['line'].apply(lambda x: x.split(' -')[0])
    df['spread_margin'] = np.where(df['winning_team'] == df['line_winning_team'], abs(df['point_differential'] -
                                   abs(df['spread'])), df['point_differential'] + abs(df['spread']))
    df['pick_correct'] = df['winning_team'] == df['line_winning_team']

    pprint(df.info())
    print(df['pick_correct'].sum() / len(df['pick_correct']))

    fig, ax = plt.subplots(figsize=(14, 8))
    fig = sns.boxplot(df, x='spread_margin')

    plt.show()

def cfb_rankings():

    # Create team rankings based on stats

    # Configure API key authorization: ApiKeyAuth
    configuration = cfbd.Configuration()
    configuration.api_key['Authorization'] = config.cfbd_api_key
    configuration.api_key_prefix['Authorization'] = 'Bearer'

    # Create team list with current records
    year = 2021
    games_api = cfbd.GamesApi(cfbd.ApiClient(configuration))
    team_records = games_api.get_team_records(year=year)

    df = pd.DataFrame.from_records([dict(team=t.team, away_games=t.away_games, home_games=t.home_games)
                                    for t in team_records])
    df['home_wins'] = df['home_games'].apply(lambda x: x.wins)
    df['home_losses'] = df['home_games'].apply(lambda x: x.losses)
    df['home_total'] = df['home_games'].apply(lambda x: x.games)
    df['home_winning_percent'] = df['home_wins'] / df['home_total']
    df = df.drop('home_games', axis=1)
    df['away_wins'] = df['away_games'].apply(lambda x: x.wins)
    df['away_losses'] = df['away_games'].apply(lambda x: x.losses)
    df['away_total'] = df['away_games'].apply(lambda x: x.games)
    df['away_winning_percent'] = df['away_wins'] / df['away_total']
    df = df.drop('away_games', axis=1)

    # create an instance of the API class: games results
    games_api = cfbd.GamesApi(cfbd.ApiClient(configuration))
    games = games_api.get_games(year=year)

    pprint(games[0])

if __name__ == '__main__':

    pd.set_option('display.max_columns', None)
    #pd.set_option('display.max_rows', None)
    cfb_rankings()
