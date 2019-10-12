from library.core.TestCase import TestCase
import xlrd
import requests
import os
from settings import TEST_CASE_ROOT

class MWGServiceAPITest(TestCase):
    """"军运服务--API"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        file_name=os.path.join(TEST_CASE_ROOT,'mwg.xlsx')
        cls.urls = MWGServiceAPITest.read_excel(file_name, 'url')
        cls.MAX_TIMEOUT = 60.0

    # 读数据
    @staticmethod
    def read_excel(filename, sheetname='sheet1'):
        book = xlrd.open_workbook(filename)
        sheet = book.sheet_by_name(sheetname)
        rows = sheet.nrows  # 获取行数
        cols = sheet.ncols  # 获取列数
        url_dic = {}

        for r in range(rows):  # 读取每一行的数据
            name = sheet.cell_value(r, 0)
            url = sheet.cell_value(r, 1)
            url_dic.setdefault(name, url)
            # print(name,'->',url)
        return url_dic

    def test_C001_JYLY(self):
        """军运留言"""
        res = requests.get(self.urls.get('军运留言'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))

    def test_C002_ZSCX(self):
        """证书查询"""
        res = requests.get(self.urls.get('证书查询'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))
    def test_C003_ZCJY(self):
        """智闯军运"""
        res = requests.get(self.urls.get('智闯军运'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))

    def test_C004_ZXYXH(self):
        """知行英雄汇"""
        res = requests.get(self.urls.get('知行英雄汇'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))

    def test_C005_JYZAS(self):
        """军运障碍赛"""
        res = requests.get(self.urls.get('军运障碍赛'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))

    def test_C006_GDHW(self):
        """更多好玩"""
        res = requests.get(self.urls.get('更多好玩'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))

    def test_C007_WHTQ(self):
        """武汉天气"""
        res = requests.get(self.urls.get('武汉天气'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))

    def test_C008_JTZY(self):
        """交通指引"""
        res = requests.get(self.urls.get('交通指引'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))

    def test_C009_CYZY(self):
        """餐饮指引"""
        res = requests.get(self.urls.get('餐饮指引'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))

    def test_C010_WZWH(self):
        """玩转武汉"""
        res = requests.get(self.urls.get('玩转武汉'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))

    def test_C011_HMNC(self):
        """和玛挪车"""
        res = requests.get(self.urls.get('和玛挪车'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))

    def test_C012_5GKYH(self):
        """5G看樱花"""
        res = requests.get(self.urls.get('5G看樱花'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))

    def test_C013_HSH(self):
        """和生活"""
        res = requests.get(self.urls.get('和生活'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))

    def test_C014_FWTT(self):
        """飞闻头条"""
        res = requests.get(self.urls.get('飞闻头条'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))

    def test_C015_ZYFWZN(self):
        """志愿服务指南"""
        res = requests.get(self.urls.get('志愿服务指南'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))

    def test_C016_TYZSDB(self):
        """通用知识读本"""
        res = requests.get(self.urls.get('通用知识读本'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))

    def test_C017_JYXCL(self):
        """解忧小策略"""
        res = requests.get(self.urls.get('解忧小策略'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))

    def test_C018_WQDC(self):
        """问卷调查"""
        res = requests.get(self.urls.get('问卷调查'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))

    def test_C019_FWZX(self):
        """服务咨询"""
        res = requests.get(self.urls.get('服务咨询'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))

    def test_C020_KSPC(self):
        """考试评测"""
        res = requests.get(self.urls.get('考试评测'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))

    def test_C021_WTSB(self):
        """问题上报"""
        res = requests.get(self.urls.get('问题上报'), timeout=60)
        self.assertTrue(res.status_code < 400, 'http status code < 400')
        self.assertTrue(res.elapsed.total_seconds() < self.MAX_TIMEOUT, 'timeout <60')
        print('%s(%s):url:%s,status code:%s,time:%s' % (getattr(self, "_testMethodName", ""),self.shortDescription(),res.url, res.status_code, res.elapsed.total_seconds()))


