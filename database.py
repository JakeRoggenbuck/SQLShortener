import os.path
import sqlite3
from datetime import datetime


class DataBase:
    def __init__(self):
        self.db_name = "database.db"

    def check_file(self):
        return os.path.isfile(self.db_name)

    def setup_db(self):
        if not self.check_file():
            self.connect_db()
            self.create_table()

    def connect_db(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        sql_command = """
            CREATE TABLE links (
            message_number INTEGER PRIMARY KEY,
            url VARCHAR(2000),
            tag VARCHAR(50));"""
        self.write_db(sql_command)

    def write_db(self, command, *value):
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute(command, *value)
        connection.commit()

    def tag_check(self, tag):
        sql_command = "SELECT * FROM links WHERE tag is ?"
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute(sql_command, (tag,))
        result = cursor.fetchall()
        return result

    def write(self, url, tag):
        sql_command = """INSERT INTO links
        (message_number, url, tag)
        VALUES (NULL, ?, ?);"""
        if self.tag_check(tag) == []:
            self.write_db(sql_command, (url, tag))
            return True
        else:
            return False

    def read_db(self, command, *value):
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute(command, *value)
        result = cursor.fetchall()
        return result

    def read_all(self):
        data = "SELECT * FROM links"
        return self.read_db(data)
