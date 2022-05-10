import json
import datetime

def get_date_list(begin_date, end_date):
    dates = []
    t = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    date = begin_date
    while date <= end_date:
        dates.append(date)
        t += datetime.timedelta(days=1)
        date = datetime.datetime.strftime(t, "%Y-%m-%d")
    return dates


def addwzztochina():

    now = datetime.datetime.now()
    now += datetime.timedelta(days=-1)
    nowdate = datetime.datetime.strftime(now, "%Y-%m-%d")
    begindate = "2022-01-01"

    datelist = get_date_list(begindate, nowdate)
    citylist = ['香港', '台湾', '上海', '吉林', '浙江', '黑龙江', '北京', '江西', '广东', '山东', '福建',
                    '四川', '江苏', '内蒙古', '河南', '湖南', '山西', '辽宁', '青海', '云南', '海南', '广西',
                    '河北', '安徽', '湖北', '陕西', '重庆', '新疆', '天津', '甘肃', '贵州', '宁夏', '澳门', '西藏']

    wzzf = open("wzzinc.json", 'r', encoding="utf-8")
    wzzdata = json.load(wzzf)
    wzzf.close()
    chinaf = open("./data/china.json", 'r', encoding="utf-8")
    chinadata = json.load(chinaf)
    chinaf.close()
    for date in datelist:
        for city in citylist:
            chinadata[city][date]["wzzInc"] = int(wzzdata[date][city])
    file = open("./data/china.json", 'w', encoding="utf-8")
    json.dump(chinadata, file, indent=3, ensure_ascii=False)
