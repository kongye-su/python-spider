import os 
import time
import requests
from lxml.etree import tostring
from lxml.etree import HTML
from urllib.request import urlretrieve


headers = {'Host': 'mlol.qt.qq.com',
'Connection': 'keep-alive',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'accept-encoding': "gzip, deflate, br",
'Cache-Control': 'no-cache',
'User-Agent':'Mozilla/5.0 (Linux; Android 10; MI 8 Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045438 Mobile Safari/537.36 lolapp/8.5.4.10609 lolappcpu/armeabi-v7a'
}


def storeImg(url,num=-1):
    """存储图片

    Args:
        url (string): 文章的url
        num (int, optional): 格式化存储图片的名字. 默认为 -1.
    """
    res = requests.get(url,headers=headers,verify=False)

    html = HTML(res.text)

    p_s = html.cssselect('.article_content p')

    p_s.reverse()
    for p in p_s:
        img = p.xpath('./img')
        if img:
            img = img[0]
            src = img.get('src')
            if src:
                urlretrieve(src,'掌盟每日一笑/images/{}.jpg'.format((num)))
        else:
            innerhtml = tostring(p,encoding='utf-8').decode()
            if '福利'in innerhtml:
                break

def getDocUrl(url=None):
    """获得下一页文章的url

    Args:
        url ([string], firstPathUrl): 当以firstPathUrl传入时，访问第一页。否则，默认访问下一页（nextPathUrl).
    
    Return:
        [Generator]: 详情页URL的生成器
    """
    if not url:
        # 如果url未传参，则默认访问下一页
        nextPageUrlID = '' # 你的带有session_id参数的url
        url = nextPageUrlID
    
    res = requests.get(url,headers=headers)

    return parse(res)

def parse(res):
    """解析res

    Args:
        res (requests.Response): 请求url得到的回应

    Yields:
        [Generator]: 资讯详情url的生成器
    
    Return:
        [list]: res内容不是json类型时返回一个空列表
    """
    try :
        json = res.json()
        info = json['data']['feedsInfo']
        for i in info:
            url = i['feedBase']['intent']
            yield url
    except Exception:
        # 对res内容不是json类时处理
        return []
        
def main():
    # 获得存储目录图片数量，以格式化命名
    dirName = os.path.dirname(__file__)
    imgPath = os.path.join(dirName,'images')
    num = len(os.listdir(imgPath))
    print('现有照片：%d 张' %num)
    # 第一页的Url
    firstPageUrl = 'https://mlol.qt.qq.com/go/mlol_news/search/pull?input=%E6%AF%8F%E6%97%A5%E4%B8%80%E7%AC%91&search_type=0&favzone=lol&ip=10.0.2.15&network=NETWORK_WIFI&=&slidetype=0&next=&plat=android&version=10609'
    
    firstUrls = getDocUrl(firstPageUrl)
    # 获得第一页图片
    for url in firstUrls:
        storeImg(url,num)
        num+=1
    # 循环存储图片，ctrl+c退出
    while True:
        urls = getDocUrl()
        if urls:
            for url in urls:
                storeImg(url,num)
                num+=1
        else:
            break
        time.sleep(2)
    


if __name__ =="__main__":
    main()










