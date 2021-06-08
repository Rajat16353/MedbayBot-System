import json


def check_age_and_gender(diseases, age, gender):
    obj = AGE_GENDER()
    diseases_info = obj.check_age_and_gender(diseases, age, gender)
    del obj
    return diseases_info


class AGE_GENDER:
    def __init__(self):
        with open('static/Dataset/age_and_gender_data.json', 'r') as f:
            self.AGE_DICT = json.load(f)

    def check_age_and_gender(self, diseases, age, gender):
        diseases_info = []
        for idx, dis in enumerate(diseases):
            if dis[0] not in self.AGE_DICT.keys():
                temp_dis_obj = {}
                temp_dis_obj['disease_name'] = dis[0]
                temp_dis_obj['probability'] = dis[1]
                diseases_info.append(temp_dis_obj)
                continue
            age_group = self.AGE_DICT[dis[0]]['age_group']
            gender_group = self.AGE_DICT[dis[0]]["gender"]
            temp_dis_obj = {}
            temp_dis_obj['disease_name'] = dis[0]
            temp_dis_obj['probability'] = dis[1]
            temp_dis_obj['common_in_age_groups'] = age_group
            temp_dis_obj['occurs_in_gender'] = gender_group
            temp_dis_obj['likely'] = None
            temp_dis_obj['priority'] = None
            for age_limit in age_group:
                age_limit = age_limit.split('-')
                # print(age_limit)
                if float(age) > float(age_limit[0]) and float(age) < float(age_limit[1]):
                    temp_dis_obj['likely'] = 'Highly Likely'
                    break
            if temp_dis_obj['likely'] == None:
                temp_dis_obj['likely'] = 'Not likely'
            if "PRIORITYM" in gender_group and "PRIORITYF" in gender_group:
                temp_dis_obj['priority'] = "Common in both Males and Females"
            elif "PRIORITYM" in gender_group:
                temp_dis_obj['priority'] = "More common in Males"
            elif "PRIORITYF" in gender_group:
                temp_dis_obj['priority'] = "More common in Females"

            if gender.upper() in gender_group:
                diseases_info.append(temp_dis_obj)
        return diseases_info
