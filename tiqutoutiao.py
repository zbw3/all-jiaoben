# -- python---
# ---coding:utf-8---
# author:@Marco:2024/11/8
import json
import requests
import random
import re
import os
import time
from bs4 import BeautifulSoup
from jinja2 import Template
from datetime import datetime


# 函数：抓取每个链接中的文字和图片
def scrape_link(link):
    if "log_form" in link:
        # 使用split()方法根据"?"分割
        url_parts = link.split('?log_from=')
        # 第一部分（链接主体）
        base_url = url_parts[0]
        # 第二部分（查询参数）
        query_string = url_parts[1] if len(url_parts) > 1 else ''
        # 可能需要修改cookies
        cookies = {
            'ttwid': '1%7CRE0Fp6zfgO8H_j7VW_8287YlrgFtrhSL_YJSn-YcLfI%7C1731051027%7Cf4bb4201492338750ba483494c971a11db5cf5d6a0dbf2579a4c0c9de3ace093'}
        params = {'log_from': query_string}
        response = requests.get(url=base_url, params=params, cookies=cookies)
        # return response.text
    else:
        cookies = {'ttwid': '1%7CRE0Fp6zfgO8H_j7VW_8287YlrgFtrhSL_YJSn-YcLfI%7C1731469276%7Cfb86a1bcf2f662b79b3f5141d660b36aea3a6ea4741bead000644154d8fa81b0', }
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36', }
        response = requests.get(link, cookies=cookies, headers=headers)
        # return response.text

    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)

    # 提取标题（作为文件名）
    title = soup.find('h1').text.strip()  # 根据实际标签选择器调整
    # 清理标题以适应文件名
    safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
    # 获取当前时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 创建文件夹保存GIF，加入时间戳
    folder_name = f"toutiao{timestamp}_{safe_title}"
    # 创建文件夹保存GIF
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    content = []

    # 查找所有 class="pgc-h-arrow-right" 的 <h1> 标签
    h1_tags = soup.find_all('h1', class_='pgc-h-arrow-right')
    # 遍历每个 <h1> 标签并查找紧跟其后的图片
    for h1 in h1_tags:
        # 获取 <h1> 标签中的文本
        cleaned_text = h1.get_text()
        # 使用正则表达式去除数字、"、"、"[看]"
        text = re.sub(r'\d+、|\[看\][<>:"/\\|?*]', '', cleaned_text)

        # 找到 h1 标签后面紧跟的 <div class="pgc-img"> 标签
        pgc_img_div = h1.find_next_sibling('div', class_='pgc-img')

        # 提取 <img> 标签中的图片链接
        if pgc_img_div:
            img_tag = pgc_img_div.find('img')
            if img_tag and 'src' in img_tag.attrs:
                image = img_tag['src']
                gif_name = os.path.join(folder_name, f"{text}.gif")
                # print(f"下载动图: {image}")
                img_response = requests.get(image)
                if img_response.status_code == 200:
                    with open(gif_name, 'wb') as f:
                        f.write(img_response.content)
                else:
                    print(f"动图下载失败: {image}")
                # 将文本和图片链接存入内容列表中
                content.append({'text': text, 'image': image})
    print(content)

    return content


json_file_path = "url.json"
toutiao_link = []


def read_json():
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_files:
            article = json.load(json_files)
            # 检查是否是列表
            if isinstance(article, list):
                for article in article:
                    # 获取标题、链接和阅读量
                    # title = article.get("title")
                    url = article.get("url")
                    # read_count = article.get("read_count")
                    toutiao_link.append(url)

                    # 输出文章信息
                    # print(f"标题: {title}, 链接: {url}, 阅读量: {read_count}")
                # print(toutiao_link)
                return toutiao_link
            else:
                print("数据格式不符合预期，应该是一个列表。")
    except FileNotFoundError:
        print(f"文件未找到: {json_file_path}")
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


to_link = read_json()


def get_image():
    print(to_link[2:10])
    for link in to_link[2:3]:
        print(link)
        if link != '':
            scrape_link(link)
            time.sleep(30)


get_image()