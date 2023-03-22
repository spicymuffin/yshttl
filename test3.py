import requests

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://portal.yonsei.ac.kr',
    'Referer': 'https://portal.yonsei.ac.kr/ui/index.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'listCnt': '3',
    'currPage': '1',
}


response = requests.post(
    'https://portal.yonsei.ac.kr/com/lgin/SsoCtr/isLogin.do', headers=headers, data=data)

s = response.headers["Set-Cookie"]
# find cookie vals
__smVisitorID_cookie_name = "__smVisitorID"
__smVisitorID_length = len("jyzO4zEkrL1")
index = s.rfind(__smVisitorID_cookie_name)
__smVisitorID = s[index+len(__smVisitorID_cookie_name)+1:index +
                  __smVisitorID_length+len(__smVisitorID_cookie_name)+1]

JSESSIONID_cookie_name = "JSESSIONID"
JSESSIONID_length = len(
    "gfTagH0rZlueeLmsWKternK7GMhE5t1OQmg8cblPTVfOidLxx0QKWaFiWy3f7Ab1.amV1c19kb21haW4vcG9ydGFsMV8x")
index = s.find(JSESSIONID_cookie_name)
JSESSIONID = s[index+len(JSESSIONID_cookie_name)+1:index +
               JSESSIONID_length+len(JSESSIONID_cookie_name)+1]
print(__smVisitorID)
print(JSESSIONID)

cookies = {
    '__smVisitorID': __smVisitorID,
    'JSESSIONID': JSESSIONID,
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,it;q=0.7,ru;q=0.6,ko;q=0.5,ja;q=0.4',
    'Connection': 'keep-alive',
    # 'Cookie': '__smVisitorID=g2siQHZujNM; JSESSIONID=wiRtWNabvBQiyuNJCGaLPrNCJ67YdXAvQTWIbSDSbVXHgrbIxw8GlPZmE1w2kh7Z.amV1c19kb21haW4vcG9ydGFsMl8x',
    'Referer': 'https://portal.yonsei.ac.kr/com/lgin/SsoCtr/j_login_sso.do',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

payload = {
    'wpName': 'my_username',
    'wpPassword': 'my_password',
    'wpLoginAttempt': 'Log in',
    # 'wpLoginToken': '',
}

response = requests.get('https://infra.yonsei.ac.kr/sso/PmSSOService', data=payload)

print(response.headers)



'''
<form id="ssoLoginForm" name="ssoLoginForm" method="post" action="/sso/PmSSOAuthService" onsubmit="return false;" style="display:contents;">
    <input type="hidden" id="app_id" name="app_id" value="nportalYonsei">
    <input type="hidden" id="retUrl" name="retUrl" value="https://portal.yonsei.ac.kr:443">
    <input type="hidden" id="failUrl" name="failUrl" value="https://portal.yonsei.ac.kr:443">
    <input type="hidden" id="baseUrl" name="baseUrl" value="https://portal.yonsei.ac.kr:443">
    <input type="hidden" id="loginUrl" name="loginUrl" value="">
    <input type="hidden" id="loginType" name="loginType" value="invokeID">
    <input type="hidden" id="E2" name="E2" value="">
    <input type="hidden" id="E3" name="E3" value="">
    <input type="hidden" id="E4" name="E4" value="">

    
                    <input type="hidden" id="ssoGubun" name="ssoGubun" value="Redirect">
    
                    <input type="hidden" id="refererUrl" name="refererUrl" value="https://portal.yonsei.ac.kr/passni/spLogin.jsp">
    
                    <input type="hidden" id="a" name="a" value="aaaa">
    
                    <input type="hidden" id="b" name="b" value="bbbb">
    
<!-- 여기서 작업 변경 -->
     <div class="box01">
        <p class="text01">나는 <span>연세인</span><br><span>나의 미래</span>를 만든다!</p>
        <p class="text02">진리와 자유를 향한 연세의 도전</p>
    </div>
    
        <div class="box02">
            <div>
                <div class="login-top">
                    <div class="logo-wrap"></div>
                    <ul class="login-tab">
                        <li class="is-active">
                            <a href="#none;" onclick="javascript:idPwLogin(this);">ID&amp;PW 로그인</a>
                        </li>
                        <li>
                            <a href="#none;" onclick="javascript:certLogin(this);">네이버 인증서 로그인</a>
                        </li>
                    </ul>
                </div>
                <div class="login-cont-wrap">
                    <div>
                        <!-- 오픈전 임시로 문구 표시 -->
                        <div style="height:30px;">※ 기존 연세포털(https://portal.yonsei.ac.kr)의 비밀번호로 로그인해 주십시오.</div>
                        <div id="id_pw" class="login-cont is-active">
                            <input type="text" id="loginId" name="loginId" title="아이디 혹은 학번" placeholder="학번(교번) (ID No.)" maxlength="16">
                            <input type="password" id="loginPasswd" name="loginPasswd" title="비밀번호" placeholder="비밀번호 (Password)" maxlength="16" style="display:block;">

                            <div id="info" class="error info">
                                로그인 정보 &gt; ID : 교직원 번호, 초기비밀번호 : 생년월일 6자리<br>
                                <font class="info-en">INFO &gt; ID : Employee number, Init PW: BirthDay (6 digit)</font>
                                <p class="error1" style="display:block;"></p>
                            </div>

                            <a href="#none;" id="loginBtn" class="submit" onclick="fSubmitSSOLoginForm()">로그인(Login)</a>

                        </div>
                        <div id="naver" class="login-cont">
                            <input id="loginNaverId" type="text" name="loginId" title="아이디 혹은 학번" placeholder="학번(교번) (ID No.)">
                            <div id="info" class="error info">
                                로그인 정보 &gt; ID : 교직원 번호, 초기비밀번호 : 생년월일 6자리<br>
                                <font class="info-en">INFO &gt; ID : Employee number, Init PW: BirthDay (6 digit)</font>
                                <p class="error1" style="display:block;"></p>
                            </div>
                            <a id="naverIdLogin_loginButton" onclick="NaverLoginex(event);">네이버 인증서 로그인</a>
                        </div>
                    </div>
                    <p>이용 후 반드시 로그아웃 해주세요!<br>Please be sure to log out after use.</p>
                </div>
            </div>
            <div class="m_box02">
                <ul>
                    <li>
                        <a href="javascript:checkCertNew_id();" title="새 창 열림"><span>아이디 찾기</span></a>
                    </li>
                    <li>
                        <a href="javascript:checkCertNew_pwd();" title="새 창 열림"><span>임시 비밀번호 발급</span></a>
                    </li>
                    <li>
                        <a href="https://underwood1.yonsei.ac.kr/haksa/HELP/dugrock-01.htm" target="_blank" title="새 탭 열림"><span>로그인 도움말</span></a>
                    </li>
                </ul>
                <p>COPYRIGHT© 2022 YONSEI UNIV. ALL RIGHTS RESERVED.</p>
            </div>
        </div>

        <div id="naverIdLogin" style="display:none;"><a id="naverIdLogin_loginButton" href="#"><img src="https://static.nid.naver.com/oauth/big_g.PNG?version=js-2.0.1" height="60"></a></div>
        <div id="naverdisplay" style="display:none;"><a id="naverIdLogin_loginButton" onclick="NaverLoginex(event);"><img src="/sso/user/pm/img/btnW_naver.png" tabindex="0" alt="네이버인증서로그인" style="width:260px;cursor:pointer;"></a></div>

    </form>
'''