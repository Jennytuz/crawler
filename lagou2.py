import requests
import time
import json
import utils
from datetime import datetime
from models2 import Post
import logging
logger = logging.getLogger(__name__)

def main():
    url_start = "https://www.lagou.com/jobs/list_福州?city=%E7%A6%8F%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput="
    url_parse = "https://www.lagou.com/jobs/positionAjax.json?city=福州&needAddtionalResult=false"
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.lagou.com/jobs/list_%E5%89%8D%E7%AB%AF?px=default&city=%E7%A6%8F%E5%B7%9E',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    for x in range(1, 5):
        data = {
            'first': 'true',
            'pn': str(x),
            'kd': '前端'
                }
        s = requests.Session()
        s.get(url_start, headers=headers, timeout=3)  # 请求首页获取cookies
        cookie = s.cookies  # 为此次获取的cookies
        response = s.post(url_parse, data=data, headers=headers, cookies=cookie, timeout=3)  # 获取此次文本
        time.sleep(5)
        response.encoding = response.apparent_encoding
        text = json.loads(response.text)
        info = text["content"]["positionResult"]["result"]
        if info:
            for msg_item in info:
                _insert(msg_item)
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

if __name__ == '__main__':
	main()

