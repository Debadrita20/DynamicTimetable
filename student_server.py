import datetime
import pickle
import socket
from threading import Thread

import mysql.connector
date='20-04-2023'
# date=datetime.date.today()

class ThreadForClient(Thread):
    def __init__(self, ip, port, u, co):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.username = u
        self.conn = co
        print('Client having Username ', self.username, ' connected to the student server')
        print('IP Address: ', self.ip, '\nPort No.: ', self.port)

    def run(self):
        while True:
            data = self.conn.recv(1024).decode('utf-8')
            message = ''
            connected = True
            if data == '1':
                c=mydb.cursor()
                c.execute("SELECT class,year FROM student_info where username='" + self.username + "'")
                res=c.fetchone()
                c.execute("SELECT subject FROM teach_subjects where class='"+res[0]+"' and year='"+str(res[1])+"' and com='Y'")
                subjects=c.fetchall()
                c.execute("SELECT elective FROM stud_elective where username='" + self.username + "'")
                electives=c.fetchall()
                times=[]
                today=datetime.datetime.strptime(date,'%d-%m-%Y').weekday()
                week_start= datetime.datetime.strptime(date,'%d-%m-%Y') - datetime.timedelta(days=today)
                week_start_date=week_start.strftime("%d-%m-%Y")
                week_end= week_start + datetime.timedelta(days=7)
                week_end_date = week_end.strftime("%d-%m-%Y")
                for su in subjects:
                    c.execute("SELECT subject,day,start_time,end_time FROM original_routine where subject='"+su[0]+"' and class='"+res[0]+"' and year='"+str(res[1])+"' and changed='N'")
                    t=c.fetchall()
                    for x in t:
                        times.append(x)
                    c.execute("SELECT subject,date,start_time,end_time,type FROM routine where subject='" + su[0] + "' and class='" + res[0] +"' and year='"+str(res[1])+"' and istemp='N'")
                    t=c.fetchall()
                    for x in t:
                        times.append(x)
                    c.execute("SELECT subject,date,start_time,end_time,type FROM routine where subject='" + su[
                        0] + "' and class='" + res[0] + "' and year='" + str(res[1]) + "' and istemp='Y' and date>='"+week_start_date+"' and date<='"+week_end_date+"'")
                    t = c.fetchall()
                    for x in t:
                        times.append(x)
                for el in electives:
                    c.execute("SELECT subject,day,start_time,end_time FROM original_routine where subject='" + el[
                        0] + "' and class='" + res[0] + "' and year='" + str(res[1]) + "' and changed='N'")
                    t = c.fetchall()
                    for x in t:
                        times.append(x)
                    c.execute("SELECT subject,date,start_time,end_time,type FROM routine where subject='" + el[
                        0] + "' and class='" + res[0] + "' and year='" + str(res[1]) + "' and istemp='N'")
                    t = c.fetchall()
                    for x in t:
                        times.append(x)
                    c.execute("SELECT subject,date,start_time,end_time,type FROM routine where subject='" + el[
                        0] + "' and class='" + res[0] + "' and year='" + str(res[
                                  1]) + "' and date>='" + week_start_date + "' and istemp='Y' and date<='" + week_end_date + "'")
                    t = c.fetchall()
                    for x in t:
                        times.append(x)
                week=dict()
                week_days=['MON','TUE','WED','THU','FRI','SAT','SUN']
                for tin in range(len(times)):
                    ti=times[tin]
                    if len(ti)==5:
                        day=datetime.datetime.strptime(ti[1],'%d-%m-%Y').weekday()
                        if week_days[day] in week:
                            week[week_days[day]].append((ti[0],ti[2],ti[3],ti[4]))
                        else:
                            week[week_days[day]]=[(ti[0], ti[2], ti[3], ti[4])]
                    else:
                        if ti[1] in week:
                            week[ti[1]].append((ti[0],ti[2],ti[3],'c'))
                        else:
                            week[ti[1]]=[(ti[0], ti[2], ti[3], 'c')]
                c.execute("SELECT * FROM holiday where date>='"+week_start_date + "' and date<='" + week_end_date + "'")
                hhs=c.fetchall()
                hs,bc=[],[]
                for h in hhs:
                    d,n=h[0],h[1]
                    day = datetime.datetime.strptime(d, '%d-%m-%Y').weekday()
                    hs.append(week_days[day])
                    bc.append(n)
                tt=''
                for w in week_days:
                    if w in hs:
                        tt+=w+": HOLIDAY- "+bc[hs.index(w)]+"\n"
                        continue
                    if w not in week:
                        tt+=w+": No Classes\n"
                        continue
                    clss=week[w]
                    clss.sort(key=lambda x: x[1])
                    tt+=w+":\n"
                    for cls in clss:
                        tt+=cls[1]+"-"+cls[2]+" "+cls[0]+"("+cls[3]+")\n"
                message=tt
            elif data=='2':
                c=mydb.cursor()
                c.execute("SELECT class,year FROM student_info where username='" + self.username + "'")
                res = c.fetchone()
                print(str(res))
                c.execute("SELECT no FROM stud_elective where username='" + self.username + "'")
                ns=c.fetchall()
                ns=[x[0] for x in ns]
                c.execute("SELECT subject,elec_no FROM electives where cls='"+res[0]+"' and yr='"+str(res[1])+"'")
                elecs=c.fetchall()
                if elecs is None:
                    self.conn.send('None'.encode('utf-8'))
                    continue
                flag=0
                for e in elecs:
                    if e[1] not in ns:
                        flag=1
                        break
                if flag==0:
                    self.conn.send('None'.encode('utf-8'))
                    continue
                self.conn.send('Yes'.encode('utf-8'))
                el_dict=dict()
                for e in elecs:
                    if e[1] in el_dict:
                        el_dict[e[1]].append(e[0])
                    else:
                        el_dict[e[1]]=[e[0]]
                self.conn.send(pickle.dumps(el_dict))
                cho_el=pickle.loads(self.conn.recv(1024))
                sql="INSERT INTO stud_elective(username,elective,no) VALUES (%s,%s,%s)"
                for ce in cho_el:
                    c.execute(sql,(self.username,ce[1],ce[0]))
                mydb.commit()
                message='Successfully Updated'
            elif data=='3':
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
            elif data == '4':
                message = 'Logged out..\n'
                connected = False
            self.conn.send(message.encode('utf-8'))
            if not connected:
                break
        print('Client having Username ', self.username, ' logged out from IP Address ', self.ip, ' and port ', self.port)


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 2016))

    mydb = mysql.connector.connect(host="localhost", user="user", password="1234", database="mydb")

    while True:
        s.listen(5)
        (conn, (ip, port)) = s.accept()  # accept connection from a client
        u = conn.recv(1024).decode('utf-8')
        newthread = ThreadForClient(ip, port, u, conn)  # create a new thread for this client
        newthread.start()  # start the thread