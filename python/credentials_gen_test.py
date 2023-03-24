import json
import rsa
import base64

userid = "**replaced ALIAS using filter-repo**"
userpw = "password"
ssoChallenge = '7CFE0AA1B13EC75201B1B77E5943CB237F2BE8D9'
jsonObj = {'userid': userid, 'userpw': userpw, 'ssoChallenge': ssoChallenge}

y = json.dumps(jsonObj, separators=(',', ':'))
message = str(y)

publicKeyHex = ('9fdcd9d44dccf0369ab9493bfd7b8ee90c4f8e67246f87e7f0978cd9f8e4ebd977d49fd4940a313f93785249b88bc033548cc0bd5305ba572383c6e2a378ae1e0399edb0dc6cbfbcb6a72fdebe3b8fc8e0e434f442f328b30134ea60e605ce2571e1a4dc713446e4193e47081fb831ee8c127f6debb977765aba6fb46e7af1bb', '10001')
publicKey = rsa.PublicKey(int(publicKeyHex[0], 16), int(publicKeyHex[1], 16))

encMsg = rsa.encrypt(message.encode(), publicKey)
print(encMsg.hex())

