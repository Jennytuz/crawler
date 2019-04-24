import json
import logging
import time
from datetime import datetime

import requests
import utils
from models import Post

requests.packages.urllib3.disable_warnings()
from urllib.parse import urlsplit
import html

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class WeiXinCrawler:
    def crawl(self, offset=0):
        """
        爬取更多文章
        :return:
        """
        url = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&"\
            "__biz=MzI2OTA3MTA5Mg==&"\
            "f=json&"\
            "offset={offset}&"\
            "count=10&"\
            "is_ok=1&"\
            "scene=126&"\
            "uin=777&"\
            "key=777&"\
            "pass_ticket=Hbqp97LrbNKf6hgWuXAc%2FoWp9JnaRMgX3yq1ipOP4jxPoVnmT43AB6HTH38c4prF&"\
            "wxtoken=&"\
            "appmsg_token=1003_%252FsjVJ0I%252F2UkPyb6pioMmJ3EukhtGKS9urruwRw~~&"\
            "x5=0&"\
            "f=json".format(offset=offset)


        headers = """
                    Host:mp.weixin.qq.com
                    Accept-Encoding:br, gzip, deflate
                    Cookie:devicetype=iOS12.2; lang=zh_CN; pass_ticket=Hbqp97LrbNKf6hgWuXAc/oWp9JnaRMgX3yq1ipOP4jxPoVnmT43AB6HTH38c4prF; version=1700032a; wap_sid2=CKuk/6UHElxyVVlQaE9JZDczaExNRXhBai1CQVlrRGNjT0l2RTVtdVdEcldQaThkZmdldjhEVmVsNlFhZ0FNdXl5SWFCYnlsLW9FMl9CRDFSdENQcUZDOUlXSWp2ZXNEQUFBfjCe75HlBTgNQJVO; wxuin=1958728235; wxtokenkey=777; rewardsn=; pgv_pvid=9658881596
                    Connection:keep-alive
                    Accept:*/*
                    User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.3(0x17000321) NetType/WIFI Language/zh_CN
                    Referer:https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzI2OTA3MTA5Mg==&scene=126&bizpsid=0&subscene=0&devicetype=iOS12.2&version=1700032a&lang=zh_CN&nettype=WIFI&a8scene=0&fontScale=94&pass_ticket=Hbqp97LrbNKf6hgWuXAc%2FoWp9JnaRMgX3yq1ipOP4jxPoVnmT43AB6HTH38c4prF&wx_header=1
                    Accept-Language:zh-cn
                    X-Requested-With:XMLHttpRequest
                    """
        headers = utils.str_to_dict(headers)
        response = requests.get(url, headers=headers, verify=False)
        result = response.json()
        if result.get("ret") == 0:
            msg_list = result.get("general_msg_list")
            logger.info("抓取数据：offset=%s, data=%s" % (offset, msg_list))
            self.save(msg_list)
            # 递归调用
            has_next = result.get("can_msg_continue")
            if has_next == 1:
                next_offset = result.get("next_offset")
                time.sleep(2)
                self.crawl(next_offset)
        else:
            # 错误消息
            # {"ret":-3,"errmsg":"no session","cookie_count":1}
            logger.error("无法正确获取内容，请重新从Fiddler获取请求参数和请求头")
            exit()

    @staticmethod
    def save(msg_list):
        msg_list = msg_list.replace("\/", "/")
        data = json.loads(msg_list)
        msg_list = data.get("list")
        for msg in msg_list:
            p_date = msg.get("comm_msg_info").get("datetime")
            msg_info = msg.get("app_msg_ext_info")  # 非图文消息没有此字段
            if msg_info:
                WeiXinCrawler._insert(msg_info, p_date)
                multi_msg_info = msg_info.get("multi_app_msg_item_list")
                for msg_item in multi_msg_info:
                    WeiXinCrawler._insert(msg_item, p_date)
            else:
                logger.warning(u"此消息不是图文推送，data=%s" % json.dumps(msg.get("comm_msg_info")))
    
    @staticmethod
    def _insert(item, p_date):
        keys = ('title', 'author', 'content_url', 'digest', 'cover', 'source_url')
        sub_data = utils.sub_dict(item, keys)
        post = Post(**sub_data)
        p_date = datetime.fromtimestamp(p_date)
        post["p_date"] = p_date
        logger.info('save data %s ' % post.title)
        try:
            post.save()
        except Exception as e:
            logger.error("保存失败 data=%s" % post.to_json(), exc_info=True)

    def update_post(self, post):

        post_url_params = {'__biz': 'MzI2OTA3MTA5Mg==',
                           'mid': '2651793256',
                           'idx': '1',
                           'sn': '91666add0a2f4dd320fa8c6065455cc4',
                           'chksm': 'f11e60f3c669e9e5a03ee6124e103d84f2fe802d464c8ca35c9259d728fc1ab199c7713fd7e3',
                           'scene': '4'}

        data_url_params = {'__biz': 'MzI2OTA3MTA5Mg==', 'appmsg_type': '9', 'mid': '2651793256',
                      'sn': '91666add0a2f4dd320fa8c6065455cc4', 'idx': '1', 'scene': '21',
                      'title': '%25E5%2588%2586%25E5%25BC%2580%25E5%25A4%259A%25E5%25B9%25B4%25E7%259A%2584%25E6%2583%2585%25E4%25BE%25A3%25E5%2586%258D%25E8%25A7%2581%25E9%259D%25A2%25EF%25BC%259A%25E8%25B6%258A%25E6%2598%25AF%25E4%25B8%258D%25E7%2594%2598%25E5%25BF%2583%25E7%259A%2584%25E7%2588%25B1%25E6%2583%2585%25EF%25BC%258C%25E8%25B6%258A%25E8%25A6%2581%25E4%25BA%25B2%25E6%2589%258B%25E4%25BA%2586%25E6%2596%25AD',
                      'ct': '1553356619', 'abtest_cookie': 'BAABAAoACwASABMABQAjlx4AVpkeAM2ZHgDZmR4A3JkeAAAA',
                      'devicetype': 'iOS12.2', 'version': '1700032a',
                      'f': 'json', 'r': '0.6048423341041006', 'is_need_ad': '1', 
                      'both_ad': '0', 'reward_uin_count': '24', 'msg_daily_idx': '1',
                      'is_original': '0', 'uin': '777', 'key': '777',
                      'pass_ticket': 'Hbqp97LrbNKf6hgWuXAc%25252FoWp9JnaRMgX3yq1ipOP4jxPoVnmT43AB6HTH38c4prF',
                      'wxtoken': '204390160', 'clientversion': '26060030',
                      'appmsg_token': '1003_%252FsjVJ0I%252F2UkPyb6pioMmJ3EukhtGKS9urruwRw~~',
                      'x5': '1'}

        # url转义处理
        content_url = html.unescape(post.content_url)
        # 截取content_url的查询参数部分
        content_url_params = urlsplit(content_url).query
        # 将参数转化为字典类型
        content_url_params = utils.str_to_dict(content_url_params, "&", "=")
        # 更新到data_url
        data_url_params.update(content_url_params)
        body = "is_only_read=1&req_id=2900i1sqRlQwikp0KEVJieW4&pass_ticket=Hbqp97LrbNKf6hgWuXAc%25252FoWp9JnaRMgX3yq1ipOP4jxPoVnmT43AB6HTH38c4prF&is_temp_url=0"
        data = utils.str_to_dict(body, "&", "=")

        headers = """
                    Host:mp.weixin.qq.com
                    Accept-Encoding:br, gzip, deflate
                    Cookie:devicetype=iOS12.2; lang=zh_CN; pass_ticket=Hbqp97LrbNKf6hgWuXAc/oWp9JnaRMgX3yq1ipOP4jxPoVnmT43AB6HTH38c4prF; version=1700032a; wap_sid2=CKuk/6UHElxyVVlQaE9JZDczaExNRXhBai1CQVlrRGNjT0l2RTVtdVdEcldQaThkZmdldjhEVmVsNlFhZ0FNdXl5SWFCYnlsLW9FMl9CRDFSdENQcUZDOUlXSWp2ZXNEQUFBfjCe75HlBTgNQJVO; wxuin=1958728235; wxtokenkey=777; rewardsn=; pgv_pvid=9658881596
                    Connection:keep-alive
                    Accept:*/*
                    User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.3(0x17000321) NetType/WIFI Language/zh_CN
                    Referer:https://mp.weixin.qq.com/s?__biz=MzI2OTA3MTA5Mg==&mid=2651793256&idx=1&sn=91666add0a2f4dd320fa8c6065455cc4&chksm=f11e60f3c669e9e5a03ee6124e103d84f2fe802d464c8ca35c9259d728fc1ab199c7713fd7e3&scene=4&subscene=126&ascene=0&devicetype=iOS12.2&version=1700032a&nettype=WIFI&abtest_cookie=BAABAAoACwASABMABQAjlx4AVpkeAM2ZHgDZmR4A3JkeAAAA&lang=zh_CN&fontScale=94&pass_ticket=Hbqp97LrbNKf6hgWuXAc%2FoWp9JnaRMgX3yq1ipOP4jxPoVnmT43AB6HTH38c4prF&wx_header=1
                    Accept-Language:zh-cn
                    X-Requested-With:XMLHttpRequest
        """

        headers = utils.str_to_dict(headers)

        url = "https://mp.weixin.qq.com/mp/getappmsgext"
        r = requests.post(url, data=data, verify=False, params=data_url_params, headers=headers)

        result = r.json()
        if result.get("appmsgstat"):
            post['read_num'] = result.get("appmsgstat").get("read_num")
            post['like_num'] = result.get("appmsgstat").get("like_num")
            post['reward_num'] = result.get("reward_total_count")
            post['u_date'] = datetime.now()
            logger.info("「%s」read_num: %s like_num: %s reward_num: %s" %
                        (post.title, post['read_num'], post['like_num'], post['reward_num']))
            post.save()
        else:
            logger.warning(u"没有获取的真实数据，请检查请求参数是否正确，data=%s" % r.text)


if __name__ == '__main__':
    crawler = WeiXinCrawler()
    for post in Post.objects(read_num=0):
        crawler.update_post(post)
        time.sleep(1) # 防止恶意刷
