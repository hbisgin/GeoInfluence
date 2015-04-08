import twitter

tw={}
tw['OAUTH_TOKEN']= '2184712454-gAtpJPWGyiGMjbqXz3S0ycmKqFMDPSyBAXutBub'
tw['OAUTH_TOKEN_SECRET']= 'IYWPNDihCLVS3k3t15TWZcsdhDAxeDNgJEj2lRTPlvSVV'
tw['CONSUMER_KEY']= 'gWPAsZSr8Vff6oNEGIcZgA'
tw['CONSUMER_SECRET']= 'qbM61zxJWGzKrgOIXF9c9PBkgDznf5V0RNX7236mX4'

def oauth_login():
    """Twitter authorization """
    auth = twitter.oauth.OAuth(tw['OAUTH_TOKEN'], tw['OAUTH_TOKEN_SECRET'], tw['CONSUMER_KEY'], tw['CONSUMER_SECRET'])
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api