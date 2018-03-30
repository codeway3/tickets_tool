import re
import time
import logging
import logging.handlers
from datetime import datetime, timedelta
from res.stations import stations
from res.pinyin import PinYin
import requests

logger = logging.getLogger(__name__)


def get_arg(arguments):
    # 当没有传入附加参数时 将默认参数均设置为True
    argkeys = ['-C', '-D', '-G', '-K', '-O', '-T', '-Y', '-Z']
    for key in argkeys:
        if arguments[key]:
            return arguments
    for key in argkeys:
        arguments[key] = True
    return arguments


def get_station_info(arguments):
    p2e = PinYin()
    p2e.load_word()
    try:
        from_station = stations.get(p2e.hanzi2pinyin(string=arguments['<from>']))
        if from_station is None:
            raise ValueError
        to_station = stations.get(p2e.hanzi2pinyin(string=arguments['<to>']))
        if to_station is None:
            raise KeyError
    except ValueError:
        logger.info('Invalid from_station name: {}'.format(arguments['<from>']))
        exit()
    except KeyError:
        logger.info('Invalid to_station name: {}'.format(arguments['<to>']))
        exit()
    else:
        return from_station, to_station


def get_date_info(arguments):
    tmp_date = arguments['<date>']
    trs = {'今天': 0, '明天': 1, '后天': 2, '大后天': 3, '0': 0, '1': 1, '2': 2, '3': 3}
    if tmp_date in trs.keys():
        now = datetime.today() + timedelta(days=trs[tmp_date])
        date = now.strftime('%Y-%m-%d')
    else:
        try:
            if len(tmp_date) == 10:
                date = tmp_date
            elif len(tmp_date) == 8:
                date = time.strftime('%Y-%m-%d', time.strptime(tmp_date, '%Y%m%d'))
            elif len(tmp_date) == 6:
                date = time.strftime('%Y-%m-%d', time.strptime(tmp_date, '%y%m%d'))
            else:
                raise Exception
        except:
            logger.info('Invalid date: {}'.format(arguments['<date>']))
            exit()
    return date


def get_url(arguments):
    html = requests.get('https://kyfw.12306.cn/otn/leftTicket/init').text
    url_model = 'https://kyfw.12306.cn/otn/{}?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'
    query_code = re.search(r"CLeftTicketUrl = '(.*?)';", html).group(1)
    date = get_date_info(arguments)
    from_station, to_station = get_station_info(arguments)
    url = url_model.format(
        query_code, date, from_station, to_station
    )
    return url


def get_head():
    headers = {
        'Cookie': 'RAIL_DEVICEID=X27r3coZZsqOEYKcfbc0xY1_s5aYoCcX8-EzeZWGLUnNBaQVKrNcMwrr2ZscDxUDPEGmzyBRzcU54fvt5aDnvxRcgGhKv7hmP5LTsQiLIRZ8aN1SoBhtTgW6Zh9EBiltVGXjplRWU_IE_3OTRf7QarduXP-k6DKt;'
    }
    return headers
