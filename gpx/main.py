# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as ec
from tqdm import tqdm

def main():
    #本地宝
    print("爬取上海每日新增病例中")
    baseurl1 = "http://sh.bendibao.com/news/202233/249111.shtm"
    datalist1 = getdata1(baseurl1)
    savepath1 = ".\\上海每日新增病例统计表.txt"
    savedata1(savepath1, datalist1)
    print("爬取上海每日新增病例成功")

    #百度
    print("爬取全国主要地区每日新增病例中")
    baseurl2 = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner"
    savepath2 = ".\\全国主要地区每日新增病例统计表.txt"
    getdataandsave2(baseurl2, savepath2)
    print("爬取全国主要地区每日新增病例成功")

    #新增感染者位置
    print("爬取上海病例位置信息中")
    baseurl3 = "http://sh.bendibao.com/news/202244/250578.shtm"
    datalist3 = getdata3(baseurl3)
    savepath3 = ".\\上海每日新增病例位置.txt"
    savedata3(savepath3, datalist3)
    print("爬取上海病例位置信息成功")

    print("爬取全球主要地区每日新增病例中")
    baseurl4 = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner#tab4"
    savepath4 = ".\\全球主要地区每日新增病例统计表.txt"
    getdataandsave4(baseurl4, savepath4)
    print("爬取全球主要地区每日新增病例成功")

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


def getdata1(baseurl):
    # 解析数据
    datalist = []
    url = baseurl
    html = askurl(url)
    bs = BeautifulSoup(html, "html.parser")
    table = bs.find("tbody")
    for i in table.children:
        for j in i.children:
            datalist.append(j.get_text())
    return datalist


def savedata1(savepath, datalist):
    # 保存数据
    file = open(savepath, "w+", encoding="utf-8")
    for i in range(len(datalist)):
        if i == 0 or i > 4:
            file.write(datalist[i])
            if i % 7 == 4 or i == 0:
                file.write("\n")
            else:
                file.write(",")
    file.close()


def getdataandsave2(baseurl2, savepath2):

    file = open(savepath2, "w+", encoding="utf-8")
    #打开网站
    option = webdriver.ChromeOptions()
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    option.add_argument('--headless') # 设置option
    browser = webdriver.Chrome(options=option)
    browser.implicitly_wait(40)
    browser.get(baseurl2)
    time.sleep(3)
    #点击展开全部
    openfolder = browser.find_elements(By.CLASS_NAME, "Common_1-1-345_3lDRV2")[1]
    openfolder.click()
    time.sleep(3)
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
    for tr in tqdm(alltrs):
        if tr.get_attribute("class") == "VirusTable_1-1-345_3m6Ybq":
            file.write("城市")
            file.write("\n")
            alltds = tr.find_elements(By.TAG_NAME, "td")
            for td in range(len(alltds)):
                if alltds[td].text == "-":
                    file.write("0")
                else:
                    file.write(alltds[td].text)
                if td == len(alltds) - 1:
                    file.write("\n")
                else:
                    file.write(",")
        elif tr.get_attribute("class") == "VirusTable_1-1-345_2AH4U9" or tr.get_attribute("data-type") == "btn":
            alltds = tr.find_elements(By.TAG_NAME, "td")
            for td in range(len(alltds)):
                if alltds[td].text == "-":
                    file.write("0")
                else:
                    file.write(alltds[td].text)
                if td == len(alltds) - 1:
                    file.write("\n")
                else:
                    file.write(",")
        else:
            file.write("具体区域")
            file.write("\n")
    browser.quit()
    file.close()

def getdata3(baseurl):
    # 解析数据
    datalist = []
    url = baseurl
    html = askurl(url)
    bs = BeautifulSoup(html, "html.parser")
    thenewurl = bs.find("tbody").find_all("tr")[2].find_all("td")[2].find("a")["href"]
    html = askurl(thenewurl)
    bs = BeautifulSoup(html, "html.parser")
    allps = bs.find("div", {"class": "content"}).find_all("p")
    allparts = ["黄浦区", "徐汇区", "长宁区", "静安区", "普陀区", "虹口区", "杨浦区", "浦东新区", "闵行区", "宝山区", "嘉定区", "金山区", "松江区", "青浦区",
                "奉贤区", "崇明区"]
    city = "上海市"
    part = ""
    i = 2
    while i < len(allps) - 3:
        text = allps[i].text.strip()
        if text in allparts:
            part = text
            i += 2
        elif text == "已对相关居住地落实终末消毒措施。":
            i += 1
        else:
            datalist.append(city + part + text[:-1])
            i += 1
    return datalist

def savedata3(savepath, datalist):
    # 保存数据
    file = open(savepath, "w+", encoding="utf-8")
    for i in range(len(datalist)):
        file.write(datalist[i])
        file.write("\n")
    file.close()

def getdataandsave4(baseurl4, savepath4):

    file = open(savepath4, "w+", encoding="utf-8")
    #打开网站
    option = webdriver.ChromeOptions()
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    option.add_argument('--headless') # 设置option
    browser = webdriver.Chrome(options=option)
    browser.implicitly_wait(40)
    browser.get(baseurl4)
    time.sleep(3)
    #点击展开全部
    openfolder = browser.find_elements(By.CLASS_NAME, "Common_1-1-345_3lDRV2")[2]
    openfolder.click()
    time.sleep(1)
    table = browser.find_elements(By.CLASS_NAME, "VirusTable_1-1-345_3U6wJT")[0].find_element(By.TAG_NAME, "tbody")
    alltrs = table.find_elements(By.TAG_NAME, "tr")
    for onetr in tqdm(alltrs):
        alltds = onetr.find_elements(By.TAG_NAME, "td")
        for onetd in alltds:
            file.write(onetd.text)
            file.write(",")
        file.write("\n")
    browser.quit()
    file.close()

if __name__ == '__main__':
    main()


