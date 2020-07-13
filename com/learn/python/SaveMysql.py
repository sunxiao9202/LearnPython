import pymysql

# 使用 connect 方法，传入数据库地址，账号密码，数据库名就可以得到你的数据库对象
db = pymysql.connect("127.0.0.1", "root", "root", "python")

# 接着我们获取 cursor 来操作我们的 avIdol 这个数据库
cursor = db.cursor()

# 比如我们来创建一张数据表
sql = "select keyword from label_keyword"
cursor.execute(sql)

res = list(cursor.fetchall())
list = []
if res is not None:
    for i in res:
        list.append(i[0])

print(list)

# 最后我们关闭这个数据库的连接
db.close()
