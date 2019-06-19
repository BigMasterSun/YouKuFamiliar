# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/5/26 12:26
from TcpClient import tcpclient
from lib import common
from conf import settings
import os

user_dic = {
    'cookie': None
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
                'user_type': 'admin'
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
            'user_type': 'admin'
        }
        back_dic = common.send_back(send_dic, client)
        if back_dic.get('flag'):
            print(back_dic.get('msg'))
            user_dic['cookie'] = back_dic.get('session')
            break
        else:
            print(back_dic.get('msg'))


def upload_movie(client):
    while True:
        # 获取本地上传的文件列表
        movie_list = os.listdir(settings.UPLOAD_DIR)
        if movie_list:
            for i, m in enumerate(movie_list):
                print("%s----%s" % (i, m))
            choice = input("请选择要上传的电影编号：")
            if not choice.isdigit():
                print("请输入数字！")
                continue
            choice = int(choice)
            if not (choice >= 0 and choice < len(movie_list)):
                print("请输入合法编号！")
                continue
            file_name = movie_list[choice]
            file_path = os.path.join(settings.UPLOAD_DIR, file_name)
            file_md5 = common.get_file_md5(file_path)
            # 先检查文件是否已经上传过
            send_dic = {
                'type': 'check_movie',
                'session': user_dic['cookie'],
                'file_md5': file_md5
            }
            back_dic = common.send_back(send_dic, client)
            if back_dic.get('flag'):
                is_free = input("请选择是否免费？(y/n)")
                is_free = 1 if is_free == 'y' else 0
                file_size = os.path.getsize(file_path)
                send_dic = {
                    'type': 'upload_movie',
                    'session': user_dic['cookie'],
                    'file_size': file_size,
                    'file_md5': file_md5,
                    'is_free': is_free,
                    'file_name': file_name
                }
                back_dic = common.send_back(send_dic, client, file_path)
                if back_dic.get('flag'):
                    print(back_dic.get('msg'))
                else:
                    print(back_dic.get('msg'))
            else:
                print(back_dic.get('msg'))
        else:
            print("暂无可上传的电影！")
        break


def delete_movie(client):
    while True:
        # 先获取服务端没有被删除的电影列表
        send_dic = {
            'type': 'get_movie_list',
            'session': user_dic['cookie'],
            'movie_type': 'all'
        }
        back_dic = common.send_back(send_dic, client)
        if back_dic.get('flag'):
            movie_list = back_dic.get('movie_list')
            for i, m in enumerate(movie_list):
                print("%s>>>>>>%s" % (i, m[0]))
            choice = input("请选择要删除的电影：")
            if not choice.isdigit():
                print("请输入数字！")
                continue
            choice = int(choice)
            if not (choice >= 0 and choice <= len(movie_list)):
                print("请输入合法编号！")
                continue
            send_dic = {
                'type': 'delete_movie',
                'session': user_dic['cookie'],
                'movie_id': movie_list[choice][2]
            }
            back_dic = common.send_back(send_dic, client)
            if back_dic.get('flag'):
                print(back_dic.get('msg'))
            else:
                print(back_dic.get('msg'))
        else:
            print(back_dic.get('msg'))
        break


def release_notice(client):
    title = input("请输入标题：")
    content = input("请输入内容：")
    send_dic = {
        'type': 'release_notice',
        'session': user_dic['cookie'],
        'title': title,
        'content': content
    }
    back_dic = common.send_back(send_dic, client)
    if back_dic.get('flag'):
        print(back_dic.get('msg'))
    else:
        print(back_dic.get('msg'))


method_map = {
    '1': register,
    '2': login,
    '3': upload_movie,
    '4': delete_movie,
    '5': release_notice
}


def admin_view():
    client = tcpclient.get_client()
    while True:
        print('''
        1.注册
        2.登陆
        3.上传视频
        4.删除视频
        5.发布公告
        q.退出
        ''')
        choice = input("请选择功能编号：")
        if choice == 'q':
            break
        if choice not in method_map:
            print("请输入合法编号！")
            continue
        method_map[choice](client)
