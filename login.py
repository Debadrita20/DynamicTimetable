import pickle
import socket


def teacher(u):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 2014))
    print('Hello ', u)
    s.send(u.encode('utf-8'))

    while True:
        print('\n***************************************\nList of Actions:')
        print('1. View Own Timetable')
        print("2. View Students' Timetable")
        print('3. Schedule New Classes or Exams')
        print('4. Cancel Classes or exams')
        print('5. Reschedule Classes or exams')
        print('6. View Message Box')
        print('7. Logout')
        ch = input('Enter your choice (1-7): ')
        if ch not in ['1', '2', '3', '4', '5', '6', '7']:
            print('Invalid Action..Try Again')
            continue
        elif ch == '1':
            s.send(ch.encode('utf-8'))
            tt = s.recv(1024).decode('utf-8')
            print(tt)
        elif ch == '2':
            s.send(ch.encode('utf-8'))
            cls = pickle.loads(s.recv(1024))
            print('Enter the name of the class among the following which you want to view')
            for cl in cls:
                print(cl)
            scl = input()
            if scl.upper() not in cls:
                print('Either you do not have proper authorization for viewing this class or timetable does not exist')
            else:
                s.send(scl.encode('utf-8'))
                tt = s.recv(1024).decode('utf-8')
                print(tt)
        elif ch == '3':
            s.send(ch.encode('utf-8'))
            cls = pickle.loads(s.recv(1024))
            print('Enter the class among the following for which you want to schedule')
            for i, cl in enumerate(cls):
                print(str(i + 1), ": ", cl)
            prmt = 'Enter your choice(1-' + str(len(cls)) + '): '
            scl = input(prmt)
            if scl not in [str(i + 1) for i in range(len(cls))]:
                print('Invalid Choice')
            else:
                req = [cls[int(scl) - 1]]
                print('Enter type: c for regular class, d for doubt class, e for exam')
                type = input().lower()
                print('Enter date in dd/mm/yyyy format')
                date = input()
                print('Enter timing in format HH:MM-HH:MM e.g. if the class is to be from 2:30 pm to 3:30 pm, '
                      'enter 14:30-15:30')
                time = input()
                istemp = 'Y'
                if type == 'c':
                    print('Is this only for one time? Or should it be repeated in the future weeks? Enter R/NR for '
                          'repeating/non-repeating')
                    r = input()
                    if r == 'R':
                        istemp = 'N'
                    else:
                        istemp = 'Y'
                req.append(type)
                req.append(date)
                req.append(time)
                req.append(istemp)
                s.send(pickle.dumps(req))
                m = s.recv(1024).decode('utf-8')
                print(m)
        elif ch == '4':
            s.send(ch.encode('utf-8'))
            cls = pickle.loads(s.recv(1024))
            print('Enter the class among the following which you want to cancel')
            for i, cl in enumerate(cls):
                print(str(i + 1), ": ", cl)
            prmt = 'Enter your choice(1-' + str(len(cls)) + '): '
            scl = input(prmt)
            if scl not in [str(i + 1) for i in range(len(cls))]:
                print('Invalid Choice')
            else:
                req = [cls[int(scl) - 1]]
                type = cls[int(scl)-1][len(cls[int(scl)-1])-1]
                r='NR'
                if type == 'c':
                    print('Is this only for one time? Or should it be repeated in the future weeks? Enter R/NR for '
                          'repeating/non-repeating')
                    r = input()
                if r == 'R':
                    istemp = 'N'
                else:
                    istemp = 'Y'
                req.append(istemp)
                s.send(pickle.dumps(req))
                m = s.recv(1024).decode('utf-8')
                print(m)
        elif ch == '5':
            s.send(ch.encode('utf-8'))
            cls = pickle.loads(s.recv(1024))
            print('Enter the class among the following for which you want to reschedule')
            for i, cl in enumerate(cls):
                print(str(i + 1), ": ", cl)
            prmt = 'Enter your choice(1-' + str(len(cls)) + '): '
            scl = input(prmt)
            if scl not in [str(i + 1) for i in range(len(cls))]:
                print('Invalid Choice')
            else:
                req = [cls[int(scl) - 1]]
                print('Enter date in dd/mm/yyyy format')
                date = input()
                print('Enter timing in format HH:MM-HH:MM e.g. if the class is to be from 2:30 pm to 3:30 pm, '
                      'enter 14:30-15:30')
                time = input()
                type = cls[int(scl) - 1][len(cls[int(scl) - 1]) - 1]
                r = 'NR'
                if type == 'c':
                    print('Is this only for one time? Or should it be repeated in the future weeks? Enter R/NR for '
                          'repeating/non-repeating')
                    r = input()
                if r == 'R':
                    istemp = 'N'
                else:
                    istemp = 'Y'
                req.append(date)
                req.append(time)
                req.append(istemp)
                s.send(pickle.dumps(req))
                m = s.recv(1024).decode('utf-8')
                print(m)
        elif ch == '6':
            s.send(ch.encode('utf-8'))
            msgs = pickle.loads(s.recv(1024))
            if len(msgs) == 0:
                print('You have no unread messages')
            else:
                print('You have some new messages')
                for msg in msgs:
                    print(msg)
        elif ch == '7':
            s.send(ch.encode('utf-8'))
            break
    print('Thank you!!!')


