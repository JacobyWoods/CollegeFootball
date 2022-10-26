from __future__ import print_function
import time
import cfbd
from cfbd.rest import ApiException
from pprint import pprint
import pandas as pd
import numpy as np
import config


def get_cfbd_api():

    # Configure API key authorization: ApiKeyAuth
    configuration = cfbd.Configuration()
    configuration.api_key['Authorization'] = config.cfbd_api_key
    configuration.api_key_prefix['Authorization'] = 'Bearer'

    # create an instance of the API class (teams)
    teams_api = cfbd.TeamsApi(cfbd.ApiClient(configuration))

    # create list of all schools
    teams = teams_api.get_fbs_teams()
    team_names = [t.school for t in teams]

    # create an instance of the API class (conferences)
    conferences_api = cfbd.ConferencesApi(cfbd.ApiClient(configuration))

    # create a list of all conferences
    conferences = conferences_api.get_conferences()

    # create an instance of the API class (Betting Lines)
    betting_lines_api = cfbd.BettingApi(cfbd.ApiClient(configuration))

    # create list of betting lines
    year = 2021
    betting_lines = betting_lines_api.get_lines(year=year)

    df = pd.DataFrame.from_records([dict(home_team=b.home_team, home_score=b.home_score, away_team=b.away_team,
                                    away_score=b.away_score, line=b.lines) for b in betting_lines])
    df['line'] = df['line'].apply(lambda x: 'NaN' if x == [] else x[0])
    df = df[(df['line'] != 'NaN')]
    df['line'] = df['line'].apply(lambda x: x.formatted_spread)


    pd.set_option('display.max_columns', None)
    #pd.set_option('display.max_rows', None)

    pprint(df.head())

if __name__ == '__main__':

    get_cfbd_api()
