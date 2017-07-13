from db_connect import Connection
from db_connect import Encrypt
import sys


class MysqlSubmit:
    def proof(self, username, password):
        result = Connection().selectSQL("select password from users where name=%s", username)
        if result == None:
            return 2
        # elif str(result)[3:-3]==Encrypt().md5(password):
        elif str(result)[3:-3] == password:
            return 0
        else:
            return 1
        Connection().closeConnection()


if __name__ == "__main__":
    print (MysqlSubmit().proof(sys.argv[1], sys.argv[2]))
