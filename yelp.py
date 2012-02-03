# Initial design of Class Wrapper for super happy fun time access of the Yelp API
# Mad love to the crew @ yelp and the code @ https://github.com/Yelp/yelp-api/blob/master/v2/python/

import oauth2 as oauth
import simplejson as json
import urllib2
import urllib

class YelpApi:
  token = ""
  consumer = ""
  search_url =  "http://api.yelp.com/v2/search"
  biz_url = "http://api.yelp.com/v2/business/"
  request_url = ""
  oauth_request =""  


  def  __init__(self, consumer_key, consumer_secret, token_key, token_secret):
    self.consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    self.token = oauth.Token(key=token_key, secret=token_secret)
	
  def biz_search(self, biz_name):
    self.request_url = "%s%s" % (self.biz_url, biz_name)
    self.init_request()
    return self.send_request()
	
	
  def search(self, params):
    if not params:
	  raise Exception('No params specified - search halted')

    encoded_params = urllib.urlencode(params)
    self.request_url = "%s?%s" % (self.search_url, encoded_params)
    self.init_request()
    return self.send_request()
	
  def init_request(self):
    self.oauth_request = oauth.Request('GET', self.request_url, {})
    self.oauth_request.update({'oauth_nonce': oauth.generate_nonce(),
                       'oauth_timestamp': oauth.generate_timestamp(),
                       'oauth_token': self.token.key,
                       'oauth_consumer_key': self.consumer.key})
    self.oauth_request.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.consumer, self.token)
    self.request_url = self.oauth_request.to_url()
	
  def send_request(self):
    try:
      conn = urllib2.urlopen(self.request_url, None)
      try:
        response = json.loads(conn.read())
      finally: 
        conn.close()
    except urllib2.HTTPError, error:
        raise Exception('Yo dawg, you got mad HTTP problems up in yo grill : %s' % error)

    return response
	



