import hmac, sha, base64
from datetime import datetime

TIMEFORMAT = "%a, %d %b %Y %H:%M:%S +0000"

def generate_auth_param(secret_key, path, params=None, timestamp=None):
    """
    Given your secret key, the path you are trying to query, and
    the parameters for querying, generates an authentication value
    that should be sent along with the request as 'app3_auth' to 
    allow you to access private records.
    
    The timestamp format should be as specified in RFC 2822 and in UTC:
        "%a, %d %b %Y %H:%M:%S +0000"
        
    - See http://www.faqs.org/rfcs/rfc2822.html
    
    If no parameters are provided, an empty dictionary is substitued
    If no timestamp is provied, the current time is used.
    """    
    if not params: params = {}

    params = '\n'.join(["%s=%s" % (key, val) for key, val in params.items()])
    
    if not timestamp:
        timestamp = datetime.utcnow().strftime(TIMEFORMAT)
    
    message = unicode("%s\n%s\n%s" % (path, params, timestamp), "utf-8")

    auth = hmac.new(
        key = secret_key,
        msg = message,
        digestmod = sha,
    ).digest()
    
    return base64.encodestring(auth).strip()

def is_within_n_minutes(sent_time, n=15):
    """
    Check whether one of our timestamps is within n minutes of
    now. (All times are in UTC)
    """
    sent_time = datetime.strptime(sent_time, TIMEFORMAT)
    
    return not (datetime.utcnow() - sent_time).seconds > n * 60
    

def is_authorized(auth, secret_key, path, params, timestamp):
    """
    Given an auth string, the secret key, path and params requested, and
    the timestamp of the request, decide whether the request is authorized
    or not.
    """
    if not is_within_n_minutes(timestamp, 15): return False # Timeskew... Could be reply attack?
    
    provided_auth = generate_auth_param(secret_key, path, params, timestamp)
    
    return provided_auth == auth
    
