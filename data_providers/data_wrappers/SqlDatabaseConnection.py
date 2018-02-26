import sys, os.path
sys.path.append(os.path.abspath('../'))
from database_connections.MySqlConnection import MySqlConnection

class SqlDatabaseConnection():
    def __init__(self):
        self.conn = MySqlConnection()

    def execute_single(self, sql, data_tuple=None):
        self.conn.execute_single(sql, data_tuple)

    def execute_many(self, sql, data_tuple_list):
        self.conn.execute_many(sql, data_tuple_list)

    def query_first(self, sql, data_tuple=None):
        return self.conn.query_first(sql, data_tuple)

    def query_all(self,sql, data_tuple=None):
        return self.conn.query_all(sql, data_tuple)

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    conn = SqlDatabaseConnection()
    sql = "SELECT * FROM COMPANY WHERE CODE = 'test'"
    print(conn.query_first(sql))
    conn.close()
