#coding=utf-8
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

    def __init__(self, rows, arguments):
        self.rows = rows
        self.arguments = arguments

    def _get_duration(self, row):
        duration = row.get('lishi').replace(':', 'h') + 'm'
        if duration.startswith('00'):
            return duration[3:]
        if duration.startswith('0'):
            return duration[1:]
        return duration

    @property
    def trains(self):
        for tmp in self.rows:
            row = tmp['queryLeftNewDTO']
            row_code = row['station_train_code']
            #解析列车车次字母
            if row_code[0] in self.alpha_tab:
                check_code = '-' + row_code[0]
            else:
                check_code = '-O'
            if self.arguments[check_code]:
                train = [
                    row['station_train_code'],
                    '\n'.join([(colored('yellow', '始') if row['start_station_name'] == row['from_station_name'] else colored('blue', '过'))
                                + ' ' + colored('green', row['from_station_name']),
                               (colored('purple', '终') if row['end_station_name'] == row['to_station_name'] else colored('blue', '过'))
                                + ' ' + colored('red', row['to_station_name']),
                               ' ']),
                    '\n'.join([colored('green', row['start_time']),
                               colored('red', row['arrive_time'])]),
                    '\n'.join([self._get_duration(row),
                               '当日到达' if not int(row['day_difference']) else '次日到达']),
                    #商务座
                    row['swz_num'],
                    #一等座
                    row['zy_num'],
                    #二等座
                    row['ze_num'],
                    #软卧
                    row['rw_num'],
                    #硬卧
                    row['yw_num'],
                    #硬座
                    row['yz_num'],
                    #无座
                    row['wz_num']
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
    #print(arguments) #验证docopt参数
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    tmp_date = arguments['<date>']
    date = time.strftime('%Y-%m-%d', time.strptime(tmp_date, '%Y%m%d')) if len(tmp_date) == 8 else tmp_date
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
        date, from_station, to_station
    )
    r = requests.get(url, verify = False)
    #print(r) #验证url返回状态码
    rows = r.json()['data'] #一级解析
    trains = TrainCollection(rows, arguments) #二级解析 创建trains对象
    trains.pretty_print() #完全解析 命令行输出查询结果

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning) # 禁用安全请求警告
    cli()