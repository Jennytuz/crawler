#coding: utf-8

import time
import re
import urllib.parse

import requests
from lxml import etree

KEY = "前端" #抓取的关键字
CITY = "厦门" #目标城市
# 0:[0, 2k), 1: [2k, 5k), 2: [5k, 10k), 3: [10k, 15k), 4: [15k, 25k), 5: [25k, 50k), 6: [50k, +inf)
SALARY_OPTION = 7 #薪资范围，值范围 0 ~ 6，其他值代表无范围
#进入『拉勾网』任意页面，无需登录
#打开 Chrome / Firefox 的开发者工具，从中复制一个 Cookie 放在此处
#防止被封，若无法拉取任何信息，首先考虑换 Cookie
COOKIE = "JSESSIONID=ABAAABAAADEAAFI9D4271297D6AB05BFA04D75A6A8F8C72; user_trace_token=20190411152943-d8427049-c9ba-4974-b4ef-19ad97568a48; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1554967783; _ga=GA1.2.486748293.1554967783; _gid=GA1.2.2118347023.1554967783; LGSID=20190411152949-96f2c595-5c2b-11e9-91ba-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E5%2589%258D%25E7%25AB%25AF%3Fcity%3D%25E7%25A6%258F%25E5%25B7%259E%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; LGUID=20190411152949-96f2c777-5c2b-11e9-91ba-5254005c3644; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216a0b4d7bf21ab-0b49a0a18ee139-36687e04-1024000-16a0b4d7bf3446%22%2C%22%24device_id%22%3A%2216a0b4d7bf21ab-0b49a0a18ee139-36687e04-1024000-16a0b4d7bf3446%22%7D; sajssdk_2015_cross_new_user=1; sm_auth_id=72f2wg1wvk5etr6p; LG_LOGIN_USER_ID=4428ff3a9f82451cf4d8549d2ec27d293f284ed57503bc25; _putrc=439D6025799D68DD; login=true; unick=%E5%A7%9C%E7%90%B3; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=22188ddf82d3e9d4a57a0e090b29cd75cc90fbeef5e77ebe; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_navigation; X_MIDDLE_TOKEN=0a5a1b50f35b24493f1254df78da8f8e; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1554967896; LGRID=20190411153140-d930f83c-5c2b-11e9-91be-5254005c3644; X_HTTP_TOKEN=777bc829fe7ffa5f0097694551913ea3d0580808fa; SEARCH_ID=08d5d86251b34b0ca3194a85ec39c2a3"

def init_segment():
    #按照 4.4 的方式，申请百度云分词，并填写到下面
    APP_ID = "15993898"
    API_KEY = "ljcRFMa84OyxKSTXtz5YGYd6"
    SECRET_KEY = "GijfE3hqwA3qs76zHPIkVMjq9PdfEOma"

    from aip import AipNlp
    #保留如下词性的词 https://cloud.baidu.com/doc/NLP/NLP-FAQ.html#NLP-FAQ
    retains = set(["n", "nr", "ns", "s", "nt", "an", "t", "nw", "vn"])

    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    def segment(text):
        '''
        对『任职信息』进行切分，提取信息，并进行一定处理
        '''
        try:
            result = []
            #调用分词和词性标注服务，这里使用正则过滤下输入，是因为有特殊字符的存在
            items = client.lexer(re.sub('\s', '', text))["items"]

            cur = ""
            for item in items:
                #将连续的 retains 中词性的词合并起来
                if item["pos"] in retains:
                    cur += item["item"]
                    continue

                if cur:
                    result.append(cur)
                    cur = ""
                #如果是 命名实体类型 或 其它专名 则保留
                if item["ne"] or item["pos"] == "nz":
                    result.append(item["item"])
            if cur:
                result.append(cur)
                 
            return result
        except Exception as e:
            print("fail to call service of baidu nlp.")
            return []

    return segment

#以下无需修改，拉取『拉勾网』的固定参数
SALARY_INTERVAL = ("2k以下", "2k-5k", "5k-10k", "10k-15k", "15k-25k", "25k-50k", "50k以上")
if SALARY_OPTION < len(SALARY_INTERVAL) and SALARY_OPTION >= 0:
    SALARY = SALARY_INTERVAL[SALARY_OPTION]
