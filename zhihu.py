# 请求url 'https://www.zhihu.com/api/v4/members/jennyintheworld/followees'
# 请求方法 'GET'
# user-agent 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
# 查询参数 include:data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics
#         offset: 20
#         limit: 20

import requests 
class SimpleCrawler:
        def crawl(self, params=None):
            url = 'https://www.zhihu.com/api/v4/members/jennyintheworld/followees'
            params = {
               "include":"data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics",
               "limit": 20,
               "offset":20 
            }
            headers = {
                'authority':'www.zhihu.com',
                'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
            }

            response = requests.get(url,headers=headers,params=params)
            print('请求url：',response.url)
            print('返回数据：',response.text)

            for follower in response.json().get('data'):
                print(follower)

if __name__ == "__main__":
    SimpleCrawler().crawl()