"""
.. module::config
   :platform: Unix
      :synopsis: This module contains configuration files of the app.

      .. moduleauthor:: Alexandros Ntavelos <a.ntavelos@gmail.com>

      """

import os

VERSION = "0.4.0"

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

CHANNELS_PATH = os.path.join(PROJECT_PATH, "data/channels.dat")
