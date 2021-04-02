#!/usr/bin/python
import time
import subprocess
import os
import telegram
import urllib.request
import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pathlib import Path
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import youtube_dl
flag11 = 0
api = open('api.txt','r')
api_cont = api.read().strip()
bot = telegram.Bot(token=api_cont)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update, context):
    chat_id = update.message.chat.id
    print(chat_id)
    """Send a message when the command /start is issued."""
    update.message.reply_text("輸入yt videolink來下載歌曲(ex: yt your.video.link)")
"""
def handle(msg):
        chat_id = msg['chat']['id']
        command = msg['text']

        print ("Command from client : %s  " %command)
"""
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
def sendAudio(update, context):
    #youtube search
        global flag11
        chat_id = update.message.chat.id
        command = update.message.text
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
            bot.sendMessage(chat_id=chat_id,text='輸入你想要的檔案名稱(輸入exit來取消)')
            #watchid = vid['href']
            #watchid = watchid.replace('/watch?v=','')
            #title = vid['title']
            #print (title)
            print (link)
            flag11 = 1
        elif command == 'exit':
            link = ''
            bot.sendMessage(chat_id=chat_id, text="Bye!")
        elif flag11 == 1:
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
                    bot.send_audio(chat_id=chat_id, audio=open(command + ".mp3",'rb'))
                    print ("Sent!")
                    os.remove(command +'.mp3')
                    link = ""
                else:
                    bot.sendMessage(chat_id,text='檔案大小超過50MB 請用瀏覽器來下載檔案(Chrome請點選播放器右邊的三個點，按下下載按鈕，謝謝')
                    os.system("mv "+command+".mp3 ./mp3/")

                    bot.sendMessage(chat_id=chat_id, text="http://mp3.bentley.taipei/"+command+".mp3")

                    #bot.sendMessage(chat_id=chat_id, "success")
                    print ("Sent!")
                flag11=0
        elif flag11==0:
            bot.sendMessage(chat_id, text="輸入格式錯誤ㄛ")
    #end youtube search



def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(api_cont, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, sendAudio))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
if __name__ == "__main__":
    main()