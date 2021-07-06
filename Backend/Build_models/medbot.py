import warnings
import pandas as pd
import pickle

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
# from sklearn.externals import joblib

warnings.simplefilter("ignore")

# Load Dataset scraped from NHS inform (https://www.nhsinform.scot/illnesses-and-conditions/a-to-z) & Wikipedia
# Scrapping and creation of dataset csv is done in a separate program
# Individual Disease
df_norm = pd.read_csv("static/Dataset/dis_sym_dataset_norm.csv")

X_norm = df_norm.iloc[:, 1:]
Y_norm = df_norm.iloc[:, 0:1]

"""Using **Logistic Regression (LR) Classifier** as it gives better accuracy compared to other classification models as observed in the comparison of model accuracies in Model_latest.py
Cross validation is done on dataset with cv = 5
"""

model = LogisticRegression()
model = model.fit(X_norm, Y_norm)

filename = 'norm_model.pkl'
pickle.dump(model, open("static/Models/"+filename, 'wb'))

print('Models created and saved successfully')
