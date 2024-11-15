import os
import random
import shutil


def get_unique_file_path(target_folder, filename):
    """生成一个唯一的文件路径，避免文件名冲突"""
    base, ext = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    while os.path.exists(os.path.join(target_folder, unique_filename)):
        unique_filename = f"{base}_{counter}{ext}"
        counter += 1
    return os.path.join(target_folder, unique_filename)


def get_gif_images_from_subfolders(base_folder, selected_folder, max_images_per_html=20):
    # 获取所有某某某文件夹
    subfolders = [f.path for f in os.scandir(base_folder) if f.is_dir()]

    # 存放每个文件夹的可选 GIF 图片
    folder_images_map = {folder: [f for f in os.listdir(folder) if f.endswith('.gif')] for folder in subfolders}

    # 存放生成的 HTML 文件名
    html_files = []

    while True:
        # 准备当前 HTML 文件
        current_html_content = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>GIF Images</title>
            <style>
                img {
                    max-width: 100%;
                    height: auto;
                    display: block;
                    margin: 20px auto;
                }
                .caption {
                    text-align: center;
                    margin-bottom: 20px;
                }
            </style>
        </head>
        <body>
            <h1>随机 GIF 图片</h1>
        '''

        current_html_image_count = 0

        # 遍历所有文件夹
        for folder, images in folder_images_map.items():
            if current_html_image_count >= max_images_per_html:
                break  # 已经达到最大图片数量

            # 如果文件夹中的图片已经被全部取出，跳过
            if not images:
                new_folder_name = f"{folder} 图片已全部取出"
                os.rename(folder, os.path.join(base_folder, new_folder_name))
                continue

            # 随机选择一张 GIF 图片
            selected_image = random.choice(images)
            selected_image_path = os.path.join(folder, selected_image)

            # 生成唯一的目标文件路径
            unique_target_path = get_unique_file_path(selected_folder, selected_image)

            # 移动已选择的图片到目标文件夹
            shutil.move(selected_image_path, unique_target_path)  # 移动文件
            images.remove(selected_image)  # 从可选图片中移除

            # 添加到 HTML 内容
            relative_image_path = os.path.relpath(unique_target_path, base_folder)  # 获取相对路径
            current_html_content += f'<div class="caption"><img src="{relative_image_path}" alt="{selected_image}">\n'
            current_html_content += f'<p>{selected_image}</p></div>\n'  # 添加文件名作为标题

            # 增加已选图片计数
            current_html_image_count += 1

            # 如果该文件夹的图片已全部取出，更新文件夹名称
            if not images:
                new_folder_name = f"{folder} 图片已全部取出"
                os.rename(folder, os.path.join(base_folder, new_folder_name))

        # 如果当前 HTML 文件没有图片，退出循环
        if current_html_image_count == 0:
            break

        current_html_content += '''
        </body>
        </html>
        '''

        # 生成 HTML 文件
        html_file_name = f'gifs_{len(html_files) + 1}.html'
        with open(os.path.join(base_folder, html_file_name), 'w', encoding='utf-8') as f:
            f.write(current_html_content)

        html_files.append(html_file_name)

    print(f"生成的 HTML 文件: {html_files}")


# 设置基本文件夹路径
base_folder = r'G:\toutiao\20241113toutiao'  # 替换为你的路径
selected_folder = r'G:\toutiao\selected_image'  # 替换为你的目标文件夹路径

# 确保目标文件夹存在
os.makedirs(selected_folder, exist_ok=True)

get_gif_images_from_subfolders(base_folder, selected_folder)
