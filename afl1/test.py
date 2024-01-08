import mysql.connector
from mysql.connector import errorcode

config = {
  'host':'cloudgroup6.mysql.database.azure.com',
  'user':'Cloudgroup6',
  'password':'Kugruppe6',
  'database':'cloud',
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()
graph_id = 1702928
cursor.execute("SELECT * FROM dcrusers")

rows = cursor.fetchall()
print (rows[0][1])

conn.close()
