import db

mysql = db.Mysql()

res = mysql.query(sql)
print(res)