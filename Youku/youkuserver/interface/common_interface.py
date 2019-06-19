# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/5/26 12:24
from db import models
from lib import common
from TcpServer import user_data
from interface import user_interface


def register(back_dic, conn):
    user_list = models.User.select(name=back_dic.get('name'))
    if not user_list:
        user_obj = models.User(
            name=back_dic.get('name'),
            password=back_dic.get('password'),
            is_vip=0,
            is_locked=0,
            user_type=back_dic.get('user_type'),
            register_time=common.get_now_time()
        )
        user_obj.insert()
        send_dic = {'flag': True, 'msg': '注册成功！'}
    else:
        send_dic = {'flag': False, 'msg': '当前用户已存在！'}
    common.send_msg(send_dic, conn)


def login(back_dic, conn):
    user_list = models.User.select(name=back_dic.get('name'))
    user_obj = user_list[0]
    if user_list:
        if back_dic.get('user_type') == user_obj.user_type:
            if back_dic.get('password') == user_obj.password:
                send_dic = {'flag': True, 'msg': '登录成功！'}
                session = common.get_session(back_dic.get('name'))
                user_data.mutex.acquire()
                user_data.alive_user[back_dic.get('addr')] = [session, user_obj.id]
                user_data.mutex.release()
                send_dic['session'] = session
                send_dic['is_vip'] = user_obj.is_vip
                # 普通用户加公告
                if back_dic.get('user_type') == 'user':
                    notice = user_interface.get_notice_list(1)
                    send_dic['notice'] = notice
            else:
                send_dic = {'flag': False, 'msg': '密码错误，请确认！'}
        else:
            send_dic = {'flag': False, 'msg': '当前用户不是被许可登录的类型！'}
    else:
        send_dic = {'flag': False, 'msg': '当前用户不存在！'}
    common.send_msg(send_dic, conn)


@common.login_auth
def get_movie_list(back_dic, conn):
    movie_list = models.Movie.select()
    back_movie_list = []
    if movie_list:
        for n in movie_list:
            if not n.is_delete:
                if back_dic.get('movie_type') == 'all':
                    back_movie_list.append([n.name, '免费' if n.is_free else '收费', n.id])
                elif back_dic.get('movie_type') == 'free':
                    if n.is_free:
                        back_movie_list.append([n.name, '免费', n.id])
                elif back_dic.get('movie_type') == 'charge':
                    if not n.is_free:
                        back_movie_list.append([n.name, '收费', n.id])
        if back_movie_list:
            send_dic = {'flag': True, 'movie_list': back_movie_list}
        else:
            send_dic = {'flag': False, 'msg': '暂无可删除的电影'}
    else:
        send_dic = {'flag': False, 'msg': '暂无可删除的电影'}
    common.send_msg(send_dic, conn)


