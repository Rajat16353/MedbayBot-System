import json
from bs4 import BeautifulSoup
import re
import time
import requests

with open('static/Dataset/final_dis_symp.json', 'r') as f:
    diseases_list = json.load(f)
diseases = list(diseases_list.keys())

not_found = []
dis_info = []
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'Accept': '*/*',
    'authority': 'www.google.com'
}
cnt = 1

for dis in diseases:
    query = dis.lower()
    URL = 'https://www.google.com/search?q={}'.format(query)
    # print(URL)
    time.sleep(2)
    page = requests.get(URL, headers=headers)
    page = BeautifulSoup(page.content, 'html5lib')
    with open('page.html', 'w') as f:
        print(page, file=f)
    try:
        if re.search(r'description', str(page.find('div', class_='TzHB6b cLjAic'))) != None:
            page = page.find('div', class_='TzHB6b cLjAic')
        else:
            page = page.find('div', class_='TzHB6b cLjAic LMRCfc')
        subtitle = page.find(
            'div', class_='PZPZlf XcVN5d MUxGbd u31kKd gsrt lyLwlc lEBKkf').get_text()
        smalltext = page.find(
            'div', class_='AEbBGb PZPZlf MUxGbd lyLwlc lEBKkf').get_text()
        points = []
        for p in page.find_all('div', class_='Is4rb PZPZlf'):
            points.append(p.get_text())
        page = re.sub(r'</h.+?>', '\n', str(page))
        page = re.sub(r'<.+?>', '', page)
        page = re.sub(subtitle+'.+', '', page)
        temp = {}
        temp['name'] = dis
        temp['overview'] = page
        temp['subtitle'] = subtitle
        temp['smalltext'] = smalltext
        temp['points'] = points
        query = dis.lower()+'treatment'
        URL = 'https://www.google.com/search?q={}'.format(query)
        # print(URL)
        time.sleep(2)
        page = requests.get(URL, headers=headers)
        page = BeautifulSoup(page.content, 'html5lib')
        if re.search(r'description', str(page.find('div', class_='LuVEUc XleQBd B03h3d P6OZi V14nKc ptcLIOszQJu__wholepage-card wp-ms'))) != None:
            page = page.find(
                'div', class_='LuVEUc XleQBd B03h3d P6OZi V14nKc ptcLIOszQJu__wholepage-card wp-ms')
        title = page.find('div', class_='i8CXdc PZPZlf mfMhoc').get_text()
        content = page.find('div', class_='m6vS6b PZPZlf').get_text()
        temp_sub = []
        for pg in page.find_all('div', class_='X0D4ae'):
            temp_1 = {}
            temp_1['subtitle'] = pg.find(
                'div', class_='HF8uc PZPZlf oz3cqf rOVRL').get_text()
            temp_1['text'] = pg.find('div', class_='aOYNtc PZPZlf').get_text()
            temp_sub.append(temp_1)
        treatment = {}
        treatment['title'] = title
        treatment['content'] = content
        treatment['additional'] = temp_sub
        temp['treatment'] = treatment
        dis_info.append(temp)
        print(cnt, dis)
        cnt += 1
    except:
        not_found.append(dis)

with open('static/Dataset/dis_info_v2.json', 'w') as f:
    json.dump(dis_info, f, indent=4)
