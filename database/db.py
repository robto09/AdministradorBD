# -*- coding: utf-8 -*-
from collections import namedtuple

import psycopg2
import psycopg2.extras

import parametros as connector

bd_conn = psycopg2.connect(connector.bd_connection)

DBApi = namedtuple('DB', ['update', 'query', 'flush', 'update_flush', 'query_one', 'insert', 'execute', 'conn'])


def update(c, commit=False):
    def wrap(sql, args=None):
        cur = c.cursor()
        cur.execute(sql, args)
        if commit:
            c.commit()
        cur.close()

    return wrap


def update_flush(c):
    return update(c, commit=True)


def insert(c):
    def wrap(sql):
        cur = c.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute(sql, )
        c.commit()
        cur.close()

    return wrap


def query(c):
    def wrap(sql, args=None):
        cur = c.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute(sql, args)
        # res = cur.fetchall()
        c.commit()
        # cur.close()
        return cur

    return wrap


def query_one(c):
    def wrap(sql, args=None):
        cur = c.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute(sql, args)
        res = None
        for rs in cur:
            res = rs
        c.commit()
        cur.close()
        return res

    return wrap


def flush(c):
    def wrap():
        c.commit()
    return wrap


def execute(c):
    def wrap(sql):
        cur = c.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute(sql,)
        c.commit()
        cur.close()
    return wrap


def configurar(c):
    return DBApi(update(c), query(c), flush(c), update_flush(c), query_one(c), insert(c), execute(c), c)


DB = {
    'bd': configurar(bd_conn)
}
