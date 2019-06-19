# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/5/26 12:24
from lib import common
from db import models
import os
from conf import settings


@common.login_auth
def check_movie(back_dic, conn):
    movie_list = models.Movie.select(file_md5=back_dic.get('file_md5'))
    if movie_list:
        send_dic = {'flag': False, 'msg': '当前电影已存在'}
    else:
        send_dic = {'flag': True, 'msg': '可以上传'}
    common.send_msg(send_dic, conn)


@common.login_auth
def upload_movie(back_dic, conn):
    file_name = common.get_session(back_dic.get('file_name')) + back_dic.get('file_name')
    file_size = back_dic.get('file_size')
    file_md5 = back_dic.get('file_md5')
    is_free = back_dic.get('is_free')
    file_path = os.path.join(settings.MOVIE_DIR, file_name)
    recv_size = 0
    with open(file_path, 'wb') as f:
        while recv_size < file_size:
            recv_data = conn.recv(1024)
            f.write(recv_data)
            recv_size += len(recv_data)
    movie_obj = models.Movie(
        name=file_name,
        path=file_path,
        is_free=is_free,
        is_delete=0,
        file_md5=file_md5,
        upload_time=common.get_now_time(),
        user_id=back_dic.get('user_id')
    )
    movie_obj.insert()
    send_dic = {'flag': True, 'msg': '上传成功'}
    common.send_msg(send_dic, conn)


@common.login_auth
def delete_movie(back_dic, conn):
    movie_list = models.Movie.select(id=back_dic.get('movie_id'))
    movie_obj = movie_list[0]
    movie_obj.is_delete = 1
    movie_obj.update()
    send_dic = {'flag': True, 'msg': '删除成功'}
    common.send_msg(send_dic, conn)


@common.login_auth
def release_notice(back_dic, conn):
    notice_obj = models.Notice(
        title=back_dic.get('title'),
        content=back_dic.get('content'),
        create_time=common.get_now_time(),
        user_id=back_dic.get('user_id')
    )
    notice_obj.insert()
    send_dic = {'flag': True, 'msg': '公告发布成功'}
    common.send_msg(send_dic, conn)