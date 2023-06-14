# -*- coding: utf-8 -*-
import os
import subprocess
import warnings

import pymysql
from werkzeug.security import generate_password_hash

from Service.utils import getConfig

warnings.filterwarnings("ignore")
__doc__ = """部署MySQL的脚本"""

# 数据库相关配置
dbInfo = getConfig("Database")
adminInfo = getConfig("Admin")
DB_Config = {
    "host": dbInfo["Host"],
    "port": dbInfo["Port"],
    "database": dbInfo["Database"],
    "user": dbInfo["Account"],
    "password": dbInfo["Password"]
}
DB_DDL = os.path.join(os.getcwd(), "DDL.sql").replace("\\", "/")
Admin_Config = {
    'id': adminInfo['ID'],
    'account': adminInfo['Account'],
    'password': adminInfo['Password'],
    'signature': adminInfo['Signature'],
    'email': adminInfo['E-Mail'],
    'telephone': adminInfo['Telephone'],
    'role': 'admin'
}

# 初始化数据库
print("初始化数据库")
rootPasswd = input("请输入MySQL root用户密码：")
try:
    db = pymysql.connect(host=DB_Config["host"],
                         port=DB_Config["port"],
                         user="root",
                         password=rootPasswd)
    cursor = db.cursor()
except pymysql.err.OperationalError:
    print("数据库连接失败，请检查MySQL服务是否正常，或root用户的密码是否正确")
    exit(1)
print("数据库连接成功，正在使用root用户初始化数据库")
# 创建数据库
cursor.execute("CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARSET utf8 COLLATE utf8_general_ci;" % DB_Config["database"])
# 创建数据库管理员
cursor.execute("CREATE USER IF NOT EXISTS '%s'@'%s' IDENTIFIED BY '%s';" % (DB_Config["user"], DB_Config["host"], DB_Config["password"]))
cursor.execute("GRANT ALL PRIVILEGES ON %s.* TO '%s'@'%s';" % (DB_Config["database"], DB_Config["user"], DB_Config["host"]))
db.commit()
# 导入DDL
subprocess.call("mysql -u%s -p%s -h%s -P%s %s < %s" % ('root', rootPasswd, DB_Config["host"], DB_Config["port"], DB_Config["database"], DB_DDL), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
# 创建平台管理员
cursor.execute("USE %s;" % DB_Config["database"])
cursor.execute(f"INSERT INTO user(id,account,password,signature,email,telephone,role) VALUES ({Admin_Config['id']},'{Admin_Config['account']}','{generate_password_hash(Admin_Config['password'])}','{Admin_Config['signature']}','{Admin_Config['email']}','{Admin_Config['telephone']}','{Admin_Config['role']}')")
# 创建定制error
cursor.execute(r"""INSERT INTO error VALUES (404,'404错误：可莉找不到您请求的资源。','[404]Pages not Found.','如果您通过输入链接或收藏夹访问到该页面，这说明链接有误或有些文章已被删除或修改，不妨回到主页搜到那篇文章重新保存一下？ (oﾟvﾟ)ノ\n如果您在站内浏览时访问到该页面，这说明我们网站中某些跳转链接有误。இ௰இ您可以通过最下方的联系方式向我们反馈。感谢您对该项目的支持。\n如您还有其他意见/建议，同样欢迎与我们联系。\n祝您生活愉快。','2023-06-01 12:00:00',1,'https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status/404'),(418,'418错误：我不能为你冲咖啡，因为我只是个茶壶。','[418]I\'m a teapot.','本身这只是个玩笑，但现在这个响应多数时候表示服务器因爬虫而拒绝请求。也就是说，其实我已经看穿你用的是爬虫了。 ┏ (゜ω゜)=☞\n爬虫是个实用技术，但是下次记得稍微伪装一下，比如加个请求头啥的。 ε=ε=ε=(~￣▽￣)~\n并且注意要限制爬虫的速度，把别人服务器爬崩了可就摊上事了。 :\'(','2023-06-01 12:00:00',1,'https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status/418'),(500,'500错误：树状图设计者出现Bug。','[500]Internal Server Error.','这表示树状图设计者(我们的服务器)出现了内部错误இ௰இ 您可以通过最下方的联系方式向我们反馈。感谢您对该项目的支持。\n如您还有其他意见/建议，同样欢迎与我们联系。\n祝您生活愉快。','2023-06-01 12:00:00',1,'https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status/500'),(503,'503错误：土豆服务器当前不可用。','[503]Service Unavailable.','这表示服务器目前不可用，可能是我们正在维护，或者租用的某个土豆服务器崩掉了。\n这应该不是我们的锅。','2023-06-08 15:08:06',1,'https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status/503');""")
db.commit()
db.close()
print("数据库初始化完成")
