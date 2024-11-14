# -- python---
# ---coding:utf-8---
# author:@Marco:2024/11/8
import requests
import random
import re
import os
from bs4 import BeautifulSoup
from jinja2 import Template
from datetime import datetime


# 函数：抓取每个链接中的文字和图片
def scrape_link(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)

    # 提取标题（作为文件名）
    title = soup.find('h1').text.strip()  # 根据实际标签选择器调整
    # 清理标题以适应文件名
    safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
    # 获取当前时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 创建文件夹保存GIF，加入时间戳
    folder_name = f"weixin{timestamp}_{safe_title}"
    # 创建文件夹保存GIF
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    content = []

    # 查找所有 class="pgc-h-arrow-right" 的 <h1> 标签
    for section in soup.find_all('section', style="outline: 0px;width: 542px;visibility: visible;"):
        strong_tag = section.find('strong')
        # print(strong_tag)
        gif_image = section.find('img', {'data-type': 'webp'})

        if strong_tag and gif_image:
            text_content = strong_tag.text
            # 使用正则表达式去除数字、"、"、"[看]"
            text = re.sub(r'\d+、|\[看\][<>:"/\\|?*]', '', text_content)

            print("提取的文本内容:", text)
            image = gif_image['data-src']
            gif_name = os.path.join(folder_name, f"{text}.gif")
            # print(f"下载动图: {image}")
            img_response = requests.get(image)
            if img_response.status_code == 200:
                with open(gif_name, 'wb') as f:
                    f.write(img_response.content)
            else:
                print(f"动图下载失败: {image}")
            content.append({'text': text, 'image': image})
        else:
            print("Warning: Missing 'strong' tag or GIF image in a section.")

    # print(content)

    return content


# 获取三个链接的内容
link1_content = scrape_link('https://mp.weixin.qq.com/s/Y_07ri3uIuFD2c_cyM_IGw')
# link2_content = scrape_link('https://www.toutiao.com/article/7431848167253770752/?log_from=634945d07b138_1731051270550')
# link3_content = scrape_link('https://www.toutiao.com/article/7431538553202442752/?log_from=00b658cc47ce6_1731052396927')
