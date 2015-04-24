# -*- coding: utf-8 -*-
"""
Get user profiles of followers of governors

Created on Wed Apr 22 18:25:21 2015

@author: Talha
"""
import json
import os,sys
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)


def joinFileNamesWithDF():
    import pandas as pd
    path = '../raw_data/'
    files = sorted(os.listdir(path), key=lambda x: os.path.getsize(path+x))
    fnamegov = {}
    for filename in (files):
        with open(path+filename) as followers_file:
            followers = json.load(followers_file)
        fnamegov[filename] = followers['parameters']['screen_name']    
    df = pd.read_csv('../data/governors-challengers.csv')
    df2 = pd.DataFrame(list(fnamegov.items()),columns=['fname','twgov'])
    df = df.merge(df2)
    df.index = df.fname
    return df


def geoCode():
    """
    7.12GB follower user profiles are to be encoded as the following:
    {'State1':{'govTw':'','govName':'','flocs':{'latlon1':cnt1,...}},...}
    """
    from utilities.geocoder import Geocoder
    from collections import Counter
    
    df = joinFileNamesWithDF()
    
    path = '../utilities/geodata/'
    gc = Geocoder(path+'state_abbr_file', path+'city_file')
    
    path = '../followers/'
    files = sorted(os.listdir(path), key=lambda x: os.path.getsize(path+x))
    locs = {}
    for f in (files):
        with open(path+f) as profiles_file :
            profiles = json.load(profiles_file)
        # let's get the locations out of this JSON response
        i = 0
        locations = []
        for r in profiles:
            if r['location'] != '':
                locations.append(r['location'])
                i=i+1
        print("\nNumber of non-empty location info in user profiles: ",i)
        print('Rate of non-empty user-profile location fields: {0:.2f} %'.format(i*100/len(profiles)))
                
        latlon = []
        for loc in locations:
            point = gc.geocode(loc.strip())
            if point != None:
                latlon.append(','.join((point[0], point[1])))
        
        counter = dict(Counter(latlon))
        print('Number of locations geocoded:',sum(counter.values()))
        state = df.ix[f]['state']
        locs[state] = {}
        locs[state]['twgov'] = df.ix[f]['twgov']
        locs[state]['flocs'] = counter

    with open('../data/geocoded.json', 'w') as outfile:
        json.dump(locs, outfile)
    
    
def downloadFollowers():
    """
    Makes Twitter user lookup requests for Governors' followers
    Saves user profiles into files with the same filename of follower IDs
    """
    from auth import keys
    from utilities.twhelper import oauth_login, make_twitter_request
    
    twitter_api = oauth_login(keys.user['hesobi'])
    
    # filenames sorted by their size in ascending order
    files = sorted(os.listdir('../raw_data'), key=lambda x: os.path.getsize('../raw_data/'+x))
    
    for filename in (files):
        # read in the governor's follower IDs
        followers_file = open('../raw_data/'+filename)
        followers = json.load(followers_file)
        fids = followers['data']['followers']
        gov = followers['parameters']['screen_name']
        followers_file.close()
        
        # make twitter requests to lookup the followers
        resp=[]
        for i in range(1+len(fids)//100):
            res = make_twitter_request(twitter_api.users.lookup, user_id=fids[100*i:100*(i+1)])
            try:
                resp.extend(res)
            except:
                print (filename,'no results returned:',i)
                pass
    
        # save the user lookups    
        with open('../followers/'+filename, 'w') as outfile:
            json.dump(resp, outfile)