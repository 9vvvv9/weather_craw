#!C:\Users\lenovo\AppData\Local\Programs\Python\Python38\python.exe
# -*- coding: utf-8 -*-

import lxml
from bs4 import BeautifulSoup
import requests
import pymysql  # 导入MySQL驱动

conn=pymysql.connect(host='localhost',user='root',passwd='root',db='weather',port=3306,charset='utf8')  #连接数据库
cursor=conn.cursor()   # 使用cursor()方法获取操作游标

def get_cityid():
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'} 
    url = 'http://www.weather.com.cn/textFC/sichuan.shtml'

    response = requests.get(url, headers=headers)    # 提交requests get 请求
    soup = BeautifulSoup(response.content, "lxml")       # 用Beautifulsoup 进行解析
    
    province = soup.find('div', class_='conMidtab')
    city = province.find_all(name='div', class_='conMidtab3')   #每个conMidtab3代表一个市，city代表市的集合

    for each_city in city:
        area = each_city.find_all('tr')    #area是每个区的集合
        for index, each_area in enumerate(area):
        #enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据(tr)和数据下标(index) 
            td_list = each_area.find_all('td')
            if index == 0:
                city_name = td_list[1].text.replace('\n', '')
                cityid_html = td_list[1].find('a')['href']
                cityid = cityid_html[34:43]
                #print(city_name)
                #print(cityid)
            else:
                city_name = td_list[0].text.replace('\n', '')
                cityid_html = td_list[0].find('a')['href']
                cityid = cityid_html[34:43]
            print(city_name,cityid)
            cursor.execute('insert into city(city_name,city_id) values(%s,%s)',(city_name,cityid))
            #准备执行的sql,并执行SQL语句
            conn.commit()  # 提交事务

if __name__=='__main__':
    get_cityid()

cursor.close()  # 关闭光标对象
conn.close()  #关闭数据库连接
