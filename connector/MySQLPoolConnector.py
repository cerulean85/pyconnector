import os, sys, yaml
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from pymysqlpool.pool import Pool, TimeoutError
from pymysql import OperationalError

class MySQLPoolConnector:

    _instance = None
    db_address = 'localhost'
    username = 'user'
    password = 'pass'
    db_name = ''
    auto_commit = True

    def getDBOption(self):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = root_dir.split('/')
        if root_dir[len(root_dir) - 1] == 'handler':
            tmp = ''
            for i in range(0, len(root_dir) - 1):
                dir_str = root_dir[i]
                tmp = tmp + dir_str + '/'

        with open(f'earth-compose.yml') as f:
            db_option = yaml.load(f, Loader=yaml.FullLoader)
            db_option = db_option['db']
            self.db_address = db_option['address']
            self.db_name = db_option['name']
            self.username = db_option['username']
            self.password = db_option['password']
            self.auto_commit = db_option['auto_commit']

    def getPool(self):
        return Pool(host=self.db_address, user=self.username, 
            password=self.password, db=self.db_name, autocommit=self.auto_commit)

    def getConn(self):
        try:
            conn = self.pool.get_conn()
        except TimeoutError as err:
            self.pool = self.getPool()
            self.pool.init()
            conn = self.pool.get_conn()
        return conn
    
    def releasePool(self, conn):
        self.pool.release(conn)

def execute(query, pool_connector):
    pool = pool_connector.getInstance()
    conn = pool.getConn()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()

    try:
        conn.commit()
    except OperationalError as err:
        print(err)

    pool.releasePool(conn)
    return result
