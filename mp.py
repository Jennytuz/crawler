__author__ = 'jenny'
# url 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzAxNzUzNDIwMg==&scene=126&sessionid=1541935275&devicetype=iOS12.0&version=16070323&lang=zh_CN&nettype=WIFI&a8scene=0&fontScale=94&pass_ticket=nOv1cSwRYA4bWAa7nQ69lyTPTSdiWl7a%2Fqqpy1hrov0%3D&wx_header=1'
# Host mp.weixin.qq.com
# Cookie	wxtokenkey=777; devicetype=iOS12.0; lang=zh_CN; pass_ticket=nOv1cSwRYA4bWAa7nQ69lyTPTSdiWl7a/qqpy1hrov0=; rewardsn=; version=16070323; wap_sid2=CJ3LyiMSXFN0THdCLTV1TjcxbHhHajZUMGVGOFR3UXZpcDZjc3BQejB4b2FhUjhRUXA1UzhtMTRVc0ROMnJwZHBDbmVnUFRhSVM5VVJNUGtkTEpHZWU5a2NWZ1Y5WURBQUF+MLmeoN8FOA1AAQ==; wxuin=0; aics=pIMRE629wGKDMd0Ip2c95Un6x5DTWfd0ffERuokH; pgv_pvid=3988798964; ua_id=pWCKx36R02bNDIogAAAAAHkEWomlkneUkNC_QV6vIg4=; sd_cookie_crttime=1534998400240; sd_userid=38851534998400240
# X-WECHAT-KEY	7d91db1fe52a74388a576d609a7c4d836de918f64606f69ffc0e5d2c56438e135619c5d72ce0c5146ac971a0f1b163a5b640d23a61cc5426136fd32d0989cd93c74cc68517a46d24110f7f366aafc73e
# X-WECHAT-UIN	NzQ2MjIzNjU%3D
# Accept text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
#User-Agent	Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_CN
#Accept-Language	zh-cn
#Accept-Encoding	gzip
#Connection	keep-alive
import requests

def headers_to_dictionary(headers):
    headers = headers.split("\n")
    d_headers = dict()
    for h in headers:
        h = h.strip()
        if h:
            k,v = h.split(":",1)
            d_headers[k] = v.strip()
    return d_headers

def crawl():
        url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzUyMjY2ODg5NA==&scene=126&bizpsid=1553006956&sessionid=1553006956&subscene=0&devicetype=iOS12.1.3&version=17000329&lang=zh_CN&nettype=WIFI&a8scene=0&fontScale=94&pass_ticket=ujnURerD%2F%2F1%2FT%2FCSC6CbjeISJgLm7ap7YG2SWYZgsl1TRmbqMWBXMuLV5uB6M9It&wx_header=1"  
            
        headers = """
Host: mp.weixin.qq.com
Cookie: devicetype=iOS12.1.3; lang=zh_CN; pass_ticket=ujnURerD//1/T/CSC6CbjeISJgLm7ap7YG2SWYZgsl1TRmbqMWBXMuLV5uB6M9It; version=17000329; wap_sid2=CKuk/6UHElxEckh4Q2pxdWkyVzJXazhVLVF5dlBqWnV0Z1VhM0pwNk9zNnpRUHBLM0k3a2tGX2xFNFFYaEVQU1gxQlA3dnRJWk5xNW5Tb3VRMzFmT0JVQ2pRcXZHLWdEQUFBfjD2gsTkBTgNQJVO; wxuin=1958728235; pgv_pvid=9658881596
X-WECHAT-KEY: d075543e7371b6d70739b61750cda1ab3946dc22cf944da490962f3ac6f2b9cd77ce4a659577c204970563dce2fbf70c61c14f1f96e86d44616a9b9c7f151f1d6b776c9e2542874da7511c3d873e2151
X-WECHAT-UIN: MTk1ODcyODIzNQ%3D%3D
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D5032a MicroMessenger/7.0.3(0x17000321) NetType/WIFI Language/zh_CN
Accept-Language: zh-cn
Accept-Encoding: br, gzip, deflate
Connection: keep-alive
        """
        headers = headers_to_dictionary(headers)
        response = requests.get(url, headers = headers, verify= False)
        print(response.text)

        if '<title>验证</title>' in response.text:
            raise Exception("获取微信公众号文章失败，可能是因为你的请求参数有误，请重新获取")
        data = extract_data(response.text)
        for item in data:
            print(item)
        with open("weixin_history.html", "w", encoding="utf-8") as f:
            f.write(response.text)

def extract_data(html_content):
    """
    从html页面中提取历史文章数据
    :param html_content 页面源代码
    :return: 历史文章列表
    """
    import re
    import html
    import json

    rex = "msgList = '({.*?})'"
    pattern = re.compile(pattern=rex, flags=re.S)
    match = pattern.search(html_content)
    if match:
        data = match.group(1)
        data = html.unescape(data)
        data = json.loads(data)
        articles = data.get("list")
        for item in articles:
            print(item)
        return articles

if __name__ == "__main__":
    crawl()