import pickle
import socket
from threading import Thread

import mysql.connector


class ThreadForClient(Thread):
    def __init__(self, ip, port, u, co):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.username = u
        self.conn = co
        print('Client having Username ', self.username, ' connected to the administration server')
        print('IP Address: ', self.ip, '\nPort No.: ', self.port)

    def run(self):
        while True:
            data = self.conn.recv(1024).decode('utf-8')
            print('Action ',data,' selected')
            message = ''
            connected = True
            if data == '1':
                pkt=self.conn.recv(1024).decode('utf-8')
                uu=pkt[:pkt.index(';')]
                pp=pkt[pkt.index(';')+1:pkt.rindex(';')]
                tt = pkt[pkt.rindex(';')+1:]
                cc=''
                yy=''
                # print(uu,' ',pp,' ',tt)
                if tt=='Student':
                    # print('here')
                    cc=self.conn.recv(1024).decode('utf-8')
                    yy=self.conn.recv(1024).decode('utf-8')
                    # print(cc,' ',yy)
                c=mydb.cursor()
                c.execute("SELECT * FROM auth where username='" + uu + "'")
                rr = c.fetchone()
                # print(rr)
                if rr is None:
                    sql='INSERT INTO auth VALUES(%s,%s,%s)'
                    val=(uu,pp,tt[0])
                    c.execute(sql,val)
                    if tt=='Student':
                        sql='INSERT INTO student_info VALUES(%s,%s,%s)'
                        val=(uu,cc,int(yy))
                        c.execute(sql, val)
                    mydb.commit()
                    message='New user successfully registered'
                else:
                    message='Username already exists..try again with another username'

            elif data=='2':
                c=mydb.cursor()
                c.execute("SELECT * FROM classes")
                all_clss=c.fetchall()
                c.execute("SELECT class,year FROM original_routine")
                done_classes=c.fetchall()
                to_do_classes=[x for x in all_clss if x not in done_classes]
                self.conn.send(pickle.dumps(to_do_classes))
                ind=int(self.conn.recv(1024).decode('utf-8'))
                print(ind,' ', type(ind))
                week=pickle.loads(self.conn.recv(1024))
                sql = 'INSERT INTO original_routine VALUES(%s,%s,%s,%s,%s,%s,%s)'
                for dd in week:
                    c.execute(sql, (dd[3],to_do_classes[ind][0],to_do_classes[ind][1],dd[0],'N',dd[1],dd[2]))
                    mydb.commit()
                message = 'Timetable Successfully Uploaded'
            elif data=='3':
                self.conn.send('Ready'.encode('utf-8'))
                hh=pickle.loads(self.conn.recv(1024))
                print(str(hh))
                c=mydb.cursor()
                sql='INSERT INTO holiday VALUES(%s,%s)'
                for h in hh:
                    print(str(h),' declared')
                    c.execute(sql,h)
                    mydb.commit()
                message='Holidays Successfully Declared'
            elif data=='4':
                c = mydb.cursor()
                c.execute("SELECT * FROM classes")
                all_clss = c.fetchall()
                c.execute("SELECT cls,yr FROM electives")
                done_classes = c.fetchall()
                to_do_classes = [x for x in all_clss if x not in done_classes]
                self.conn.send(pickle.dumps(to_do_classes))
                ind = int(self.conn.recv(1024).decode('utf-8'))
                eles = pickle.loads(self.conn.recv(1024))
                sql = 'INSERT INTO electives VALUES(%s,%s,%s,%s)'
                for i,op in enumerate(eles):
                    for ss in op:
                        c.execute(sql, (to_do_classes[ind][0],to_do_classes[ind][1],ss,i+1))
                    mydb.commit()
                message = 'List Successfully Uploaded'
            elif data=='5':
                c = mydb.cursor()
                ss = pickle.loads(self.conn.recv(1024))
                sql = 'INSERT INTO teach_subjects(username,subject,class,year) VALUES(%s,%s,%s,%s)'
                for s in ss:
                    c.execute(sql, s)
                    mydb.commit()
                message = 'Successfully Uploaded'
            elif data=='6':
                c = mydb.cursor()
                c.execute("SELECT * FROM messages where username='" + self.username + "'")
                res=c.fetchall()
                msgs=[]
                for r in res:
                    mm=r[1]+': '+r[2]
                    msgs.append(mm)
                    if r[3]=='N':
                        sql='DELETE FROM messages WHERE username=%s and timestamp=%s and msg=%s'
                        c.execute(sql,(r[0],r[1],r[2]))
                        mydb.commit()
                self.conn.send(pickle.dumps(msgs))
                continue
            elif data == '7':
                message = 'Logged out..\n'
                connected = False
            self.conn.send(message.encode('utf-8'))
            if not connected:
                break
        print('Client having Username ', self.username, ' logged out from IP Address ', self.ip, ' and port ', self.port)


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 2012))

    mydb = mysql.connector.connect(host="localhost", user="user", password="1234", database="mydb")

    while True:
        s.listen(5)
        (conn, (ip, port)) = s.accept()  # accept connection from a client
        u = conn.recv(1024).decode('utf-8')
        newthread = ThreadForClient(ip, port, u, conn)  # create a new thread for this client
        newthread.start()  # start the thread