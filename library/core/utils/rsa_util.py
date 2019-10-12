import base64
from rsa import common
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_v1_5_cipper
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA


def create_rsa_key():
    """利用默认的generate生成私钥和公钥"""
    rsa = RSA.generate(2048)
    pub = rsa.publickey().export_key()
    pri = rsa.export_key('PEM')
    with open('public.pem', 'w+') as pubfile:
        pubfile.write(pub.decode('utf-8'))
    with open('private.pem', 'w+') as privfile:
        privfile.write(pri.decode('utf-8'))


class RsaUtil(object):
    oauth_config = {
        "client_secret": "3JWMh734wh3YxRIeEO0wXlnkaoxujqNE",
        "client_public_key": "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDG0rmwKNdjA8crVaZizYl1LIMS\n6CJ7gaTqTdLUZn3nJ2WVqjYirm2AIgtFOF3Z7SJnGcOfHBmm7IvZTpLcbjUjYlos\nrA4b4PhkDilU3tmPkCun7SojW7qVwKRMOEwY35fNMuzagUcO6P/kl39p4WVpLh3W\n+ofIj/+FFWopGw1FbQIDAQAB\n-----END PUBLIC KEY-----",
        "client_private_key": "-----BEGIN PRIVATE KEY-----\nMIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAJXKD64CAX4mRR3Z\nx0lgU393vR7ZFDDBKQBhUWVEJjVgLu6JmppY7joQgdpZPeQWh39su4AVuY2b3CaZ\nrrtATyEvpXMdJegfSszwVTYnha1YLYj9ftP0KqQMFBjq1IXsVIRl6iSb1BxcXtDd\nZE3WzDsUiTq7DJfqp6fR7CUvIHB1AgMBAAECgYEAgtsMCaLc9Pyv4t0PGU4ag7/y\nKtHPrqwAisF53zLDAlwtg9wYgQBx1a34Eu1lgS4hXzN5NfNEr65ajCo0GIec1/Ut\nkzUI9/dpsH9SpCj30FDVK9Id4KosABm4FGiuBwpwAs3bv7VTUJDjraoKwqq8do4i\nnadg2mRx1gUOGNZa7B0CQQDRBf7xM+ciYH10ur8r9piOyWLYC+UeeQzhG9kspc4A\nVbofJ4LNKn7ztRggGCzPQWyaOAu1/U+zqAWvcbNAx9eLAkEAt3QTQHIhnAR7XEWT\n8g6uA3jm+SuTPP9edEAZW28/Buv0omc64nrIOK3y9469kNpwyCQIWMi3POd8XYtz\nP4HX/wJBALHq0J6u90ajqyX471CUjja75I7RUS0nDHdwJOOEHlzam5p5HzVTvsvi\nka5/5WRk4/RBUHaQL49UrcIwncu+TxECQFC62934W6H0tvScCcbzftA4XCw6aMjm\n+AHgU0hRZEL/guAU3Wzc609F/S3DutgLyKXKdYHckgZTN/9SZp0D3rECQD/4C/If\nYe9mmUzgn76ldVkfHXywF2SvxBFCRkzIbNihV3sT8p6q3cV6HO9sXvqKcu7KkTiV\n4OfXBbcZ1JtgGOE=\n-----END PRIVATE KEY-----",
        "client_id": "5d3fdc22dbdd7a668be5fbff"
    }
    client_public_key = RSA.importKey(oauth_config.get('client_public_key'))
    client_private_key = RSA.importKey(oauth_config.get('client_private_key'))
    client_secret = oauth_config.get('client_secret')
    client_id = oauth_config.get('client_id')

    def encrypt_by_public_key(self, encrypt_message, public_key=None):
        """使用公钥加密.
            :param encrypt_message: 需要加密的内容.
            :type encrypt_message: bytes/bytearray/memoryview
            加密之后需要对进行base64转码
        """
        if not public_key:
            public_key = self.client_public_key
        cipher = PKCS1_v1_5_cipper.new(public_key)
        encrypt_result = cipher.encrypt(encrypt_message)
        print("encrypt_result before b64encode>>>\n", encrypt_result)
        encrypt_result = base64.b64encode(encrypt_result)
        return encrypt_result

    def decrypt_by_private_key(self, decrypt_message, private_key=None):
        """使用私钥解密.
            :param decrypt_message: 需要解密的内容.
            解密之后的内容直接是字符串，不需要在进行转义
        """
        if not private_key:
            private_key = self.client_private_key
        decrypt_result = b""
        max_length = self.get_max_length(private_key, False)
        decrypt_message = base64.b64decode(decrypt_message)
        print("decrypt_message decode>>>\n", decrypt_message)
        cipher = PKCS1_v1_5_cipper.new(private_key)
        while decrypt_message:
            input_data = decrypt_message[:max_length]
            decrypt_message = decrypt_message[max_length:]
            out_data = cipher.decrypt(input_data, '')
            decrypt_result += out_data
        return decrypt_result.decode('utf-8')

    def get_max_length(self, rsa_key, encrypt=True):
        """加密内容过长时 需要分段加密 换算每一段的长度.
            :param rsa_key: 钥匙.
            :param encrypt: 是否是加密.
        """
        blocksize = common.byte_size(rsa_key.n)
        reserve_size = 11  # 预留位为11
        if not encrypt:  # 解密时不需要考虑预留位
            reserve_size = 0
        maxlength = blocksize - reserve_size
        return maxlength

    def sign_by_private_key(self, message,private_key=None):
        """私钥签名.
            :param message: 需要签名的内容.
            签名之后，需要转义后输出
        """
        if not private_key:
            private_key=self.client_private_key
        cipher = PKCS1_v1_5.new(private_key)  # 用公钥签名，会报错 raise TypeError("No private key") 如下
        # if not self.has_private():
        #   raise TypeError("No private key")
        hs = SHA.new(message)
        signature = cipher.sign(hs)
        return base64.b64encode(signature)

    def verify_by_public_key(self, message, signature,public_key=None):
        """公钥验签.
            :param message: 验签的内容.
            :param signature: 对验签内容签名的值（签名之后，会进行b64encode转码，所以验签前也需转码）.
        """
        if not public_key:
            public_key=self.client_public_key
        signature = base64.b64decode(signature)
        cipher = PKCS1_v1_5.new(public_key)
        hs = SHA.new(message)

        return cipher.verify(hs, signature)

    def get_basic(self):
        """获取basic"""
        encrypy_result = self.encrypt_by_public_key(self.client_secret.encode('utf-8'))
        content = str(self.client_id + ":").encode('utf-8') + encrypy_result
        self._basic = base64.b64encode(content).decode('utf-8')
        return self._basic


