# Copyright 2021 TerminalWarlord under the terms of the MIT
# license found at https://github.com/TerminalWarlord/TikTok-Downloader-Bot/blob/master/LICENSE
# Encoding = 'utf-8'
# For collaboration mail me at dev.jaybee@gmail.com
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
import shutil
import requests
import json
import os
import re
from bs4 import BeautifulSoup as bs
import time
from datetime import timedelta
import math
import base64
from progress_bar import progress, TimeFormatter, humanbytes
from dotenv import load_dotenv

load_dotenv()
bot_token = os.environ.get('BOT_TOKEN')
workers = int(os.environ.get('WORKERS'))
api = int(os.environ.get('API_KEY'))
hash = os.environ.get('API_HASH')
chnnl = os.environ.get('CHANNEL_URL')
BOT_URL = os.environ.get('BOT_URL')
app = Client("JayBee", bot_token=bot_token, api_id=api, api_hash=hash, workers=workers)



@app.on_message(filters.command('start'))
def start(client, message):
    kb = [[InlineKeyboardButton('ቻናላችንን ይቀላቀሉ ⚽', url=chnnl),]]
    reply_markup = InlineKeyboardMarkup(kb)
    app.send_message(chat_id=message.from_user.id, text=f"ሰላም እንዴት ነህ/ሽ ፣ እኔ ቲክቶክ ቪድዮ Saver ነኝ፣ የቲክቶክ ቪድዮዎችን ያለ Water Mark ማውረድ እችላለሁ\n\n"
                          "__**በ**__ __@DREAM_SPORT__ የተሰራ\n",
                     parse_mode='md',
                     reply_markup=reply_markup)




@app.on_message(filters.command('help'))
def help(client, message):
    kb = [[InlineKeyboardButton('ቻናላችንን ይቀላቀሉ ⚽', url=chnnl),]]
    reply_markup = InlineKeyboardMarkup(kb)
    app.send_message(chat_id=message.from_user.id, text=f"ሰላም እንዴት ነህ/ሽ ፣ እኔ ቲክቶክ ቪድዮ Saver ነኝ፣ የቲክቶክ ቪድዮዎችን ያለ Water Mark ማውረድ እችላለሁ\n\n"
                                            "__የቲክቶክ ቪድዮ ሊንክ ይላኩልኝ__",
                     parse_mode='md',
                     reply_markup=reply_markup)


@app.on_message((filters.regex("http://")|filters.regex("https://")) & (filters.regex('tiktok')|filters.regex('douyin')))
def tiktok_dl(client, message):
    a = app.send_message(chat_id=message.chat.id,
                         text='__ወደ ሰርቨራችን በመጫን ላይ...__',
                         parse_mode='md')
    link = re.findall(r'\bhttps?://.*[(tiktok|douyin)]\S+', message.text)[0]
    link = link.split("?")[0]



    
    params = {
      "link": link
    }
    headers = {
      'x-rapidapi-host': "tiktok-downloader-download-tiktok-videos-without-watermark.p.rapidapi.com",
      'x-rapidapi-key': "cea7ad19b5mshbc7d971f41a0637p11d63djsn58869ff27a79"
    }
    
    ### Get your Free TikTok API from https://rapidapi.com/TerminalWarlord/api/tiktok-info/
    #Using the default one can stop working any moment. 
    
    api = f"https://tiktok-downloader-download-tiktok-videos-without-watermark.p.rapidapi.com/vid/index"
    r = requests.get(api, params=params, headers=headers).json()['video'][0]
    directory = str(round(time.time()))
    filename = str(int(time.time()))+'.mp4'
    size = int(requests.head(r).headers['Content-length'])
    total_size = "{:.2f}".format(int(size) / 1048576)
    try:
        os.mkdir(directory)
    except:
        pass
    with requests.get(r, timeout=(50, 10000), stream=True) as r:
        r.raise_for_status()
        with open(f'./{directory}/{filename}', 'wb') as f:
            chunk_size = 1048576
            dl = 0
            show = 1
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                dl = dl + chunk_size
                percent = round(dl * 100 / size)
                if percent > 100:
                    percent = 100
                if show == 1:
                    try:
                        a.edit(f'__**URL :**__ __{message.text}__\n'
                               f'__**አጠቃላይ የፋይል መጠን :**__ __{total_size} MB__\n'
                               f'__**የጫነው መጠን :**__ __{percent}%__\n',
                               disable_web_preview=False)
                    except:
                        pass
                    if percent == 100:
                        show = 0

        a.edit(f'__ወደ ሰርቨር ጭኗል!\n'
               f'ወደ ቴሌግራም በመጫን ላይ... ⏳__')
        start = time.time()
        title = filename
        app.send_document(chat_id=message.chat.id,
                          document=f"./{directory}/{filename}",
                          caption=f"**የፋይል ስም :** __{filename}__\n"
                          f"**የፋይል መጠን :** __{total_size} MB__\n\n"
                          f"__በ @{BOT_URL} ቦት የተጫነ__",
                          file_name=f"{directory}",
                          parse_mode='md',
                          progress=progress,
                          progress_args=(a, start, title))
        a.delete()
        try:
            shutil.rmtree(directory)
        except:
            pass


app.run()
