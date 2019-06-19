# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/5/26 12:24
import os

IP = '127.0.0.1'
PORT = 8080
BACK_LOG = 5

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MOVIE_DIR = os.path.join(BASE_DIR, 'movie_db')