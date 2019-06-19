# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/5/26 12:25
import socket
from conf.settings import IP, PORT, BACK_LOG
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from TcpServer import user_data
import json
import struct
from interface import common_interface, admin_interface, user_interface
from lib import common


pool = ThreadPoolExecutor(10)
mutex = Lock()
user_data.mutex = mutex


method_map = {
    'register': common_interface.register,
    'login': common_interface.login,
    'check_movie': admin_interface.check_movie,
    'upload_movie': admin_interface.upload_movie,
    'get_movie_list': common_interface.get_movie_list,
    'delete_movie': admin_interface.delete_movie,
    'release_notice': admin_interface.release_notice,
    'buy_vip': user_interface.buy_vip,
    'download_movie': user_interface.download_movie,
    'check_download_record': user_interface.check_download_record,
    'check_notice': user_interface.check_notice
}


def dispatch(back_dic, conn):
    if back_dic.get('type') in method_map:
        method_map[back_dic.get('type')](back_dic, conn)
    else:
        send_dic = {'flag': False, 'msg': '请进行合法的功能操作！'}
        common.send_msg(send_dic, conn)


def get_server():
    server = socket.socket()
    server.bind((IP, PORT))
    server.listen(BACK_LOG)
    while True:
        conn, addr = server.accept()
        pool.submit(working, conn, addr)


def working(conn, addr):
    while True:
        try:
            header = conn.recv(4)
            data_bytes = conn.recv(struct.unpack('i', header)[0])
            back_dic = json.loads(data_bytes.decode('utf-8'))
            back_dic['addr'] = str(addr)
            dispatch(back_dic, conn)
        except ConnectionResetError as e:
            conn.close()
            user_data.mutex.acquire()
            user_data.alive_user.pop(str(addr))
            user_data.mutex.release()
            print(e)
            break




