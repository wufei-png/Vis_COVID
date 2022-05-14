import json
from googletrans import Translator
# with open('./data.json') as f:
#   data = json.load(f)
#   print(type(data))
# def chzn2en(filename):
#     translator = Translator()
#     tranlated = translator.translate(filename,dest='en')
#     # print(filename)
#     # print(tranlated.extra_data)
#     # print(tranlated.extra_data['all-translations'])
#     candi_eng=[]
#     candi_eng.append(tranlated.text)
#     # if(tranlated.extra_data['all-translations']==None):
#     #   print(filename,'没有all-translations','它的tranlated是',tranlated.text)
#     #   return
#     if(tranlated.extra_data['all-translations']!=None):
#       for i in range(len(tranlated.extra_data['all-translations'])):
#         if(tranlated.extra_data['all-translations'][i][0]=='noun'):
#           candi_eng.extend(tranlated.extra_data['all-translations'][i][1])
#           # for data in candi_eng:
#           #   print(data)
#           return candi_eng
# chzn2en('英国')
def test(data):
  data['Japan']['4/2/22']={'confirmed': 0, 'recoveries': 0, 'deaths': 0}
with open('./data.json') as f:
  data = json.load(f)
  datakeys=list(data.keys())
  datakeys_copy=set(datakeys)
  # for datakey in datakeys:
  #   print(datakey)
  # print(data['Japan'])
  # print(data['Japan'])
  # data['Japan']['4/2/22']={'confirmed': 0, 'recoveries': 0, 'deaths': 0}
  print()
  test(data)
  print(data['Japan'])
  # datakey_copy=set(datakey)
  # print('Japan' in datakey_copy)
  # datakey_copy.remove('Japan')
  # print('Japan' in datakey_copy)

  # print('Algeria' in list(data.keys()))