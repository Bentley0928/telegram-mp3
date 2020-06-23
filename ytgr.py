#!/usr/bin/python
import time
import subprocess
import telepot
import os
import urllib.request
import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import youtube_dl

def handle(msg):
        chat_id = msg['chat']['id']
        command = msg['text']

        print ("Command from client : %s  " %command)

    #youtube search
        if command.startswith('yt'):
            param = command[3:]
            response = urlopen("https://www.youtube.com/results?search_query="+param)
            data = response.read()
            response.close()
            soup = BeautifulSoup(data,"html.parser")
            vid = soup.find(attrs={'class':'yt-uix-tile-link'})
            #link = "https://www.youtube.com"+vid['href']
            global link
            link = param
            send1 = bot.sendMessage(chat_id,'輸入你想要的檔案名稱')
            #watchid = vid['href']
            #watchid = watchid.replace('/watch?v=','')
            #title = vid['title']
            #print (title)
            print (link)
            #bot.sendMessage(chat_id,title+"\n"+link)
        else:
            options = {
                'format': 'bestaudio/best',
                'outtmpl': command +'.mp3',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320'
                }]
            }
            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([link])
                print (command)
                bot.sendAudio(chat_id,audio=open(command + ".mp3",'rb'))
                print ("Sent!")
                os.remove(command +'.mp3')
                link = ""
    #end youtube search



#api credentials
api = open('api.txt','r')
api_cont = api.read().strip()
bot = telepot.Bot(api_cont)
bot.message_loop(handle)
print ('[+] Server is Listenining [+]')
print ('[=] Type Command from Telegram [=]')

while 1:
        time.sleep(10)
