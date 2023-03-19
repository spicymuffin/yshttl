import time
import datetime
import requests

cookies = {
    '__smVisitorID': 'R8JCRnctK4O',
    'JSESSIONID': 'cmiacUZFKi11IMtrbrd55rTevnn4nW7SQIQU1q9yesZj4aOwxb1nFcmJSDuW5RSW.amV1c19kb21haW4vcG9ydGFsMV8x',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Connection': 'keep-alive',
    # 'Cookie': '__smVisitorID=R8JCRnctK4O; JSESSIONID=cmiacUZFKi11IMtrbrd55rTevnn4nW7SQIQU1q9yesZj4aOwxb1nFcmJSDuW5RSW.amV1c19kb21haW4vcG9ydGFsMV8x',
    'Referer': 'https://portal.yonsei.ac.kr/portal/MainCtr/index.do',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

response = requests.get('https://portal.yonsei.ac.kr/ui/thirdparty/portal/main.jsp', cookies=cookies, headers=headers)

print(response.headers)