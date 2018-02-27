import pymysql

class MySqlConnection():
    def __init__(self):
        self.conn = None
        self.open()

    def open(self):
        self.conn = pymysql.connect(host="localhost",
                                    user="root",
                                    password="password",
                                    db="company_data")

    def __exec(self, sql, data_tuple):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, data_tuple)
        except (AttributeError, pymysql.OperationalError):
            self.open()
            cursor = self.conn.cursor()
            cursor.execute(sql, data_tuple)
        return cursor

    def execute_single(self, sql, data_tuple):
        cursor = self.__exec(sql, data_tuple)
        self.conn.commit()
        cursor.close()

    def execute_many(self, sql, data_tuple_list):
        try:
            cursor = self.conn.cursor()
            cursor.executemany(sql, data_tuple_list)
        except (AttributeError, pymysql.OperationalError):
            self.open()
            cursor = self.conn.cursor()
            cursor.executemany(sql, data_tuple_list)
        self.conn.commit()
        cursor.close()

    def query_first(self, sql, data_tuple):
        cursor = self.__exec(sql,data_tuple)
        result = cursor.fetchone()
        cursor.close()
        return result

    def query_all(self,sql, data_tuple):
        cursor = self.__exec(sql,data_tuple)
        result = cursor.fetchall()
        cursor.close()
        return result

    def close(self):
        self.conn.close()
