# #!/usr/bin/python
# # -*- coding: UTF-8 -*-

# import sys
# import time
# import requests
# import wget
# from bs4 import BeautifulSoup
# import shutil



# Headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

# url="https://thatisbiz.fireside.fm"

# downloadPath="/opt/data/media/Music/Podcast"


# def getHtml(url):
#     response=requests.get(url=url,headers=Headers)
#     result=""
#     print(response)
#     if 200==response.status_code:
#         result= response.text

#     # print(result)
#     return result
    

# def parseList(result):
#     if ""==result:
#         return 
    
#     soup = BeautifulSoup(result, 'html.parser')
#     for div in soup.select("div.list-item"):
#         a = div.select_one("h3 > a")
#         print(a)
#         title=a.get_text().strip()
#         href=a.get('href').strip()

#         parseDetail(url+href,title)
#         print("---------------------")


# def parseDetail(url,title):
#     result=getHtml(url)
#     if ""==result:
#         return 
    
#     detail = BeautifulSoup(result, 'html.parser')
#     a = detail.select_one("a.btn")
#     audio_url=a.get('href').strip()
#     print(audio_url)
#     slite=audio_url.split(".")
#     prefix=slite[len(slite)-1]
#     print("prefix",prefix)

#     filePath=downloadPath+"/"+title.replace(" ","_")+"."+prefix
#     print("filePath",filePath)
#     # wget.download(audio_url, out=filePath)
#     download(audio_url, filePath)




# def download(url,filepath):

#     r = requests.get(url,headers=Headers, stream=True)
#     if r.status_code == 200:
#         print("200")
#         with open(filepath, 'wb') as f:
#             print("正在下载：",filepath)
#             r.raw.decode_content = True
#             shutil.copyfileobj(r.raw, f)




# ##################

# # download("https://media.fireside.fm/file/fireside-audio/podcasts/audio/9/9a91414e-51b0-42ae-bee7-2c17d3c1c146/episodes/c/c8480c99-08ed-4d9e-b26e-4367bc1e549a/c8480c99-08ed-4d9e-b26e-4367bc1e549a.mp3"
# #          ,downloadPath+"/aaaa.mp3")


# parseList(getHtml(url))







