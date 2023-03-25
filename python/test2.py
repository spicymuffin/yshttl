import requests

cookies = {
    'JSESSIONID': 'xwOcz4ux87aOJFWfYxM9CuT6A2ADkGis4AcQb7Cm1nkNsWy9xZifOOaNpZlgi8fX.amV1c19kb21haW4vc3NvMV8x',
    '__smVisitorID': 'sD5xQPjpKul',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': 'JSESSIONID=xwOcz4ux87aOJFWfYxM9CuT6A2ADkGis4AcQb7Cm1nkNsWy9xZifOOaNpZlgi8fX.amV1c19kb21haW4vc3NvMV8x; __smVisitorID=sD5xQPjpKul',
    'Origin': 'https://infra.yonsei.ac.kr',
    'Referer': 'https://infra.yonsei.ac.kr/sso/PmSSOService',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = [
    ('app_id', 'nportalYonsei'),
    ('retUrl', 'https://portal.yonsei.ac.kr:443'),
    ('failUrl', 'https://portal.yonsei.ac.kr:443'),
    ('baseUrl', 'https://portal.yonsei.ac.kr:443'),
    ('loginUrl', ''),
    ('loginType', 'invokeID'),
    ('E2', '243e5e56a288739ae71db63d8bbd0ac7b316913564bb9cb3ea70fdb80ac3841596e2bbc0c0bebae1477dc506837ae2462d1e8443f5de75ae7cd52400cddc030ff2f50769bae6292daeb870318fbdfb69ef2a567b9edca737e15c8cec025b2a1c0283bb0cfdc3131540315f732fad5304aef22fcfff89a487c2194516a47998cd'),
    ('E3', ''),
    ('E4', ''),
    ('ssoGubun', 'Redirect'),
    ('refererUrl', 'https://portal.yonsei.ac.kr/passni/spLogin.jsp'),
    ('a', 'aaaa'),
    ('b', 'bbbb'),
    ('loginId', ''),
    ('loginPasswd', ''),
    ('loginId', ''),
]

response = requests.post('https://infra.yonsei.ac.kr/sso/PmSSOAuthService', cookies=cookies, headers=headers, data=data)