import socket
from threading import Thread

import mysql.connector

class ThreadForClient(Thread):
    def __init__(self, ip, port, u,p, co):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.username = u
        self.password=p
        self.conn = co
        print('Client connected to the authorization server')
        print('IP Address: ', self.ip, '\nPort No.: ', self.port)

    def run(self):
        mydb = mysql.connector.connect(host="localhost", user="user", password="1234", database="mydb")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM auth where username='" + self.username + "'")
        u, p, t = mycursor.fetchone()
        if p == self.password:
            msg=t
        else:
            msg="Incorrect username or password"
        self.conn.send(msg.encode('utf-8'))


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 2010))
    while True:
        s.listen(5)
        (conn, (ip, port)) = s.accept()  # accept connection from a client
        conn.send('Connected to authorization server'.encode('utf-8'))
        u = conn.recv(1024).decode('utf-8')
        p=conn.recv(1024).decode('utf-8')
        newthread = ThreadForClient(ip, port, u,p, conn)  # create a new thread for this client
        newthread.start()  # start the thread