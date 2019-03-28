import requests
import json
from lxml import etree

def getOnePage(n):
    # 获取网站信息
    url = f'https://maoyan.com/board/4?offset={n*10}'
    # 告诉服务器，我们是浏览器  是字典类型
    header = {"User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"}
    r = requests.get(url)
    return r.text

def parse(text):
    #初始化
    html = etree.HTML(text)
    #提起我们需要的信息，需要xpath语法
    names = html.xpath('//div[@class="movie-item-info"]/p[@class="name"]/a/@title')
    times = html.xpath('//p[@class="releasetime"]/text()')
    item = dict()
    #zip 是拉链函数
    for name,time in zip(names,times):
        item['name'] = name
        item['time'] = time
        #生成器 循环迭代
        yield item

def saveFile(data):
    with open('move.json','a',encoding='utf-8') as f:
        #把我们字典，列表转化成字符串
        datas  = json.dumps(data,ensure_ascii= False) + ",\n"
        f.write(datas)

def run():
    for n in range(0,10):
        text = getOnePage(n)
        items = parse(text)

        for item in items:
            saveFile(item)

if __name__ == '__main__':
    run()