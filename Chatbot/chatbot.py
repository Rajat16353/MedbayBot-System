import random
import json
import re
import numpy as np
import pickle
import os
import nltk
import logging
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
from datetime import datetime

from MedBot.medbot import mb_get_symptoms, mb_get_cooccuring_symptoms, mb_get_predicted_diseases
from MedBot.age_gender import check_age_and_gender
from DrugInfo.drug import drug_interface
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').disabled = True


def chat(request_json):
    chatbot = Chatbot()
    response_json = chatbot.chat(request_json)
    del chatbot
    return response_json


def chat_test(text):
    chatbot = Chatbot()
    intent = chatbot.chat_test(text)
    del chatbot
    return intent


class Chatbot:

    def __init__(self):
        self.response_json = {}
        self.lemmatizer = WordNetLemmatizer()
        self.model = load_model('static/Models/chatbot_model.h5')
        with open('static/Dataset/intent.json', 'r') as f:
            self.INTENTS = json.load(f)
        with open('static/Dataset/words.pkl', 'rb') as f:
            self.WORDS = pickle.load(f)
        with open('static/Dataset/classes.pkl', 'rb') as f:
            self.CLASS = pickle.load(f)
        self.response_json['response'] = None
        self.response_json['found_symptoms'] = None
        self.response_json['diseases_list'] = None
        self.response_json['final_symptoms'] = None
        self.response_json['co_occuring'] = None
        self.response_json['error'] = None
        self.response_json['name'] = None
        self.response_json['age'] = None
        self.response_json['gender'] = None
        self.response_json['gender_query'] = None
        self.response_json['drug_info_flag'] = None
        self.response_json['drug_list'] = None
        self.time = datetime.now().strftime("%H:%M")
        self.day = datetime.now().strftime("%A")
        self.date = datetime.now().strftime("%B %d, %Y")

    def exception_raised(self, exception):
        self.response_json['error'] = exception
        return self.response_json

    def extract_name(self, text):
        words = nltk.word_tokenize(text)
        words = list(map(lambda k: k.capitalize(), words))
        pos_tags = nltk.pos_tag(words)
        chunks = nltk.ne_chunk(pos_tags, binary=True)
        print(chunks)
        name = ''
        for chunk in chunks:
            if isinstance(chunk, nltk.tree.Tree):
                for tup in chunk:
                    name += ' ' + tup[0]
        return name.strip()

    def extract_age(self, text):
        words = text.split()
        for word in words:
            word = re.sub(',', '', word)
            if word.isdigit():
                age = int(word)
        return age

    def clean_up_sentence(self, sentence):
        # tokenize the pattern - split words into array
        sentence_words = nltk.word_tokenize(sentence)
        # stem each word - create short form for word
        sentence_words = [self.lemmatizer.lemmatize(
            word.lower()) for word in sentence_words]
        return sentence_words
    # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

    def bag_of_words(self, sentence, show_details=True):
        sentence_words = self.clean_up_sentence(sentence)
        # bag of words - matrix of N words, vocabulary matrix
        bag = [0]*len(self.WORDS)
        for s in sentence_words:
            for i, w in enumerate(self.WORDS):
                if w == s:
                    # assign 1 if current word is in the vocabulary position
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)
        return(np.array(bag))

    def predict_class(self, sentence):
        # filter out predictions below a threshold
        p = self.bag_of_words(sentence, show_details=False)
        res = self.model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append(
                {"intent": self.CLASS[r[0]], "probability": str(r[1])})
        return return_list

    def get_response(self, intent):
        tag = intent[0]['intent']
        list_of_intents = self.INTENTS['intents']
        for i in list_of_intents:
            if(i['intent'] == tag):
                result = random.choice(i['responses'])
                break
        return result

    def get_symptoms(self, request_json):
        self.response_json['found_symptoms'] = mb_get_symptoms(
            request_json['text'])
        if request_json['name'] != None and request_json['age'] != None and request_json['gender'] != None:
            pass
        else:
            self.response_json['response'], intent = self.chatbot_response(
                'prediction without user details')
            return self.response_json
        if self.response_json['found_symptoms'] == []:
            self.response_json['found_symptoms'] == None
            self.response_json['response'] = "Sorry!! I couldn't find the symptoms in my database"
        return self.response_json

    def get_final_symptoms(self, request_json):
        list_symp_tup = mb_get_cooccuring_symptoms(
            request_json['text'], request_json['skip_symptoms'])
        self.response_json['co_occuring'] = list_symp_tup['co_occuring']
        if self.response_json['co_occuring'] == []:
            self.response_json['response'] = "Sorry, But I couldn't find anymore symptoms"
            return self.response_json
        if len(self.response_json['co_occuring']) == 1:
            for i in range(len(self.response_json['response'])):
                if self.response_json['response'][i].find("<symptom>") != -1:
                    self.response_json['response'][i] = 'Are you also experiencing <symptom>'
                    break
        for symp in list_symp_tup['co_occuring'][:2]:
            for i in range(len(self.response_json['response'])):
                if self.response_json['response'][i].find("<symptom>") != -1:
                    self.response_json['response'][i] = self.response_json['response'][i].replace(
                        "<symptom>", symp['symptom'], 1)
                self.response_json['response'][i] = self.replace_variables(
                    self.response_json['response'][i], request_json)
        return self.response_json

    def get_predicted_disease(self, request_json):
        diseases_list = mb_get_predicted_diseases(
            request_json['text'])
        self.response_json['response'], intent = self.chatbot_response(
            'Final Disease prediction done')
        self.response_json['diseases_list'] = check_age_and_gender(
            diseases_list, request_json['age'], request_json['gender'])
        if self.response_json['diseases_list'] == []:
            self.response_json['diseases_list'] = None
            self.response_json['response'] = "I couldn't find any disease matching the symptoms you provided in my database"
        return self.response_json

    def chatbot_response(self, text):
        intent = self.predict_class(text)
        res = self.get_response(intent)
        return res, intent

    def replace_variables(self, res, request_json):
        if res.find("<HUMAN>") != -1 or res.find("<AGE>") != -1 or res.find("<GENDER>") != -1:
            if request_json['name'] != None:
                res = res.replace("<HUMAN>", request_json['name'])
                if res.find("<AGE>") != -1:
                    res = res.replace("<AGE>", str(request_json['age']))
                elif res.find("<GENDER>") != -1:
                    res = res.replace("<GENDER>", request_json['gender'])
            else:
                res, intent = self.chatbot_response(
                    'user details not provided')
                return res
        elif res.find("<TIME>") != -1:
            res = res.replace("<TIME>", self.time)
        elif res.find("<DAY>") != -1:
            res = res.replace("<DAY>", self.day)
        elif res.find("<DATE>") != -1:
            res = res.replace("<DATE>", self.date)
        return res

    def get_validated_response(self, request_json):
        res, intent = self.chatbot_response(request_json['text'])
        if intent[0]["intent"] == 'NameResponse':
            request_json['name'] = self.extract_name(request_json['text'])
            self.response_json['name'] = request_json['name']
        if intent[0]["intent"] == 'GetAge':
            request_json['age'] = self.extract_age(request_json['text'])
            self.response_json['age'] = request_json['age']
            self.response_json['gender_query'] = ["Male", "Female"]
        # if request_json['text'].isdigit():
        #     request_json['age'] = self.extract_age(request_json['text'])
        #     self.response_json['age'] = request_json['age']
        #     self.response_json['gender_query'] = ["Male", "Female"]
        #     res, intent = self.chatbot_response('I am 12 years old')
        if intent[0]["intent"] == 'GenderCheck':
            request_json['gender'] = request_json['text']
            self.response_json['gender'] = request_json['gender']
        if isinstance(res, str):
            res = self.replace_variables(res, request_json)
        else:
            for i in range(len(res)):
                res[i] = self.replace_variables(res[i], request_json)
        return res, intent

    def chat(self, request_json):
        if isinstance(request_json['text'], str):
            self.response_json['response'], intent = self.get_validated_response(
                request_json)
        else:
            text = "get the co-occuring symptoms"
            self.response_json['response'], intent = self.chatbot_response(
                text)
        if intent[0]["intent"] == "DrugInfo" or 'drug_name' in request_json.keys() or 'selected_drug_link' in request_json.keys():
            self.response_json['drug_info_flag'] = True
            if request_json['text'] == '':
                response_list = drug_interface(request_json)
                self.response_json['drug_list'] = response_list
                self.response_json['response'] = None

            return self.response_json
        elif intent[0]["intent"] == "FindDisease":
            return self.get_symptoms(request_json)
        elif intent[0]["intent"] == "AdditionalSymptoms":
            if 'predict' in request_json.keys():
                if request_json['predict'] != False:
                    return self.get_predicted_disease(request_json)
            else:
                return self.exception_raised('Predict: value not set')
            return self.get_final_symptoms(request_json)
        print(self.response_json)
        return self.response_json

    def chat_test(self, text):
        return self.predict_class(text)
