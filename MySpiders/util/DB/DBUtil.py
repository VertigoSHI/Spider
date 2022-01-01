from configparser import ConfigParser
from enum import Enum

import pymysql
from pymysql import err

DBConfigPath = "DBConfig.conf"
config = ConfigParser()
config.read(DBConfigPath)


# 接口类 定义基本操作
class BaseDBUtil:
    DB_name = None

    @classmethod
    def create_DB(cls, DBName):
        raise NotImplementedError

    @classmethod
    def create_table_with_schema(cls, tableName, schemaList: {}):
        raise NotImplementedError

    @classmethod
    def create_table_with_class(cls, tableName, data_class: object):
        raise NotImplementedError

    @classmethod
    def save(cls, DBName, tableName, data):
        raise NotImplementedError

    @classmethod
    def read_in_loop(cls, DBName, tableName):
        raise NotImplementedError

    @classmethod
    def read(cls, DBName, tableName) -> []:
        raise NotImplementedError

    @classmethod
    def execute(cls, expression: str):
        raise NotImplementedError


class DBOperationResult:
    is_success: bool = None
    msg: str = None

    def __init__(self, result: bool, msg: str):
        self.is_success = result
        self.msg = msg

    @staticmethod
    def success():
        return DBOperationResult(True, "")

    @staticmethod
    def fail(msg: str):
        return DBOperationResult(False, msg)


class MysqlDBUtil(BaseDBUtil):
    DB_name = "mysql"
    username = config.get(DB_name, "user")
    password = config.get(DB_name, "pass")
    port = config.get(DB_name, "port")
    host = config.get(DB_name, "host")

    db = pymysql.connect(user=username, password=password, port=int(port), host=host)
    cursor = db.cursor()

    # 创建库
    @classmethod
    def create_DB(cls, DBName):
        pass

    @classmethod
    def execute(cls, expression: str):
        try:
            cls.cursor.execute(expression)
        except err.MySQLError as e:
            cls.db.rollback()
            return DBOperationResult.fail(str(e))
        else:
            cls.db.commit()
            return DBOperationResult.success()

    @classmethod
    def read(cls, DBName, tableName) -> []:
        pass

    @classmethod
    def create_table_with_schema(cls, tableName, schemaList: {}):
        pass

    @classmethod
    def create_table_with_class(cls, tableName, data_class: object):
        pass

    @classmethod
    def save(cls, DBName, tableName, data):
        pass

    @classmethod
    def read_in_loop(cls, DBName, tableName):
        pass
