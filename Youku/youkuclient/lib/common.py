# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/5/26 12:26
import struct
import json
import hashlib
import os


def send_back(send_dic, client, file=None):
    data_bytes = json.dumps(send_dic).encode('utf-8')
    header = struct.pack('i', len(data_bytes))
    client.send(header)
    client.send(data_bytes)
    if file:
        with open(file, 'rb') as f:
            for line in f:
                client.send(line)
    head = client.recv(4)
    data = client.recv(struct.unpack('i', head)[0])
    back_dic = json.loads(data.decode('utf-8'))
    return back_dic


def get_md5(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()


def get_file_md5(file_path):
    md5 = hashlib.md5()
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        file_index = [0, file_size//3, (file_size//3)*2, file_size-10]
        with open(file_path, 'rb') as f:
            for i in file_index:
                f.seek(i)
                md5.update(f.read(10))
        return md5.hexdigest()