def student(u):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 2016))
    print('Hello ', u)
    s.send(u.encode('utf-8'))

    while True:
        print('\n***************************************\nList of Actions:')
        print('1. View Own Timetable')
        print("2. Sign Up for Electives")
        print('3. View Message Box')
        print('4. Logout')
        ch = input('Enter your choice (1-4): ')
        if ch not in ['1', '2', '3', '4']:
            print('Invalid Action..Try Again')
            continue
        elif ch == '1':
            s.send(ch.encode('utf-8'))
            tt = s.recv(1024).decode('utf-8')
            print(tt)
        elif ch == '2':
            s.send(ch.encode('utf-8'))
            m=s.recv(1024).decode('utf-8')
            if m=='None':
                print('No electives to sign up for at this point of time')
                continue
            else:
                li=pickle.loads(s.recv(1024))
                print('List of Electives')
                for choi in li.keys():
                    print(str(choi)+': '+str(li[choi]))
                print('Enter the chosen electives (you can choose some later) in the following format:')
                print('1. Distributed Computing\n2. Optimization Systems\nDone')
                print('Enter the word "Done" after choosing the electives you want now')
                ch_li=[]
                while True:
                    cc=input()
                    if cc=='Done':
                        break
                    nu=cc[:cc.index('.')].strip()
                    sub=cc[cc.index('.')+1:].strip()
                    ch_li.append((nu,sub))
                s.send(pickle.dumps(ch_li))
                m = s.recv(1024).decode('utf-8')
                print(m)
        elif ch == '3':
            s.send(ch.encode('utf-8'))
            msgs = pickle.loads(s.recv(1024))
            if len(msgs) == 0:
                print('You have no unread messages')
            else:
                print('You have some new messages')
                for msg in msgs:
                    print(msg)
        elif ch == '4':
            s.send(ch.encode('utf-8'))
            break
        '''elif ch == '3':
                    s.send(ch.encode('utf-8'))
                    print('Enter type: sp for project work supervised by a teacher, p for placement commitments, '
                          'e for extra-curriculars')
                    type = input().lower()
                    print('Enter date in dd/mm/yyyy format')
                    date = input()
                    print('Enter timing in format HH:MM-HH:MM e.g. if the class is to be from 2:30 pm to 3:30 pm, '
                          'enter 14:30-15:30')
                    time = input()
                    namesp = 'NA'
                    if type == 'sp':
                        namesp = input('Enter name of the supervisor: ')
                    req = [type, date, time, namesp]
                    s.send(pickle.dumps(req))
                    m = s.recv(1024).decode('utf-8')
                    print(m)
                elif ch == '4':
                    s.send(ch.encode('utf-8'))
                    cls = s.recv(1024).decode('utf-8')
                    print('Enter the booking among the following which you want to cancel')
                    for i, cl in enumerate(cls):
                        print(str(i + 1), ": ", cl)
                    prmt = 'Enter your choice(1-' + str(len(cls)) + '): '
                    scl = input(prmt)
                    if scl not in [str(i + 1) for i in range(len(cls))]:
                        print('Invalid Choice')
                    else:
                        req = [cls[int(scl) - 1]]
                        s.send(pickle.dumps(req))
                        m = s.recv(1024).decode('utf-8')
                        print(m)'''
    print('Thank you!!!')


