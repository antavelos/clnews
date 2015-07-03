"""
.. module:: utils
   :platform: Unix
      :synopsis: This module contains general use functions.

      .. moduleauthor:: Alexandros Ntavelos <a.ntavelos@gmail.com>

      """
import re

def remove_html(string):
    p = re.compile(r'<.*?>')
    string = p.sub('', string)

    return string
