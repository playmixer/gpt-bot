import logging
from datetime import datetime
import os


def logger(prefix='', suffix=''):
    if not os.path.exists("./logs"):
        os.mkdir("./logs")
    logging.basicConfig(filename=f'./logs/{prefix}{datetime.now().strftime("%Y-%m-%d")}{suffix}.log', encoding='utf-8',
                        level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    return logging
