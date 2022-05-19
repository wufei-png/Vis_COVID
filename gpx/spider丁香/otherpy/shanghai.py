# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import re

def main():
    #本地宝
    baseurl1 = "http://wsjkw.sh.gov.cn/yqtb/index"
    alllinks = getalllinks(baseurl1)
    getdatafromlink(alllinks)

def askurl(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44"}
    # 模拟浏览器头部信息，向网站发送消息
    # 机器类型,用户代理
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

def getalllinks(baseurl):
    # 解析数据
    getalllink = False
    alllinks = []
    page = 1
    while not getalllink:
        if page == 1:
            url = baseurl + ".html"
        else:
            url = baseurl + "_" + str(page) + ".html"
        page += 1
        html = askurl(url)
        bs = BeautifulSoup(html, "html.parser")
        table = bs.find('ul').find_all("li")
        for oneline in table:
            if oneline.find("a").text[-5:] == "居住地信息":
                if oneline.find("span").text == "2022-04-05":
                    getalllink = True
                    break
                else:
                    alllinks.append(oneline.find("a")["href"])
    return alllinks

def savedata(savepath, datalist):
    # 保存数据
    file = open(savepath, "w+", encoding="utf-8")
    for i in range(len(datalist)):
        file.write(datalist[i])
        file.write("\n")
    file.close()


def getdatafromlink(alllinks):
    parts = ["浦东新区", "黄浦区", "静安区", "徐汇区", "长宁区", "普陀区", "虹口区", "杨浦区",
             "宝山区", "闵行区", "嘉定区", "金山区", "松江区", "青浦区", "奉贤", "崇明区"]
    shanghaidata = {}
    for link in alllinks:
        oneday_shanghaidata = {}
        onedaydata = []
        html = askurl(link)
        bs = BeautifulSoup(html, "html.parser")

        date = bs.find("h1").text.strip()
        k = 0
        while not "9" >= date[k] >= "0":
            k += 1
        i = k
        while date[i] != "月":
            i += 1
        j = i
        while date[j] != "日":
            j += 1
        newdate = "2022-"
        if i == k+1:
            newdate += "0"
        newdate += date[k:i] + "-"
        if i+2 == j:
            newdate += "0"
        newdate += date[i+1:j]
        date = newdate

        allpartdata = bs.find("section", {"data-id": "106156"}).find("section", {"data-id": "106156"}).find("p").text.split("，")[1].split("和")
        shanghaitotal = {}
        if "确诊病例" in allpartdata[0]:
            if re.sub("\D", "", allpartdata[0]) != "":
                shanghaitotal["新增确诊"] = re.sub("\D", "", allpartdata[0])
            else:
                shanghaitotal["新增确诊"] = 0
        if "无症状感染者" in allpartdata[1]:
            if re.sub("\D", "", allpartdata[1]) != "":
                shanghaitotal["新增无症状"] = re.sub("\D", "", allpartdata[1])
            else:
                shanghaitotal["新增无症状"] = 0
        oneday_shanghaidata["上海全境"] = shanghaitotal

        allplaces = bs.find_all("section", {"data-id": "72469"})
        for numplace in range(len(allplaces)):
            allp = allplaces[numplace].find_all("p")
            for nump in range(len(allp)):
                if nump == 0:
                    shanghaionepart = {}
                    allwzzorganran = allp[nump].text.split("，")
                    for wzzorganran in allwzzorganran:
                        if "确诊病例" in wzzorganran:
                            if re.sub("\D", "", wzzorganran) != "":
                                shanghaionepart["新增确诊"] = re.sub("\D", "", wzzorganran)
                        if "无症状感染者" in wzzorganran:
                            if re.sub("\D", "", wzzorganran) != "":
                                shanghaionepart["新增无症状"] = re.sub("\D", "", wzzorganran)
                    oneday_shanghaidata[parts[numplace]] = shanghaionepart
                elif nump != len(allp) - 1:
                    if allp[nump].text:
                        onedaydata.append("上海市" + parts[numplace] + allp[nump].text.strip().strip("，").strip(",").strip("、").strip("。"))

        savepath = "./data/addressdata/" + date + "上海病例位置.txt"
        savedata(savepath, onedaydata)
        shanghaidata[date] = oneday_shanghaidata

    with open("./data/shanghaiData.json", "w", encoding="utf-8") as f:
        json.dump(shanghaidata, f, indent=3, ensure_ascii=False)
