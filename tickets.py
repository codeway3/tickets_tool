# -*- coding: utf-8 -*-
"""Train tickets query via command-line.

Usage:
    tickets (<from> <to> <date>) [-GCDTKZYOv]

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
    -v          调换起始车站

Example:
    tickets beijing shanghai 2016-08-25
    tickets 北京 上海 明天
"""
import os
import logging
import logging.handlers
from train import TrainCollection
from utils import logger, get_arg, get_head, get_url
import requests
from docopt import docopt
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def logger_init():
    path = './log'
    if not os.path.exists(path):
        os.makedirs(path)
    filename = path + '/all.log'
    fh = logging.handlers.RotatingFileHandler(filename, mode='a+', maxBytes=1048576, backupCount=3)
    fh.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[sh, fh])


def cli():
    """command-line interface"""
    arguments = get_arg(docopt(__doc__))
    url = get_url(arguments)
    headers = get_head()
    try:
        response = requests.get(url, verify=False, headers=headers)
        logger.debug(response)
    except Exception:
        logger.error('Requests error!')
        exit()
    if response.status_code == requests.codes.ok:
        try:
            res_json = response.json()
        except Exception:
            logger.error('JSON parse failed. Try again.')
            exit()
        else:
            logger.debug(res_json)
            if res_json['status']:
                rows = res_json['data']  # 一级解析
                trains = TrainCollection(rows, arguments)  # 二级解析 创建trains对象
                try:
                    trains.pretty_print()
                except Exception:
                    logger.error('prettytable print failed.')
                    exit()
            else:
                logger.error('Result not found. Please check the log.')


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全请求警告
    logger_init()
    cli()
