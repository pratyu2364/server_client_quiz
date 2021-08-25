PROJECT OVERVIEW


This is 1-server 3-client based online quiz. Server sends questions to all 3 clients and the one
who presses the buzzer in 10 seconds gets a chance to answer the question in exactly 10 seconds.
If the cliet who buzzered fails to answer in the given time, the server moves to the next question.
If the client who buzzered gives correct answer then he is rewarded 1 point.
If the client who buzzered gives wrong answer then he is rewarded -0.5 point.
A client is declared winner if he reaches 5 points or more than that.

REQUIRED MODULES:

Python3
with
socket,sys,select,time modules

HOW TO RUN:

Open terminal and go to the required directory.
Run the server using the cmd python3 server.py.
Runnning server without any clients connected will be display a blank screen.
Run the client using the cmd python3 client.py
(NOTE:the game will only start after connecting exactly 3 clients, if you want to change the number of.
clients then go line 40 and 48 in server.py and change j = no of clients that u want).

HOW TO PLAY:

Once to run the client.py
It will ask for USERNAME,type it and press Enter
Once all 3 clients are connected, questions will start comming from server side.
To  buzze press any alphabet from your keyboard.
Once the game ends your score will be diplayed at your terminal.

RED ALERTS:

don't directly disconnect from the server it will crash the programme.
don't press any thing except alphabets for buzzing.
at the end u will extra blank lines due to some internal bugs, so just scroll up to check your score.
sometimes running 3 clients on one os may result into time delays, whenever there is such issue.
do crash the server and then rerun the whole project.
Programme is smoothly working on Ubuntu without time delay or sync issue.

IMP NOTE
PORT = 2000 and IP ="127.0.0.1" is taken by default if the client.py does not display anything after entering username then the port might be busy,for that u need to change the PORT NUMBER in both client and server side
