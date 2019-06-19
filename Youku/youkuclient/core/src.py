# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/5/26 12:26
from core import admin, user

method_map = {
    '1': admin.admin_view,
    '2': user.user_view
}


def run():
    while True:
        print('''
        1、管理员视图
        2、用户视图
        q、退出
        ''')
        choice = input("请选择操作身份：")
        if choice == 'q':
            break
        if choice not in method_map:
            print("请输入合法编号！")
            continue
        method_map[choice]()