import requests

cookies = {
    '__smVisitorID': 'g-tIgkujyF6',
    'JSESSIONID': 'iZQLV7aJYhvlXWvBymRWmLMiFwxBp1aVUR1YnZ3KWZ5Ny4FixmeZc3Szn9CHnjKI.amV1c19kb21haW4vc3NvMV8x',
}

headers = {

}

response = requests.get('https://portal.yonsei.ac.kr/ui/thirdparty/portal/main.jsp', cookies=cookies, headers=headers)

print(response.headers)