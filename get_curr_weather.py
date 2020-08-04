#!C:\Users\lenovo\AppData\Local\Programs\Python\Python38\python.exe
# -*- coding: utf-8 -*-

import requests
import re
import time
from datetime import datetime
import json  #可以使用 json 模块来对 JSON 数据进行编解码
import pymysql  # 导入MySQL驱动

# 使用cursor()方法获取操作游标
# conn=pymysql.connect(host='localhost',user='root',passwd='root',db='weather',port=3306,charset='utf8')  #连接数据库
# cursor=conn.cursor() 
# city_id = '101270101'

def get_currtem(city_id,cursor):
    
    #获取毫秒
    t = time.time()  #time.time()用于获取当前时间戳(1970纪元后经过的浮点秒数)
    #时间戳都以自从1970年1月1日午夜（历元）经过了多长时间来表示
    #round() 方法返回浮点数x的四舍五入值
    millisecond = int(round(t * 1000))   #毫秒级时间戳
    #伪装headers
    headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
                'Connection':'Keep-Alive',
                'Host':'d1.weather.com.cn',  #请求的web服务器域名地址
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                'Referer':'http://www.weather.com.cn/weather1dn/'+city_id+'.shtml'
                #http://www.weather.com.cn/weather1dn/101010100.shtml
            }
    #referer的作用就是记录你在访问一个目标网站时，在访问前你的原网站的地址
    #python提交request申请时，类似于在浏览器中的空地址栏里键入网页然后访问，
    #此时无referer，这时网站的设置可能是要求有referer，且referer的网站必须是你进来之前的网站
    #破解referer反爬虫的办法：
    #构造header的时候，传入Referer参数，它的值为与你要爬取的东西相关的网站，或者原网站

    res = requests.get('http://d1.weather.com.cn/sk_2d/'+city_id+'.html?_='+str(millisecond),params=None, headers=headers)  #为请求添加 HTTP 头部
    res.encoding = 'utf-8'   #修改服务器响应编码为utf-8
    res.raise_for_status()   #要检查请求是否成功,若不成功则产生一个异常
    content = res.text  #文本编码

    #compile 函数用于编译正则表达式，生成一个正则表达式（ Pattern ）对象，供 match() 和 search() 这两个函数使用
    #re.compile(pattern[, flags])
    #前面的 r 表示字符串为非转义的原始字符串，让编译器忽略反斜杠，也就是忽略转义字符
    #[^\}]表示匹配除了\、}之外的所有字符
    tq_regex = re.compile(r'\{[^\}]*\}')   #re.compile() 返回 RegexObject 对象

    #re.search 扫描整个字符串并返回第一个成功的匹配的对象，否则返回None
    json_str = tq_regex.search(content)
    # 可以使用group(num) 或 groups() 匹配对象函数来获取匹配表达式(而不是对象)
    # groups()返回一个包含所有小组字符串的元组
    # jsonstr.group():返回{}里面的内容
    # json.loads(): 对数据进行解码
    dict_json = json.loads(json_str.group())  # 将 JSON 对象转换为 Python 字典(dict)
    # print(dict_json)
    currtem = dict_json['temp']+'℃'   #获取字典中的实时温度
    dt=datetime.now() #创建一个datetime类对象
    time_str = str(dt.strftime('%y-%m-%d %I:%M:%S %p'))
    print(time_str)
    print(city_id,currtem)
    cursor.execute('insert into current_weather(city_id,current_tem,time_now) values(%s,%s,%s)',(city_id,currtem,time_str))
    #准备执行的sql,并执行SQL语句
    #conn.commit()  # 提交事务


# if __name__=='__main__':
#     get_currtem(city_id,cursor)


# cursor.close()  # 关闭光标对象
# conn.close()  #关闭数据库连接



    



