import time
import matplotlib.pyplot as plot
import numpy as np
import sqlite3
from download_handle import DownloaderHandle


# 用来获取 时间戳
def gettime():
    return int(round(time.time() * 1000))


# 将爬到的数据存到数据库里
def save(gdp, product1, product2, product3, income, outcome, name):
    conn = sqlite3.connect(name)
    c = conn.cursor()
    # 创建表data
    try:
        # 向表中插入数据
        for i in range(20):
            c.execute("insert into data(gdp) values(%f)" % gdp[i])
        for i in range(10):
            c.execute("insert into data(product1) values(%f)" % product1[i])
        for i in range(10):
            c.execute("insert into data(product2) values(%f)" % product2[i])
        for i in range(10):
            c.execute("insert into data(product3) values(%f)" % product3[i])
        for i in range(19):
            c.execute("insert into data(income) values(%f)" % income[i])
        for i in range(19):
            c.execute("insert into data(outcome) values(%f)" % outcome[i])
    except:
        pass
    conn.commit()
    conn.close()
    return 1


# 判断表是否为空并返回表行数
def judgeblank(name):
    conn = sqlite3.connect(name)
    c = conn.cursor()
    # 判断表是否为空
    try:
        # 若不存在data则创建并返回1
        c.execute('create table data (gdp real, product1 real, product2 real, product3 real,\
         income real, outcome real)')
    except:
        return 0
        # 若已经存在则返回0
    conn.commit()
    conn.close()
    return 1


# 从数据库中调出数据
def outtable(gdp, product1, product2, product3, income, outcome, name):
    conn = sqlite3.connect(name)
    c = conn.cursor()
    pastdata = c.execute("SELECT gdp, product1,product2,product3,income,outcome FROM data;")
    for item in pastdata:
        if item[0] is not None:
            gdp.append(item[0])
        elif item[1] is not None:
            product1.append(item[1])
        elif item[2] is not None:
            product2.append(item[2])
        elif item[3] is not None:
            product3.append(item[3])
        elif item[4] is not None:
            income.append(item[4])
        elif item[5] is not None:
            outcome.append(item[5])
    conn.commit()
    conn.close()


if __name__ == '__main__':
    data = DownloaderHandle()
    # 下面是参数填充
    data.params['m'] = 'QueryData'
    data.params['dbcode'] = 'hgnd'
    data.params['rowcode'] = 'zb'
    data.params['colcode'] = 'sj'
    data.params['wds'] = '[]'
    data.params['dfwds'] = '[{"wdcode":"zb","valuecode":"A0201"}]'
    data.params['k1'] = str(gettime())
    judge = judgeblank("sqlite.db")
    # 如果不存在本地数据则下载并存储
    if judge == 1:
        # 发出请求下载数据和存到本地数据库
        data.download()
        data.handle_gdp()
        data.handle_come()
        save(data.GDP, data.product1, data.product2, data.product3, data.income, data.outcome, "sqlite.db")
    # 从数据库中调取数据
    GDP = []
    Product1 = []
    Product2 = []
    Product3 = []
    Income = []
    Outcome = []
    # 调取
    outtable(GDP, Product1, Product2, Product3, Income, Outcome, "sqlite.db")
    # 画gdp的图
    years_gdp = np.arange(1999, 2019, 1)
    years_product = np.arange(2009, 2019, 1)
    # 第一个figure
    f = plot.figure(figsize=(20, 20))
    # 第一个子图
    plot.subplot(2, 1, 1)
    plot.plot(years_gdp, GDP, color='red', marker='o', linestyle='solid', label='GDP')
    plot.title('The relationship between year and GDP')
    plot.xlabel("year")
    plot.ylabel("GPD")
    plot.xticks(np.arange(1999, 2019, 1))
    plot.grid(True)
    plot.legend()
    # 第二个子图
    plot.subplot(2, 1, 2)
    # 设置条形图宽度
    total_width, n = 0.8, 3
    width = total_width / n
    x = years_product - (total_width - width) / 2
    # 设置每个图的参数
    plot.bar(x, Product1, width=width, label='product1')
    plot.bar(x + width, Product2, width=width, label='product2')
    plot.bar(x + 2 * width, Product3, width=width, label='product3')
    # 设置标签和表头
    plot.title('The relationship between year and the added value of three tertiary industry')
    plot.xlabel("year")
    plot.ylabel("Three Industry added value")
    # 设置X轴的刻度
    plot.xticks(np.arange(2009, 2019, 1))
    plot.grid(True)
    plot.legend()

    # 第二个figure
    # 第一个子图
    years_income = np.arange(1999, 2018, 1)
    f2 = plot.figure(figsize=(20, 20))
    plot.subplot(2, 1, 1)
    plot.plot(years_income, Income, marker='o', mec='r', mfc='w', label='income')
    plot.plot(years_income, Outcome, marker='*', ms=10, label='outcome')
    plot.xticks(np.arange(1999, 2018, 1))
    plot.title('The relationship between year and the income/outcome')
    plot.xlabel("year")
    plot.ylabel("income/outcome value")
    plot.legend()
    # 第二个子图
    plot.subplot(2, 1, 2)
    # 设置条形图宽度
    total_width, n = 0.8, 2
    width = total_width / n
    x = years_income - (total_width - width) / 2
    # 设置每个图的参数
    plot.bar(x, Income, width=width, label='income')
    plot.bar(x + width, Outcome, width=width, label='outcome')
    # 设置标签和表头
    plot.title('The relationship between year and the income/outcome')
    plot.xlabel("year")
    plot.ylabel("income/outcome value")
    # 设置X轴的刻度
    plot.xticks(np.arange(1999, 2018, 1))
    plot.grid(True)
    plot.legend()
    # 显示图像
    plot.show()
