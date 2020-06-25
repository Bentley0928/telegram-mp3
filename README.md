# teletubemp3 - A Telegram Bot

**teletubemp3 is a Telegram Bot which converts YouTube video(s) to mp3 and send directly to your Telegram.**

<img alt="yt despacito" src="./screenshot.png" width="350">

### How does it work?

* It takes your command ( `yt videolink` )
* Download that video using **youtube_dl** library
* Converts it into mp3 using **youtube_dl**
* Sends it to your chatbox

### Installation
```
git clone https://github.com/Bentley0928/telegram-mp3.git
cd telegram-mp3
pip3 install telepot
pip3 install requests
pip3 install bs4
pip3 install youtube-dl
pip3 install youtube_dl
brew install youtube-dl
brew install ffmpeg
```
Now create a file *api.txt* and put your **api-key**

### Run
While in the directly, run

`python ytgr.py`

You'll see 
```
[+] Server is Listenining [+]
[=] Type Command from Telegram [=]
```

### Usage
In your Telegram message box. Text

`yt videolink`

The Bot will find out the video from YouTube, converts it and send it to your Telegram.
