import base.singleton as sn

import datetime
import pymongo


class MigrationTransformer(pymongo.son_manipulator.SONManipulator):
    def _encode_date(self, value):
        return str(datetime.datetime)

    def _handle_list(self, value):
        for index, item in enumerate(value):
            if isinstance(item, dict):
                value[index] = self._handle_dict(item)
            elif isinstance(item, list):
                value[index] = self._handle_list(item)
            elif type(value) is datetime.datetime:
                value[index] = self._encode_date(item)
        return value

    def _handle_dict(self, item):
        for (key, value) in item.items():
            if type(value) is datetime.datetime:
                item[key] = self._encode_datetimr(value)
            elif isinstance(value, dict):  # recurse into sub-docs
                item[key] = self._handle_dict(value)
            elif isinstance(value, list):  # recurse into sub-docs
                item[key] = self._handle_list(value)
        return item

    def transform_incoming(self, son, collection):
        for (key, value) in son.items():
            # datetime.datetime is instance of datetime.date
            # compare type explicitly only
            if type(value) is datetime.datetime:
                son[key] = self._encode_date(value)
            elif isinstance(value, dict):  # recurse into sub-docs
                son[key] = self.transform_incoming(value, collection)
            elif isinstance(value, list):  # recurse into sub-docs
                son[key] = self._handle_list(value)
        return son


class MongoConnection(sn.Singleton):
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db_name = "cs261"
        self.db = self.client[self.db_name]
        self.db.add_son_manipulator(MigrationTransformer())

    def find(self, name):
        db = self.client[name]

    def insert_one(self, data, collection):
        self.db[collection].insert_one(data)
