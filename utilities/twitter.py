import twitter
from tw import *
import pandas as pd

df = pd.read_csv('data/governors-challengers.csv')
challengers = df.twch.dropna().tolist()

twitter_api = oauth_login(username='tozcss')
twitter_api.lists.members.create_all(screen_name=','.join(challengers),slug='Challengers',owner_screen_name='tozcss')
