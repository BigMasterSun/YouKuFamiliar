# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/5/26 12:26

import os
import sys

BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)

from TcpServer import tcpserver

if __name__ == '__main__':
    tcpserver.get_server()