def admin(u):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 2012))
    print('Hello ', u)
    s.send(u.encode('utf-8'))

    while True:
        print('\n***************************************\nList of Actions:')
        print('1. Register new user')
        print("2. Initialize the Timetable")
        print('3. Declare Holidays')
        print('4. Publish List of Electives')
        print('5. Update the list of subjects offered by a teacher')
        print('6. View Message Box')
        print('7. Logout')
        ch = input('Enter your choice (1-7): ')
        if ch not in ['1', '2', '3', '4', '5', '6', '7']:
            print('Invalid Action..Try Again')
            continue
        elif ch == '1':
            s.send(ch.encode('utf-8'))
            uu = input('Username: ')
            pp = input('Password: ')
            tt = input('Designation (Admin/Teacher/Student): ')
            pkt=uu+';'+pp+';'+tt
            s.send(pkt.encode('utf-8'))
            if tt=='Student':
                cls=input('Class: ')
                yr=input('Year: ')
                s.send(cls.encode('utf-8'))
                s.send(yr.encode('utf-8'))
            m = s.recv(1024).decode('utf-8')
            print(m)
        elif ch == '2':
            s.send(ch.encode('utf-8'))
            clss = pickle.loads(s.recv(1024))
            print('Select the number for the class for which timetable is to be uploaded')
            for i, c in enumerate(clss):
                print(str(i + 1) + ': ' + str(c))
            ch = int(input('Enter your choice: '))
            s.send(str(ch-1).encode('utf-8'))
            print('Enter the timetable')
            week = []
            days_of_the_week = ["MONDAY", 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY']
            for _ in range(6):
                print('Enter the classes for ', days_of_the_week[_])
                no_cl = input('If there are no classes for this day, press 0, else press any other number: ')
                if no_cl == '0':
                    continue
                while True:
                    print('Format: HH:MM-HH:MM SUBJECT\nE.g. 11:30-13:00 Optimization Techniques')
                    inp = input().strip()
                    st_t = inp[:inp.index('-')]
                    en_t = inp[(inp.index('-') + 1):inp.index(' ')]
                    sub = inp[(inp.index(' ') + 1):]
                    week.append((days_of_the_week[_][0:3], st_t, en_t, sub))
                    choice = input('Want to continue with more classes on this day? Press 0, else press any other '
                                   'number')
                    if choice != '0':
                        break
            s.send(pickle.dumps(week))
            m = s.recv(1024).decode('utf-8')
            print(m)
        elif ch == '3':
            s.send(ch.encode('utf-8'))
            me=s.recv(1024).decode('utf-8')
            holidays = []
            while True:
                dd = input('Date (dd-mm-yyyy): ')
                hh = input('Reason: ')
                holidays.append((dd, hh))
                wtc = input('Do you want to declare more holidays? (y/n): ')
                if wtc == 'n' or wtc == 'N':
                    break

            s.send(pickle.dumps(holidays))
            m = s.recv(1024).decode('utf-8')
            print(m)
        elif ch == '4':
            s.send(ch.encode('utf-8'))
            clss = pickle.loads(s.recv(1024))
            print('Select the number for the class for which list of electives is to be uploaded')
            for i, c in enumerate(clss):
                print(str(i + 1) + ': ' + str(c))
            ch = int(input('Enter your choice: '))
            s.send(str(ch-1).encode('utf-8'))
            print('Enter the number of electives a student needs to take, e.g. if a student has to take 3 subjects '
                  'out of 6 total subjects, enter 3')
            n_elec = int(input())
            elec_options = []
            print('Enter the options for each Elective in comma-separated format like Distributed Computing,'
                  'Mobile Computing\n')
            for _ in range(n_elec):
                prmt = 'Elective ' + str(_)
                subs = input(prmt)
                sub_list = subs.split(',')
                sub_list = [sub.strip() for sub in sub_list]
                elec_options.append(sub_list)
            s.send(pickle.dumps(elec_options))
            m = s.recv(1024).decode('utf-8')
            print(m)
        elif ch == '5':
            s.send(ch.encode('utf-8'))
            s_t_combos = []
            print('Enter the new subjects being offered by a teacher')
            while True:
                t_name = input('Name of teacher: ')
                s_name = input('Name of subject: ')
                c_name = input('Name of class: ')
                y = int(input('Year: '))
                s_t_combos.append((t_name, s_name, c_name, y))
                flag = input('Press 0 to continue. Else press any other key: ')
                if flag != '0':
                    break
            s.send(pickle.dumps(s_t_combos))
            m = s.recv(1024).decode('utf-8')
            print(m)
        elif ch == '6':
            s.send(ch.encode('utf-8'))
            msgs = pickle.loads(s.recv(1024))
            if len(msgs) == 0:
                print('You have no unread messages')
            else:
                print('You have some new messages')
                for msg in msgs:
                    print(msg)
        elif ch == '7':
            s.send(ch.encode('utf-8'))
            break
    print('Thank you!!!')


if __name__ == '__main__':
    host = '127.0.0.1'
    ints = {'A': admin, 'T': teacher, 'S': student}
    BUFFER_SIZE = 1024
    m = ''
    print('Dynamic TimeTable System Interface')
    while True:
        u = input('Enter your username: ')
        p = input('Enter your password: ')
        r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        r.connect((host, 2010))
        print(r.recv(1024).decode('utf-8'))
        r.send(u.encode('utf-8'))
        r.send(p.encode('utf-8'))
        m = r.recv(1024).decode('utf-8')
        r.close()
        if len(m) > 1:
            print(m)
            ch = input('Do you want to try again or quit? \nEnter 1 for first option '
                       'and any other number for the second\n')
            if ch == '1':
                continue
            else:
                break
        else:
            break
    if m != '':
        ints[m](u)
