import requests
import random
import re
import os
import json
from bs4 import BeautifulSoup
from jinja2 import Template
from datetime import datetime

"""
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36', }
params = {
    'category': 'pc_user_hot',
    'token': 'MS4wLjABAAAA5TUdfw1L2Ov1d9KMSYgdL513iQtG9RZy2nXUL29OF3iK9IrTgkRGNPh-C6cwyHEc',
    'aid': '24',
    'app_name': 'toutiao_web',
    'msToken': 'lC_KQRWXIgPge4TuRWrzdkrMFnY0aqoA_R3q4W2dZvhn8f46WyAHW28I0o0_FdXFZRptHKlyn383nFLPsvkKogZnt0vGlVenG4pJCuix7A3fYzkSvr9EdKw8XAHm7gzP',
    'a_bogus': 'dy8wQQzfDDgsvdWp54KLfY3qVWH3Ym6J0t9bMDhqznfwSg39HMPD9exoxkwv/pEjNG/pIebjy4hbYp9grQAn0rDUHWwEUdQ2mgWkKl5Q5xSSs1feeLbQrsJx-kTlFeep5JV3EcvhqJKcFYSg09Oc57HvPjoja3LkFk6FOoQ/',
}
response = requests.get('https://www.toutiao.com/api/pc/list/feed', params=params, headers=headers)
"""


def scrape_link():
    # print(response.json())
    content = []
    for i in response.json()['data']:
        # print(i)
        if 'article_url' not in i:
            continue

        read_count = i['itemCell']['itemCounter']['readCount']
        title = i['title']
        url = i['article_url']
        # print(read_count, title, url)
        if read_count > 1000:
            content.append({'title': title, 'url': url, 'read_count': read_count})

    # print(content)
    return content


content_list = scrape_link()
# print(content_list)
data_to_write = [{'title': i['title'], 'url': i['url'], 'read_count': i['read_count']} for i in content_list]
print(data_to_write)

# 读取现有的 JSON 文件
try:
    with open('url.json', 'r', encoding='utf-8') as json_file:
        existing_data = json.load(json_file)
except FileNotFoundError:
    # 如果文件不存在，初始化为空列表
    existing_data = []

# 检查并添加新数据
for item in data_to_write:
    # 使用一个生成器表达式检查是否已存在
    if not any(existing_item['title'] == item['title'] and existing_item['url'] == item['url'] for existing_item in existing_data):
        existing_data.append(item)


# 写入 JSON 文件
with open('url.json', 'w', encoding='utf-8') as json_file:
    json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
