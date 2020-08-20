#!C:\Users\lenovo\AppData\Local\Programs\Python\Python38\python.exe
# -*- coding: utf-8 -*-

import lxml
from bs4 import BeautifulSoup
import requests
import pymysql  # 导入MySQL驱动
from datetime import datetime
from get_user_agent import get_user_agent

# conn=pymysql.connect(host='localhost',user='root',passwd='root',db='weather',port=3306,charset='utf8')  #连接数据库
# cursor=conn.cursor()   # 使用cursor()方法获取操作游标

#user_agent = get_user_agent()
def get_temperature(cursor,user_agent):

    #User-Agent能使服务器识别客户使用的操作系统及版本、CPU 类型、浏览器及版本、浏览器渲染引擎、浏览器语言、浏览器插件等
    headers = {'User-Agent':user_agent} 
    url = 'http://www.weather.com.cn/textFC/sichuan.shtml'

    response = requests.get(url, headers=headers)    # 提交requests get 请求
    soup = BeautifulSoup(response.content, "lxml")       # 用Beautifulsoup 进行解析
    #response.encoding = 'utf-8'

    province = soup.find('div', class_='conMidtab')
    # da = province.find(name='div', class_='conMidtab5')
    # td_li = da.find('tr').find_all('td')
    # date = td_li[2].text
    
    date = datetime.now().strftime('%m月%d日')
    #print(date)
    city = province.find_all(name='div', class_='conMidtab3')   #每个conMidtab3代表一个市，city代表市的集合
    for each_city in city:
        area = each_city.find_all('tr')    #area是每个区的集合
        for index, each_area in enumerate(area):
        #enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据(tr)和数据下标(index) 
            td_list = each_area.find_all('td')
            if index == 0:
                city_name = td_list[1].text.replace('\n', '')
                weather_day = td_list[2].text.replace('\n', '')
                wind_day = td_list[3].text.replace('\n', '')
                tem_max = td_list[4].text.replace('\n', '')
                weather_night = td_list[5].text.replace('\n', '')
                wind_night = td_list[6].text.replace('\n', '')
                tem_min = td_list[7].text.replace('\n', '')
            else:
                city_name = td_list[0].text.replace('\n', '')
                weather_day = td_list[1].text.replace('\n', '')
                wind_day = td_list[2].text.replace('\n', '')
                tem_max = td_list[3].text.replace('\n', '')
                weather_night = td_list[4].text.replace('\n', '')
                wind_night = td_list[5].text.replace('\n', '')
                tem_min = td_list[6].text.replace('\n', '')
                #print(type(city_name))
            print(city_name, weather_day, wind_day, tem_max, weather_night, wind_night, tem_min)
            cursor.execute('insert into forecast(date,city_name,weather_day,wind_day,tem_max,weather_night, wind_night, tem_min) values(%s,%s,%s,%s,%s,%s,%s,%s)',(date,city_name,weather_day,wind_day,tem_max,weather_night, wind_night, tem_min))
            #准备执行的sql,并执行SQL语句
            # conn.commit()  # 提交事务
            # cursor.close()  # 关闭光标对象
            # conn.close()  #关闭数据库连接

# if __name__=='__main__':
#     get_temperature(user_agent)


