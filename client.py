import select
import socket
import sys
import time
from Questions import *#importing this just to find number of questions present
IP = "127.0.0.1"
PORT =2000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP,PORT))
username = str(input("ENTER YOUR USERNAME: "))
username = username.encode("utf-8")
client_socket.send(username)
no_of_questions = len(qna2)
j=0
client_list =[sys.stdin,client_socket]
msg1 = client_socket.recv(1024)
msg1 =msg1.decode("utf-8")
msg2 =client_socket.recv(1024)
msg2 =msg2.decode("utf-8")
print(msg1)
time.sleep(1)
print(msg2)

while(j<no_of_questions):
    msg = client_socket.recv(1024)
    msg = msg.decode("utf-8")
    msg3 =client_socket.recv(1024)
    msg3 = msg3.decode("utf-8")

    if msg ==f"well played {username},":

        print(msg)
        time.sleep(0.5)
        print(msg3)
        client_socket.close()
        break
        sys.exit()

    print(msg)
    time.sleep(0.5)
    print(msg3)
        #break
    read_sockets,_,exception_sockets = select.select([sys.stdin,client_socket],[],[],10)

    if(len(read_sockets)>0):#timeout for buzzing
        if read_sockets[0]== sys.stdin:
            msg = sys.stdin.readline().strip()
            msg = msg.encode("utf-8")
            client_socket.send(msg)
            data2 = client_socket.recv(1024)
            data2 = data2.decode("utf-8")
            print(data2)
            if  data2 == "Answer the question":
                read_sockets_ans,_,exception_sockets = select.select([sys.stdin,client_socket],[],[],10)
                if(len(read_sockets_ans)>0):#timeout for answering the questions
                    if read_sockets_ans[0]== sys.stdin:
                        msg3 = sys.stdin.readline().strip()
                        msg3 = msg3.encode("utf-8")
                        client_socket.send(msg3)
                        rep=client_socket.recv(1024)
                        rep=rep.decode("utf-8")
                        print(rep)
                else:
                    rep=client_socket.recv(1024)
                    rep=rep.decode("utf-8")
                    print(rep)
                    j=j+1

        else:
            m=client_socket.recv(1024)
            m = m.decode("utf-8")
            print(m)
            j=j+1
            #print(m)
            #continue


data3=client_socket.recv(1024) #if game is over without anyone reaching the score of 4
if data3:                      #then client with max score wins
    data3=data3.decode("utf-8")
    print(data3)
    time.sleep(1)
    data4=client_socket.recv(1024)
    data4=data4.decode("utf-8")
    print(data4)
