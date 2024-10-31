
py_step('target = ' + py_result )
py begin

import mysql.connector
import json
from datetime import datetime


mydb = mysql.connector.connect(
  host="localhost",
  port="3306",
  user="root",
  password="541deren!",
  database="rpa_data"
)
mycursor = mydb.cursor()

year, month, day = map(int, target['日期'].replace("年", "-").replace("月", "-").replace("日", "").split("-"))  
date_obj = datetime(year, month, day)  

mysql_date_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')  

sql = "INSERT INTO rpa_data VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s)"
val=(target['发票号码'],target['购买方公司'],target['销售方公司'],target['购买方开户公司及账户'],target['销售方开户公司及账户'],target['购买方纳税人识别号'],target['销售方纳税人识别号'],target['税额'],target['金额'],target['总价'],mysql_date_str)

mycursor.execute(sql,val)

mydb.commit()

py finish