if __name__ == '__main__':
    message = 'hello world,hello world'
    public_key_str = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAl9SDv5/eZYxUczacLnn9
R6P45N5KywaFKize7uEHf1wJEDsPG4dCR9WyxmCtW4sDDimi1HrD0p2Y7lqYIoSA
ftOG1k3/MsnQMSW+coWwLH9jKL818CQ5Kj5gQ5KuE1KibDY1sGYkgQ0kClr3vVI6
xWBsA683NuTdviB+2kWDsOsKQJOK7fUimDhiNRBBHapj9dibuXDYzJ37oOWolX+R
b/u39gXz8Py5ClCvUUFxjlUSkEjVzzQXgz+JVCkc8p/7KvdHDylUm/UULT0GUzGP
LO7Pda449TurjwWY+f8Tm9H7g8WupDEeJpTnI5vphZj+fFbKkd8qEn7JWwmQXvWO
UwIDAQAB
-----END PUBLIC KEY-----"""
    private_key_str = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAl9SDv5/eZYxUczacLnn9R6P45N5KywaFKize7uEHf1wJEDsP
G4dCR9WyxmCtW4sDDimi1HrD0p2Y7lqYIoSAftOG1k3/MsnQMSW+coWwLH9jKL81
8CQ5Kj5gQ5KuE1KibDY1sGYkgQ0kClr3vVI6xWBsA683NuTdviB+2kWDsOsKQJOK
7fUimDhiNRBBHapj9dibuXDYzJ37oOWolX+Rb/u39gXz8Py5ClCvUUFxjlUSkEjV
zzQXgz+JVCkc8p/7KvdHDylUm/UULT0GUzGPLO7Pda449TurjwWY+f8Tm9H7g8Wu
pDEeJpTnI5vphZj+fFbKkd8qEn7JWwmQXvWOUwIDAQABAoIBACtXlr6asB2UCD2V
jtMzrsqHNBN9o6M+esA16/QMWBwS1WGFQoRMwe6Iwg6gZYyW6+ncl+eJHiKfK5uL
UBe2dIn/72N5A4tnkh+dkzbVFBw3x0JIB2lEpe75vHg9xKSud8BlX0E6f1w5uJqe
Kk+ozC8xHdSVbbEld2mBlETSCEx185QwU46PDdITfo1MXa01f7ryescsD2HPWIRu
cBPyZtVZjn1lMHIJHPApyLEaXo8BnzAteKpkH/Pg6gxGgLIXikDoHWv5GE5uKdkp
TLoTpwus6svL5389YEgIyQVT5dfPOEUbIxBg8NBNz70s5UPUImbjzwMZRoOv6pPu
BR2yRf0CgYEAu2nQvaHKYpIj0sAAq6cTsKggUql4yXBivnsHp/5fH0wp1855g2r3
4vnfaN9MPqJh7oB3rsoJ6WvpusbviNCSy07zbsgBZRA1rw8r+bBG4cx1jUwd4z2/
cZCgDujp0zMAhn8DN5tmwGA4iDDCV0Mw+ygYQWMOLL55foAUOZIPXqcCgYEAz2UE
ZBl0OBbBn0kDsXA5L/gM+iIYXASHq8v1p4E0s1wFG/kcW/Q2WAjIkKHnhRmxD1x4
b9NkukCe2BtpJK97cCASglm3tKh4T8X9bbduG1O8FvJR/r3e0tWLFF9TuootkTrR
azmkFXCcV1q6LNHVIT97vLk3JKDJZwSvakar1HUCgYAPXiftxNyRpKYnW/MyICsv
KzorTRZIfly6feAs2GD4cghkV9wC+LyG8jJtqRHZePtK0WH/BTY229B4rmNp9qBy
53ByvxfOL7wXNMlIWjoVvexNv9Ybki6mo1NcpaC23tHGNZgP8UBFuh4onMby3OGh
VrJWekbpSF0yEFKYPe/gtQKBgFIh7UU/F1mHGZLdNYs1qFAo6eq9SexXFuugUF7P
unE1hgh39RUtd8ARamxs0eVSMV6l/kQ68W8ZXE61PER9AmN7MBlTMn9nII5nGGA0
/nPwC1MDEBnUU8QnMXcV8XC0fCtBoeHW5/ZdrGyjz4skZkVOgNBSgVYOHvSfVGDA
MBhpAoGBAJZkP0RorBgZ23BuY/oLP/QNm8yqa+EoSajfGUtgrBUC0XRUbArRcRwh
Duj8/x7CNCT7brP/LynbsmJ9XWAEJW/kiwlAuZiQAD3WLriK/69GunN7+K+HPQro
cMLct7Ms2y+dsnuHItTpx7pyeb3Q1GryZJ+u9tN7uDQa50D+fpTT
-----END RSA PRIVATE KEY-----"""
    public_key = RSA.importKey(public_key_str)
    private_key = RSA.importKey(private_key_str)
    print("明文内容：>>> ")
    print(message)
    rsaUtil = RsaUtil()
    encrypy_result = rsaUtil.encrypt_by_public_key(message.encode('utf-8'), public_key)
    print("加密结果：>>> ")
    print(encrypy_result)

    decrypt_result = rsaUtil.decrypt_by_private_key(encrypy_result, private_key)
    print("解密结果：>>> ")
    print(decrypt_result)
    sign = rsaUtil.sign_by_private_key(message.encode('utf-8'),private_key)
    print("签名结果：>>> ")
    print(sign)
    print("验签结果：>>> ")
    print(rsaUtil.verify_by_public_key(message.encode('utf-8'), sign,public_key))
    # create_rsa_key()
