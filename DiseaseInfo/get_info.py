import json


def get_disease_info(request_json):
    dis_obj = DiseaseInfo()
    response_json = dis_obj.get_disease_info(request_json)
    del dis_obj
    return response_json


class DiseaseInfo:

    def __init__(self):
        self.response_json = {}
        with open('static/Dataset/dis_info.json', 'r') as f:
            self.dis_info = json.load(f)
        self.response_json['dis_info'] = None
        self.response_json['error'] = None

    def get_disease_info(self, request_json):
        disease_name = request_json['disease_name']
        for dis in self.dis_info:
            if dis['name'].lower() == disease_name.lower():
                self.response_json['dis_info'] = dis
                return self.response_json
        self.response_json['error'] = 'Sorry, No extra info found'
        return self.response_json
