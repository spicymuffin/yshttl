
function fSubmitSSOLoginForm() {
    var tap_check = $('tap_check').value;
    if (tap_check == 'id') {
        fSubmitSSOLoginForm2();
    } else {
        NaverLoginex(e);
    }
}

function fSubmitSSOLoginForm2() {
    var loginId = $('loginId').value;
    var loginPasswd = $('loginPasswd').value;

    if ($('loginId').value == '') {
        alert('아이디를 입력하여 주십시요3.');
        $('loginId').focus();
        return false;
    }

    if ($('loginPasswd').value == '') {
        alert('비밀번호를 입력하여 주십시요.');
        $('loginPasswd').focus();
        return false;
    }

    $('loginId').value = '';
    $('loginPasswd').value = '';

    var ssoChallenge = '7CFE0AA1B13EC75201B1B77E5943CB237F2BE8D9';

    var jsonObj = { 'userid': loginId, 'userpw': loginPasswd, 'ssoChallenge': ssoChallenge };
    var jsonStr = Object.toJSON(jsonObj);

    //document.ssoLoginForm.E2.value = rstr2hex( jsonStr );

    var rsa = new RSAKey();
    rsa.setPublic('9fdcd9d44dccf0369ab9493bfd7b8ee90c4f8e67246f87e7f0978cd9f8e4ebd977d49fd4940a313f93785249b88bc033548cc0bd5305ba572383c6e2a378ae1e0399edb0dc6cbfbcb6a72fdebe3b8fc8e0e434f442f328b30134ea60e605ce2571e1a4dc713446e4193e47081fb831ee8c127f6debb977765aba6fb46e7af1bb', '10001');

    document.ssoLoginForm.E2.value = rsa.encrypt(jsonStr);

    /*
    var expDate  = new Date();
    expDate.setDate(expDate.getDate()+1);

    if (document.ssoLoginForm.idSave.checked == true) {
        jsSetCookie('cookieLoginId', loginId, expDate, '/');
    }else{
        jsSetCookie('cookieLoginId', '', expDate, '/');
    }
    */

    //return true;

    document.ssoLoginForm.submit();
}