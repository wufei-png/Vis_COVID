# -*- coding: utf-8 -*-
import json

def deal_worlddatalist(date):
    allcountryjson = getallcountrydata(date)
    WriteFilePath = "./data/world.json"
    with open(WriteFilePath, 'w', encoding="utf-8") as file:
        json.dump(allcountryjson, file, indent=3, ensure_ascii=False)

def getallcountrydata(date):
    begindate = date[:4] + date[5:7] + date[8:10]
    allcountry = ['法国', '德国', '韩国', '英国', '西班牙', '印度', '意大利', '土耳其', '巴西', '荷兰', '俄罗斯', 
                    '越南', '日本', '比利时', '阿根廷', '奥地利', '瑞士', '伊朗', '希腊', '葡萄牙', '丹麦', '瑞典', 
                    '墨西哥', '斯洛伐克', '塞尔维亚', '智利', '伊拉克', '马来西亚', '爱尔兰', '乌克兰', '挪威', '哈萨克斯坦',
                     '秘鲁', '格鲁吉亚', '斯洛文尼亚', '芬兰', '罗马尼亚', '约旦', '黎巴嫩', '危地马拉', '澳大利亚', '蒙古',
                     '阿塞拜疆', '波兰', '波多黎各', '克罗地亚', '立陶宛', '多米尼加', '玻利维亚', '孟加拉国', '捷克', '厄瓜多尔', 
                     '塞浦路斯', '留尼旺', '中国', '突尼斯', '巴拿马', '洪都拉斯', '加拿大', '巴勒斯坦', '保加利亚', '拉脱维亚', 
                     '巴基斯坦', '利比亚', '摩洛哥', '科威特', '毛里求斯', '沙特阿拉伯', '乌拉圭', '亚美尼亚', '老挝', '埃及', 
                     '巴拉圭', '爱沙尼亚', '波黑', '委内瑞拉', '泰国', '马提尼克', '瓜德罗普岛', '阿联酋', '摩尔多瓦', '博茨瓦纳', 
                     '阿尔及利亚', '卡塔尔', '冰岛', '埃塞俄比亚', '新西兰', '阿曼', '缅甸', '特立尼达和多巴哥', '文莱', '法属圭亚那', 
                     '古巴', '黑山', '莫桑比克', '巴林', '牙买加', '阿尔巴尼亚', '斯里兰卡', '斯威士兰', '贝宁', '乌干达', '白俄罗斯', 
                     '巴巴多斯', '肯尼亚', '以色列', '不丹', '苏里南', '刚果（金）', '阿富汗', '匈牙利', '新喀里多尼亚', '尼日利亚', 
                     '伯利兹', '乌兹别克斯坦', '圭亚那', '泽西岛', '布隆迪共和国', '法属波利尼西亚', '喀麦隆', '库拉索岛', '加纳', 
                     '马约特', '卢旺达', '安哥拉', '柬埔寨', '坦桑尼亚', '纳米比亚', '哥斯达黎加', '叙利亚', '关岛', '马尔代夫', 
                     '科特迪瓦', '哥伦比亚', '萨尔瓦多', '莱索托', '苏丹', '马拉维', '吉尔吉斯斯坦', '巴哈马', '阿鲁巴', '毛里塔尼亚', 
                     '根西岛', '开曼群岛', '马达加斯加', '塞舌尔', '海地', '加蓬', '马恩岛', '佛得角', '索马里', '马里', '刚果（布）', 
                     '多哥', '尼加拉瓜', '斐济', '塞内加尔', '多米尼克', '百慕大', '北马里亚纳群岛联邦', '美属维尔京群岛', '也门共和国', 
                     '摩纳哥', '格陵兰', '圣文森特和格林纳丁斯', '卢森堡', '格林那达', '圣马丁岛', '印度尼西亚', '赞比亚共和国', '中非共和国', 
                     '几内亚', '尼泊尔', '新加坡', '布基纳法索', '安提瓜和巴布达', '南苏丹', '荷属圣马丁', '圣其茨和尼维斯', '列支敦士登', 
                     '科摩罗', '赤道几内亚', '东帝汶', '圣巴泰勒米岛', '马耳他', '英属维尔京群岛', '特克斯和凯科斯群岛', '巴布亚新几内亚', 
                     '吉布提', '法罗群岛', '安道尔', '塞拉利昂', '圣多美和普林西比', '厄立特里亚', '尼日尔', '几内亚比绍', '安圭拉', 
                     '圣皮埃尔和密克隆群岛', '乍得', '圣马力诺', '冈比亚', '利比里亚', '直布罗陀', '津巴布韦', '北马其顿', '塔吉克斯坦', 
                     '圣卢西亚', '蒙特塞拉特', '荷兰加勒比地区', '钻石公主号邮轮', '福克兰群岛', '梵蒂冈', '菲律宾', '美国', '南非']
    allcountryjson = {}
    for onecountry in allcountry:
        NewonecountryData = {}
        countryfilename = "./data/worldData/"+onecountry+".json"
        with open(countryfilename, 'r', encoding="utf-8") as f:
            onecountryData = json.load(f)["data"]
            for onedaycountrydata in onecountryData:
                if int(onedaycountrydata["dateId"]) > int(begindate):
                    NewonecountryData[str(onedaycountrydata["dateId"])[:4] + "-" + str(onedaycountrydata["dateId"])[4:6] + "-" + str(onedaycountrydata["dateId"])[6:8]] = onedaycountrydata
        allcountryjson[onecountry] = NewonecountryData
    return allcountryjson

def deal_chinadatalist(date):
    allcityjson = getchinadata(date)
    WriteFilePath = "./data/china.json"
    with open(WriteFilePath, 'w', encoding="utf-8") as file:
        json.dump(allcityjson, file, indent=3, ensure_ascii=False)

def getchinadata(date):

    begindate = date[:4] + date[5:7] + date[8:10]
    allcity = ['香港', '台湾', '上海市', '吉林省', '浙江省', '黑龙江省', '北京市', '江西省', '广东省', '山东省',
               '福建省', '四川省', '江苏省', '内蒙古自治区', '河南省', '湖南省', '山西省', '辽宁省', '青海省',
               '云南省', '海南省', '广西壮族自治区', '河北省', '安徽省', '湖北省', '陕西省', '重庆市', '新疆维吾尔自治区',
               '天津市', '甘肃省', '贵州省', '宁夏回族自治区', '澳门', '西藏自治区']
    allcitynames = ['香港', '台湾', '上海', '吉林', '浙江', '黑龙江', '北京', '江西', '广东', '山东', '福建',
                    '四川', '江苏', '内蒙古', '河南', '湖南', '山西', '辽宁', '青海', '云南', '海南', '广西',
                    '河北', '安徽', '湖北', '陕西', '重庆', '新疆', '天津', '甘肃', '贵州', '宁夏', '澳门', '西藏']
    allcityjson = {}
    for onecity in range(len(allcity)):
        NewonecityData = {}
        cityfilename = "./data/provinceData/"+allcity[onecity]+".json"
        with open(cityfilename, 'r', encoding="utf-8") as f:
            onecityData = json.load(f)["data"]
            for onedaycitydata in onecityData:
                if int(onedaycitydata["dateId"]) > int(begindate):
                    NewonecityData[str(onedaycitydata["dateId"])[:4]+"-"+str(onedaycitydata["dateId"])[4:6]+"-"+str(onedaycitydata["dateId"])[6:8]] = onedaycitydata
        allcityjson[allcitynames[onecity]] = NewonecityData
    return allcityjson

