# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import otherpy.addwzz as addwzzz
import otherpy.dealdata as dealdata
import otherpy.dealjsonlist as dealjsonlist
import otherpy.wzz as wzz
import otherpy.oneday_allcity as oneday_allcity
import otherpy.shanghai as shanghai

def getOriHtmlText(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        r = requests.get(url, timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding = "utf-8"
        return r.text
    except:
        return "There are some errors when get the original html!"


def getTheList(url):
    html = getOriHtmlText(url)
    soup = BeautifulSoup(html, 'html.parser')
    # 获取国家数据
    worldText = soup.find('script', {"id": "getListByCountryTypeService2true"}).text
    worldDataText = worldText[worldText.find('window.getListByCountryTypeService2true = '):]
    worldDataStr = worldDataText[worldDataText.find('[{'):worldDataText.find('}catch')]
    worldDataJson = json.loads(worldDataStr)
    with open("./otherpy/worldData.json", "w", encoding="utf-8") as f:
        json.dump(worldDataJson, f, indent=3, ensure_ascii=False)
        print("写入国家数据文件成功！")

    # # 获取各省份数据
    provinceText = soup.find('script', {"id": "getAreaStat"}).text
    provinceDataText = provinceText[provinceText.find('window.getAreaStat = '):]
    provinceDataStr = provinceDataText[provinceDataText.find('[{'):provinceDataText.find('}catch')]
    provinceDataJson = json.loads(provinceDataStr)
    with open("./otherpy/provinceData.json", "w", encoding="utf-8") as f:
        json.dump(provinceDataJson, f, indent=3, ensure_ascii=False)
        print("写入省份数据文件成功！")


def main():
    getTheList("https://ncov.dxy.cn/ncovh5/view/pneumonia")
    dealjsonlist.get_the_world_data()
    dealjsonlist.get_the_province_data()
    dealdata.deal_worlddatalist()
    dealdata.deal_chinadatalist()
    #wzz.getallpagedata()
    #addwzz.addwzztochina()
    print("写入昨天各城市疫情数据中")
    oneday_allcity.main()
    print("写入昨天各城市疫情数据成功")
    print("写入上海各区历史数据和感染者位置信息中")
    shanghai.main()
    print("写入上海各区历史数据和感染者位置信息成功")

if __name__ == '__main__':
    main()