import requests

# curl 命令
curl_command = "curl 'https://led-api.dian-stable.com/led/plugin/execute/540/stable' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: zh-CN,zh;q=0.9' \
  -H 'content-type: application/json; charset=UTF-8' \
  -H 'name: %E7%9D%BF%E5%AE%89' \
  -H 'origin: https://led.dian-stable.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://led.dian-stable.com/' \
  -H 'sec-ch-ua: \"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: \"macOS\"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'token: 3af0edc6ad01146abce9fe662bdd588e' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' \
  --data-raw '{\"deviceNo\":\"861711505339918\",\"tester\":\"睿安\"}'"


# 提取请求方法、请求头、请求体和URL
method = curl_command.split()[1]
headers = {}
data_index = curl_command.find("-d")
for header in curl_command.split():
    if header.startswith("-H"):
        header_parts = header.split(": ")
        if len(header_parts) == 2:
            headers[header_parts[0][2:]] = header_parts[1]
        else:
            print("Invalid header format:", header)
if data_index != -1:
    data = curl_command[data_index + 3:]
    url = curl_command.split()[-1]
else:
    data = None
    url = curl_command.split()[-1]

# 发送请求
response = requests.request(method, url, headers=headers, data=data)

# 打印响应内容
print(response.text)
