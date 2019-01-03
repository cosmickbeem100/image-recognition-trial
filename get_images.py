#!/opt/conda/bin/python
# -*- coding: utf-8 -*-

import urllib.request
from urllib.parse import quote
import httplib2
import json
import os

# get credentials(API_KEY and Custom Search Engine)
CREDENTIALS = "./credentials/credentials.json"
with open(CREDENTIALS, "r") as f:
    content = f.read()
    #print(content)
    params = json.loads(content)
    API_KEY = params["API_KEY"]
    CUSTOM_SEARCH_ENGINE = params["CUSTOM_SEARCH_ENGINE_ID"]

# make a query for an image search
def getImageUrl(search_item, total_num):
    img_list = []
    i = 0
    while i<total_num:
        query_img = "https://www.googleapis.com/customsearch/v1?key=" + API_KEY + "&cx=" + CUSTOM_SEARCH_ENGINE + "&num=" + str(10 if(total_num-i)>10 else (total_num-i)) + "&start=" + str(i+1) + "&q=" + quote(search_item) + "&searchType=image"
        print(query_img)
        res = urllib.request.urlopen(query_img)
        data = json.loads(res.read().decode("utf-8"))
        for j in range(len(data["items"])):
            img_list.append(data["items"][j]["link"])
        i = i + 10
    return img_list

# apply the given query and get images as a result
def getImage(search_item, img_list, dir="./"):
    opener = urllib.request.build_opener()
    http = httplib2.Http(".cache")
    for i in range(len(img_list)):
        try:
            fn, ext = os.path.splitext(img_list[i])
            print(img_list[i])
            response, content = http.request(img_list[i])
            #print(ext)
            ext = ext.split("?").pop()
            #print(ext)
            with open(dir+search_item+str(i)+ext, "wb") as f:
                f.write(content)
        except:
            print("failed to download images.")
            continue

# do the search
TARGET = "西野七瀬"
MAX_ITEMS = 5
DIR = "./images/"
if __name__ == "__main__":
    img_list = getImageUrl(TARGET, MAX_ITEMS)
    print(img_list)
    getImage(TARGET, img_list, DIR)