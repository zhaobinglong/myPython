import pymysql
import configparser

class Mysql:
    def __init__(self):
        cf = configparser.ConfigParser()
        cf.read("config.ini")
        self.content = pymysql.Connect(
            host=cf['db']['host'],  # mysql的主机ip
            port=int(cf['db']['port']),  # 端口
            user=cf['db']['user'],  # 用户名
            passwd=cf['db']['passwd'],  # 数据库密码
            db=cf['db']['db'],  # 数据库名
            charset=cf['db']['charset'],  # 字符集
        )
        self.cursor = self.content.cursor(pymysql.cursors.DictCursor)

    def query(self,sql):
        # sql = "select * from user"
        # print(sql)
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            print ("Error: unable to fetch data")
            return 
        # return res
        # for row in self.cursor.fetchall():
        #     print(row)
        # print('db end')
        

    def end(self):
        self.content.commit()
        self.cursor.close()
        self.content.close()


# if __name__ == '__main__':
#     mysql = Mysql()
#     mysql.query()
#     mysql.end()