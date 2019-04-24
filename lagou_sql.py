import requests
import time
import json
import utils
from datetime import datetime
from models2 import Post
import logging
import pymysql
logger = logging.getLogger(__name__)

config={
    "host":"localhost",
    "user":"root",
    "password":"942745jl",
    "database":"lagou",
    "charset":"utf8"
}

def lagou(page,position,city):
    url_start = "https://www.lagou.com/jobs/list_"+city+"?city=%E5%8E%A6%E9%97%A8=false&fromSearch=true&labelWords=&suginput="
    url_parse = "https://www.lagou.com/jobs/positionAjax.json?city="+city+"&needAddtionalResult=false"
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.lagou.com/jobs/list_%E5%89%8D%E7%AB%AF?px=default&city=%E5%8E%A6%E9%97%A8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }

    data = {
        'first': 'true',
        'pn': page,
        'kd': position
        }
    s = requests.Session()
    s.get(url_start, headers=headers, timeout=3)  # 请求首页获取cookies
    cookie = s.cookies  # 为此次获取的cookies
    response = s.post(url_parse, data=data, headers=headers, cookies=cookie, timeout=3)  # 获取此次文本
    time.sleep(5)
    response.encoding = response.apparent_encoding
    text = json.loads(response.text)
    info = text["content"]["positionResult"]["result"]

    db = pymysql.connect(**config)
    positionName = []
    if info:
        for i in info:
            count=0
            positionName.append(i['positionName'])
            timeNow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            #连接数据库
            cursor = db.cursor()
            if i['companyLabelList']:
                companyLabelList = "".join(i['companyLabelList'])
            else:
                companyLabelList=""

            if i['industryLables']:
                industryLables = "".join(i['industryLables'])
            else:
                industryLables=""

            if i['positionLables']:
                positionLables = "".join(i['positionLables'])
            else:
                positionLables=""

            sql = "insert into lagou(positionName,workYear,salary,companyShortName\
                ,companyIdInLagou,education,jobNature,positionIdInLagou,createTimeInLagou\
                ,city,industryField,positionAdvantage,companySize,positionLables\
                ,industryLables,financeStage,companyLabelList,district\
                ,companyFullName,firstType,secondType\
                ,createByMe,keyByMe\
                )VALUES (%s,%s,%s,%s, \
                %s,%s,%s,%s,%s\
                ,%s,%s,%s,%s,%s\
                ,%s,%s,%s,%s\
                ,%s,%s,%s\
                ,%s,%s\
                )"
            cursor.execute(sql,(i['positionName'],i['workYear'],i['salary'],i['companyShortName']
                                ,i['companyId'],i['education'],i['jobNature'],i['positionId'],i['createTime']
                                ,i['city'],i['industryField'],i['positionAdvantage'],i['companySize'],positionLables
                                ,industryLables,i['financeStage'],companyLabelList,i['district']
                                ,i['companyFullName'],i['firstType'],i['secondType']
                                ,timeNow,position
                                ))
            db.commit()  #提交数据
            cursor.close()
            count=count+1
        db.close()
    else:
        print('获取失败')
        

def _insert(item):
        keys = ('companyFullName', 'jobNature', 'positionName', 'salary', 'financeStage', 'district','education','companySize','companyLabelList','skillLables','positionId','secondType','firstType','thirdType','createTime','city')
        sub_data = utils.sub_dict(item, keys)
        # print(sub_data)
        post = Post(**sub_data)
        print('save data %s ' % post.companyFullName)
        try:
            post.save()
        except Exception as e:
            print("保存失败 data=%s" % post.to_json(), exc_info=True)
def main(position,city):
        page = 1
        while page<=30:
            print('---------------------第',page,'页--------------------')
            lagou(page,position,city)
            page=page+1

if __name__ == '__main__':
	main('数据分析','深圳')

