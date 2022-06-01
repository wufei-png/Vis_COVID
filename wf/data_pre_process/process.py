import os
import pandas as pd
from googletrans import Translator
import json
from tqdm import tqdm
#需要处理的 4-2---5-12
# 主体思路: 读取csv特定的数据 读取文件标题使用谷歌api翻译，寻找data.json中的key,添加进去
def chzn2en(filename):
    candi_eng=[]
    if(filename=='英国'):
      candi_eng.append('United Kingdom')
      return candi_eng
    if(filename=='多米尼克'):
      candi_eng.append('Dominica')
      return candi_eng
    if(filename=='多米尼加'):
      candi_eng.append('Dominican Republic')
      return candi_eng
    translator = Translator()
    tranlated = translator.translate(filename,dest='en')
    # print(filename)
    # print(tranlated.extra_data)
    # print(tranlated.extra_data['all-translations'])
    candi_eng.append(tranlated.text)
    # if(tranlated.extra_data['all-translations']==None):
    #   print(filename,'没有all-translations','它的tranlated是',tranlated.text)
    #   return
    if(tranlated.extra_data['all-translations']!=None):
      for i in range(len(tranlated.extra_data['all-translations'])):
        if(tranlated.extra_data['all-translations'][i][0]=='noun'):
          candi_eng.extend(tranlated.extra_data['all-translations'][i][1])
    print(candi_eng)
    return candi_eng

def getfiles():
    filenames=os.listdir(r'D:\onedrive\OneDrive - sjtu.edu.cn\大三下\数据可视化与可视分析\大作业\Vis_COVID\data_pre_process\data')
    return filenames

def adddata(olddata,newdata,country):
  if(len(newdata)!=41):
    raise Exception("长度不是41")
  date=2
  month=4
  for x in range(41):
    if(date==31):
      date=1
      month=5
    time=str(month)+'/'+str(date)+'/22'
    olddata[country][time]={'confirmed': newdata[40-x][0], 'recoveries': newdata[40-x][1], 'deaths': newdata[x][2]}
    date=date+1
    # olddata[key]

def add0data(olddata,country):
  date=2
  month=4
  for x in range(41):
    if(date==31):
      date=1
      month=5
    time=str(month)+'/'+str(date)+'/22'
    olddata[country][time]={'confirmed': 0, 'recoveries': 0, 'deaths': 0}
    date=date+1
  # olddata[key]

with open('./data.json') as f:
  data = json.load(f)
  print(type(data))
  datakeys=list(data.keys())
  # print('Dominica' in datakeys)
  datakeys_copy=set(datakeys)
  # for datakey in datakeys:
  #   print(datakey)
  # print(data['Japan'])
  # print(data['Japan'])
  # data['Japan']['4/2/22']={'confirmed': 0, 'recoveries': 0, 'deaths': 0}
  filenames=getfiles()
  for filename in tqdm(filenames,ncols=80):
    # print(filename.split('.')[0])
      newdata = pd.read_csv("D:\onedrive\OneDrive - sjtu.edu.cn\大三下\数据可视化与可视分析\大作业\Vis_COVID\data_pre_process\data"+'\\'+filename,sep=',',usecols=[2,4,6])
      newdata=newdata.values.tolist()[:41]
      # print(len(newdata))
      candi_engs=chzn2en(filename.split('.')[0])
      for candi_eng in candi_engs:
          if candi_eng in datakeys:
            datakeys_copy.remove(candi_eng)
            adddata(data, newdata, candi_eng)
            break
  # print(data['Japan'])
  print('还剩下这些国家没有数据的',datakeys_copy)
  for remain_country in datakeys_copy:
    add0data(data, remain_country)
  # print(data['CAR'])
  with open('new_data.json', 'w') as file_obj:
    json.dump(data, file_obj)
      # data = pd.read_csv("D:\onedrive\OneDrive - sjtu.edu.cn\大三下\数据可视化与可视分析\大作业\Vis_COVID\data_pre_process\data"+'\\'+filename,sep=',',usecols=[2,4,6])
  # print(data.values.tolist()[:41])
  f.close()
#   data = pd.read_csv(r'D:\onedrive\OneDrive - sjtu.edu.cn\大三下\数据可视化与可视分析\大作业\Vis_COVID\data_pre_process\data\多哥.csv',sep=',',header='infer',usecols=[5])

# filename = "\阿尔及利亚.csv"
# data = pd.read_csv("D:\onedrive\OneDrive - sjtu.edu.cn\大三下\数据可视化与可视分析\大作业\Vis_COVID\data_pre_process\data" + filename,sep=',',usecols=[2,4,6])

# print(data.values.tolist()[:41])