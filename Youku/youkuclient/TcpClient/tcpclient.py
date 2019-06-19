# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/5/26 12:26
import socket
from conf.settings import IP, PORT


def get_client():
    client = socket.socket()
    client.connect((IP, PORT))
    return client
