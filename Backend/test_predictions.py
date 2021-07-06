from random import randint
import unittest
import json
import os
import logging
from Chatbot.chatbot import chat_test, chat
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').disabled = True


class Prediction(unittest.TestCase):

    def setUp(self):
        with open('static/Dataset/final_dis_symp.json', 'r') as f:
            self.dis_symp = json.load(f)
        with open('static/Dataset/test_intent.json', 'r') as f:
            self.chat_json = json.load(f)
        self.request_json = {}
        self.request_json['name'] = 'Tatya'
        self.request_json['age'] = 30
        self.request_json['gender'] = 'Male'
        self.request_json['predict'] = 1

    def _check_equal(self, prediction, expected):
        if prediction == expected:
            return True
        return False

    def _check_accuracy(self, disease_name, symptoms):
        match_cnt = 0
        for i in range(100):
            symptoms[i] = list(map(lambda k: k.lower(), symptoms[i]))
            self.request_json['text'] = symptoms[i]
            response_obj = chat(self.request_json)
            if response_obj['diseases_list'] != None:
                disease_predicted = response_obj['diseases_list'][0]['disease_name']
                if self._check_equal(disease_predicted.lower(), disease_name[i].lower()):
                    match_cnt += 1
        return match_cnt

    def _loop_over(self, diseases, random_index, n=0):
        symptoms = []
        disease_name = []
        for i in range(100):
            disease = diseases[random_index]
            disease_name.append(disease)
            if n != 0:
                symptoms.append(self.dis_symp[disease][:n])
            else:
                symptoms.append(self.dis_symp[disease])

            random_index = (random_index + 5) % 407
        return self._check_accuracy(disease_name, symptoms)

    def test_symptoms(self):
        random_index = randint(0, 408)
        diseases = list(self.dis_symp.keys())
        one = self._loop_over(diseases, random_index)
        two = self._loop_over(diseases, random_index+1)
        three = self._loop_over(diseases, random_index+2)
        print("Predictions Accuracy:", str((one+two+three)/3)+'%')

    def test_reduce_symptoms(self):
        random_index = randint(0, 408)
        diseases = list(self.dis_symp.keys())
        one = self._loop_over(diseases, random_index, -2)
        two = self._loop_over(diseases, random_index+1, -2)
        three = self._loop_over(diseases, random_index+2, -2)
        print("Prediction on Reduced Symptoms Accuracy:",
              str((one+two+three)/3)+'%')

    def test_chatbot(self):
        match_cnt = 0
        for obj in self.chat_json['intents']:
            for text in obj['text']:
                intent = chat_test(text)
                if self._check_equal(intent[0]['intent'], obj['intent']):
                    match_cnt += 1
        print("Chatbot Testing Accuracy:", str((match_cnt*100)/35)+'%')


if __name__ == '__main__':
    unittest.main()
