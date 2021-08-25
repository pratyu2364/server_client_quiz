import socket
import select
import sys
import time
from Questions import*

IP = "127.0.0.1"
PORT =2000
global server_socket
global host
global port
sockets_list = []
address_list = []
questions2 = []
answers2 = []
i=0
for question in qna2:#qna2 is a dictionary of Questions mapped to answers
    answers2.append(qna2[question])
    questions2.append(question)

questions =["Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","Q10"]#sample questions for testing
answers =["1","2","3","4","5","6","7","8","9","10"]#sample answers for testing
clients = {}# clients object map username
client_score ={}#client user name map score count i=0 def
def accepting_connections(server_socket):
    for c in sockets_list:
        c.close()

    del sockets_list[:]
    #del address_list[:]
    j=0
    while True:
            conn, address = server_socket.accept()#accepting connections
            server_socket.setblocking(1)  # prevents timeout
            j=j+1
            sockets_list.append(conn)
            user=conn.recv(1024)# receiving username from client
            user=user.decode("utf-8")
            clients[conn] = user
            if j<3:
                print(f"Connection has been established to {user}")

                conn.send(str.encode(f" Hi {user} ,Total questions are 50. First one to reach 5 points wins.If you don't know the question just don't press buzzer"))
                time.sleep(1)
                conn.send(str.encode("Welcome to the game"))


            elif j==3:
                print(f"Connection has been established to {user}")
                conn.send(str.encode(f"Total questions are 10. First one to reach 4 points wins.\n First enter any alphabet for buzzer and then answer the question"))
                print("Maximum Clients connected")
                time.sleep(1)
                conn.send(str.encode("Welcome to the quiz\n"))

                game_function(server_socket) #main part starts from here
                break

def game_function(server_socket):
    for i in sockets_list:
        user = clients[i]
        client_score[user]=0
    for i in range(len(questions2)):

        for notified_socket in sockets_list:
            msg=questions2[i].encode("utf-8")
            notified_socket.send(msg)#sending questions to clients
            time.sleep(0.5)
            notified_socket.send(str.encode("press any alphabet to buzz:"))
        response= select.select(sockets_list, [],[],10)#setting timeout for the buzzer
        if len(response[0])>0:

            who_buzzed=response[0][0]
            b=who_buzzed.recv(1024)
            b=b.decode('utf-8')
            response=()
            for notified_socket in sockets_list:

                if notified_socket != who_buzzed:
                    notified_socket.send(str.encode(f"sorry {clients[notified_socket]} , {clients[who_buzzed]} has pressed the buzzer "))
            if b:
                who_buzzed.send(str.encode("Answer the question"))
                response2= select.select([who_buzzed], [],[],10)#setting timeout for answering
                if len(response2[0])>0:
                    ans=who_buzzed.recv(1024)
                    ans = ans.decode("utf-8")
                    user = clients[who_buzzed]#user who pressed the buzzer
                    response2 = ()
                    if ans == str(answers2[i]):
                        who_buzzed.send(str.encode("correct ans, you received 1 point"))
                        client_score[user]=client_score[user]+1
                        time.sleep(1)
                        if client_score[user] >=5: #loop breaking condition
                            for  i in client_score:
                                print(f"{i} : {client_score[i]}")
                            print (f"winner is  {user} !!!")
                            for notified_socket in sockets_list:
                                if(notified_socket!= who_buzzed):

                                    notified_socket.send(str.encode(f"well played {clients[notified_socket]},"))
                                    time.sleep(0.5)
                                    notified_socket.send(str.encode(f"your final score is {client_score[clients[notified_socket]]}\ngame is over, {user} is  winner with {client_score[user]} points"))
                                else:
                                    notified_socket.send(str.encode(f"well played {clients[notified_socket]},"))
                                    time.sleep(0.5)
                                    notified_socket.send(str.encode(f"your final score is {client_score[clients[notified_socket]]}\ngame is over, you are the winner"))
                            break
                            server_socket.close()
                            sys.exit()

                    else:
                        who_buzzed.send(str.encode("wrong ans, you received -0.5 point"))
                        client_score[user]=client_score[user]-0.5
                        time.sleep(1)
                else:
                    for notified_socket in sockets_list:
                        if notified_socket !=who_buzzed:
                            notified_socket.send(str.encode(f"{clients[who_buzzed]} did not answer after pressing the buzzer in 10 seconds"))
                        else:
                            notified_socket.send(str.encode("you did not answer in 10 seconds after pressing the buzzer"))
        else:
            for notified_socket in sockets_list:
                notified_socket.send(str.encode("Nobody pressed the buzzer in 10 seconds so moving to next question \n"))
                continue

    max=-999# if no one is able to get 5 points and questions are over then the client with max score is the winner
    for i in client_score:
            if(client_score[i]>max):
                client_with_max =i
                max = client_score[i]
    for  notified_socket in sockets_list:
        notified_socket.send(str.encode(f"well played {clients[notified_socket]},"))
        time.sleep(0.5)
        notified_socket.send(str.encode(f"your final score is {client_score[clients[notified_socket]]}\ngame is over, {client_with_max} is  winner with {client_score[user]} points"))
        server_socket.close()
        sys.exit()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP, PORT))
    server_socket.listen(5)
    accepting_connections(server_socket)

main()
