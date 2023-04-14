import requests
import os
from bs4 import BeautifulSoup

ilink = input("请输入目标链接(试卷汇总页面)：")
year_filter = input("请输入需要筛选的试卷年份（不需要筛选请按回车）：")
subject_filter = input("请输入需要筛选的学科（语文、数学、英语、物理、化学、生物），多个学科以逗号隔开（不需要筛选请按回车）：")
region_filter = input("请输入需要筛选的地区（海淀、西城等），多个地区以逗号隔开（不需要筛选请按回车）：")

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"}
r = requests.get(ilink, headers=headers)
soup = BeautifulSoup(r.text.encode(r.encoding), 'lxml')
tr_list = soup.find('table').find_all('tr')
links = []
links_final = []
file = 0
error = 0
success = 0

print("当前页面标题为：", soup.title.string)
print("当前页面编码为：", r.encoding)

# 提取链接
for tr in tr_list:
    a_list = tr.find_all('a')
    for a in a_list:
        href = a.get('href')
        links.append(href)

# 格式化链接
for i in range(len(links)):
    links[i] = links[i].replace('https://www.gaokzx.com', '')

# 删除重复项
links_final = list(set(links))

# 格式化链接
for i in range(len(links_final)):
    links_final[i] = links_final[i].replace('/c/', 'https://www.gaokzx.com/c/')

# 开始下载
for item in links_final:
    # 遍历页面
    print("正在检索第", links_final.index(item) + 1, "个链接")
    r = requests.get(item, headers=headers)
    soup = BeautifulSoup(r.text.encode(r.encoding), 'lxml')
    # 寻找下载链接
    dlink = soup.find_all(class_='download')
    if dlink:
        for link in dlink:
            # 获取文件名
            filename = link.u.text + ".pdf"
            # 判断年份、学科和地区是否符合筛选条件
            if year_filter in filename and (subject_filter == '' or any(subject in filename for subject in subject_filter.split(','))) and (region_filter == '' or any(region in filename for region in region_filter.split(','))):
                print("\t正在下载", filename)
                open("./exams/" + filename, 'wb').write(requests.get("https://www.gaokzx.com" + link.get('href')).content)
                success += 1
                file += 1
            else:
                print("\t跳过文件", filename)
                file += 1
    else:
        print("\t获取到0个文件")

# 数据汇总
print("执行完毕")
print("总共获取到", file, "个文件")
print("成功下载了", success, "个文件")
print("总共出现了", error, "个错误")
print("详情请检查输出")
