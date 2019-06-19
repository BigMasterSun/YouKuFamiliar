# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/5/26 11:35

from orm_pool.orm import StringField, IntegerField, Models


class User(Models):
    table_name = 'user'
    id = IntegerField(name='id', primary_key=True)
    name = StringField(name='name')
    password = StringField(name='password')
    is_vip = IntegerField(name='is_vip')
    is_locked = IntegerField(name='is_locked')
    user_type = StringField(name='user_type')
    register_time = StringField(name='register_time')


class Notice(Models):
    table_name = 'notice'
    id = IntegerField(name='id', primary_key=True)
    title = StringField(name='title')
    content = StringField(name='content')
    create_time = StringField(name='create_time')
    user_id = IntegerField(name='user_id')


class Movie(Models):
    table_name = 'movie'
    id = IntegerField(name='id', primary_key=True)
    name = StringField(name='name')
    path = StringField(name='path')
    is_free = IntegerField(name='is_free')
    is_delete = IntegerField(name='is_delete')
    file_md5 = StringField(name='file_md5')
    upload_time = StringField(name='upload_time')
    user_id = IntegerField(name='user_id')


class DownloadRecord(Models):
    table_name = 'download_record'
    id = IntegerField(name='id', primary_key=True)
    user_id = IntegerField(name='user_id')
    movie_id = IntegerField(name='movie_id')
    download_time = StringField(name='download_time')
