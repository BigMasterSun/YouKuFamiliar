# -*- coding: utf-8 -*-
# @Author  : Sunhaojie
# @Time    : 2019/5/26 11:24
from orm_pool import MysqlPool

# 定义数据类型
class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

class StringField(Field):
    def __init__(self, name, column_type='varchar(255)', primary_key=False, default=None):
        super().__init__(name, column_type, primary_key, default)

class IntegerField(Field):
    def __init__(self, name, column_type='int', primary_key=False, default=0):
        super().__init__(name, column_type, primary_key, default)

# 自定义元类
class MyMetaClass(type):
    def __new__(cls, class_name, class_bases, class_attrs):
        if class_name == 'Models':
            return type.__new__(cls, class_name, class_bases, class_attrs)
        table_name = class_attrs.get('table_name', class_name)
        primary_key = None
        mapping = {}
        for k, v in class_attrs.items():
            if isinstance(v, Field):
                mapping[k] = v
                if v.primary_key:
                    if primary_key:
                        raise TypeError("一张表只能有一个主键")
                    primary_key = v.name
        for k in mapping.keys():
            class_attrs.pop(k)
        if not primary_key:
            raise TypeError("一张表必须有一个主键")
        class_attrs['table_name'] = table_name
        class_attrs['primary_key'] = primary_key
        class_attrs['mapping'] = mapping
        return type.__new__(cls, class_name, class_bases, class_attrs)

class Models(dict, metaclass=MyMetaClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __getattr__(self, item):
        return self.get(item, '没有该键')

    def __setattr__(self, key, value):
        self[key] = value

    @classmethod
    def select(cls, **kwargs):
        ms = MysqlPool.Mysql()
        # select * from %s where %s=%s
        if not kwargs:
            sql = 'select * from %s' % cls.table_name
            res = ms.select(sql)
        else:
            k = list(kwargs.keys())[0]
            v = kwargs.get(k)
            sql = 'select * from %s where %s=?' % (cls.table_name, k)
            sql = sql.replace('?', '%s')
            res = ms.select(sql, v)
        if res:
            return [cls(**r) for r in res]

    def update(self):
        ms = MysqlPool.Mysql()
        # update %s set %s=%s where %s=%s
        fields = []
        pr = None
        values = []
        for k, v in self.mapping.items():
            if v.primary_key:
                pr = getattr(self, v.name, v.default)
            else:
                fields.append(v.name + '=?')
                values.append(getattr(self, v.name, v.default))
        sql = 'update %s set %s where %s=%s' % (self.table_name, ','.join(fields), self.primary_key, pr)
        sql = sql.replace('?', '%s')
        ms.execute(sql, values)

    def insert(self):
        ms = MysqlPool.Mysql()
        # insert into %s(%s,..) values(%s,..)
        fields = []
        args = []
        values = []
        for k, v in self.mapping.items():
            if not v.primary_key:
                fields.append(v.name)
                args.append('?')
                values.append(getattr(self, v.name, v.default))
        sql = 'insert into %s(%s) values(%s)' % (self.table_name, ','.join(fields), ','.join(args))
        sql = sql.replace('?', '%s')
        ms.execute(sql, values)


