"""
用于从12306的车站信息列表更新生成本地的车站信息文件

TODO
在12306更新过数据格式后 该模块需要重写
"""
import re
import requests
from pprint import pprint


url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8963'
r = requests.get(url, verify=False)
stations = re.findall(r'([A-Z]+)\|([a-z]+)', r.text)
stations = dict(stations)
stations = dict(zip(stations.values(), stations.keys()))
pprint(stations, indent=4)
