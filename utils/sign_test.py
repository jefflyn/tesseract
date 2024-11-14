import base64
import hashlib
import hmac
import time
import urllib.parse

timestamp = str(round(time.time() * 1000))
secret = 'SECa6abb98f7d1a96a36085d39d4a17edcc0c32621d80049c3c298bcc8acca66cc7'
secret_enc = secret.encode('utf-8')
string_to_sign = '{}\n{}'.format(timestamp, secret)
string_to_sign_enc = string_to_sign.encode('utf-8')
hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
print(timestamp)
print(sign)