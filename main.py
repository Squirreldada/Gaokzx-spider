import requests
import os
from bs4 import BeautifulSoup

ilink = input("请输入目标链接(试卷汇总页面)：")
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"}
r = requests.get(ilink, headers = headers)
soup = BeautifulSoup(r.text.encode(r.encoding),'lxml')
list = soup.find('table').find_all('tr')
links = []
links_final = []
file = 0
error = 0
success = 0

print("当前页面标题为：", soup.title.string)
print("当前页面编码为：", r.encoding)

# 提取链接
for item in list:
    a = item.find_all('a')
    for ta in a:
        href = ta.get('href')
        links.append(href)

# 格式化链接
for item in links:
    links[links.index(item)] = item.replace('https://www.gaokzx.com','')

# 删除重复项
for item in links:
    hasItem = False
    for item2 in links_final:
        if item2 == item:
            hasItem = True
    if(hasItem == False):
        links_final.append(item)

# 格式化链接
for item in links_final:
    links_final[links_final.index(item)] = item.replace('/c/','https://www.gaokzx.com/c/')

print("当前共有", len(links_final), "个链接")

# 新建文件夹
if not os.path.exists("./exams/"):
    os.mkdir("./exams/")

# 开始下载
for item in links_final:
    # 遍历页面
    print("正在检索第",links_final.index(item) + 1, "个链接")
    r = requests.get(item, headers = headers)
    soup = BeautifulSoup(r.text.encode(r.encoding),'lxml')
    # 寻找下载链接
    dlink = soup.find_all(class_='download')
    if dlink:
        file += len(dlink)
        print("\t获取到", len(dlink), "个文件，正在下载")
        for link in dlink:
            if link.find_all('u'):
                print("\t\t正在下载", link.u.text + ".pdf")
                open("./exams/" + link.u.text + ".pdf", 'wb').write(requests.get("https://www.gaokzx.com"+link.get('href')).content)
                success += 1
            else:
                print("[错误]无法获取目标文件名")
                print("页面链接：", item)
                print("文件链接：", "https://www.gaokzx.com"+link.get('href'))
                error += 1
    else:
        print("\t获取到0个文件")
        
# 数据汇总
print("执行完毕")
print("总共获取到", file, "个文件")
print("成功下载了", success, "个文件")
print("总共出现了", error, "个错误")
print("详情请检查输出")
