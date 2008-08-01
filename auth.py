import hmac, sha, base64
from datetime import datetime

TIMEFORMAT = "%a, %d %b %Y %H:%M:%S +0000"

def generate_auth(request):
    """
    The timestamp format should be as specified in RFC 2822 and in UTC:
        "%a, %d %b %Y %H:%M:%S +0000"
        
    - See http://www.faqs.org/rfcs/rfc2822.html
    """
    params = request.params
    if not params: params = {}
    
    params = '&'.join(["%s=%s" % (key, val) for key, val in params.items()])
    
    #message = unicode("%s\n%s\n%s" % (request.path, params, request.app3_timestamp), "utf-8")
    message = "%s\n%s\n%s" % (request.path, params, request.app3_timestamp)
    
    auth = hmac.new(
        key = request.secret_key,
        msg = message,
        digestmod = sha,
    ).digest()
    
    return base64.encodestring(auth).strip()

def generate_timestamp():
    """
    """
    return datetime.utcnow().strftime(TIMEFORMAT)

def is_within_n_minutes(sent_time, n=15):
    """
    Check whether one of our timestamps is within n minutes of
    now. (All times are in UTC)
    """
    sent_time = datetime.strptime(sent_time, TIMEFORMAT)
    
    return not (datetime.utcnow() - sent_time).seconds >= n * 60
    
def is_authorized(request):
    """
    """
    # Time skew... Could be replay attack?
    if not is_within_n_minutes(request.app3_timestamp, 15): 
        return False
    
    return request.app3_auth == generate_auth(request)