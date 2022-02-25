from concurrent.futures import thread
from imp import acquire_lock
from posixpath import split
import socket
from urllib import response


import re


from pythonosc import dispatcher
from pythonosc import udp_client
from pythonosc import osc_server

import threading
import time as timer
import sys
#import pyttsx3
import ttsGenerator
import os
from datetime import datetime

import config

server = 'irc.chat.twitch.tv'
port = 6667
nickname = config.nickname #irc nickname
token = config.token #twitch oauth token
channel = config.channel #twitch channle to look at 
ip = "127.0.0.1"
sendport = 9000
rescieveport = 9001
fileopen = open("logs.txt","a")


sock = socket.socket()
client = udp_client.SimpleUDPClient(ip, sendport)

lock = threading.Lock()
thread_numb = 0

#engine = pyttsx3.init(driverName='sapi5')

ttslock = threading.Lock()

def main():
    kill = False
    global thread_numb
    msgcount = 0
    while True and not kill:
        
        resp = sock.recv(1024).decode('utf-8')

        if resp.startswith('PING'):
            encodedmsg = 'PONG :tmi.twitch.tv\n'
            sock.send(encodedmsg.encode("utf-8"))

        elif len(resp) > 0:
            msg = resp.split(' ')

            
            
            usrnm = msg[0].split('!')
            
            usrnm = usrnm[0][1:]
            
            
            
            try:
                extra = msg[4:]
            except:
                extra = []

            msg = msg[3][1:].rstrip()

            
            if msg[0] == "!": 
                if msg == "!kill" and usrnm == nickname:
                    kill = True
                    
                    break
                splitmsg = re.findall(r'[A-Za-z]+|\d+', msg)
                time = 1
                if len(splitmsg) > 1:
                    try:
                        time = min(9,int(splitmsg[1])) # cap out max input time in seconds
                    except:
                        time = 1

                
                
                msg = splitmsg[0]
                msg = '!' + msg
                
                if thread_numb < 15:
                    with lock:
                        thread_numb = thread_numb + 1
                        msgcount += 1

                    fileopen.write(f"time:{datetime.now().time()} message: {msg} {extra}, username: {usrnm}\n")
                    
                    thread = threading.Thread(target=Handle, args=[msg, time, extra, usrnm, msgcount])
                    thread.start()

                    
                
                
        

      
def Handle(resp: str, time: int, extra, usrnm:str, msgcount:int):#why must switches forsake me

        global thread_numb
        

        if resp == "!forward":
            client.send_message("/input/MoveForward",1)
            timer.sleep(time)
            client.send_message("/input/MoveForward",0)

        elif resp == "!back":
            client.send_message("/input/MoveBackward",1)
            timer.sleep(time)
            client.send_message("/input/MoveBackward",0)

        elif resp == "!mleft":
            client.send_message("/input/MoveLeft",1)
            timer.sleep(time)
            client.send_message("/input/MoveLeft",0)

        elif resp == "!mright":
            client.send_message("/input/MoveRight",1)
            timer.sleep(time)
            client.send_message("/input/MoveRight",0)

        elif resp == "!lleft":
            client.send_message("/input/LookLeft",1)
            timer.sleep(time/4)
            client.send_message("/input/LookLeft",0)

        elif resp == "!lright":
            client.send_message("/input/LookRight",1)
            timer.sleep(time/4)
            client.send_message("/input/LookRight",0)

        elif resp == "!ldown": #these are inverted in game for some reason
            client.send_message("/input/LookUp",1)
            timer.sleep(time)
            client.send_message("/input/LookUp",0)

        elif resp == "!lup":
            client.send_message("/input/LookDown",1)
            timer.sleep(time)
            client.send_message("/input/LookDown",0)

        elif resp == "!jump":
            for i in range(time):
                client.send_message("/input/Jump",1)
                timer.sleep(.5)
                client.send_message("/input/Jump",0)
                timer.sleep(.5)

        elif resp == "!dright":
            client.send_message("/input/DropRight",1)
            timer.sleep(time)
            client.send_message("/input/DropRight",0)

        elif resp == "!dleft":
            client.send_message("/input/DropLeft",1)
            timer.sleep(time)
            client.send_message("/input/DropLeft",0)

        elif resp == "!uright":
            client.send_message("/input/UseRight",1)
            timer.sleep(time)
            client.send_message("/input/UseRight",0)

        elif resp == "!gright":
            client.send_message("/input/GrabRight",1)
            timer.sleep(time)
            client.send_message("/input/GrabRight",0)

        elif resp == "!uleft":
            client.send_message("/input/UseLeft",1)
            timer.sleep(time)
            client.send_message("/input/UseLeft",0)

        elif resp == "!gleft":
            client.send_message("/input/GrabLeft",1)
            timer.sleep(time)
            client.send_message("/input/GrabLeft",0)

        elif resp == "!tts":
            newstr = ""
            for i in range(len(extra)):
                newstr = newstr + extra[i] + " "
                
            newstr = newstr.rstrip()


            
            while not ttslock.acquire():
                timer.sleep(.1)
            ttsGenerator.generate_ttsmp3(text= newstr, usrnme=usrnm, num=msgcount)
            ttslock.release()


        
        with lock:
            thread_numb = thread_numb - 1
        sys.exit
        

            


if __name__ == '__main__':

    

    sock.connect((server,port))


    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))
    

    #resp = sock.recv(1024).decode('utf-8')
    print("running...")
    main()
    dir = 'tempaudio/'
    for file in os.scandir(dir):
        os.remove(file.path)
    fileopen.close()
    
    #manager = oscStuff.OSC_Handler()

   

    #progloop = asyncio.get_event_loop()
    #progloop.run_until_complete(main())






#/input/Run

#/input/Back

#/input/Menu

#/input/ComfortLeft

#/input/ComfortRight

#/input/PanicButton

#/input/QuickMenuToggleLeft

#/input/QuickMenuToggleRight

#/input/ToggleSitStand

#/input/AFKToggle