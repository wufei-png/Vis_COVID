# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as ec
import json


def main():

    #百度
    baseurl2 = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner"
    getdataandsave2(baseurl2)

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



def getdataandsave2(baseurl2):

    allcitydata = {}

    #打开网站
    option = webdriver.ChromeOptions()
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    option.add_argument('--headless') # 设置option
    browser = webdriver.Chrome(options=option)
    browser.implicitly_wait(40)
    browser.get(baseurl2)
    time.sleep(4)
    #点击展开全部
    openfolder = browser.find_element(By.ID, "nationTable").find_elements(By.TAG_NAME, "div")[-1]
    openfolder.click()
    time.sleep(4)
    #定位表格
    alltrs = browser.find_element(By.ID, "nationTable").find_element(By.TAG_NAME, "table").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    for tr in alltrs:
        alltds = tr.find_elements(By.TAG_NAME, "td")
        clickelem = alltds[0].find_element(By.TAG_NAME, "div").find_elements(By.TAG_NAME, "span")[1]
        #点击各省份展开元素
        if ec.element_to_be_clickable(clickelem):
            browser.execute_script("arguments[0].click();", clickelem)
    alltrs = browser.find_element(By.ID, "nationTable").find_element(By.TAG_NAME, "table").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    #取出行，判断是否为城市
    title = ["新增确诊", "新增无症状", "累计确诊", "风险地区"]
    onecitydata = {}
    city = ""

    for tr in alltrs:
        if tr.get_attribute("class") == "VirusTable_1-1-346_3m6Ybq":
            if city != "":
                allcitydata[city] = onecitydata
            onecitydata = {}
            alltds = tr.find_elements(By.TAG_NAME, "td")
            for td in range(len(alltds)):
                if td == 0:
                    city = alltds[td].text
                else:
                    onecitydata[title[td-1]] = alltds[td].text
        elif tr.get_attribute("data-type") == "btn":
            onepart = {}
            alltds = tr.find_elements(By.TAG_NAME, "td")
            for td in range(len(alltds)):
                if td != 0:
                    if alltds[td].text == "-":
                        onepart[title[td - 1]] = 0
                    else:
                        onepart[title[td-1]] = alltds[td].text
            onecitydata[alltds[0].text] = onepart
    browser.quit()
    with open("./data/oneday_allcityData.json", "w", encoding="utf-8") as f:
        json.dump(allcitydata, f, indent=3, ensure_ascii=False)




