from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

# 短信应用SDK AppID
appid = 1400185234  # SDK AppID是1400开头

# 短信应用SDK AppKey
appkey = "a80fcf217cf739252966e2c6c7ee09bf"

# 需要发送短信的手机号码
phone_numbers = ["18507550586"]

# 短信模板ID，需要在短信应用中申请
template_id = 280325

# 签名
sms_sign = "咕噜魔法阵"  # NOTE: 这里的签名"腾讯云"只是一个示例，真实的签名需要在短信控制台中申请，另外签名参数使用的是`签名内容`，而不是`签名ID`

ssender = SmsSingleSender(appid, appkey)
# 当模板没参数时，`params = []`，数组具体的元素个数和模板中变量个数必须一致，例如事例中templateId:5678对应一个变量，参数数组中元素个数也必须是一个

try:
    # 签名参数未提供或者为空时，会使用默认签名发送短信
    # params = ['002895 川恒股份', '12.85']
    # result = ssender.send_with_param(86, phone_numbers[0], template_id, params, sign=sms_sign, extend="", ext="")
    params = ['天然橡胶2105', '14465-14665', '做多，止损位：14400']
    result = ssender.send_with_param(86, phone_numbers[0], 849005, params, sign=sms_sign, extend="", ext="")
except HTTPError as e:
    print(e)
except Exception as e:
    print(e)

print(result)


