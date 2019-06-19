# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/5/26 12:24
from lib import common
from db import models
import os


@common.login_auth
def buy_vip(back_dic, conn):
    user_obj = models.User.select(id=back_dic.get('user_id'))[0]
    user_obj.is_vip = 1
    user_obj.update()
    send_dic = {'flag': True, 'msg': '恭喜，购买成功！您已是尊贵的VIP用户了！'}
    common.send_msg(send_dic, conn)


@common.login_auth
def download_movie(back_dic, conn):
    movie_obj = models.Movie.select(id=back_dic.get('movie_id'))[0]
    user_obj = models.User.select(id=back_dic.get('user_id'))[0]
    file_name = movie_obj.name
    path = movie_obj.path
    file_size = os.path.getsize(path)
    wait_time = 0
    if back_dic.get('movie_type') == 'free':
        if not user_obj.is_vip:
            wait_time = 10
    send_dic = {
        'flag': True,
        'file_name': file_name,
        'file_size': file_size,
        'wait_time': wait_time
    }
    common.send_msg(send_dic, conn, path)
    download_obj = models.DownloadRecord(
        user_id=user_obj.id,
        movie_id=movie_obj.id,
        download_time=common.get_now_time()
    )
    download_obj.insert()


@common.login_auth
def check_download_record(back_dic, conn):
    download_list = models.DownloadRecord.select(user_id=back_dic.get('user_id'))
    user_obj = models.User.select(id=back_dic.get('user_id'))[0]
    back_record_list = []
    if download_list:
        for n in download_list:
            movie_obj = models.Movie.select(id=n.movie_id)[0]
            back_record_list.append({
                'user': user_obj.name,
                'movie': movie_obj.name,
                'download_time': str(n.download_time)
            })
        if back_record_list:
            send_dic = {'flag': True, 'record_list': back_record_list}
        else:
            send_dic = {'flag': False, 'msg': '暂无下载记录'}
    else:
        send_dic = {'flag': False, 'msg': '暂无下载记录'}
    common.send_msg(send_dic, conn)


@common.login_auth
def check_notice(back_dic, conn):
    back_list = get_notice_list()
    if back_list:
        send_dic = {'flag': True, 'back_list': back_list}
    else:
        send_dic = {'flag': False, 'msg': '暂无公告'}
    common.send_msg(send_dic, conn)


def get_notice_list(count=None):
    notice_list = models.Notice.select()
    back_list = []
    if notice_list:
        if not count:
            for n in notice_list:
                back_list.append({
                    'title': n.title,
                    'content': n.content
                })
        else:
            notice_list = sorted(notice_list, key=lambda notice:notice.create_time, reverse=True)
            back_list.append({
                'title': notice_list[0].title,
                'content': notice_list[0].content
            })
        if back_list:
            return back_list
        else:
            return False
    else:
        return False
