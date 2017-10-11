# -*- coding: utf-8 -*-
"""Train tickets query via command-line.

Usage:
    tickets [-GCDTKZYO] (<from> <to> <date>)

Options:
    -h,--help   显示帮助菜单
    -G          高铁
    -C          城际
    -D          动车
    -T          特快
    -K          快速
    -Z          直达
    -Y          旅游
    -O          其他

Example:
    tickets beijing shanghai 2016-08-25
    tickets 北京 上海 明天
"""
from res.stations import stations
from res.pinyin import PinYin
from train import TrainCollection
from docopt import docopt
from datetime import datetime, timedelta
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def get_arg():
    arguments = docopt(__doc__)
    # 当没有传入附加参数时 将默认参数均设置为True
    argkeys = ['-C', '-D', '-G', '-K', '-O', '-T', '-Y', '-Z']
    for key in argkeys:
        if arguments[key]:
            return arguments
    for key in argkeys:
        arguments[key] = True
    return arguments


def deal_arg(arguments):
    p2e = PinYin()
    p2e.load_word()
    from_station = stations.get(p2e.hanzi2pinyin(string=arguments['<from>']))
    to_station = stations.get(p2e.hanzi2pinyin(string=arguments['<to>']))
    tmp_date = arguments['<date>']
    trs = {'今天': 0, '明天': 1, '后天': 2, '大后天': 3, '0': 0, '1': 1, '2': 2, '3': 3}
    if tmp_date in trs.keys():
        now = datetime.today() + timedelta(days=trs[tmp_date])
        date = now.strftime('%Y-%m-%d')
    else:
        date = time.strftime('%Y-%m-%d', time.strptime(tmp_date, '%Y%m%d')) if len(tmp_date) == 8 else tmp_date
    return date, from_station, to_station


def get_urls(arguments):
    date, from_station, to_station = deal_arg(arguments)
    url_models = ['https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT',
                  'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT']
    for url_model in url_models:
        url = url_model.format(
            date, from_station, to_station
        )
        yield url


def get_head():
    headers = {
        'Cookie': 'RAIL_DEVICEID=X27r3coZZsqOEYKcfbc0xY1_s5aYoCcX8-EzeZWGLUnNBaQVKrNcMwrr2ZscDxUDPEGmzyBRzcU54fvt5aDnvxRcgGhKv7hmP5LTsQiLIRZ8aN1SoBhtTgW6Zh9EBiltVGXjplRWU_IE_3OTRf7QarduXP-k6DKt;'
    }
    return headers


def cli():
    """command-line interface"""
    arguments = get_arg()
    headers = get_head()
    for url in get_urls(arguments):
        response = requests.get(url, verify=False, headers=headers)
        if response.status_code == requests.codes.ok:
            res_json = response.json()
            if res_json['status']:
                rows = res_json['data']  # 一级解析
                trains = TrainCollection(rows, arguments)  # 二级解析 创建trains对象
                trains.pretty_print()
                break


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全请求警告
    cli()
