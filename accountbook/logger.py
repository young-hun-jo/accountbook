import logging
import sys


class Logger(object):
    def __init__(self):
        self.SERVER_NAME = "zedd-accountbook"
        self.logger = logging.getLogger(self.SERVER_NAME)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s [%(name)s] [%(process)d] [%(threadName)s:%(thread)d] [%(filename)s(%(lineno)d)] %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def get_logger(self):
        return self.logger


logger = Logger().get_logger()
