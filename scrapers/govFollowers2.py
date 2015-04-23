# -*- coding: utf-8 -*-
"""
Get user profiles of followers of governors

Created on Wed Apr 22 18:25:21 2015

@author: Talha
"""
import json
import os,sys
os.chdir(r'C:\Users\Talha\Documents\WinPython3\projects\GeoInfluence\utilities')
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from auth import keys
from utilities.twhelper import oauth_login, make_twitter_request

twitter_api = oauth_login(keys.user['tozcss'])

# filenames sorted by their size in ascending order
files = sorted(os.listdir('../raw_data'), key=lambda x: os.path.getsize('../raw_data/'+x))

for filename in files[35:45]:
    # read in the governor's follower IDs
    followers_file = open('../raw_data/'+filename)
    followers = json.load(followers_file)
    fids = followers['data']['followers']
    gov = followers['parameters']['screen_name']

    resp=[]
    for i in range(1+len(fids)//100):
        res = make_twitter_request(twitter_api.users.lookup, user_id=fids[100*i:100*(i+1)])
        resp.extend(res)
    
    with open('../followers/'+filename, 'w') as outfile:
        json.dump(resp, outfile)