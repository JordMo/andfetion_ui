from library.core.TestCase import TestCase
import xlrd
import requests
import os

from library.core.utils.rsa_util import RsaUtil
from settings import TEST_CASE_ROOT


class MsgAPITest(TestCase):
    """"消息解耦平台接口"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

    def test_C001_sendSmsCode(self):
        """发送短信验证码接口"""
        res = OAuthRest().sendSmsCode("13802885477")
        self.assertTrue(res.status_code == 200, 'http status code ==200')
        self.assertTrue(res.elapsed.total_seconds() < 10, 'timeout <60')
        print('url:%s,status code:%s,time:%s' % (res.url, res.status_code, res.elapsed.total_seconds()))

    def test_C002_login_by_smsCode(self):
        """短信验证码登录"""
        res = OAuthRest().login("13802885477","948096")
        self.assertTrue(res.status_code == 200, 'http status code ==200')
        self.assertTrue(res.elapsed.total_seconds() < 10, 'timeout <60')
        print(res.json())
        print('url:%s,status code:%s,time:%s' % (res.url, res.status_code, res.elapsed.total_seconds()))


class OAuthRest:

    def sendSmsCode(self, mobile):
        url = " http://221.176.34.113:8761/v1/origin/qrlogin/oauth/smscode?msisdn={}".format(mobile)
        basic = RsaUtil().get_basic()
        print("Basic:", basic)
        headers = {
            "authorization": "Basic {}".format(basic)
        }

        res = requests.post(url=url, headers=headers)
        return res

    def login(self, mobile, smsCode):
        """获取token接口"""
        url = " http://221.176.34.113:8761/v1/origin/qrlogin/oauth/token"
        basic = RsaUtil().get_basic()
        print("Basic:", basic)
        headers = {
            "authorization": "Basic {}".format(basic)
        }
        params = {
            "grant_type": "sms_code",
            "sms_code": smsCode,
            "username": mobile}

        res = requests.post(url=url,params=params, headers=headers)
        return res

    def introspect(self, accessToken):
        pass

    def refresh(self, refreshToken):
        pass

    def sip_password(self,access_token):
        """获取sip_password接口"""
        url = "http://221.176.34.113:8761/v1/origin/sso/api/sip_password"
        # access_token = "e97f1d75fdd2412b9fa20a822b67eb27"
        headers = {
            "authorization": "Bearer {}".format(access_token)
        }

        res = requests.post(url=url, headers=headers)
        return res

    def uam_token(self,access_token):
        """获取uam_token接口"""
        url = "http://221.176.34.113:8761/v1/origin/sso/api/uam_token"
        # access_token = "e97f1d75fdd2412b9fa20a822b67eb27"
        headers = {
            "authorization": "Bearer {}".format(access_token)
        }

        res = requests.post(url=url, headers=headers)
        return res



if __name__ == '__main__':
    # res = OAuthRest().sendSmsCode("13802885477")
    # print(res.status_code,res.text)
    # res = OAuthRest().login("13802885477", "672497")
    # print(res.json())
    # access_token=res.json().get('access_token')
    # print("access_token:",access_token)
    # res = OAuthRest().sip_password(access_token)
    # print(res.json())
    # res = OAuthRest().uam_token(access_token)
    # print(res.status_code)
    # print(res.raise_for_status())
    # print(res.json())
    print("\u767b\u5f55\u6210\u529f,\u6b63\u5728\u8df3\u8f6c\u4e2d")
