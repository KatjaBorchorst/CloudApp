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
graph_id = "1702928"
id = int(graph_id)
sim_id = 1938786

query = f"SELECT * FROM dcrgraphs WHERE graph_id = {id}"
cursor.execute(query)
rows = cursor.fetchall()
print(rows[0] == None)
conn.close()
