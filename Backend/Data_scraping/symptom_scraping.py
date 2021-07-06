import pickle
import re
import time
import requests
import warnings
import json

from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")

# Fetch disease list from 'https://www.nhsinform.scot/illnesses-and-conditions/a-to-z'
diseases = []

URL = 'https://www.nhsinform.scot/illnesses-and-conditions/a-to-z'

page = requests.get(URL, verify=False)

# use beautifulSoup to parse html document and get the required data
soup = BeautifulSoup(page.content, 'html5lib')

# find all h2 tags with class module__title as it contains the name of diseases
all_diseases = soup.find_all('h2', class_='module__title')

# print(all_diseases)

# save all the diseases diseases list
for element in all_diseases:
    diseases.append(element.get_text().strip())

# unpickle list_diseaseNames.pkl and save it in diseases2
with open('static/Dataset/list_diseaseNames.pickle', 'rb') as handle:
    diseases2 = pickle.load(handle)

print('Length of user defined list:', len(diseases2))
print('Length of list downoaded from site:', len(diseases))
print('Number of common diseases in both list:', len(
    set(diseases).intersection(set(diseases2))))

# print(diseases2)

a = set(diseases)
b = set(diseases2)
c = list(a.union(b))

c.sort()

print('Length of final list:', len(c))
# for i,dis in enumerate(c):
#   print(i,dis)

# ex = 'Acute lymphoblastic leukaemia'
# print(ex.find(":"))
# print(ex[:ex.find(":")])

for i in range(len(c)):
    if c[i].find(":") != -1:
        c[i] = c[i][:c[i].find(":")]
        # print(c[i])
c = set(c)
# print(len(c))
c = list(c)
c.sort()

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
cnt = 1
f_cnt = 1
notFound = []
disease = {}
for dis in c:
    query = dis + ' symptoms'
    URL = 'https://www.google.com/search?q={}'.format(query)
    # print(URL)
    time.sleep(2)
    page = requests.get(URL, headers=headers)
    page = BeautifulSoup(page.content, 'html5lib')
    with open('page.html', 'w') as f:
        print(page, file=f)

    try:
        page = page.find('div', class_='UDZeY OTFaAf')
    # try:
        symp1 = page.find_all('div', class_='PZPZlf')
        symp1 = symp1[1].get_text()
        # print(symp1)
        # except:
        # print(cnt, dis)
        # notFound.append(dis)
        # cnt += 1
        # try:
        parent = page.find_all('div', class_='rfZj8c')[::-1]
        # print(parent[0])
        symp2 = []
        for element in parent[1].find_all('div', class_='m6vS6b PZPZlf'):
            symp2.append(element.get_text())
            # print(symp2)

        disease[dis] = {}
        disease[dis]['symptoms'] = []
        disease[dis]['symptoms'].append(symp1)
        disease[dis]['symptoms'].append(symp2)
        # found[dis] = result.get_text()
        print(f_cnt, dis, ":", disease[dis])
        f_cnt += 1
    except:
        # print(cnt, dis)
        notFound.append(dis)
        cnt += 1

dis_list = notFound
disease

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
cnt = 1
f_cnt = 1
notFound = []
# disease = {}
for dis in dis_list:
    query = dis + ' symptoms'
    URL = 'https://www.google.com/search?q={}'.format(query)
    # print(URL)
    # print(URL)
    time.sleep(2)
    page = requests.get(URL, headers=headers)
    page = BeautifulSoup(page.content, 'html5lib')
    with open('page.html', 'w') as f:
        print(page, file=f)

    try:
        page = page.find('ul', class_='i8Z77e')
        # print(page)
        sym = []
        # try:
        symp1 = page.find_all('li', class_='TrT0Xe')
        # print(symp1)
        for element in symp1:
            sym.append(element.get_text())
        # except:
        #   print(cnt, dis)
        #   notFound.append(dis)
        #   cnt += 1

        disease[dis] = {}
        disease[dis]['symptoms'] = sym
        # found[dis] = result.get_text()
        print(f_cnt, dis, ":", disease[dis])
        f_cnt += 1
    except:
        # print(cnt, dis)
        notFound.append(dis)
        cnt += 1

# cnt = 1
# for key,value in disease.items():
#   print(cnt,key,value['symptoms'])
#   cnt += 1

with open('static/Dataset/dis_json.json', 'w') as f:
    json.dump(disease, f, indent=4)
f.close()
