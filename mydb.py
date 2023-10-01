import mysql.connector

database = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    passwd='abc123'
)

cursorObject = database.cursor()

cursorObject.execute("CREATE DATABASE elderco")

print("All Done!")