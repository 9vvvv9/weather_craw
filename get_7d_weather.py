#!C:\Users\lenovo\AppData\Local\Programs\Python\Python38\python.exe
# -*- coding: utf-8 -*-

import lxml
from bs4 import BeautifulSoup
import requests
import pymysql  # 导入MySQL驱动
import js2xml
from lxml import etree

# city_id = '101270101'
# conn=pymysql.connect(host='localhost',user='root',passwd='root',db='weather',port=3306,charset='utf8')  #连接数据库
# cursor=conn.cursor()   # 使用cursor()方法获取操作游标

def get_weather(city_id,cursor):
    
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'} 
    url = 'http://www.weather.com.cn/weathern/'+city_id+'.shtml'

    response = requests.get(url, headers=headers)    # 提交requests get 请求
    soup = BeautifulSoup(response.content, "lxml")       # 用Beautifulsoup 进行解析
    #response.content: 以字节的方式访问请求响应体，对于非文本请求:Requests 会自动为你解码 gzip 和 deflate 传输编码的响应数据
    src = soup.select('body script')[6].string
    src_text = js2xml.parse(src, encoding='utf-8', debug=False)  # javascript代码解析，返回一个Element对象
    #print(type(src_text))
    src_tree = js2xml.pretty_print(src_text)   # 将Element解析为标签形式的代码（类似html标签）
    #print(src_tree)
    selector = etree.HTML(src_tree)   # 建立xpath树
    event_day = selector.xpath('//var[@name="eventDay"]/array/string/text()')  #列表
    event_night = selector.xpath('//var[@name="eventNight"]/array/string/text()')
    sunup = selector.xpath('//var[@name="sunup"]/array/string/text()')
    sunset = selector.xpath('//var[@name="sunset"]/array/string/text()')

    weather_7d = soup.find('div', class_='blueFor-container')
    list_date = []  
    list_desc = []
    list_wind = []
    date_7d = weather_7d.find('ul', class_='date-container')   #日期的集合
    li_list = date_7d.find_all('li') 
    for index,each_date in enumerate(li_list):
        date1 = li_list[index].text.replace('\n', '')
        date = date1[0:-2]
        list_date.append(date)
    #print(list_date)
    desc_7d = weather_7d.find('ul', class_='blue-container sky')
    li_list2 = desc_7d.find_all('li') 
    for index,each_desc in enumerate(li_list2):
        desc1 = li_list2[index].text.replace('\n', '')
        desc = desc1[0:-3]
        wind_size = desc1[-3:]
        list_desc.append(desc)
        list_wind.append(wind_size)
    list_desc.remove('')
    print(list_desc)


    weather_con = list(zip(event_day,event_night,sunup,sunset,list_date,list_desc,list_wind))
    #print(type(weather_con[0]))
    print(weather_con)

    for each_day in weather_con:
        #sql = 'insert into forecast_7d(each_day,each_night,each_sunup,each_sunset) values(%s,%s,%s,%s)',(weather_con[0],weather_con[1],weather_con[2],weather_con[3])
        cursor.execute('insert into forecast_7d(city_id,each_day,each_night,each_sunup,each_sunset,each_date,each_desc,each_wind) values(%s,%s,%s,%s,%s,%s,%s,%s)',(city_id,each_day[0],each_day[1],each_day[2],each_day[3],each_day[4],each_day[5],each_day[6]))

    # conn.commit()  # 提交事务
    # cursor.close()  # 关闭光标对象
    # conn.close()  #关闭数据库连接

    # print(type(event_day[0]))
    # print(event_day)
    # print(event_night)
    # print(sunup)
    # print(sunset)


    

