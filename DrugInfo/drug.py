import re
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')


def drug_interface(req_data):
    drug = Drug()
    if "drug_name" in req_data.keys():
        drug_name = req_data["drug_name"]
        if drug_name != None or not isinstance(drug_name, int) or drug_name.isalnum():
            return drug.get_drug_name(drug_name, error=None)
        else:
            return drug.get_drug_name(drug_name, error="Invalid Input !!")

    if "selected_drug_link" in req_data.keys():
        return drug.get_selected_drug(req_data["selected_drug_link"])


class Drug:
    def __init__(self):
        self.response_json = {}
        self.response_json["drug_name"] = None
        self.response_json["drug_list"] = []
        self.response_json["drug_info"] = {}
        self.response_json["error"] = None

        self.headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

    def get_drug_name(self, drug, error=None):
        self.response_json["drug_name"] = drug
        self.response_json["error"] = error

        if error == None:
            URL = f'https://www.1mg.com/search/all?filter=true&name={drug}'

            response = requests.get(URL, headers=self.headers)
            page = BeautifulSoup(response.content, 'html5lib')
            info = page.find('div', class_='style__sku-list-container___jSRzr')
            if info == None:
                self.response_json["error"] = "Item not found"
                return self.response_json

            links = info.find_all('a')

            drug_names = set()
            title_class = ''

            if links[0].find_all(class_='style__pro-title___3zxNC') != []:
                title_class = 'style__pro-title___3zxNC'
            else:
                title_class = 'style__pro-title___3G3rr'
            for link in links:
                title = link.find(class_=title_class).get_text().strip()
                if title not in drug_names:
                    drug_names.add(title)
                    link_href = link['href']

                    temp = {}
                    temp['name'] = title
                    temp['link'] = link_href
                    self.response_json['drug_list'].append(temp)

        return self.response_json

    def get_selected_drug(self, selected_drug_link):
        drug_URL = f'https://www.1mg.com{selected_drug_link}'
        response = requests.get(drug_URL, verify=False, headers=self.headers)
        page = BeautifulSoup(response.content, 'html5lib')

        if selected_drug_link.startswith("/otc"):
            soup = page.find(
                'div', class_='ProductDescription__product-description___1PfGf')
            info = self._clean_data(soup)
            self.response_json["drug_info"] = info

            if soup == None:
                self.response_json["error"] = "Info not found !!"
        else:
            side_effect_soup = page.find('div', id='side_effects')
            side_effect_info = self._clean_data(side_effect_soup)
            self.response_json["drug_info"]["side_effect"] = side_effect_info

            uses_benefits_soup = page.find('div', id='uses_and_benefits')
            uses_benefits_info = self._clean_data(uses_benefits_soup)
            self.response_json["drug_info"]["uses_benefits"] = uses_benefits_info

            if side_effect_info == None or uses_benefits_info == None:
                self.response_json["error"] = "Info not found !!"

        return self.response_json

    def _clean_data(self, soup):
        info = re.sub('<[/]*s.+?>', '', str(soup))
        info = re.sub('<[bhl].+?>', '\n', info)
        info = re.sub('</h.+?>', '\n', info)
        info = re.sub('<.+?>', '', info)
        return info
