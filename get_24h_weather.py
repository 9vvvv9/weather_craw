#!C:\Users\lenovo\AppData\Local\Programs\Python\Python38\python.exe
# -*- coding: utf-8 -*-

import lxml
from bs4 import BeautifulSoup
import requests
import pymysql  # 导入MySQL驱动
import js2xml
from lxml import etree

#city_id = '101270101'
def get_weather(city_id,cursor):
    # conn=pymysql.connect(host='localhost',user='root',passwd='root',db='weather',port=3306,charset='utf8')  #连接数据库
    # cursor=conn.cursor()   # 使用cursor()方法获取操作游标

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'} 
    url = 'http://www.weather.com.cn/weather1d/'+city_id+'.shtml#input'
    response = requests.get(url, headers=headers)    # 提交requests get 请求
    soup = BeautifulSoup(response.content, "lxml")       # 用Beautifulsoup 进行解析
    src = soup.select('body script')[6].string
    src_text = js2xml.parse(src, encoding='utf-8', debug=False)  # javascript代码解析，返回一个Element对象
    #print(type(src_text))
    src_tree = js2xml.pretty_print(src_text)  # 将Element解析为标签形式的代码（类似html标签）
    #print(src_tree)
    selector = etree.HTML(src_tree)  # 建立xpath树
    event_24hour = selector.xpath('//property[@name="1d"]/array/string/text()')  #列表
    #print(event_24hour)

    list_hour = []
    for index,each_3h in enumerate(event_24hour):
        hour = event_24hour[index].split(',')   #使用split(',')将一个字符串中有','的,分裂成多个字符串组成的列表
        list_hour.append(tuple(hour))    #将此列表转化成元组，并填入新列表中
    print(list_hour)

    for each_hour in list_hour:
        #print(type(each_3hour))
        cursor.execute('insert into forecast_24h(time,city_id,temperature,hour_desc,wind,wind_size) values(%s,%s,%s,%s,%s,%s)',(each_hour[0],city_id,each_hour[3],each_hour[2],each_hour[4],each_hour[5]))
        
    # conn.commit()  # 提交事务
    # cursor.close()  # 关闭光标对象
    # conn.close()  #关闭数据库连接


    

