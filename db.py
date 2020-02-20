import pymysql

class Mysql:
    def __init__(self):
        self.content = pymysql.Connect(
            host='154.8.226.223',  # mysql的主机ip
            port=3306,  # 端口
            user='root',  # 用户名
            passwd='3ZbvwYRUFc',  # 数据库密码
            db='old_wang',  # 数据库名
            charset='utf8',  # 字符集
        )
        self.cursor = self.content.cursor()

    def query(self):
        sql = "select * from user"
        self.cursor.execute(sql)
        for row in self.cursor.fetchall():
            print(row)

    def end(self):
        self.cursor.close()
        self.content.close()


if __name__ == '__main__':
    mysql = Mysql()
    mysql.query()
    mysql.end()