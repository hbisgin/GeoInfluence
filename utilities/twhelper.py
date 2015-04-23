from __future__ import print_function
import twitter
import sys
import time
from urllib.request import URLError #urllib2
from http.client import BadStatusLine #httplib

def oauth_login(tw):
    """Twitter authorization
       Expects a dictionary with 4 k,v pairs.
       Returns twitter_api handle
    """
    auth = twitter.oauth.OAuth(tw['OAUTH_TOKEN'], tw['OAUTH_TOKEN_SECRET'],
			tw['CONSUMER_KEY'], tw['CONSUMER_SECRET'])
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api
	

def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw): 
	
	# A nested helper function that handles common HTTPErrors. Return an updated
	# value for wait_period if the problem is a 500 level error. Block until the
	# rate limit is reset if it's a rate limiting issue (429 error). Returns None
	# for 401 and 404 errors, which requires special handling by the caller.
	def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):
	
		if wait_period > 3600: # Seconds
			print ('Too many retries. Quitting.',file=sys.stderr)
			raise e
	
		# See https://dev.twitter.com/docs/error-codes-responses for common codes
	
		if e.e.code == 401:
			print ('Encountered 401 Error (Not Authorized)',file=sys.stderr)
			return None
		elif e.e.code == 404:
			print ('Encountered 404 Error (Not Found)',file=sys.stderr)
			return None
		elif e.e.code == 429: 
			print ('Encountered 429 Error (Rate Limit Exceeded)',file=sys.stderr)
			if sleep_when_rate_limited:
				print ("Retrying in 15 minutes...ZzZ...",file=sys.stderr)
				sys.stderr.flush()
				time.sleep(60*15 + 5)
				print ('...ZzZ...Awake now and trying again.',file=sys.stderr)
				return 2
			else:
				raise e # Caller must handle the rate limiting issue
		elif e.e.code in (500, 502, 503, 504):
			print ('Encountered',e.e.code,'Error. Retrying in',wait_period,'seconds',file=sys.stderr)
			time.sleep(wait_period)
			wait_period *= 1.5
			return wait_period
		else:
			raise e

	# End of nested helper function
	
	wait_period = 2 
	error_count = 0 

	while True:
		try:
			return twitter_api_func(*args, **kw)
		except twitter.api.TwitterHTTPError as e:
			error_count = 0 
			wait_period = handle_twitter_http_error(e, wait_period)
			if wait_period is None:
				return
		except URLError as e:
			error_count += 1
			time.sleep(wait_period)
			wait_period *= 1.5
			print ("URLError encountered. Continuing.",file = sys.stderr)
			if error_count > max_errors:
				print ("Too many consecutive errors...bailing out.",file=sys.stderr)
				raise
		except BadStatusLine as e:
			error_count += 1
			time.sleep(wait_period)
			wait_period *= 1.5
			print ("BadStatusLine encountered. Continuing.",file=sys.stderr)
			if error_count > max_errors:
				print ("Too many consecutive errors...bailing out.",file=sys.stderr)
				raise
