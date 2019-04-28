import requests


# 定义一个下载和数据处理的类
class DownloaderHandle(object):
    def __init__(self):
        # 存储爬到的东西
        self.text = {}
        self.GDP = []
        self.product1 = []
        self.product2 = []
        self.product3 = []
        self.income = []
        self.outcome = []
        self.content_come = {}
        # 目标网址(问号前面的东西)
        self.url = 'http://data.stats.gov.cn/easyquery.htm'
        # 填充参数
        self.params = {}
        # 头部填充
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
                              Firefox/61.0 Safari/537.36'}

    # 从网站上爬取数据
    def download(self):
        # 建立会话
        s = requests.session()
        # 爬取GDP和三产业增长数据
        s.get(self.url, headers=self.header, params=self.params)
        self.params['dfwds'] = '[{"wdcode":"sj","valuecode":"LAST20"}]'
        r = s.get(self.url, headers=self.header, params=self.params)
        self.text = r.json()
        # 爬取国家财政收入和支出
        self.params['dfwds'] = '[{"wdcode":"zb","valuecode":"A0801"}]'
        s.get(self.url, headers=self.header, params=self.params)
        self.params['dfwds'] = '[{"wdcode":"sj","valuecode":"LAST20"}]'
        r = s.get(self.url, headers=self.header, params=self.params)
        self.content_come = r.json()

    # 处理GDP和三类产业数据
    def handle_gdp(self):
        for i in range(20):
            self.GDP.append(self.text['returndata']['datanodes'][39-i]['data']['data'])
        for i in range(10):
            self.product1.append(self.text['returndata']['datanodes'][int(49-i)]['data']['data'])
        for i in range(10):
            self.product2.append(self.text['returndata']['datanodes'][int(69-i)]['data']['data'])
        for i in range(10):
            self.product3.append(self.text['returndata']['datanodes'][int(89-i)]['data']['data'])

    # 处理收入数据
    def handle_come(self):
        for i in range(19):
            self.income.append(self.content_come['returndata']['datanodes'][19-i]['data']['data'])
        for i in range(19):
            self.outcome.append(self.content_come['returndata']['datanodes'][39-i]['data']['data'])

