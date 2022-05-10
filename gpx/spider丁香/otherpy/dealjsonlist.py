import json
import requests

def deal_worlddatalist():
    with open("./otherpy/worldData.json", 'r', encoding="utf-8") as f:
        worldDataJson = json.load(f)
    return worldDataJson

def get_the_world_data():
    # 获取每个国家对应的json
    worldDataJson = deal_worlddatalist()
    # 记录错误数量
    errorNum = 0
    for i in range(0, len(worldDataJson)):
        provinceName = worldDataJson[i]['provinceName']
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }

            r = requests.get(worldDataJson[i]['statisticsData'], timeout=30, headers=headers)
            r.raise_for_status()
            r.encoding = 'utf-8'
            everCountryDataJson = json.loads(r.text)
            toWriteFilePath="./data/worldData/"+provinceName+".json"
            with open(toWriteFilePath, 'w', encoding="utf-8") as file:
                json.dump(everCountryDataJson, file, indent=3, ensure_ascii=False)
        except:
            errorNum += 1
            print("在获取 "+provinceName+" 数据时出错！")
    print("各国数据获取完成！")
    print("错误数据量为："+str(errorNum))


# 处理各省数据列表
def deal_provincedatalist():
    with open("./otherpy/provinceData.json", 'r', encoding="utf-8") as f:
        provinceDataJson = json.load(f)
    return provinceDataJson

# 获取各个省份对应的json
def get_the_province_data():
    provinceDataJson = deal_provincedatalist()
    # 统计出现爬取错误的数据数量
    errorNum = 0
    for i in range(0, len(provinceDataJson)):
        provinceName = provinceDataJson[i]['provinceName']
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
            r = requests.get(provinceDataJson[i]['statisticsData'], timeout=30, headers=headers)
            r.raise_for_status()
            r.encoding = 'utf-8'
            everProvinceDataJson = json.loads(r.text)
            toWriteFilePath = "./data/provinceData/"+provinceName+".json"
            with open(toWriteFilePath, 'w', encoding="utf-8") as file:
                json.dump(everProvinceDataJson, file, indent=3, ensure_ascii=False)
        except:
            errorNum += 1
            print("在获取 "+provinceName+" 数据时出错")
    print("各省份数据获取完成！")
    print("错误数据量为："+str(errorNum))

