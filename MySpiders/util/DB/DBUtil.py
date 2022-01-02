from configparser import ConfigParser
from enum import Enum

import pymysql
from pymysql import err

DBConfigPath = "DBConfig.conf"
config = ConfigParser()
config.read(DBConfigPath)


class BaseDBUtil:
    """
    基本DB操作工具类
    """
    DB_name = None

    @classmethod
    def create_DB(cls, DBName):
        raise NotImplementedError

    @classmethod
    def create_table_with_schema(cls, DBName, tableName, schemaList: {}):
        raise NotImplementedError

    @classmethod
    def create_table_with_class(cls, DBName, tableName, data_class: object):
        raise NotImplementedError

    @classmethod
    def save(cls, DBName, tableName, data):
        raise NotImplementedError

    @classmethod
    def read_in_loop(cls, DBName, tableName):
        raise NotImplementedError

    @classmethod
    def read(cls, DBName, tableName):
        raise NotImplementedError

    @classmethod
    def execute(cls, expression: str):
        raise NotImplementedError


class DBOperationResult:
    """
    操作结果
    """
    is_success: bool = None
    msg: str = None
    data: iter = None

    def __init__(self, result: bool, msg: str, data: []):
        self.is_success = result
        self.msg = msg
        self.data = data

    @staticmethod
    def success(data):
        return DBOperationResult(True, "", data)

    @staticmethod
    def fail(msg: str):
        return DBOperationResult(False, msg, None)


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
        cls.execute('create database if not exists' + DBName + ';')

    @classmethod
    def execute(cls, expression: str):
        try:
            cls.cursor.execute(expression)
        except err.MySQLError as exception:
            cls.db.rollback()
            return DBOperationResult.fail(str(exception))
        else:
            cls.db.commit()
            return DBOperationResult.success(cls.cursor.fetchall())

    @classmethod
    def read(cls, DBName, tableName):
        sql = "use" + DBName + ";\n" + "select * from " + tableName + ";\n"
        return cls.execute(sql)

    @classmethod
    def create_table_with_schema(cls, DBName, tableName, schemaMap: {}):

        data = ""
        for schema in schemaMap:
            data = data + schema + " " + schemaMap[schema] + ",\n"
        sql = "use " + DBName + ";" \
                                "create table " + tableName + "(" + data + ");"
        return cls.execute(sql)

    # todo
    @classmethod
    def create_table_with_class(cls, DBName, tableName, data_class: object):
        schemaMap = {}
        for attr in data_class.__dict__:
            pass
        pass

    @classmethod
    def save(cls, DBName, tableName, data):
        pass

    @classmethod
    def read_in_loop(cls, DBName, tableName):
        pass
