import base.singleton as sn
from data_providers.database_connections import mysql_key_path
import base.log as l
import config

import pymysql
import json


logger = l.Logger('MySqlConnection', max_len=None)


class MySqlConnection():
    def __init__(self):
        self.conn = None
        self.open()

    def open(self):
        self.conn = pymysql.connect(host=config.mysql_host,
                                    user='root',
                                    password='root',
                                    db='cs261')

    def execute(self, sql, data):
        logger.log(('executing {}'.format(sql)))
        many = type(data) is list
        if not self.conn.open:
            self.open()

        try:
            with self.conn.cursor() as cursor:
                if many:
                    cursor.executemany(sql, data)
                else:
                    cursor.execute(sql, data)

            self.conn.commit()
        except Exception as e:
            logger.log('failed with {}'.format(e))

    def query(self, sql, data, many=False):
        logger.log(('executing {}'.format(sql)), data)
        if not self.conn.open:
            self.open()
        result = None
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, data)
                if many:
                    result = cursor.fetchall()
                else:
                    result = cursor.fetchone()

            self.conn.commit()
        except Exception as e:
            logger.log('failed with {}'.format(e))
        return result

    def __del__(self):
        self.close()

    def close(self):
        if self.conn is not None \
                and self.conn.open:
            self.conn.close()
