import json
import pandas as pd

with open('static/Dataset/final_dis_symp.json') as f:
    final_dis = json.load(f)

symp_list = []
for key, values in final_dis.items():
    for symptom in values:
        if symptom.lower() not in symp_list:
            symp_list.append(symptom.lower())

symp_list = sorted(symp_list)
# for id, symptom in enumerate(symp_list):
#     print(id, symptom)

symp_list = ['label_dis'] + symp_list
print(len(symp_list))

df_norm = pd.DataFrame(columns=symp_list)

# Read each disease and symptom list, convert into dictionary and add to dataframe
for key, values in final_dis.items():
    key = str.encode(key).decode('utf-8')
    row_norm = dict({x: 0 for x in symp_list})
    for sym in values:
        row_norm[sym.lower()] = 1
    row_norm['label_dis'] = key

    df_norm = df_norm.append(pd.Series(row_norm), ignore_index=True)

print(df_norm.shape)

# Export the dataset into CSV files
# df_comb.to_csv("/content/drive/MyDrive/MedBayBot/dis_sym_dataset_comb_v2.csv",index=None)
df_norm.to_csv("static/Dataset/dis_sym_dataset_norm.csv", index=None)

# Export disease symptoms into TXT file for better visibility
with open('static/Dataset/dis_symp_dict.txt', 'w') as f:
    for key, value in final_dis.items():
        print([key]+value, file=f)
print("done")
