# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/5/26 12:26
from TcpClient import tcpclient
from lib import common
import os
from conf import settings
import time


user_dic = {
    'cookie': None,
    'is_vip': None
}


def register(client):
    while True:
        name = input("请设置用户名：")
        password = input("请设置密码：")
        confirm_password = input("请再次确认密码：")
        if password == confirm_password:
            send_dic = {
                'type': 'register',
                'name': name,
                'password': common.get_md5(password),
                'user_type': 'user'
            }
            back_dic = common.send_back(send_dic, client)
            if back_dic.get('flag'):
                print(back_dic.get('msg'))
                break
            else:
                print(back_dic.get('msg'))
        else:
            print("两次密码输入的不一致！")


def login(client):
    if user_dic.get('cookie'):
        print("您已登录，无需重复登录！")
        return
    while True:
        name = input("请输入用户名：")
        password = input("请输入密码：")
        send_dic = {
            'type': 'login',
            'name': name,
            'password': common.get_md5(password),
            'user_type': 'user'
        }
        back_dic = common.send_back(send_dic, client)
        if back_dic.get('flag'):
            for n in back_dic.get('notice'):
                print(n['title'])
                print(n['content'])
            time.sleep(3)
            print(back_dic.get('msg'))
            user_dic['cookie'] = back_dic.get('session')
            user_dic['is_vip'] = back_dic.get('is_vip')
            break
        else:
            print(back_dic.get('msg'))


def buy_vip(client):
    if user_dic['is_vip']:
        print("您已经是VIP用户了")
        return
    while True:
        choice = input("您确认要开通会员吗？(y/n)")
        if choice == 'y':
            send_dic = {
                'type': 'buy_vip',
                'session': user_dic['cookie']
            }
            back_dic = common.send_back(send_dic, client)
            if back_dic.get('flag'):
                print(back_dic.get('msg'))
            else:
                print(back_dic.get('msg'))
        else:
            print("期待官人下次来开通会员")
        break


def check_movie(client):
    send_dic = {
        'type': 'get_movie_list',
        'session': user_dic['cookie'],
        'movie_type': 'all'
    }
    back_dic = common.send_back(send_dic, client)
    if back_dic.get('flag'):
        for i in back_dic.get('movie_list'):
            print(i[0])
    else:
        print(back_dic.get('msg'))


def download_free_movie(client):
    while True:
        send_dic = {
            'type': 'get_movie_list',
            'session': user_dic['cookie'],
            'movie_type': 'free'
        }
        back_dic = common.send_back(send_dic, client)
        if back_dic.get('flag'):
            for i, m in enumerate(back_dic.get('movie_list')):
                print("%s--%s--%s" % (i, m[0], m[1]))
            choice = input("请输入你要下载的电影编号：")
            if not choice.isdigit():
                continue
            choice = int(choice)
            if not (choice>=0 and choice<len(back_dic.get('movie_list'))):
                continue
            send_dic = {
                'type': 'download_movie',
                'session': user_dic['cookie'],
                'movie_id': back_dic.get('movie_list')[choice][2],
                'movie_type': 'free'
            }
            back_dic = common.send_back(send_dic, client)
            if back_dic.get('flag'):
                file_name = back_dic.get('file_name')
                path = os.path.join(settings.DOWNLOAD_DIR, file_name)
                file_size = back_dic.get('file_size')
                wait_time = back_dic.get('wait_time')
                print("请等待>>>", wait_time)
                recv_size = 0
                with open(path, 'wb') as f:
                    while recv_size < file_size:
                        recv_data = client.recv(1024)
                        f.write(recv_data)
                        recv_size += len(recv_data)
                print("下载成功")
            else:
                print(back_dic.get('msg'))
        else:
            print(back_dic.get('msg'))
        break


def download_charge_movie(client):
    while True:
        send_dic = {
            'type': 'get_movie_list',
            'session': user_dic['cookie'],
            'movie_type': 'charge'
        }
        back_dic = common.send_back(send_dic, client)
        if back_dic.get('flag'):
            for i, m in enumerate(back_dic.get('movie_list')):
                print("%s--%s--%s" % (i, m[0], m[1]))
            choice = input("请输入你要下载的电影编号：")
            if not choice.isdigit():
                continue
            choice = int(choice)
            if not (choice>=0 and choice<len(back_dic.get('movie_list'))):
                continue
            send_dic = {
                'type': 'download_movie',
                'session': user_dic['cookie'],
                'movie_type': 'charge',
                'movie_id': back_dic.get('movie_list')[choice][2]
            }
            back_dic = common.send_back(send_dic, client)
            if back_dic.get('flag'):
                file_name = back_dic.get('file_name')
                path = os.path.join(settings.DOWNLOAD_DIR, file_name)
                file_size = back_dic.get('file_size')
                wait_time = back_dic.get('wait_time')
                print("请等待>>>", wait_time)
                recv_size = 0
                with open(path, 'wb') as f:
                    while recv_size < file_size:
                        recv_data = client.recv(1024)
                        f.write(recv_data)
                        recv_size += len(recv_data)
                print("下载成功")
            else:
                print(back_dic.get('msg'))
        else:
            print(back_dic.get('msg'))
        break


def check_download_record(client):
    send_dic = {
        'type': 'check_download_record',
        'session': user_dic['cookie']
    }
    back_dic = common.send_back(send_dic, client)
    if back_dic.get('flag'):
        for i in back_dic.get('record_list'):
            print("%s-%s-%s" % (i['user'],i['movie'],i['download_time']))
    else:
        print(back_dic.get('msg'))


def check_notice(client):
    send_dic = {
        'type': 'check_notice',
        'session': user_dic['cookie']
    }
    back_dic = common.send_back(send_dic, client)
    if back_dic.get('flag'):
        print(back_dic.get('back_list'))
    else:
        print(back_dic.get('msg'))


method_map = {
    '1': register,
    '2': login,
    '3': buy_vip,
    '4': check_movie,
    '5': download_free_movie,
    '6': download_charge_movie,
    '7': check_download_record,
    '8': check_notice
}


def user_view():
    client = tcpclient.get_client()
    while True:
        print('''
        1 注册
        2 登录
        3 冲会员
        4 查看视频
        5 下载免费视频
        6 下载收费视频
        7 查看观影记录
        8 查看公告 
        q 退出
        ''')
        choice = input("请选择功能编号：")
        if choice == 'q':
            break
        if choice not in method_map:
            print("请输入合法编号！")
            continue
        method_map[choice](client)