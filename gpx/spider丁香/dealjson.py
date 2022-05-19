import json

filename = "data.json"
with open(filename, 'r', encoding="utf-8") as f:
    Data = json.load(f)

allcountry = list(Data.keys())

# Bosnia and Herzegovina
# Channel Islands


addressworld = {'Afghanistan': "阿富汗", 'Albania': "阿尔巴尼亚", 'Algeria': "阿尔及利亚", 'Andorra': "安道尔", 'Angola': "安哥拉",
                'Antigua and Barbuda': "安提瓜和巴布达", 'Argentina': "阿根廷", 'Armenia': "亚美尼亚", 'Aruba': "阿鲁巴",
                'Australia': "澳大利亚", 'Channel Islands': "泽西岛",
                'Austria': "奥地利", 'Azerbaijan': "阿塞拜疆", 'The Bahamas': "巴哈马", 'Bahrain': "巴林", 'Bangladesh': "孟加拉国",
                'Barbados': "巴巴多斯", 'Belarus': "白俄罗斯", 'Belgium': "比利时", 'Benin': "贝宁", 'Bermuda': "百慕大",
                'Bhutan': "不丹", 'Ivory Coast': "科特迪瓦",
                'Bolivia': "玻利维亚", 'Brazil': "巴西", 'Brunei': "文莱", 'Bulgaria': "保加利亚", 'Burkina Faso': "布基纳法索",
                'Bosnia and Herzegovina': "波黑", 'United Arab Emirates': "阿联酋", 'CAR': "荷兰加勒比地区",

                'Kosovo': "塞尔维亚",
                'Republic of the Congo': "刚果（布）",
                'Congo': "刚果（金）",
                'Congo (Brazzaville)': "刚果（布）",

                'Cabo Verde': "佛得角", 'Cambodia': "柬埔寨", 'Cameroon': "喀麦隆", 'Canada': "加拿大", 'Cape Verde': "佛得角",
                'Cayman Islands': "开曼群岛",
                'Chad': "乍得", 'Chile': "智利", 'China': "中国", 'Colombia': "哥伦比亚",
                'Costa Rica': "哥斯达黎加", 'Croatia': "克罗地亚", 'Cuba': "古巴", 'Curaçao': "库拉索岛", 'Cyprus': "塞浦路斯",
                'Czech Republic': "捷克",
                'Denmark': "丹麦", 'Diamond Princess': "钻石公主号邮轮", 'Djibouti': "吉布提", 'Dominica': "多米尼克",
                'Dominican Republic': "多米尼加",
                'Ecuador': "厄瓜多尔", 'Egypt': "埃及", 'El Salvador': "萨尔瓦多", 'Equatorial Guinea': "赤道几内亚",
                'Eritrea': "厄立特里亚",
                'Estonia': "爱沙尼亚", 'Eswatini': "斯威士兰", 'Ethiopia': "埃塞俄比亚", 'Faeroe Islands': "法罗群岛", 'Fiji': "斐济",
                'Finland': "芬兰",
                'France': "法国", 'French Guiana': "法属圭亚那", 'French Polynesia': "法属波利尼西亚", 'Gabon': "加蓬", 'Gambia': "冈比亚",
                'Georgia': "格鲁吉亚", 'Germany': "德国", 'Ghana': "加纳", 'Gibraltar': "直布罗陀", 'Greece': "希腊",
                'Greenland': "格陵兰",
                'Grenada': "格林那达", 'Guadeloupe': "瓜德罗普岛", 'Guam': "关岛", 'Namibia': "纳米比亚", 'Puerto Rico': "波多黎各",
                'Guatemala': "危地马拉", 'Guinea': "几内亚", 'Guyana': "圭亚那", 'Haiti': "海地", 'Honduras': "洪都拉斯",
                'Hungary': "匈牙利",
                'Iceland': "冰岛", 'India': "印度", 'Indonesia': "印度尼西亚", 'Iran': "伊朗", 'Iraq': "伊拉克", 'Ireland': "爱尔兰",
                'Isle of Man': "马恩岛",
                'Israel': "以色列", 'Italy': "意大利", 'Jamaica': "牙买加", 'Japan': "日本", 'Jordan': "约旦", 'Kazakhstan': "哈萨克斯坦",
                'Kenya': "肯尼亚",
                'Kuwait': "科威特", 'Kyrgyzstan': "吉尔吉斯斯坦", 'Latvia': "拉脱维亚", 'Lebanon': "黎巴嫩", 'Liberia': "利比里亚",
                'Liechtenstein': "列支敦士登",
                'Lithuania': "立陶宛", 'Luxembourg': "卢森堡", 'Madagascar': "马达加斯加", 'Malaysia': "马来西亚", 'Maldives': "马尔代夫",
                'Malta': "马耳他",
                'Martinique': "马提尼克", 'Mauritania': "毛里塔尼亚", 'Mauritius': "毛里求斯", 'Mayotte': "马约特", 'Mexico': "墨西哥",
                'Moldova': "摩尔多瓦",
                'Monaco': "摩纳哥", 'Mongolia': "蒙古", 'Montenegro': "黑山", 'Montserrat': "蒙特塞拉特", 'Morocco': "摩洛哥",
                'Mozambique': "莫桑比克",
                'Nepal': "尼泊尔", 'Netherlands': "荷兰", 'New Caledonia': "新喀里多尼亚", 'New Zealand': "新西兰",
                'Nicaragua': "尼加拉瓜", 'Niger': "尼日尔",
                'Nigeria': "尼日利亚", 'North Macedonia': "北马其顿", 'Norway': "挪威", 'Oman': "阿曼", 'Pakistan': "巴基斯坦",
                'Panama': "巴拿马",
                'Papua New Guinea': "巴布亚新几内亚", 'Paraguay': "巴拉圭", 'Peru': "秘鲁", 'Philippines': "菲律宾", 'Poland': "波兰",
                'Portugal': "葡萄牙",
                'Qatar': "卡塔尔", 'Reunion': "留尼旺", 'Romania': "罗马尼亚", 'Russia': "俄罗斯", 'Rwanda': "卢旺达",
                'Saint Lucia': "圣卢西亚",
                'San Marino': "圣马力诺", 'Saudi Arabia': "沙特阿拉伯",
                'Senegal': "塞内加尔", 'Serbia': "塞尔维亚", 'Seychelles': "塞舌尔", 'Singapore': "新加坡", 'Sint Maarten': "圣马丁",
                'Slovakia': "斯洛伐克",
                'Slovenia': "斯洛文尼亚", 'Somalia': "索马里", 'South Africa': "南非", 'South Korea': "韩国", 'Spain': "西班牙",
                'Sri Lanka': "斯里兰卡",
                'St Martin': "圣马丁", 'St. Barth': "圣巴泰勒米岛", 'St. Vincent Grenadines': "圣文森特和格林纳丁斯", 'Sudan': "苏丹",
                'Suriname': "苏里南",
                'Sweden': "瑞典", 'Switzerland': "瑞士", 'Syria': "叙利亚", 'Tanzania': "坦桑尼亚", 'Thailand': "泰国",
                'Timor-Leste': "东帝汶", 'Togo': "多哥",
                'Trinidad and Tobago': "特立尼达和多巴哥", 'Uganda': "乌干达", 'Ukraine': "乌克兰", 'Zambia': "赞比亚共和国",
                'Zimbabwe': "津巴布韦",
                'Tunisia': "突尼斯", 'Turkey': "土耳其", 'United Kingdom': "英国", 'United States of America': "美国",
                'Uruguay': "乌拉圭", 'Uzbekistan': "乌兹别克斯坦", 'Vatican City': "梵蒂冈", 'Venezuela': "委内瑞拉", 'Vietnam': "越南"}
print(len(addressworld), len(allcountry))
WriteFilePath = "newdata.json"
with open(WriteFilePath, 'w', encoding="utf-8") as file:
    json.dump(Data, file, indent=3, ensure_ascii=False)
