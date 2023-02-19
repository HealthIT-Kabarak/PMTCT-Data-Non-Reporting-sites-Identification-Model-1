# -*- coding: utf-8 -*-
"""Copy of hackathon.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Y0_T7Q735rhYHxizti4bif_JLE0OjBpb
"""



import pandas as pd
import pandas as pd
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

hts_df = pd.read_excel('hst.xlsx')
pmtct_df = pd.read_excel('pmtct.xlsx')



# check if there are any duplicated rows
if hts_df.duplicated().sum() > 0:
    #print("Duplicated rows:")
    #print(hts_df[hts_df.duplicated()])
    # drop duplicates
    hts_df.drop_duplicates(inplace=True)

# check if there are any NaN values
if hts_df.isna().sum().sum() > 0:
    #print("Rows with NaN values:")
    #print(hts_df[hts_df.isna().any(axis=1)])
    # drop rows with NaN values
    hts_df.dropna(inplace=True)


# check if there are any duplicated rows
if pmtct_df.duplicated().sum() > 0:
    #print("Duplicated rows:")
    #print(pmtct_df[pmtct_df.duplicated()])
    # drop duplicates
    pmtct_df.drop_duplicates(inplace=True)

# check if there are any NaN values
if pmtct_df.isna().sum().sum() > 0:
    #print("Rows with NaN values:")
    #print(pmtct_df[pmtct_df.isna().any(axis=1)])
    # drop rows with NaN values
    pmtct_df.dropna(inplace=True)

mean_value = hts_df['datim_value'].mean()

#using mean value to replace missing values
hts_df['datim_value'].fillna(mean_value, inplace=True)
#dropping the missing values of other columns
hts_df1 = hts_df.dropna()
#print(hts_df1.isnull().sum())

#check for information concerning dataset
#print(hts_df1.info())

merged_df = pd.merge(hts_df, pmtct_df, on='facilityuid')

# check if there are any NaN values
if merged_df.isna().sum().sum() > 0:
    print("Rows with NaN values:")
    print(merged_df[merged_df.isna().any(axis=1)])
    # drop rows with NaN values
    merged_df.dropna(inplace=True)


# check if there are any duplicated rows
if merged_df.duplicated().sum() > 0:
    print("Duplicated rows:")
    print(merged_df[merged_df.duplicated()])
    # drop duplicates
    merged_df.drop_duplicates(inplace=True)



# Create target variable for classification - sites not reporting tests

merged_df['not_reporting_tests'] = 1 - merged_df['dhis2_value_y']
#merged_df["reported_tests"] = merged_df["khis_data"].apply(lambda x: 0 if x == 0 else 1)

#data = merged_df[['not_reporting_tests', 'some_other_features_you_need']]
merged_df.dropna(inplace =True)

# Select relevant features for classification
#features = ["khis_data","datim_data","dhis2_value","datim_value"]
features  = ['dhis2_value_y', 'datim_value_y','dhis2_value_x', 'datim_value_x']


# Create feature matrix and target variable
X = merged_df[features]
y = merged_df['not_reporting_tests']

# check if there are any NaN values in X or y
if X.isna().sum().sum() > 0 or y.isna().sum().sum() > 0:
    print("Rows with NaN values in X or y:")
    print(merged_df[X.isna().any(axis=1) | y.isna()])
    # drop rows with NaN values in X or y
    merged_df.dropna(inplace=True, subset=features+['not_reporting_tests'])

#print(merged_df.keys())

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,random_state=42)

# Create decision tree classifier
clf = DecisionTreeClassifier(random_state=42)

# Train the model

clf.fit(X_train, y_train)

# Export decision tree visualization to file

feature_names = [str(features[0]), str(features[1]),str(features[2]),str(features[3])]
class_names = sorted( y.unique())


class_name_str = [str(cls) for cls in class_names]

 # convert all class names to string
tree.export_graphviz(clf, out_file='pmtct-sample_data.dot', 
                     feature_names=feature_names,
                     class_names=class_name_str,
                     label='all',
                     rounded=True,
                     filled=True)

#joblib.dump(clf, 'pmtct-sample_data.joblib')
#Predict the target variable for the test set
y_pred = clf.predict(X_test)
# Evaluate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy:', accuracy)



"""# New Section

# New Section
"""

