#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF-8')

import oauth2 as oauth
import urllib2 as urllib
import json
import time

access_token_key = "1318925832-wBgtUwAvCMV33RWpw8wjDX8vhRSUiDgtP6whrFG"
access_token_secret = "fNM9CqppSJOeOzXN210uNRrZMrJexfpA5fPtAvZI9sQ"

column_delimiter = ";"
row_delimiter = "##|##"

consumer_key = "8RcGKsxLqGtaL4pqHBRAw"
consumer_secret = "KDTdw4wLX3Vx6dnxQTlYxm2GZt2SuimyOrI1KKrNo"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():
  url = "https://stream.twitter.com/1.1/statuses/filter.json"
#  keywords = 'путин OR обама'
  parameters = {"track" : 'я,ты'}  #.encode('utf-8')  
#  print parameters
  response = twitterreq(url, "POST", parameters)
  for line in response:   
    # the question is is there a single tweet in each response, if doesnt does this function extract   each tweet
    tweetjsonData = json.loads(line)
#   print tweetjsonData
    text = tweetjsonData["text"]
    text = text.replace('\n', '-newline-')
    date = tweetjsonData["created_at"]
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(date,'%a %b %d %H:%M:%S +0000 %Y'))
    sys.stdout.write(column_delimiter.join((ts, text)) + row_delimiter)



   
#    itercount = range(0,(len(statuses)-1),1)  
#    print itercount


#  for line in response:
#   print line.strip()

#print response
#  return json.load(response)

#for line in response:
#    print line.strip()
#
#if __name__ == '__main__':
#  fetchsamples()

fetchsamples()
