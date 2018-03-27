import re
import requests
html = requests.get('https://kyfw.12306.cn/otn/leftTicket/init')
data = html.text
result = re.search(r"CLeftTicketUrl = '(.*?)';", data).group(1)
print(result)
