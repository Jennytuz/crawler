import requests
import time
import json
import utils
from datetime import datetime
import logging
import math
import pandas as pd

logger = logging.getLogger(__name__)
totalCount = 0
g_data = {
    'posi': '数据分析',
    'city': '深圳'
}
result = {
        'companyId':[],
        'positionId':[],
        'positionNameByMe':[],
        'industryField':[],
        'education':[],
        'workYear':[],
        'city':[],
        'positionAdvantage':[],
        'salary':[],
        'positionName':[],
        'companyShortName':[],
        'companyFullName':[],
        'companySize':[],
        'district':[],
        'latitude':[],
        'longitude':[],
        'firstType':[],
        'secondType':[],
        'financeStage':[],
        'jobNature':[]
    }

def sendRequest(page,position,city):
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
    responseResult = text["content"]["positionResult"]["result"]

    if responseResult:
        return responseResult
    else:
        print('获取失败')

def getFinalResult(positionResult):
    for i in range(len(positionResult)):
        result['companyId'].append(positionResult[i]['companyId'])
        result['positionId'].append(positionResult[i]['positionId'])
        result['positionNameByMe'].append(g_data['posi'])
        result['industryField'].append(positionResult[i]['industryField'])
        result['education'].append(positionResult[i]['education'])
        result['workYear'].append(positionResult[i]['workYear'])
        result['city'].append(positionResult[i]['city'])
        result['positionAdvantage'].append(positionResult[i]['positionAdvantage'])
        result['salary'].append(positionResult[i]['salary'])
        result['positionName'].append(positionResult[i]['positionName'])
        result['companyShortName'].append(positionResult[i]['companyShortName'])
        result['companyFullName'].append(positionResult[i]['companyFullName'])
        result['companySize'].append(positionResult[i]['companySize'])
        result['district'].append(positionResult[i]['district'])
        result['latitude'].append(positionResult[i]['latitude'])
        result['longitude'].append(positionResult[i]['longitude'])
        result['firstType'].append(positionResult[i]['firstType'])
        result['secondType'].append(positionResult[i]['secondType'])
        result['financeStage'].append(positionResult[i]['financeStage'])
        result['jobNature'].append(positionResult[i]['jobNature'])


def main(position,city):
        print(position)
        page = 1
        while page <= 21:
            print('---------------------第',page,'页--------------------')
            responseResult = sendRequest(page,position,city)
            if responseResult:
                getFinalResult(responseResult)
            else:
                print('------------无数据------')
            page = page+1
        df = pd.DataFrame(result)
        df.to_csv('lagou3.csv')
        df.to_excel('lagou3.xlsx')

if __name__ == '__main__':
	main(g_data['posi'],g_data['city'])

