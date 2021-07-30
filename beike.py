#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 17:47:47 2020: 2021/3/30 上午1:13
@Author  : liudong
@Software: PyCharm
"""

import requests
import re
from copyheaders import headers_raw_to_dict
from bs4 import BeautifulSoup
import pandas as pd


# 根据url和参数获取网页的HTML：

def get_html(url, params):

    my_headers = b'''
    accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
    accept-language: zh-CN,zh;q=0.9
    cache-control: max-age=0
    cookie: x-zp-client-id=5bad2b52-16d9-41c5-9f7a-cca0e6f3c82a; sajssdk_2015_cross_new_user=1; sts_deviceid=17af1e74f6e106-00aa8c0ab4500d-2343360-3686400-17af1e74f6f614; ssxmod_itna2=YqIxyDciD=iQDtGC+DXCnK0Ir465CbWqD6r4rD0yuqx036dUAmDwxDT308D+1dD=; sts_sg=1; sts_chnlsid=Unknown; zp_src_url=http%3A%2F%2Fjobs.zhaopin.com%2F; ssxmod_itna=iq+x9D07Dt0QuAxlfYNDODyDf2D5kY8FFDlrjoxA5D8D6DQeGTbUqdYbH+hdOphICEq+Ti3biu+T=YiAeb=TYYx0aDbqGk=UYOheDxoq0rD74irDDxD3Db3dDSDWKD9D0bSyuEXKGWDboNDmM3DIuXDxD3SDAU4TkQxxYQDGwpLD7j5=7w=bqD+Ubig0eUK/nEnD0U4xBL=8PhnAna7rDXNNcoHnDDH9EH4iDhzHGx4/Lm2DB6pxBQSmdXj0jH9nLUVnOGbU7DoRg+X8Ak4RieDROxC/bB1t7DnyGfIQDZKiAxcThfClHD==; locationInfo_search={%22code%22:%22801%22%2C%22name%22:%22%E6%88%90%E9%83%BD%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1627565372; ZL_REPORT_GLOBAL={%22company%22:{%22actionid%22:%224841af23-4f54-48dc-9fcf-37daf4ff5a15-company%22%2C%22funczone%22:%22hiring_jd%22}%2C%22jobs%22:{%22funczoneShare%22:%22dtl_best_for_you%22%2C%22recommandActionidShare%22:%226d2e7333-4306-4393-9de0-004b11e9de44-job%22}}; at=97228547f0ef436d8a36524c23a863c1; rt=d7c15d45302044d283e3d83899a205c5; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22687622165%22%2C%22first_id%22%3A%2217af1e74f3d4a-0ab0e46907f0a2-2343360-3686400-17af1e74f3e35a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217af1e74f3d4a-0ab0e46907f0a2-2343360-3686400-17af1e74f3e35a%22%7D; acw_tc=2760826016275664160376988e8bf81b096da8b72861ed5a989e749113fa91; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1627566416
    sec-ch-ua: "Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"
    sec-ch-ua-mobile: ?0
    sec-fetch-dest: document
    sec-fetch-mode: navigate
    sec-fetch-site: same-origin
    sec-fetch-user: ?1
    upgrade-insecure-requests: 1
    user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36
    '''
    my_headers = headers_raw_to_dict(my_headers)  # 把复制的浏览器需求头转化为字典形式
    req = requests.get(url, headers=my_headers, params=params)
    req.encoding = req.apparent_encoding
    html = req.text

    return html


# 输入url和城市编号，获取由所有职位信息的html标签的字符串组成的列表：

def get_html_list(url, city_num):

    html_list = list()

    for i in range(1, 2):
        params = {'jl': str(city_num), 'kw': '贝壳找房', 'et': '2', 'p': str(i)}
        html = get_html(url, params)
        soup = BeautifulSoup(html, 'html.parser')
        html_list += soup.find_all(name='a', attrs={'class': 'joblist-box__iteminfo iteminfo'})

    for i in range(len(html_list)):
        html_list[i] = str(html_list[i])

    return html_list

def get_detail_html_list(html_list):
    detail_html_list = []

    for i in html_list:
        detail_html_list.append(get_detail_html(i))

    return detail_html_list


def get_detail_html(html):
    # 匹配所有符合条件的内容
    item = re.search('http://jobs.zhaopin.com/.*htm', html).group()

    return item


def get_job_detail(html):
    requirement = ''
    # 使用BeautifulSoup进行数据筛选
    soup = BeautifulSoup(html, 'html.parser')
    # 找到<ul class="terminal-ul clearfix">标签
    for ul in soup.find_all('ul', class_='terminal-ul clearfix'):
        # 该标签共有8个子标签，分别为：
        # 职位月薪|工作地点|发布日期|工作性质|工作经验|最低学历|招聘人数|职位类别
        lis = ul.find_all('strong')
        # 工作经验
        years = lis[4].get_text()
        # 最低学历
        education = lis[5].get_text()
    # 筛选任职要求
    for terminalpage in soup.find_all('div', class_='terminalpage-main clearfix'):
        for box in terminalpage.find_all('div', class_='tab-cont-box'):
            cont = box.find_all('div', class_='tab-inner-cont')[0]
            ps = cont.find_all('p')
            # "立即申请"按钮也是个p标签，将其排除
            for i in range(len(ps) - 1):
                requirement += ps[i].get_text().replace("\n", "").strip()   # 去掉换行符和空格

    # 筛选公司规模，该标签内有四个或五个<li>标签，但是第一个就是公司规模
    scale = soup.find(class_='terminal-ul clearfix terminal-company mt20').find_all('li')[0].strong.get_text()

    return {'years': years, 'education': education, 'requirement': requirement, 'scale': scale}


# 根据上面的HTML标签列表，把每个职位信息的有效数据提取出来，保存csv文件：

def get_csv(html_list):

    # city = position = company_name = company_size = company_type = salary = education = ability = experience = evaluation = list()  #
    # 上面赋值方法在这里是错误的，它会让每个变量指向同一内存地址，如果改变其中一个变量，其他变量会同时发生改变

    # table = pd.DataFrame(columns = ['城市','职位名称','公司名称','公司规模','公司类型','薪资','学历要求','技能要求','工作经验要求'])
    city, position, company_name, company_size, company_type, salary, education, ability, experience = ([] for i in range(9))  # 多变量一次赋值

    for i in html_list:

        if re.search(
                '<li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li>',
                i):
            s = re.search(
                '<li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li>',
                i).group(1)
            city.append(s)
            s = re.search(
                '<li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li>',
                i).group(2)
            experience.append(s)
            s = re.search(
                '<li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li>',
                i).group(3)
            education.append(s)
        else:
            city.append(' ')
            experience.append(' ')
            education.append(' ')


        if re.search('<span class="iteminfo__line1__jobname__name" title="(.*?)">', i):
            s = re.search('<span class="iteminfo__line1__jobname__name" title="(.*?)">', i).group(1)
            position.append(s)
        else:
            position.append(' ')

        if re.search('<span class="iteminfo__line1__compname__name" title="(.*?)">', i):
            s = re.search('<span class="iteminfo__line1__compname__name" title="(.*?)">', i).group(1)
            company_name.append(s)
        else:
            company_name.append(' ')

        if re.search(
                '<span class="iteminfo__line2__compdesc__item">(.*?) </span> <span class="iteminfo__line2__compdesc__item">(.*?) </span>',
                i):
            s = re.search(
                '<span class="iteminfo__line2__compdesc__item">(.*?) </span> <span class="iteminfo__line2__compdesc__item">(.*?) </span>',
                i).group(1)
            company_type.append(s)
            s = re.search(
                '<span class="iteminfo__line2__compdesc__item">(.*?) </span> <span class="iteminfo__line2__compdesc__item">(.*?) </span>',
                i).group(2)
            company_size.append(s)
        else:
            company_type.append(' ')
            company_size.append(' ')

        if re.search('<p class="iteminfo__line2__jobdesc__salary">([\s\S]*?)<', i):
            s = re.search('<p class="iteminfo__line2__jobdesc__salary">([\s\S]*?)<', i).group(1)
            s = s.strip()
            salary.append(s)
        else:
            salary.append(' ')

        s = str()
        l = re.findall('<div class="iteminfo__line3__welfare__item">.*?</div>', i)
        for i in l:
            s = s + re.search('<div class="iteminfo__line3__welfare__item">(.*?)</div>', i).group(1) + ' '
        ability.append(s)

    table = list(zip(city, position, company_name, company_size, company_type, salary, education, ability, experience))

    return table



if __name__ == '__main__':

    url = 'https://sou.zhaopin.com/'
    citys = {'成都':801}
    for i in citys.keys():
        html_list = get_html_list(url, citys[i])

        detail_url_list = get_detail_html_list(html_list)

        print(detail_url_list)

        job_detail_list = []

        for d in detail_url_list:
            job_detail_list.append(get_job_detail(d))


        file_name = i + '.csv'
        df.to_csv(file_name)
