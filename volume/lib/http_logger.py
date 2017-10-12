# coding: utf-8

import logging
import logging.handlers


class Log:
    def __init__(self, name, host, url):
        self.name = name
        self.host = host
        self.url = url
        self.initialize()

    def initialize(self):
        # create stream handler
        self.logger = logging.getLogger(self.name)
        http_handler = logging.handlers.HTTPHandler(self.host, self.url, method='POST')
        http_handler.setLevel(logging.INFO)
        
        # create logging format
        formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
        http_handler.setFormatter(formatter)
        
        # add handler to the logger
        self.logger.addHandler(http_handler)
    
    def get_logger(self):
        return self.logger

    def __str__(self):
        return ("\n Name: \t{}\n Host: \t{}\n url: \t{}\n".format(self.name, self.host, self.url))


        
