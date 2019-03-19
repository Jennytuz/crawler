import logging
import utils
import requests

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class WeiXinCrawler:
    def crawl(self):
        """
        爬取更多文章
        :return:
        """
        url = "https://mp.weixin.qq.com/mp/profile_ext?" \
                "action=getmsg" \
                "&__biz=MzIzODEyNzQ2Mw==" \
                "&f=json" \
                "&offset=10" \
                "&count=10" \
                "&is_ok=1" \
                "&scene=126" \
                "&uin=777" \
                "&key=777" \
                "&pass_ticket=ujnURerD%2F%2F1%2FT%2FCSC6CbjeISJgLm7ap7YG2SWYZgsl1TRmbqMWBXMuLV5uB6M9It" \
                "&wxtoken=" \
                "&appmsg_token=1000_wdYgkZ64QiCVLlu4dd9z4OvwP8mcdTaVw0vP9w~~" \
                "&x5=0" \
                "&f=json"


        headers = """
                    Host:mp.weixin.qq.com
                    Accept-Encoding:br, gzip, deflate
                    Cookie:devicetype=iOS12.1.3; lang=zh_CN; pass_ticket=ujnURerD//1/T/CSC6CbjeISJgLm7ap7YG2SWYZgsl1TRmbqMWBXMuLV5uB6M9It; version=17000329; wap_sid2=CKuk/6UHElxEckh4Q2pxdWkyVzJXazhVLVF5dlBqWnV0Z1VhM0pwNk9zNnpRUHBLM0k3a2tGX2xFNFFYaEVQU1gxQlA3dnRJWk5xNW5Tb3VRMzFmT0JVQ2pRcXZHLWdEQUFBfjD2gsTkBTgNQJVO; wxuin=1958728235; pgv_pvid=9658881596
                    Connection:keep-alive
                    Accept:*/*
                    User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D5032a MicroMessenger/7.0.3(0x17000321) NetType/WIFI Language/zh_CN
                    Referer:https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzIzODEyNzQ2Mw==&scene=126&bizpsid=1553006956&sessionid=1553006956&subscene=0&devicetype=iOS12.1.3&version=17000329&lang=zh_CN&nettype=WIFI&a8scene=0&fontScale=94&pass_ticket=ujnURerD%2F%2F1%2FT%2FCSC6CbjeISJgLm7ap7YG2SWYZgsl1TRmbqMWBXMuLV5uB6M9It&wx_header=1
                    Accept-Language:zh-cn
                    X-Requested-With:XMLHttpRequest
                    """
        headers = utils.str_to_dict(headers)
        response = requests.get(url, headers=headers, verify=False)
        result = response.json()
        if result.get("ret") == 0:
            msg_list = result.get("general_msg_list")
            logger.info("抓取数据：offset=%s, data=%s" % (offset, msg_list))
        else:
            # 错误消息
            # {"ret":-3,"errmsg":"no session","cookie_count":1}
            logger.error("无法正确获取内容，请重新从Fiddler获取请求参数和请求头")
            exit()


if __name__ == '__main__':
    crawler = WeiXinCrawler()
    crawler.crawl()