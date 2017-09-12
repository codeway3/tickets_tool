from prettytable import PrettyTable


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
            dur_days = 0
            if start_time > arrive_time:
                dur_days += 1
            if int(duration.split(':')[0]) > 23:
                dur_days += 1
            # 解析列车车次字母
            if train_code[0] in self.alpha_tab:
                check_code = '-' + train_code[0]
            else:
                check_code = '-O'
            # 利用获取的信息构造train
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
                               '当日到达' if dur_days == 0 else
                               '次日到达' if dur_days == 1 else
                               '两日到达']),
                    # 商务座
                    swz,
                    # 一等座
                    ydz,
                    # 二等座
                    edz,
                    # 软卧
                    rw,
                    # 硬卧
                    yw,
                    # 硬座
                    yz,
                    # 无座
                    wz,
                ]
                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        pt.align = 'l'
        print(pt)
