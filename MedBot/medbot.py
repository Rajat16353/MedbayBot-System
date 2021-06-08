import nltk
import operator
import pandas as pd
# import warnings
import pandas as pd
import re
import pickle

from collections import Counter
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

# warnings.simplefilter("ignore")
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')

with open('static/Models/norm_model.pkl', 'rb') as f:
    NORM_MODEL = pickle.load(f)


def mb_get_symptoms(user_symptoms):
    medBot = Medbot()
    symptoms_list = medBot.get_symptoms(user_symptoms)
    del medBot
    return symptoms_list


def mb_get_cooccuring_symptoms(selected_symptoms, skip_symptoms):
    medBot = Medbot()
    cooccuring_symptoms_list = medBot.get_cooccuring_symptoms(
        selected_symptoms, skip_symptoms)
    del medBot
    return cooccuring_symptoms_list


def mb_get_predicted_diseases(selected_symptoms):
    medBot = Medbot()
    predicted_diseases_list = medBot.get_predicted_diseases(selected_symptoms)
    del medBot
    return predicted_diseases_list


class Medbot:

    def __init__(self):
        self.STOPWORDS = stopwords.words('english')
        self.lemmatizer = WordNetLemmatizer()
        self.splitter = RegexpTokenizer(r'\w+')
        self.df_norm = pd.read_csv("static/Dataset/dis_sym_dataset_norm.csv")
        self.X_NORM = self.df_norm.iloc[:, 1:]
        self.Y_NORM = self.df_norm.iloc[:, 0:1]
        self.DATASET_SYMPTOMS = list(self.X_NORM.columns)
        self.DISEASES = sorted(list(set(self.Y_NORM['label_dis'])))
        self.final_symp = []
        self.EXCEPTION_WORDS = []

    def get_wordnet_pos(self, word):
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}

        return tag_dict.get(tag, wordnet.NOUN)

    def pre_process_input(self, user_symptoms):
        user_symptoms = user_symptoms.lower().split()
        symptoms = ''
        for symptom in user_symptoms:
            if symptom not in self.STOPWORDS and symptom not in self.EXCEPTION_WORDS:
                symptoms += symptom + ' '
        return symptoms.split(',')

    def process_user_symptoms(self, user_symptoms):
        user_symptoms = self.pre_process_input(user_symptoms)
        processed_user_symptoms = []
        for sym in user_symptoms:
            sym = sym.strip()
            sym = sym.replace('-', ' ')
            sym = sym.replace("'", '')
            sym = ' '.join([self.lemmatizer.lemmatize(word, self.get_wordnet_pos(word))
                            for word in self.splitter.tokenize(sym) if word not in self.STOPWORDS and not word[0].isdigit()])

            processed_user_symptoms.append(sym)
        return processed_user_symptoms

    def match_user_symptoms(self, user_symptoms):
        found_symptoms = set()
        for data_sym in self.DATASET_SYMPTOMS:
            for user_sym in user_symptoms:
                word_match_count = 0
                for sym_word in user_sym.split():
                    if re.search(sym_word, data_sym) != None:
                        word_match_count += 1
                if word_match_count == len(user_sym.split()):
                    found_symptoms.add(data_sym)
        return list(found_symptoms)

    def predict_disease(self, limit, selected_symptoms):
        sample_x = [0 for x in range(0, len(self.DATASET_SYMPTOMS))]
        for symptom in selected_symptoms:
            sample_x[self.DATASET_SYMPTOMS.index(symptom)] = 1
        prediction = NORM_MODEL.predict_proba([sample_x])
        return prediction[0].argsort()[-(limit):][::-1]

    def get_common_symptoms(self, top_10_diseases, selected_symptoms, skip_symptoms):
        match_symp = []
        for idx, index in enumerate(top_10_diseases):
            row = self.df_norm.loc[self.df_norm['label_dis']
                                   == self.DISEASES[index]].values.tolist()
            row[0].pop(0)
            for idx, val in enumerate(row[0]):
                if val != 0 and self.DATASET_SYMPTOMS[idx] not in selected_symptoms and self.DATASET_SYMPTOMS[idx] not in skip_symptoms:
                    match_symp.append(self.DATASET_SYMPTOMS[idx])
        if len(match_symp) == 0:
            return match_symp
        return Counter(match_symp)

    def get_symptoms_dict(self, dict_symp):
        symp_dictionary = {}
        symp_dictionary['co_occuring'] = []
        dict_symp_tup = sorted(
            dict_symp.items(), key=operator.itemgetter(1), reverse=True)
        for obj in dict_symp_tup:
            temp_dict = {}
            temp_dict['symptom'] = obj[0]
            temp_dict['frequency'] = obj[1]
            symp_dictionary['co_occuring'].append(temp_dict)
        return symp_dictionary

    def calculate_probability(self, selected_symptoms, disease_index):
        disease_dict = {}
        for index in disease_index:
            dis_symptoms = set()
            row = self.df_norm.loc[self.df_norm['label_dis']
                                   == self.DISEASES[index]].values.tolist()
            row[0].pop(0)
            for idx, val in enumerate(row[0]):
                if val != 0:
                    dis_symptoms.add(self.DATASET_SYMPTOMS[idx])
            prob = len(set(selected_symptoms).intersection(
                dis_symptoms))/len(dis_symptoms)
            prob = round(prob*100, 2)
            disease_dict[self.DISEASES[index]] = prob
        disease_tup = sorted(disease_dict.items(),
                             key=lambda val: val[1], reverse=True)
        # for tuple in disease_tup:
        #     print(tuple)
        return disease_tup

    def get_symptoms(self, user_symptoms):
        user_symptoms = self.process_user_symptoms(user_symptoms)
        found_symptoms = self.match_user_symptoms(user_symptoms)
        return found_symptoms

    def get_cooccuring_symptoms(self, selected_symptoms, skip_symptoms):
        top_10_diseases = self.predict_disease(10, selected_symptoms)
        match_symp = self.get_common_symptoms(
            top_10_diseases, selected_symptoms, skip_symptoms)
        return self.get_symptoms_dict(match_symp)

    def get_predicted_diseases(self, selected_symptoms):
        top_5_diseases = self.predict_disease(5, selected_symptoms)
        return self.calculate_probability(selected_symptoms, top_5_diseases)
