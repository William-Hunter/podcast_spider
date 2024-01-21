#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
from string import Template
import requests
import json
from bs4 import BeautifulSoup
import wget
import str_tool
import traceback



"""
# 列表，
https://www.ximalaya.com/revision/album/v1/getTracksList?albumId=46587439&pageNum=1&sort=1
# 获取音频信息
https://www.ximalaya.com/revision/play/v1/audio?id=365341930&ptype=1
"""

HEADERS={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
LIST_URL="https://www.ximalaya.com/revision/album/v1/getTracksList?pageNum=1&sort=1&albumId={}&pageSize={}"
DETAIL_URL="https://www.ximalaya.com/revision/play/v1/audio?ptype=1&id="
PAGE_SIZE=5

audioDir="/opt/data/sync/folders/Podcast"
stamp_path = "/opt/workspace/podcast/ximalaya.json"

def readJson(JSON_PATH):
    f = open(JSON_PATH, 'r', encoding='UTF-8')
    strr = f.read()
    f.close()
    return json.loads(strr)


def writeJson(JSON_PATH, obj):
    f = open(JSON_PATH, 'w', encoding='UTF-8')
    json.dump(obj, f, ensure_ascii=False, indent=2)
    f.close()


def downloadAudio(audio_url,title,lastdownload):
    
    prefix=audio_url.split(".")[-1]
    print("prefix",prefix)
    filename=audioDir+"/"+title.replace(" ","").replace("｜","_").replace("|","_").replace("-","_").replace("/","_").replace("#","_").replace("?","_").replace("？","_").replace(":","_")+"."+prefix
    wget.download(audio_url, out=filename)
    print("filename",filename)
    lastdownload.append(title)



def getAudio(title,audioId,lastdownload):  #获取到每个音频资源的链接
    response=requests.get(url=DETAIL_URL+audioId,headers=HEADERS)
    if 200==response.status_code:
        trackData = json.loads(response.text)
        if 200==trackData['ret']:
            print("trackData",trackData)
            audio_url=trackData['data']['src']
            print("audio_url",audio_url)
            downloadAudio(audio_url,title,lastdownload)
    else:
        print("错误信息\n",response.text)



def getList(albumId,lastdownload,channel,pageSize):       #获取到频道的音频列表
    response=requests.get(url=LIST_URL.format(albumId,pageSize),headers=HEADERS)
    if 200==response.status_code:
        jsonData = json.loads(response.text)
        print(jsonData)
        if 200 == jsonData['ret']:
            for track in jsonData['data']['tracks']:
                title=track['title']
                audioId=track['trackId']

                # 判断是否存在于表里面
                if title in lastdownload or str_tool.filter(title,channel):
                    print(title,"跳过")
                    continue

                print(title,"表里不存在")
                getAudio(title,str(audioId),lastdownload)
                print("-----------")


def loop(channel_list):#循环频道列表
    for channel_name in channel_list:
        # print("\nchannel_name",channel_name)

        if "" == channel_name:
            continue

        channel = channel_list[channel_name]
        try:
            if ("" != channel['id']):
                print("\n",channel_name)
                # result=getHtml(google_url+channel['id'])
                if 'max_count' in channel:
                    MAX_COUNT=channel['max_count']
                else:#如果没设置，就使用默认设置
                    MAX_COUNT=5
                getList(channel['id'],channel['lastdownload'],channel,MAX_COUNT)

        except Exception as err:
            # print(err)
            traceback.print_exc()
            print(f"異常賬戶：{channel_name},Unexpected {err=}, {type(err)=}")



def process():
    # 获取表里面的数据
    channel_list = readJson(stamp_path)
    loop(channel_list)
    writeJson(stamp_path, channel_list)
    



date_format = "%Y-%m-%d %H:%M:%S"

if __name__=="__main__":
    channel= {
        "id": "41432866",
        "max_count": "4",
        "lastdownload": [
            "060.自由职业是年轻人的终极梦想么？说出来让我解解馋",
            "059.高能量人生的秘密，为什么我对生活永远充满激情？",
            "058.要不是当年积极搞副业，我哪来的留学钱",
            "057.我们来“颁奖”了！那些让我们沸腾和湿润的电视剧",
            "061.付菡驾到！充满巨变的2023年，酷女孩们变了吗？"
        ]
    }


    getList(channel['id'],channel['lastdownload'],channel,1)
    now=time.strftime(date_format,time.localtime(time.time()))
    print(now+"----------------------------------------------------------------------")
    process()

