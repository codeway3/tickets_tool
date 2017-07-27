# -*- coding: utf-8 -*-
"""Train tickets query via command-line.

Usage:
    tickets [-GCDTKZYO] <from> <to> <date>

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
"""
from docopt import docopt
from stations import stations
from pinyin import PinYin
from prettytable import PrettyTable
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def colored(color, text):
    table = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[43m',
        'blue': '\033[46m',
        'purple': '\033[45m',
        'nc': '\033[0m'
    }
    cv = table.get(color)
    nc = table.get('nc')
    return ''.join([cv, text, nc])


class TrainCollection(object):

    header = 'train station time duration business first second softsleep hardsleep hardsit nosit'.split()
    alpha_tab = 'G C D T K Z Y'.split()

    def __init__(self, tmp, arguments):
        self.map = tmp['map']
        self.rows = tmp['result']
        self.arguments = arguments

    def _get_duration(self, duration):
        duration = duration.replace(':', 'h') + 'm'
        if duration.startswith('00'):
            return duration[3:]
        if duration.startswith('0'):
            return duration[1:]
        return duration

    @property
    def trains(self):
        for tmp in self.rows:
            # 数据清洗 信息提取
            row = tmp.split('|')
            train_code, start_station_code, end_station_code, from_station_code, to_station_code = row[3:8]
            start_time, arrive_time, duration = row[8:11]
            rw = row[23]
            wz, o, yw, yz = row[26:30]
            edz, ydz = row[30:32]
            swz = row[25] or row[32]  # 特等座或商务座 在数据传输中属于两列
            # 筛除停开的车次 这些车次的数据特点——起止时间均为24:00,运行时间为99h59m
            if int(duration.split(':')[0]) == 99:
                continue
            # 判断当日到达 次日到达 还是两日到达
            dur_date = 0
            if start_time > arrive_time:
                dur_date += 1
            if int(duration.split(':')[0]) > 23:
                dur_date += 1
            # 解析列车车次字母
            if train_code[0] in self.alpha_tab:
                check_code = '-' + train_code[0]
            else:
                check_code = '-O'
            # 结果筛选
            if self.arguments[check_code]:
                train = [
                    train_code,
                    '\n'.join([(colored('yellow', '始') if start_station_code == from_station_code else colored('blue', '过'))
                              + ' ' + colored('green', self.map[from_station_code]),
                              (colored('purple', '终') if end_station_code == to_station_code else colored('blue', '过'))
                              + ' ' + colored('red', self.map[to_station_code]),
                               ' ']),
                    '\n'.join([colored('green', start_time),
                               colored('red', arrive_time)]),
                    '\n'.join([self._get_duration(duration),
                               '当日到达' if dur_date == 0 else
                               '次日到达' if dur_date == 1 else
                               '两日到达']),
                    # 商务座
                    swz,  # row['swz_num'],
                    # 一等座
                    ydz,  # row['zy_num'],
                    # 二等座
                    edz,  # row['ze_num'],
                    # 软卧
                    rw,  # row['rw_num'],
                    # 硬卧
                    yw,  # row['yw_num'],
                    # 硬座
                    yz,  # row['yz_num'],
                    # 无座
                    wz,  # row['wz_num']
                ]
                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        pt.align = 'l'
        print(pt)


def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    # 当没有传入附加参数时 将默认参数均设置为True
    if (not (arguments['-C'] or arguments['-D'] or arguments['-G'] or arguments['-K'] or arguments['-O'] or arguments['-T'] or arguments['-Y'] or arguments['-Z'])):
        arguments['-C'] = arguments['-D'] = arguments['-G'] = arguments['-K'] = arguments['-O'] = arguments['-T'] = arguments['-Y'] = arguments['-Z'] = True
    # print(arguments) # 验证docopt参数
    # 调用汉字转换拼音模块
    test = PinYin()
    test.load_word()
    from_station = stations.get(test.hanzi2pinyin(string=arguments['<from>']))
    to_station = stations.get(test.hanzi2pinyin(string=arguments['<to>']))
    tmp_date = arguments['<date>']
    date = time.strftime('%Y-%m-%d', time.strptime(tmp_date, '%Y%m%d')) if len(tmp_date) == 8 else tmp_date
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
        date, from_station, to_station
    )
    # print(url)  # 验证url重组是否正确
    r = requests.get(url, verify=False)
    # print(r) # 验证url返回状态码
    # print(r.json()) # 验证request返回的json数据
    rows = r.json()['data']  # 一级解析
    # print(rows)  # 验证一级解析结果
    trains = TrainCollection(rows, arguments)  # 二级解析 创建trains对象
    trains.pretty_print()  # 完全解析 命令行输出查询结果


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全请求警告
    cli()
