import base64
import rsa
import json
import requests

# need to log into ys portal through:
# https://portal.yonsei.ac.kr/passni/spLogin.jsp
# =================== OR =====================
# https://portal.yonsei.ac.kr/SSOLegacy.do

# region constants

S1_pad = len('S1"         value="')
S1_len = len('34175A69027670C2C2B2ED852C9E1E2BD357330DE5A3D487CC24BC7324F8446B1FC345098B59C7FA28BB41737D7E5A545BA85F7B7116C9148E74EA7D515587FBECA9653CB01D8F985C7BE7052E004505AA3DA0EC4822C5BE3E348640C138612A0BBCDA1FA0532F06AD0F3D0BEC3B8CF61AFE9F6F340A606021C503323FD553EDA561838AA63D92827897AB91B4FF380C41B3E1DA45B2AC55740C9757F398575FC08634B168B580B2A6B906090AE5D007DD7F2A062B63FBCFED0A10F3D103B4B2C9E07255D2659B63E3E624F37986E902A02720AAF914BD027A6D437A0017A6EF2F052470888FC59DE716D61105F8DD92F35EAEDFD682F189735C04356829BE50')

RSAPublicKey1_pad = len("( '")
RSAPublicKey1_len = len('cd9d44dccf0369ab9493bfd7b8ee90c4f8e67246f87e7f0978cd9f8e4ebd977d49fd4940a313f93785249b88bc033548cc0bd5305ba572383c6e2a378ae1e0399edb0dc6cbfbcb6a72fdebe3b8fc8e0e434f442f328b30134ea60e605ce2571e1a4dc713446e4193e47081fb831ee8c127f6debb977765aba6fb46e7af1bb')

RSAPublicKey2_pad = len("', '")
RSAPublicKey2_len = len("10001")

ssoChallenge_pad = len("var ssoChallenge= '")

# endregion

SSOLegacy_request = requests.get(
    "https://portal.yonsei.ac.kr/SSOLegacy.do")


# region SSOLegacy_request dissect
SSOLegacy_request_content = SSOLegacy_request.content.decode()
S1_start_index = SSOLegacy_request_content.rfind("S1") + S1_pad
S1 = SSOLegacy_request_content[S1_start_index:S1_start_index + S1_len]
# endregion

# region PmSSOService data
cookies = {

}

headers = {

}

data = {
    'app_id': 'nportalYonsei',
    'retUrl': 'https://portal.yonsei.ac.kr:443',
    'failUrl': 'https://portal.yonsei.ac.kr:443',
    'baseUrl': 'https://portal.yonsei.ac.kr:443',
    'S1': S1,
    'loginUrl': '',
    'ssoGubun': 'Redirect',
    'refererUrl': 'https://portal.yonsei.ac.kr/passni/spLogin.jsp',
    'a': 'aaaa',
    'b': 'bbbb',
}

# endregion

PmSSOService_request = requests.post('https://infra.yonsei.ac.kr/sso/PmSSOService',
                                     cookies=cookies, headers=headers, data=data)


# region PmSSOService_request dissect
PmSSOService_request_content = PmSSOService_request.content.decode()
RSAPublicKey1_start_index = PmSSOService_request_content.rfind(
    "rsa.setPublic") + S1_pad
RSAPublicKey1 = PmSSOService_request_content[RSAPublicKey1_start_index:
                                             RSAPublicKey1_start_index + RSAPublicKey1_len]
RSAPublicKey2_start_index = RSAPublicKey1_start_index + \
    RSAPublicKey1_len + RSAPublicKey2_pad
RSAPublicKey2 = PmSSOService_request_content[RSAPublicKey2_start_index:
                                             RSAPublicKey2_start_index + RSAPublicKey2_len]
ssoChallenge_start_index = PmSSOService_request_content.find("var ssoChallenge= '") + ssoChallenge_pad
ssoChallenge = ""
while PmSSOService_request_content[ssoChallenge_start_index] != "'":
    ssoChallenge += PmSSOService_request_content[ssoChallenge_start_index]
    ssoChallenge_start_index += 1

# endregion

# region debug SSOLegacy_request
# print(SSOLegacy_request.content)
# endregion

# region debug PmSSOService_request
# print(PmSSOService_request.content.decode())
# print(ssoChallenge)
# print(format("LEGACY", "=^50"))
# endregion

# region output codes
# print(S1)
# print(RSAPublicKey1)
# print(RSAPublicKey2)
# endregion

userid = "**replaced USERID using filter-repo**"
userpw = "**replaced PW using filter-repo**"

jsonObj = {'userid': userid, 'userpw': userpw, 'ssoChallenge': ssoChallenge}

y = json.dumps(jsonObj, separators=(',', ':'))
message = str(y)

publicKeyHex = (RSAPublicKey1, RSAPublicKey2)
publicKey = rsa.PublicKey(int(publicKeyHex[0], 16), int(publicKeyHex[1], 16))

encMsg = rsa.encrypt(message.encode(), publicKey)


PmSSOAuthService_request_data = {
    'app_id': 'nportalYonsei',
    'retUrl': 'https://portal.yonsei.ac.kr:443',
    'failUrl': 'https://portal.yonsei.ac.kr:443',
    'baseUrl': 'https://portal.yonsei.ac.kr:443',
    'loginType': 'invokeID',
    'E2': encMsg.hex(),
    'ssoGubun': 'Redirect',
    'refererUrl': 'https://portal.yonsei.ac.kr/passni/spLogin.jsp',
    'a': 'aaaa',
    'b': 'bbbb'
}

PmSSOAuthService_request = requests.post(
    "https://infra.yonsei.ac.kr/sso/PmSSOAuthService", data=PmSSOAuthService_request_data)

print(PmSSOAuthService_request.content.decode())

s = PmSSOAuthService_request.headers["Set-Cookie"]
print(s)
# print(PmSSOAuthService_request.content.decode())
# print(PmSSOAuthService_request.headers)
# find cookie vals
__smVisitorID_cookie_name = "__smVisitorID"
__smVisitorID = ""
index = s.find(__smVisitorID_cookie_name) + \
    len(__smVisitorID_cookie_name) + 1  # this is a mess sorry
while (s[index] != ';'):
    __smVisitorID += s[index]
    index += 1

JSESSIONID_cookie_name = "JSESSIONID"
JSESSIONID = ""
index = s.find(JSESSIONID_cookie_name) + \
    len(JSESSIONID_cookie_name) + 1  # this is a mess sorry
while (s[index] != ';'):
    JSESSIONID += s[index]
    index += 1

# print(__smVisitorID)
# print(JSESSIONID)


# region cugubun_UniResult_request data
# 5p6Vgqp95tI
# mdFHOm03D4oBnjuAiIQynMKsOdqghWasUBtkKGKLrpKLJEZ0xzRCcO13f9OiRqgz.amV1c19kb21haW4vcG9ydGFsMV8x
cookies = {
    '__smVisitorID': __smVisitorID,
    'JSESSIONID': JSESSIONID,
}

headers = {

}

# endregion

cugubun_UniResult_request = requests.get(
    'https://portal.yonsei.ac.kr/ui/thirdparty/portal/main.jsp', cookies=cookies, headers=headers)


# print(cugubun_UniResult_request.content.decode())