else:
    SALARY = None
USER_AGENT = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3"
REFERER = "https://www.lagou.com/jobs/list_" + urllib.parse.quote(KEY)
BASE_URL = "https://www.lagou.com/jobs/positionAjax.json"
DETAIL_URL = "https://www.lagou.com/jobs/{0}.html"

def get_header():
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": REFERER,
        "X-Requested-With": "XMLHttpRequest",
        "Host": "www.lagou.com",
        "Connection":"keep-alive",
        "Cookie": COOKIE,
        "Origin": "https://www.lagou.com",
        "Upgrade-Insecure-Requests":"1",
        "X-Anit-Forge-Code": "0",
        "X-Anit-Forge-Token": "None",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8"
        }
    return(headers)
#抓取职位详情页
def fetch_detail(id):
    headers = get_header()
    try:
        url = DETAIL_URL.format(id)
        print(url)
        s = requests.get(url, headers=headers)

        return s.text
    except Exception as e:
        print("fetch job detail fail. " + url)
        print(e)
        raise e

#抓取职位列表页
def fetch_list(page_index):
    headers = get_header()
    params = {"px": "default", "city": CITY, "yx": SALARY}
    data = {"first": page_index == 1, "pn": page_index, "kd": KEY}
    try:
        s = requests.post(BASE_URL, headers=headers, params=params, data=data)

        return s.json()
    except Exception as e:
        print("fetch job list fail. " + data)
        print(e)
        raise e

#根据 ID 抓取详情页，并提取『任职信息』
def fetch_requirements(result, segment):
    time.sleep(2)

    requirements = {}
    content = fetch_detail(result["positionId"])
    details = [detail.strip() for detail in etree.HTML(content).xpath('//dd[@class="job_bt"]/div/p/text()')]

    is_requirement = False
    for detail in details:
        if not detail:
            continue
        if is_requirement:
            m = re.match("([0-9]+|-)\s*[\.:：、]?\s*", detail)
            if m:
                words = segment(detail[m.end():])
                for word in words:
                    if word not in requirements:
                        requirements[word] = 1
                    else:
                        requirements[word] += 1
            else:
                break
        elif re.match("\w?[\.、 :：]?(任职要求|任职资格|我们希望你|任职条件|岗位要求|要求：|职位要求|工作要求|职位需求)", detail):
            is_requirement = True

    return requirements

#循环请求职位列表
def scrapy_jobs(segment):
    #用于过滤相同职位
    duplications = set()
    #从页 1 开始请求
    page_index = 1
    job_count = 0

    print("key word {0}, salary {1}, city {2}".format(KEY, SALARY, CITY))
    stat = {}
    while True:
        print("current page {0}, {1}".format(page_index, KEY))
        time.sleep(2)
        print(fetch_list(page_index))
        content = fetch_list(page_index)["content"]

        # 全部页已经被请求
        if content["positionResult"]["resultSize"] == 0:
            break

        results = content["positionResult"]["result"]
        total = content["positionResult"]["totalCount"]
        print("total job {0}".format(total))

        # 处理该页所有职位信息
        for result in results:
            if result["positionId"] in duplications:
                continue
            duplications.add(result["positionId"])

            job_count += 1
            print("{0}. {1}, {2}, {3}".format(job_count, result["positionName"], result["salary"], CITY))
            requirements = fetch_requirements(result, segment)
            print("/".join(requirements.keys()) + "\n")
            #把『任职信息』数据统计到 stat 中
            for key in requirements:
                if key not in stat:
                    stat[key] = requirements[key]
                else:
                    stat[key] += requirements[key]

        page_index += 1
    return stat

segment = init_segment()
stat = scrapy_jobs(segment)

#将所有『任职信息』根据提及次数排序，输出前 10 位
import operator
sorted_stat = sorted(stat.items(), key=operator.itemgetter(1))
print(sorted_stat[-10:])