import configparser


cf = configparser.ConfigParser()
cf.read("config.ini")

db_host = cf.get("db", "port")

print(cf['db']['host'])