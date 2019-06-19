# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/5/26 12:24
import struct
import json
import time
import hashlib
from functools import wraps
from TcpServer import user_data


def send_msg(back_dic, conn, file=None):
    data_bytes = json.dumps(back_dic).encode('utf-8')
    header = struct.pack('i', len(data_bytes))
    conn.send(header)
    conn.send(data_bytes)
    if file:
        with open(file, 'rb') as f:
            for line in f:
                conn.send(line)


def get_now_time():
    now = time.strftime('%Y-%m-%d %X')
    return now


def get_session(name):
    md5 = hashlib.md5()
    md5.update(str(time.clock()).encode('utf-8'))
    md5.update(name.encode('utf-8'))
    return md5.hexdigest()


def login_auth(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        # args=(back_dic, conn)
        for v in user_data.alive_user.values():  # [session, user_id]
            if args[0].get('session') == v[0]:
                args[0]['user_id'] = v[1]
                break
        if args[0].get('user_id'):
            return fn(*args, **kwargs)
        else:
            send_dic = {'flag': False, 'msg': '你不是许可的用户，请先登录！'}
            send_msg(send_dic, args[1])
    return inner


