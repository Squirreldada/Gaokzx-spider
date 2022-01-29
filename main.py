import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"}
r = requests.get('https://www.gaokzx.com/c/202112/57428.html', headers = headers)
soup = BeautifulSoup(r.text.encode("ISO-8859-1"),'lxml')
list = soup.find('table').find_all('tr')
links = []
links_final = []

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
for item in links:
    links[links.index(item)] = item.replace('/c/','https://www.gaokzx.com/c/')

print("当前共有", len(links_final), "个链接")
# print(links)