# -*- coding: utf-8 -*-

__author__ = 'masaru'

from pymongo import MongoClient


class MongoDB():
    def __init__(self, host, port, db_name):
        self.client = MongoClient(host, port)
        self.db_name = db_name
        self.db = self.load_database()

    def load_database(self):
        return self.client[self.db_name]

    def load_collection(self, col_name):
        return self.db[col_name]