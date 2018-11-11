import ssl

from urllib.request import Request
from urllib.request import urlopen #与目标服务器建立连接

context = ssl._create_unverified_context()

#构建http请求对象Request
request = Request(url = 'https://foofish.net/pip.html',
                  method='Get',
                  headers={'host':'foofish.net'},
                  data= None)

#http响应
response = urlopen(request, context=context)
headers = response.info() #响应头
content = response.read() #响应体
code = response.getcode() #状态码
