import dbConnect
import socket

cursor = dbConnect.db.cursor()
query = "select * from fitness360db.groups"
cursor.execute(query)
tables = cursor.fetchall()
for table in tables:
    print(table)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to an IP with Port, could be a URL
sock.connect(('0.0.0.0', 8080))
# Send some data, this method can be called multiple times
sock.send("Twenty-five bytes to send")
# Receive up to 4096 bytes from a peer
sock.recv(4096)
# Close the socket connection, no more data transmission
sock.close()
