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
from pathlib import Path
import youtube_dl

def handle(msg):
        chat_id = msg['chat']['id']
        command = msg['text']

        print ("Command from client : %s  " %command)

    #youtube search
        if command == '/start':
            bot.sendMessage(chat_id,'輸入yt videolink來下載歌曲(ex: yt your.video.link)')
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
            bot.sendMessage(chat_id,'輸入你想要的檔案名稱(輸入exit來取消)')
            #watchid = vid['href']
            #watchid = watchid.replace('/watch?v=','')
            #title = vid['title']
            #print (title)
            print (link)
            #bot.sendMessage(chat_id,title+"\n"+link)
        elif command == 'exit':
            link = ''
            bot.sendMessage(chat_id, "Bye!")
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
                size = Path(command+'.mp3').stat().st_size
                if size<50000000:
                    bot.sendAudio(chat_id,audio=open(command + ".mp3",'rb'))
                    print ("Sent!")
                    os.remove(command +'.mp3')
                    link = ""
                else:
                    bot.sendMessage(chat_id,'檔案大小超過50MB 請用瀏覽器來下載檔案(Chrome請點選右上角選單，按下下載按鈕，謝謝')
                    os.system("mv "+command+".mp3 ./mp3/")

                    bot.sendMessage(chat_id, "http://mp3.bentley.taipei/"+command+".mp3")

                    bot.sendMessage(chat_id, "success")
                    print ("Sent!")

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
