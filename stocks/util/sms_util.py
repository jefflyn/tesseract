from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from twilio.rest import Client

from stocks.util import date_const
from stocks.util.redis_util import redis_client

# 短信应用SDK AppID
appid = 1400185234  # SDK AppID是1400开头
# 短信应用SDK AppKey
appkey = "a80fcf217cf739252966e2c6c7ee09bf"
# 需要发送短信的手机号码
phone_numbers = ["18507550586"]
# 短信模板ID，需要在短信应用中申请
template_id = 280325
# 签名
sms_sign = "咕噜魔法阵"
ssender = SmsSingleSender(appid, appkey)

send_counter = {}

# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'AC8128c48b3aa034887774f93bf31be8cc'
auth_token = 'fffd970e7721acdf33d1c6567a1d927b'
client = Client(account_sid, auth_token)


def send_msg_with_twilio(msg='', to=''):
    message = client.messages.create(body=msg, from_='+15874176562', to=to)
    print('send_msg_with_twilio: ' + message.status)
    return message


def send_msg_with_tencent(code=None, name='', price='', to=phone_numbers[0]):
    result = None
    try:
        # if code is None:
        #     return
        # 当模板没参数时，`params = []`，数组具体的元素个数和模板中变量个数必须一致，例如事例中templateId:5678对应一个变量，参数数组中元素个数也必须是一个
        params = [name, price]
        # 签名参数未提供或者为空时，会使用默认签名发送短信
        if code in send_counter.keys() and send_counter[code] > 3:
            print('%s提醒超过3次，今天不再提醒！')
            return
        result = ssender.send_with_param(86, to, template_id, params, sign=sms_sign, extend="", ext="")
        send_counter[code] += 1
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)
    return result


def send_future_msg_with_tencent(code=None, name='', price='', suggest='', to=phone_numbers[0]):
    result = None
    try:
        params = [name, price, suggest]
        # 签名参数未提供或者为空时，会使用默认签名发送短信
        if code in send_counter.keys() and send_counter[code] > 3:
            print('%s提醒超过3次，今天不再提醒！')
            return

        if redis_client.get('MSG_COUNT_' + name) is not None and float(redis_client.get('MSG_COUNT_' + name)) >= 3:
            print("该提示超过限制，不再发送信息!")
            return
        result = ssender.send_with_param(86, to, 849005, params, sign=sms_sign, extend="", ext="")
        redis_client.incr('MSG_COUNT_' + name)
        if float(redis_client.get('MSG_COUNT_' + name)) == 3:
            redis_client.expire('MSG_COUNT_' + name, date_const.ONE_MINUTE * 15)
        send_counter[code] += 1
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)
    return result


if __name__ == '__main__':
    send_msg_with_twilio(msg='hello', to='+8618507550586')

