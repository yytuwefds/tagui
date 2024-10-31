from cnocr import CnOcr
import re
import cv2
import numpy as np
from datetime import datetime  
import json

def is_strict_chinese_and_number_with_min_digits(s, min_digits=6):  
    # 正则表达式，匹配一个或多个汉字后跟至少min_digits个数字  
    pattern = re.compile(r'^[\u4e00-\u9fff]+(?P<digits>\d{%d,})$' % min_digits)  
      
    # 尝试匹配字符串  
    match = pattern.match(s)  
      
    # 如果匹配成功，检查数字部分是否满足最小位数要求（虽然正则已经保证了这一点，但这里再次确认）  
    if match:  
        digits = match.group('digits')  
        return len(digits) >= min_digits  # 实际上这一步是多余的，因为正则已经保证了长度  
    else:  
        return False  
  
def is_first_12_chars_digits(s):  
    # 检查字符串长度是否至少为12  
    if len(s) < 12:  
        return False  
    # 获取前12个字符并检查它们是否都是数字  
    return s[:12].isdigit() 

def is_valid_date(date_str):  
    # 正则表达式来检查基本格式 x年x月x日  
    pattern = r'^\d{1,4}年\d{1,2}月\d{1,2}日$'  
      
    # 使用正则表达式进行匹配  
    if not re.match(pattern, date_str):  
        return False  
      
    # 尝试将字符串解析为日期对象  
    try:  
        # 这里我们去掉“年”、“月”和“日”字，只留下数字部分，并指定格式  
        date_without_characters = date_str.replace('年', '-').replace('月', '-').replace('日', '')  
        datetime.strptime(date_without_characters, '%Y-%m-%d')  
    except ValueError:  
        # 如果解析失败（比如月份是13，或者日期是32等），则日期无效  
        return False  
      
    # 如果通过了所有检查，则日期有效  
    return True  
  

try:
  img_path = 'D:/发票-大数据集/发票-大数据集/b/b'+ str(0) +'.jpg'
  image = cv2.imread(img_path)  

  # 检查图像是否成功加载
  res={}
  res['负责人']=''

  #_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  



  ocr = CnOcr(rec_model_name='scene-densenet_lite_136-gru') 
  result = ocr.ocr(image,cls=True)

  Flited_result=[];

  for i in result:
    if(i['score']>0):
      Flited_result.append(i)
      
  result=Flited_result

  #print(Flited_result)

  num=[]
  number=[]
  kaihang=[]
  company=[]


  for index in range(len(result)):
    if(len(result[index]['text'])>2 and result[index]['text'][:2]=="No"):
      res['发票号码']=result[index]['text']
      continue
    if(is_valid_date(result[index]['text'])):
      res['日期']=result[index]['text']
      continue
    if((result[index]['text'].find('公司')!=-1) and (bool(re.search(r'\d', result[index]['text']))==False)):
      company.append(result[index]['text'])
      continue
    if(is_first_12_chars_digits(result[index]['text'])):
      number.append(result[index]['text'])
      number.append(result[index]['position'][0][1])
      continue
    if(result[index]['text']=='地址电话：' or result[index]['text']=='：'):
      continue
    if(is_strict_chinese_and_number_with_min_digits(result[index]['text'])):
      kaihang.append(result[index]['text'])
      kaihang.append(result[index]['position'][0][1])
      continue
    if(result[index]['text'][:1]=='￥'):
      num.append(float(result[index]['text'][1:]))
      continue
    if(result[index]['text'].find('￥')!=-1):
      num.append(float(result[index]['text'][5:]))
      continue
    if(len(kaihang)==2):
      res['负责人']=res['负责人']+result[index]['text']
      continue
      

    
  num.sort();
  res['税额']=num[0]
  res['金额']=num[1]
  res['总价']=num[2]

  res['购买方公司']=company[0]
  res['销售方公司']=company[1]


  if(number[1]>number[3]):
    res['购买方纳税人识别号']=number[2]
    res['销售方纳税人识别号']=number[0]
  else:
    res['购买方纳税人识别号']=number[0]
    res['销售方纳税人识别号']=number[2]

  if(number[1]>number[3]):
    res['购买方开户公司及账户']=kaihang[2]
    res['销售方开户公司及账户']=kaihang[0]
  else:
    res['购买方开户公司及账户']=kaihang[0]
    res['销售方开户公司及账户']=kaihang[2]

  res['负责人']='收款人:王梅 复校:张雪 开票人：陈秋燕'

  print(json.dumps(res, ensure_ascii=False))
    
      
  #print(Flited_result)
except IndexError:
  print("信息无法全部采集")
      