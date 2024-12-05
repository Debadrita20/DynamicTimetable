import datetime
import pickle
import socket
from threading import Thread

import mysql.connector

date='20-04-2023'
# date=datetime.date.today()
week_days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

class ThreadForClient(Thread):
    def __init__(self, ip, port, u, co):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.username = u
        self.conn = co
        print('Client having Username ', self.username, ' connected to the teacher server')
        print('IP Address: ', self.ip, '\nPort No.: ', self.port)

    def run(self):
        while True:
            data = self.conn.recv(1024).decode('utf-8')
            message = ''
            connected = True
            if data == '1':
                c = mydb.cursor()
                c.execute("SELECT subject,class,year FROM teach_subjects where username='" + self.username + "'")
                subjects = c.fetchall()
                times = []
                today = datetime.datetime.strptime(date, '%d-%m-%Y').weekday()
                week_start = datetime.datetime.strptime(date, '%d-%m-%Y') - datetime.timedelta(days=today)
                week_start_date = week_start.strftime("%d-%m-%Y")
                week_end = week_start + datetime.timedelta(days=7)
                week_end_date = week_end.strftime("%d-%m-%Y")
                for su in subjects:
                    c.execute("SELECT subject,day,start_time,end_time FROM original_routine where subject='" + su[
                        0] + "' and class='" + su[1] + "' and year='" + str(su[2]) + "' and changed='N'")
                    t = c.fetchall()
                    for x in t:
                        times.append(x)
                    c.execute("SELECT subject,date,start_time,end_time,type FROM routine where subject='" + su[
                        0] + "' and class='" + su[1] + "' and year='" + str(su[2]) + "' and istemp='N'")
                    t = c.fetchall()
                    for x in t:
                        times.append(x)
                    c.execute("SELECT subject,date,start_time,end_time,type FROM routine where subject='" + su[
                        0] + "' and class='" + su[1] + "' and year='" + str(su[2]) + "' and istemp='Y' and date>='" + week_start_date + "' and date<='" + week_end_date + "'")
                    t = c.fetchall()
                    for x in t:
                        times.append(x)
                week = dict()
                for tin in range(len(times)):
                    ti = times[tin]
                    if len(ti) == 5:
                        day = datetime.datetime.strptime(ti[1], '%d-%m-%Y').weekday()
                        if week_days[day] in week:
                            week[week_days[day]].append((ti[0], ti[2], ti[3], ti[4]))
                        else:
                            week[week_days[day]] = [(ti[0], ti[2], ti[3], ti[4])]
                    else:
                        if ti[1] in week:
                            week[ti[1]].append((ti[0], ti[2], ti[3], 'c'))
                        else:
                            week[ti[1]] = [(ti[0], ti[2], ti[3], 'c')]
                c.execute(
                    "SELECT * FROM holiday where date>='" + week_start_date + "' and date<='" + week_end_date + "'")
                hhs = c.fetchall()
                hs, bc = [], []
                for h in hhs:
                    d, n = h[0], h[1]
                    day = datetime.datetime.strptime(d, '%d-%m-%Y').weekday()
                    hs.append(week_days[day])
                    bc.append(n)
                tt = ''
                for w in week_days:
                    if w in hs:
                        tt += w + ": HOLIDAY- " + bc[hs.index(w)] + "\n"
                        continue
                    if w not in week:
                        tt+=w+": No Classes\n"
                        continue
                    clss = week[w]
                    clss.sort(key=lambda x: x[1])
                    tt += w + ":\n"
                    for cls in clss:
                        tt += cls[1] + "-" + cls[2] + " " + cls[0] + "(" + cls[3] + ")\n"
                message = tt

            elif data=='2':
                c=mydb.cursor()
                c.execute("SELECT class,year FROM teach_subjects where username='" + self.username + "'")
                classes = c.fetchall()
                clsses=[str(x[0])+'-'+str(x[1]) for x in classes]
                self.conn.send(pickle.dumps(clsses))
                cl=self.conn.recv(1024).decode('utf-8')
                cls=classes[clsses.index(cl)]
                c.execute("SELECT subject FROM teach_subjects where class='" + cls[0] + "' and year='" + str(cls[1]) + "'")
                subjects = c.fetchall()
                times = []
                today = datetime.datetime.strptime(date, '%d-%m-%Y').weekday()
                week_start = datetime.datetime.strptime(date, '%d-%m-%Y') - datetime.timedelta(days=today)
                week_start_date = week_start.strftime("%d-%m-%Y")
                week_end = week_start + datetime.timedelta(days=7)
                week_end_date = week_end.strftime("%d-%m-%Y")
                for su in subjects:
                    c.execute("SELECT subject,day,start_time,end_time FROM original_routine where subject='" + su[
                        0] + "' and class='" + cls[0] + "' and year='" + str(cls[1]) + "' and changed='N'")
                    t = c.fetchall()
                    for x in t:
                        times.append(x)
                    c.execute("SELECT subject,date,start_time,end_time,type FROM routine where subject='" + su[
                        0] + "' and class='" + cls[0] + "' and year='" + str(cls[1]) + "' and istemp='N'")
                    t = c.fetchall()
                    for x in t:
                        times.append(x)
                    c.execute("SELECT subject,date,start_time,end_time,type FROM routine where subject='" + su[
                        0] + "' and class='" + cls[0] + "' and year='" + str(cls[
                                  1]) + "' and istemp='Y' and date>='" + week_start_date + "' and date<='" + week_end_date + "'")
                    t = c.fetchall()
                    for x in t:
                        times.append(x)
                week = dict()

                for tin in range(len(times)):
                    ti = times[tin]
                    if len(ti) == 5:
                        day = datetime.datetime.strptime(ti[1], '%d-%m-%Y').weekday()
                        if week_days[day] in week:
                            week[week_days[day]].append((ti[0], ti[2], ti[3], ti[4]))
                        else:
                            week[week_days[day]] = [(ti[0], ti[2], ti[3], ti[4])]
                    else:
                        if ti[1] in week:
                            week[ti[1]].append((ti[0], ti[2], ti[3], 'c'))
                        else:
                            week[ti[1]] = [(ti[0], ti[2], ti[3], 'c')]
                c.execute(
                    "SELECT * FROM holiday where date>='" + week_start_date + "' and date<='" + week_end_date + "'")
                hhs = c.fetchall()
                hs, bc = [], []
                for h in hhs:
                    d, n = h[0], h[1]
                    day = datetime.datetime.strptime(d, '%d-%m-%Y').weekday()
                    hs.append(week_days[day])
                    bc.append(n)
                tt = ''
                for w in week_days:
                    if w in hs:
                        tt += w + ": HOLIDAY- " + bc[hs.index(w)] + "\n"
                        continue
                    if w not in week:
                        tt+=w+": No Classes\n"
                        continue
                    clss = week[w]
                    clss.sort(key=lambda x: x[1])
                    tt += w + ":\n"
                    for cls in clss:
                        tt += cls[1] + "-" + cls[2] + " " + cls[0] + "(" + cls[3] + ")\n"
                message = tt
            elif data=='3':
                c = mydb.cursor()
                c.execute("SELECT subject,class,year FROM teach_subjects where username='" + self.username + "'")
                subjects = c.fetchall()
                self.conn.send(pickle.dumps(subjects))
                req = pickle.loads(self.conn.recv(1024))
                sel = subjects[subjects.index(req[0])]
                st_time = req[3][:req[3].index('-')].strip()
                end_time = req[3][req[3].index('-') + 1:].strip()
                c.execute("SELECT * FROM routine where class='" + sel[1] + "' and year='" + str(sel[
                    2]) + "' and istemp='Y' and date='" + req[
                              1] + "' and start_time<'" + end_time + "' and end_time>='" + end_time + "'")
                ans = c.fetchall()
                if ans:
                    print('ddd ',str(ans))
                    self.conn.send('Unable to be scheduled due to conflict'.encode('utf-8'))
                    continue
                c.execute("SELECT * FROM routine where class='" + sel[1] + "' and year='" + str(sel[
                    2]) + "' and istemp='Y' and date='" + req[
                              1] + "' and end_time>'" + st_time + "' and start_time<='" + st_time + "'")
                ans = c.fetchall()
                if ans:
                    print('eee ',str(ans))
                    self.conn.send('Unable to be scheduled due to conflict'.encode('utf-8'))
                    continue
                c.execute("SELECT * FROM original_routine where class='" + sel[1] + "' and year='" + str(sel[2]) + "' and changed='N' and day='"+week_days[datetime.datetime.strptime(req[2], '%d-%m-%Y').weekday()]+ "' and end_time>'" + st_time + "' and start_time<='" + st_time + "'")
                ans = c.fetchall()
                if ans:
                    print('fff ',str(ans))
                    self.conn.send('Unable to be scheduled due to conflict'.encode('utf-8'))
                    continue
                c.execute("SELECT * FROM original_routine where class='" + sel[
                    1] + "' and year='" + str(sel[2]) + "' and changed='N' and day='" + week_days[
                              datetime.datetime.strptime(req[2],
                                                         '%d-%m-%Y').weekday()] + "' and start_time<'" + end_time + "' and end_time>='" + end_time + "'")
                ans = c.fetchall()
                if ans:
                    print('ggg ',str(ans))
                    self.conn.send('Unable to be scheduled due to conflict'.encode('utf-8'))
                    continue
                c.execute("SELECT date,start_time,end_time FROM routine where class='" + sel[1] + "' and year='" + str(sel[2]) + "' and istemp='N'")
                ans = c.fetchall()
                flag=0
                for a in ans:
                    d1=datetime.datetime.strptime(req[2],'%d-%m-%Y').weekday()
                    d2=datetime.datetime.strptime(a[0],'%d-%m-%Y').weekday()
                    if d1==d2:
                        if a[1]<end_time<=a[2] or a[1]<=st_time<a[2]:
                            print('hhh ',str(a))
                            self.conn.send('Unable to be scheduled due to conflict'.encode('utf-8'))
                            flag=1
                            break
                if flag==1:
                    continue
                sql = "INSERT INTO routine(subject,class,year,date,start_time,end_time,type,istemp) VALUES(%s,%s,%s," \
                      "%s,%s,%s,%s,%s) "
                c.execute(sql,(sel[0],sel[1],sel[2],req[2],st_time,end_time,req[1],req[4]))
                mydb.commit()
                message = 'Successfully Scheduled'

            elif data=='4':
                c = mydb.cursor()
                c.execute("SELECT subject,class,year FROM teach_subjects where username='" + self.username + "'")
                subjects = c.fetchall()
                times = []
                today = datetime.datetime.strptime(date, '%d-%m-%Y').weekday()
                week_start = datetime.datetime.strptime(date, '%d-%m-%Y') - datetime.timedelta(days=today)
                week_end = week_start + datetime.timedelta(days=7)
                for su in subjects:
                    c.execute("SELECT subject,class,year,day,start_time,end_time FROM original_routine where subject='" + su[
                        0] + "' and class='" + su[1] + "' and year='" + str(su[2]) + "' and changed='N'")
                    t = c.fetchall()
                    for x in t:
                        times.append(x)
                    c.execute("SELECT subject,class,year,date,start_time,end_time,type,istemp FROM routine where subject='" + su[
                        0] + "' and class='" + su[1] + "' and year='" + str(su[2]) + "' and istemp='N'")
                    t = c.fetchall()
                    for x in t:
                        times.append(x)
                    c.execute("SELECT subject,class,year,date,start_time,end_time,type FROM routine where subject='" + su[
                        0] + "' and class='" + su[1] + "' and year='" + str(su[
                                  2]) + "' and istemp='Y' and date>='" + date + "'")
                    t = c.fetchall()
                    for x in t:
                        times.append(x)
                clss=[]
                for tin in range(len(times)):
                    ti = times[tin]
                    if len(ti) == 8:
                        day = datetime.datetime.strptime(ti[1], '%d-%m-%Y').weekday()
                        clss.append(week_days[day]+" "+ti[0]+"("+ti[1]+"-"+str(ti[2])+") "+ti[4]+"-"+ti[5]+" "+ti[6])
                    elif len(ti)==7:
                        clss.append(ti[3] + " " + ti[0] + "(" + ti[1] + "-" + str(ti[2]) + ") " + ti[4] + "-" + ti[
                            5] + " " + ti[6])
                    else:
                        clss.append(ti[3] + " " + ti[0] + "(" + ti[1] + "-" + str(ti[2]) + ") " + ti[4] + "-" + ti[5] + " c")
                self.conn.send(pickle.dumps(clss))
                req = pickle.loads(self.conn.recv(1024))
                sel=times[clss.index(req[0])]
                if len(sel)==8:
                    if req[1]=='N':
                        sql="DELETE FROM routine where subject='"+sel[0]+"' and class='"+sel[1]+"' and year='"+str(sel[2])+"' date='"+sel[3]+"'"
                        c.execute(sql)
                        mydb.commit()
                    else:
                        sql = "DELETE FROM routine where subject='" + sel[0] + "' and class='" + sel[
                            1] + "' and year='" + str(sel[2]) + "' date='" + sel[3] + "'"
                        c.execute(sql)
                        sql="INSERT INTO routine(subject,class,year,date,start_time,end_time,type,istemp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                        day = datetime.datetime.strptime(sel[3], '%d-%m-%Y').weekday()
                        if today<day:
                            cd= week_end + datetime.timedelta(days=(day + 1))
                        else:
                            cd = week_end + datetime.timedelta(days=(day + 8))
                        val=(sel[0],sel[1],sel[2],cd,sel[4],sel[5],sel[6],sel[7])
                        c.execute(sql,val)
                        mydb.commit()
                elif len(sel)==7:
                        sql="DELETE FROM routine where subject='"+sel[0]+"' and class='"+sel[1]+"' and year='"+str(sel[2])+"' date='"+sel[3]+"'"
                        c.execute(sql)
                        mydb.commit()

                else:
                    if req[1]=='N':
                        sql="UPDATE original_routine SET changed='Y' where subject='"+sel[0]+"' and class='"+sel[1]+"' and year='"+str(sel[2])+"' day='"+sel[3]+"'"
                        c.execute(sql)
                        mydb.commit()
                    else:
                        sql = "UPDATE original_routine SET changed='Y' where subject='" + sel[0] + "' and class='" + \
                              sel[1] + "' and year='" + str(sel[2]) + "' and day='" + sel[3] + "'"
                        c.execute(sql)
                        sql="INSERT INTO routine(subject,class,year,date,start_time,end_time,type,istemp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                        if today<week_days.index(sel[3]):
                            cd= week_end + datetime.timedelta(days=(week_days.index(sel[3]) + 1))
                        else:
                            cd = week_end + datetime.timedelta(days=(week_days.index(sel[3]) + 8))
                        val=(sel[0],sel[1],sel[2],cd,sel[4],sel[5],'c','N')
                        c.execute(sql,val)
                        mydb.commit()
                message='Successfully Cancelled'
            elif data=='5':
                c = mydb.cursor()
                c.execute("SELECT subject,class,year FROM teach_subjects where username='" + self.username + "'")
                subjects = c.fetchall()
                times = []
                today = datetime.datetime.strptime(date, '%d-%m-%Y').weekday()
                week_start = datetime.datetime.strptime(date, '%d-%m-%Y') - datetime.timedelta(days=today)
                week_start_date = week_start.strftime("%d-%m-%Y")
                week_end = week_start + datetime.timedelta(days=7)
                week_end_date = week_end.strftime("%d-%m-%Y")
                for su in subjects:
                    c.execute(
                        "SELECT subject,class,year,day,start_time,end_time FROM original_routine where subject='" +
                        su[0] + "' and class='" + su[1] + "' and year='" + str(su[2]) + "' and changed='N'")
                    t = c.fetchall()
                    for x in t:
                        times.append(x)
                    c.execute(
                        "SELECT subject,class,year,date,start_time,end_time,type,istemp FROM routine where subject='" +
                        su[0] + "' and class='" + su[1] + "' and year='" + str(su[2]) + "' and istemp='N'")
                    t = c.fetchall()
                    for x in t:
                        times.append(x)
                    c.execute(
                        "SELECT subject,class,year,date,start_time,end_time,type FROM routine where subject='" + su[
                            0] + "' and class='" + su[1] + "' and year='" + str(su[
                            2]) + "' and istemp='Y' and date>='" + date + "'")
                    t = c.fetchall()
                    for x in t:
                        times.append(x)
                clss = []
                for tin in range(len(times)):
                    ti = times[tin]
                    if len(ti) == 8:
                        day = datetime.datetime.strptime(ti[1], '%d-%m-%Y').weekday()
                        clss.append(week_days[day] + " " + ti[0] + "(" + ti[1] + "-" + str(ti[2]) + ") " + ti[4] + "-" + ti[
                            5] + " " + ti[6])
                    elif len(ti) == 7:
                        clss.append(ti[3] + " " + ti[0] + "(" + ti[1] + "-" + str(ti[2]) + ") " + ti[4] + "-" + ti[
                            5] + " " + ti[6])
                    else:
                        clss.append(ti[3] + " " + ti[0] + "(" + ti[1] + "-" + str(ti[2]) + ") " + ti[4] + "-" + ti[5] + " c")
                self.conn.send(pickle.dumps(clss))
                req = pickle.loads(self.conn.recv(1024))
                sel = times[clss.index(req[0])]
                st_time=req[2][:req[2].index('-')].strip()
                end_time=req[2][req[2].index('-')+1:].strip()
                c.execute("SELECT * FROM routine where class='" + sel[1] + "' and year='" + str(sel[
                    2]) + "' and istemp='Y' and date='" + req[
                              1] + "' and start_time<'" + end_time + "' and end_time>='" + end_time + "'")
                ans = c.fetchall()
                if ans:
                    self.conn.send('Unable to be rescheduled due to conflict'.encode('utf-8'))
                    continue
                c.execute("SELECT * FROM routine where class='" + sel[1] + "' and year='" + str(sel[
                    2]) + "' and istemp='Y' and date='" + req[
                              1] + "' and end_time>'" + st_time + "' and start_time<='" + st_time + "'")
                ans = c.fetchall()
                if ans:
                    self.conn.send('Unable to be rescheduled due to conflict'.encode('utf-8'))
                    continue
                c.execute("SELECT * FROM original_routine where class='" + sel[1] + "' and year='" + str(sel[
                    2]) + "' and changed='N' and day='" + week_days[datetime.datetime.strptime(req[1],
                                                                                              '%d-%m-%Y').weekday()] + "' and end_time>'" + st_time + "' and start_time<='" + st_time + "'")
                ans = c.fetchall()
                if ans:
                    self.conn.send('Unable to be rescheduled due to conflict'.encode('utf-8'))
                    continue
                c.execute("SELECT * FROM original_routine where class='" + sel[
                    1] + "' and year='" + str(sel[2]) + "' and changed='N' and day='" + week_days[
                              datetime.datetime.strptime(req[1],
                                                         '%d-%m-%Y').weekday()] + "' and start_time<'" + end_time + "' and end_time>='" + end_time + "'")
                ans = c.fetchall()
                if ans:
                    self.conn.send('Unable to be rescheduled due to conflict'.encode('utf-8'))
                    continue
                c.execute(
                    "SELECT date,start_time,end_time FROM routine where class='" + sel[1] + "' and year='" + str(sel[
                        2]) + "' and istemp='N'")
                ans = c.fetchall()
                flag = 0
                for a in ans:
                    d1 = datetime.datetime.strptime(req[1], '%d-%m-%Y').weekday()
                    d2 = datetime.datetime.strptime(a[0], '%d-%m-%Y').weekday()
                    if d1 == d2:
                        if a[1] < end_time <= a[2] or a[1] <= st_time < a[2]:
                            self.conn.send('Unable to be rescheduled due to conflict'.encode('utf-8'))
                            flag = 1
                            break
                if flag == 1:
                    continue
                if len(sel) == 8:
                    if req[3] == 'N':
                        sql = "UPDATE routine set date='"+req[1]+"' and start_time='"+st_time+"' and end_time='"+end_time+"' where subject='" + sel[0] + "' and class='" + sel[
                            1] + "' and year='" + str(sel[2]) + "' date='" + sel[3] + "'"
                        c.execute(sql)
                        mydb.commit()
                    else:
                        sql = "UPDATE routine set date='" + req[
                            1] + "' and start_time='" + st_time + "' and end_time='" + end_time + "' and istemp='Y' where subject='" + \
                              sel[0] + "' and class='" + sel[
                                  1] + "' and year='" + str(sel[2]) + "' date='" + sel[3] + "'"
                        c.execute(sql)
                        sql = "INSERT INTO routine(subject,class,year,date,start_time,end_time,type,istemp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                        day = datetime.datetime.strptime(sel[3], '%d-%m-%Y').weekday()
                        if today < day:
                            cd = week_end + datetime.timedelta(days=(day + 1))
                        else:
                            cd = week_end + datetime.timedelta(days=(day + 8))
                        val = (sel[0], sel[1], sel[2], cd, sel[4], sel[5], sel[6], sel[7])
                        c.execute(sql, val)
                        mydb.commit()
                elif len(sel) == 7:
                    sql = "UPDATE routine set date='" + req[
                        1] + "' and start_time='" + st_time + "' and end_time='" + end_time + "' where subject='" + sel[
                              0] + "' and class='" + sel[
                              1] + "' and year='" + str(sel[2]) + "' date='" + sel[3] + "'"
                    c.execute(sql)
                    mydb.commit()

                else:
                    sql = "UPDATE original_routine SET changed='Y' where subject='" + sel[0] + "' and class='" + \
                              sel[1] + "' and year='" + str(sel[2]) + "' and day='" + sel[3] + "'"
                    c.execute(sql)
                    sql = "INSERT INTO routine(subject,class,year,date,start_time,end_time,type,istemp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                    c.execute(sql,(sel[0],sel[1],sel[2],req[1],st_time,end_time,'c',req[3]))
                    if req[1]=='Y':
                        sql = "INSERT INTO routine(subject,class,year,date,start_time,end_time,type,istemp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                        day = datetime.datetime.strptime(sel[3], '%d-%m-%Y').weekday()
                        if today < day:
                            cd = week_end + datetime.timedelta(days=(day + 1))
                        else:
                            cd = week_end + datetime.timedelta(days=(day + 8))
                        val = (sel[0], sel[1], sel[2], cd, sel[4], sel[5], sel[6], sel[7][0])
                        c.execute(sql, val)
                    mydb.commit()
                message = 'Successfully Rescheduled'
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
    s.bind(('127.0.0.1', 2014))

    mydb = mysql.connector.connect(host="localhost", user="user", password="1234", database="mydb")

    while True:
        s.listen(5)
        (conn, (ip, port)) = s.accept()  # accept connection from a client
        u = conn.recv(1024).decode('utf-8')
        newthread = ThreadForClient(ip, port, u, conn)  # create a new thread for this client
        newthread.start()  # start the thread