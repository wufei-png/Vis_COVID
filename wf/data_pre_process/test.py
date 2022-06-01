# date=42
# month=5
# for x in range(41):
#   real_data=date%30
#   if(real_data==0):
#     real_data=30
#     month=4
#   print(str(month)+'/'+str(real_data)+'/22')
#   date=date-1
# a=['wf']
# print('wf' in a)
import json
from googletrans import Translator
a={'wf':{'a':0}}
with open('new_data.json', 'w') as file_obj:
  json.dump(a, file_obj)
# def chzn2en(filename):
#     translator = Translator()
#     tranlated = translator.translate(filename,dest='en')

#     # print(filename)
#     print(tranlated.extra_data)
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
#     print(candi_eng)
#     return candi_eng
# # chzn2en('多米尼克')
# chzn2en('英国')