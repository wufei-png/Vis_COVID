from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import json
import datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def isnum(str):
    if "9" >= str >= "0":
        return True
    else:
        return False

def getdatabyurl(url):
    option = Options()
    option.add_argument("--headless")
    browser = webdriver.Firefox(options=option)
    browser.get(url)

    allcitynames = ['香港', '台湾', '上海', '吉林', '浙江', '黑龙江', '北京', '江西', '广东', '山东', '福建',
                    '四川', '江苏', '内蒙古', '河南', '湖南', '山西', '辽宁', '青海', '云南', '海南', '广西',
                    '河北', '安徽', '湖北', '陕西', '重庆', '新疆', '天津', '甘肃', '贵州', '宁夏', '澳门', '西藏']
    WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "con")))
    text = browser.find_element(By.CLASS_NAME, "con").text.split("\n")
    data = ""
    for oneline in text:
        if oneline[:13] == "31个省（自治区、直辖市）":
            data = oneline[oneline.find("本土"):]
    browser.quit()

    onedaydata = {}
    for onecity in allcitynames:
        if data.find(onecity) != -1:
            begin = data.find(onecity)
            while not isnum(data[begin]):
                begin += 1
            end = begin
            while isnum(data[end]):
                end += 1
            onedaydata[onecity] = data[begin:end]
        else:
            onedaydata[onecity] = "0"
    return onedaydata


def getonepagedata(alldata, url):
    option = Options()
    option.add_argument("--headless")
    browser = webdriver.Firefox(options=option)
    browser.get(url)
    WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "zxxx_list")))
    re_date = ""
    alllinks = browser.find_element(By.CLASS_NAME, "zxxx_list").find_elements(By.TAG_NAME, "li")
    for link in alllinks:
        date = datetime.datetime.strptime(link.text[-10:], '%Y-%m-%d')
        offset = datetime.timedelta(days=-1)
        # 获取想要的日期的时间
        re_date = (date + offset).strftime('%Y-%m-%d')
        if re_date == "2021-12-31":
            return False
        else:
            alldata[re_date] = getdatabyurl(link.find_element(By.TAG_NAME, "a").get_attribute("href"))
    browser.quit()
    print(re_date)
    return True


def getallpagedata():
    baseurl0 = "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml"
    baseurl = "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_"
    alldata={}
    isover = getonepagedata(alldata, baseurl0)
    pagenum = 2
    while isover:
        url = baseurl + str(pagenum) + ".shtml"
        isover = getonepagedata(alldata, url)
        pagenum += 1
    WriteFilePath = "wzzinc.json"
    with open(WriteFilePath, 'w', encoding="utf-8") as file:
        json.dump(alldata, file, indent=3, ensure_ascii=False)
