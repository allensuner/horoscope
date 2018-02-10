'''
This is a serverless chalice application,
docs can be found here: https://chalice.readthedocs.io/en/latest/
'''
import requests
from chalice import Chalice, BadRequestError

app = Chalice(app_name='horoscope')
HOROSCOPE_BASE_URL = 'http://sandipbgt.com/theastrologer/api/horoscope/'
SIGNS = {
    'cancer': 'https://s3-us-west-2.amazonaws.com/horoscope-icons/cancer.png',
    'aries': 'https://s3-us-west-2.amazonaws.com/horoscope-icons/aries.png',
    'leo': 'https://s3-us-west-2.amazonaws.com/horoscope-icons/leo.png',
    'gemini': 'https://s3-us-west-2.amazonaws.com/horoscope-icons/gemini.png',
    'capricorn': 'https://s3-us-west-2.amazonaws.com/horoscope-icons/capricorn.png',
    'taurus': 'https://s3-us-west-2.amazonaws.com/horoscope-icons/taurus.png',
    'sagittarius': 'https://s3-us-west-2.amazonaws.com/horoscope-icons/sagittarius.png',
    'scorpio': 'https://s3-us-west-2.amazonaws.com/horoscope-icons/scorpio.png',
    'pisces': 'https://s3-us-west-2.amazonaws.com/horoscope-icons/pisces.png',
    'libra': 'https://s3-us-west-2.amazonaws.com/horoscope-icons/libra.png',
    'virgo': 'https://s3-us-west-2.amazonaws.com/horoscope-icons/virgo.png',
    'aquarius': 'https://s3-us-west-2.amazonaws.com/horoscope-icons/aquarius.png'
}

@app.route('/horoscope', methods=['POST'], content_types=['application/x-www-form-urlencoded'])
def index():
    '''
    Serves response on route /api/horoscope
    '''
    raw_body = app.current_request.raw_body
    request_body = form_to_dict(raw_body)
    sign = request_body['text']
    channel_id = request_body['channel_id']
    user_name = request_body['user_name']
    if not is_valid_sign(sign):
        error_message = 'Invalid sign (' + sign + '), must provide valid sign for horoscope'
        raise BadRequestError(error_message)
    horoscope = get_horoscope(sign.strip())
    return {
        'response_type': 'in_channel',
        'username': user_name,
        'channel': channel_id,
        'text': horoscope,
        'mrkdwn': True
    }

def get_horoscope(sign):
    '''
    Queries horoscope api and parses the
    horoscope of the day based on the sign
    '''
    uri = (HOROSCOPE_BASE_URL + sign + '/today/')
    response = requests.get(uri)
    body = response.json()
    horoscope = body['horoscope']
    credit = body['credit']
    horoscope = horoscope.split(credit)[0]
    return horoscope

def is_valid_sign(sign):
    '''
    Checks to see if sign is valid
    '''
    if not sign:
        return False
    return sign.strip() in SIGNS

def form_to_dict(raw_form_body):
    '''
    Translates a url encoded form to a dictionary
    '''
    key_value_pairs = {}
    params = raw_form_body.split('&')
    for param in params:
        key_value_pair = param.split('=')
        if len(key_value_pair) == 2:
            key = key_value_pair[0]
            value = key_value_pair[1]
            key_value_pairs[key] = value
    return key_value_pairs
