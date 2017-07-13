import pymysql.cursors
import sys
import hashlib


# read the config file
class Config:
    def __init__(self, configfile):
        f = open(configfile, 'r')
        self.dict = {}
        for i in f:
            (key, value) = i.rstrip().split('=', 1)
            self.dict[key] = value
        f.close()


    def get_value(self, key):
        #if not self.dict.has_key(key):
        if not key in self.dict:
            return
        return self.dict[key]


# md5
class Encrypt:
    def md5(self, message):
        m = hashlib.md5()
        m.update(str(message))
        return m.hexdigest()


# connect to database and execute sql
class Connection:
    # read conf and connect to database
    def getConnection(self):
        try:
            self.conf = Config('config')
            self.host = self.conf.get_value('host')
            self.port = int(self.conf.get_value('port'))
            self.user = self.conf.get_value('user')
            self.password = self.conf.get_value('password')
            self.db = self.conf.get_value('db')
            self.charset = self.conf.get_value('charset')
            self.connection = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                              db=self.db, charset=self.charset)
            self.cursor = self.connection.cursor()
            return True
        except:
            print("error when connecting to the database,suggest checking mysqld service or config file")
            return False

    # selectSQL with one argument(be used to input username and return password)
    def selectSQL(self, sql, argument):
        if (self.getConnection()):
            self.cursor.execute(sql, argument)
            result = self.cursor.fetchone()
            return result

    #
    def updateSQL(self, sql, argument1, argument2):
        if (self.getConnection()):
            self.cursor.execute(sql, (argument1, argument2))
            self.connection.commit()

    # close the connection
    def closeConnection(self):
        if hasattr(Connection, 'connection'):
            self.connection.close()


# class Submit:

if __name__ == '__main__':
    # new user
    # password=Encrypt().md5(sys.argv[2])
    # Connection().updateSQL("insert into users(name,password) values(%s,%s)",sys.argv[1],password)

    # input name and return password
    result = Connection().selectSQL("select password from users where name=%s", sys.argv[1])
    print(str(result)[3:-3])

    # delete
    # password=Encrypt().md5(sys.argv[2])
    # Connection().updateSQL("delete from users where name=%s and password=%s",sys.argv[1],password)

    Connection().closeConnection()
