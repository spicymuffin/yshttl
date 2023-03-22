import requests
from bs4 import BeautifulSoup as bs


def get_login_token(raw_resp):
    soup = bs(raw_resp.text, 'lxml')
    token = [n['value'] for n in soup.find_all('input')
             if n['name'] == 'wpLoginToken']
    return token[0]


payload = {
    'wpName': 'my_username',
    'wpPassword': 'my_password',
    'wpLoginAttempt': 'Log in',
    # 'wpLoginToken': '',
}

with requests.session() as s:
    resp = s.get('http://en.wikipedia.org/w/index.php?title=Special:UserLogin')
    payload['wpLoginToken'] = get_login_token(resp)

    response_post = s.post('http://en.wikipedia.org/w/index.php?title=Special:UserLogin&action=submitlogin&type=login',
                           data=payload)
    response = s.get('http://en.wikipedia.org/wiki/Special:Watchlist')
