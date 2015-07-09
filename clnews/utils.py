"""
.. module:: utils
   :platform: Unix
      :synopsis: This module contains general use functions.

      .. moduleauthor:: Alexandros Ntavelos <a.ntavelos@gmail.com>

      """
import re
import os
import urlparse
import urllib
import pickle

class DataFileMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(DataFileMeta, cls).__call__(*args,
                                                                    **kwargs)
        return cls._instances[cls]


class DataFile(object):
    __metaclass__ = DataFileMeta

    def __init__(self, filename):
        if not filename or not isinstance(filename, str):
            raise TypeError

        if not os.path.exists(filename):
            open(filename, 'wb').close()

        self.filename = filename

    def load(self):
        with open(self.filename, 'rb') as f:
            try:
                return pickle.load(f)
            except EOFError:
                return {}


    def save(self, data):
        with open(self.filename, 'wb') as f:
            pickle.dump(data, f)


def remove_html(string):
    p = re.compile(r'<.*?>')
    string = p.sub('', string)

    return string

def validate_url(url):
    parse_url = urlparse.urlparse(url)
    if parse_url.scheme != 'http':
        return False

    result = urllib.urlopen(url)
    if result.code != 200:
        return False

    return True
