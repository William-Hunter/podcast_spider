#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import time
import json
import requests
import wget
from bs4 import BeautifulSoup
import shutil
import traceback
import str_tool



Headers={
  # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }



def getHtml(url):
    response=requests.get(url=url,headers=Headers)
    result=""
    print(response)
    if 200==response.status_code:
        result= response.text

    # print(result)
    return result



def parsePage(result,lastdownload,channel,MAX_COUNT):
    if ""==result:
        return 
    
    soup = BeautifulSoup(result, 'html.parser')
    
    count=0
    for li in soup.select("ul.jsx-7bbe0f84186f1998.tab > li.jsx-7bbe0f84186f1998"):
        count=count+1
        if count>MAX_COUNT:    # 如果有10次，就直接结束
            return

        # print(li)

        a=li.select_one("a.jsx-744662fb2f5b91b6.card").get("href").strip()

        # print(a)

        detail_result=getHtml(xiaoyuzhoufm_url+a)

        detail_soup = BeautifulSoup(detail_result, 'html.parser')

        title=detail_soup.select_one("main > header.wrap > h1.title").get_text().strip()

        code=detail_result.split('"enclosure":')[1].split('"isPrivateMedia":')[0]
        code=code.replace('{"url":"','')
        audio_url=code.replace('"},','')
        
        # if "?" in audio_url:
        #     audio_url=audio_url.split("?")[0]
            
        print(title,audio_url)
        print("--------------------")

        if title in lastdownload or str_tool.filter(title,channel):  #如果已经下载过，或者符合过滤规则就跳过
            print('表中已经存在')
            continue

        prefix=getPrefix(audio_url)

        download(audio_url,title,prefix)
        lastdownload.append(title)


def download(audio_url,title,prefix):
    global downloadPath
    path=title
    filePath=downloadPath+"/"+path.replace(" ","").replace("｜","_").replace("|","_").replace("-","_").replace("/","_").replace("#","_").replace("?","_").replace("？","_").replace(":","_")+"."+prefix
    print("filePath",filePath)

    # wget.download(audio_url, out=filePath)
    
    r = requests.get(audio_url,headers=Headers, stream=True)
    if r.status_code == 200:
        print("200")
        with open(filePath, 'wb') as f:
            # print("正在下载：",filePath)
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            print("下载完成：",filePath)



def getPrefix(audio_url):
    slite=audio_url.split(".")
    prefix=slite[len(slite)-1]
    print("prefix",prefix)
    return prefix


def readJson(JSON_PATH):
    f = open(JSON_PATH, 'r', encoding='UTF-8')
    strr = f.read()
    f.close()
    return json.loads(strr)


def writeJson(JSON_PATH, obj):
    f = open(JSON_PATH, 'w', encoding='UTF-8')
    json.dump(obj, f, ensure_ascii=False, indent=2)
    f.close()


def loop(check_type,channel_list):#循环频道列表
    for channel_name in channel_list:
        if "" == channel_name:
            continue

        channel = channel_list[channel_name]
        try:
            if ("" != channel['check']):
                print("\n",channel_name)
                result=getHtml(xiaoyuzhoufm_url+"/podcast/"+channel['id'])
                if 'max_count' in channel:
                    MAX_COUNT=channel['max_count']
                else:#如果没设置，就使用默认设置
                    MAX_COUNT=5
                parsePage(result,channel['lastdownload'],channel,MAX_COUNT)

        except Exception as err:
            # print(err)
            traceback.print_exc()
            print(f"異常賬戶：{channel_name},Unexpected {err=}, {type(err)=}")


stamp_path = "/opt/workspace/podcast/xiaoyuzhoufm.json"
xiaoyuzhoufm_url="https://www.xiaoyuzhoufm.com"
# downloadPath="/opt/data/media/Music/Podcast"
downloadPath="/opt/data/sync/folders/Podcast"



date_format = "%Y-%m-%d %H:%M:%S"

if __name__ == "__main__":
    now=time.strftime(date_format,time.localtime(time.time()))
    print(now+"----------------------------------------------------------------------")
    
    check_type = "daily"
    if len(sys.argv) > 1:
        check_type = sys.argv[1]     # hourly    daily     weekly      monthly
    # print(check_type)

    channel_list = readJson(stamp_path)
    # print(channel_list)
    loop(check_type,channel_list)
    writeJson(stamp_path, channel_list)

    print("执行完毕")

