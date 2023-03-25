import requests

cookies = {
    'JSESSIONID': 'J9PJLjicFdBoSO91kXDC1inNwtiqvnNR4aVMX1FW1itdN9pUxqu59mbjXODh8Y07.amV1c19kb21haW4vc3NvMl8x',
    '__smVisitorID': 'P2DcakKN85S',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': 'JSESSIONID=J9PJLjicFdBoSO91kXDC1inNwtiqvnNR4aVMX1FW1itdN9pUxqu59mbjXODh8Y07.amV1c19kb21haW4vc3NvMl8x; __smVisitorID=P2DcakKN85S',
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
    ('E2', '47cca3f1a13ef88e4a0982452f7c8718e06122c8af1b674b0b4122525f79b63ac487f903e882bc506eeed1cbbd2a9d55f058222fb63f3adfcb6162e6046c2472f394252e967102b46908cf39c475b837e019ca0c2ec063234f14fe9935a780e8ee63dde6e429e2e8680d595ed299d0da2bf33142072bc6469433c81bd4c46c36'),
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
print(response.content.decode())