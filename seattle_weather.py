# -*- coding: utf-8 -*-
"""Seattle-weather.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1a1M4JmaQSuuolJ0hiBcBBjKTMGwLsiWp
"""

import pandas as pd #Used for data manipulation and analysis.
import numpy as np #numerical computations and array manipulation
import matplotlib.pyplot as plt #creating visualizations like line plots, bar plots, scatter plots
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler #Scaled Value= (Value−Min)/(Max−Min)
from sklearn.preprocessing import StandardScaler #z-score
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler #z-score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

df=pd.read_csv("/content/seattle-weather.csv")

df.head()

df.tail() #last 5 rows

print("Column names:")
print(df.columns)

print("\nData statistics:")
print(df.describe())

print("\nData Info:")
print(df.info())

print("\nMissing values:")
print(df.isnull().sum()) #used to find and display the count of missing (null) values

#convert the 'date' column in a df into datetime format and then display the DataFrame.
df['date'] = pd.to_datetime(df['date'])
print(df['date'])

df.nunique()

plt.figure(figsize=(10,5))
sns.set_theme(style="whitegrid")
sns.countplot(x='weather', data=df, palette="ch:start=.8,rot=-.8")
plt.xlabel("weather", fontweight='bold', size=13)
plt.ylabel("Count", fontweight='bold', size=13)
plt.show()

plt.figure(figsize=(10, 5)) #figure size
sns.boxplot(data=df)
plt.title('Boxplot of Weather Attributes')
plt.xticks(rotation=0) #rotates the labels on the x-axis by 45 degrees
plt.show()

sns.pairplot(df) #pairplot(scatterplot)
plt.title('Pairplot of Weather Attributes')
plt.show()

fig, axes = plt.subplots(2, 2, figsize=(10, 5))

fig.suptitle('Price Range vs all numerical factor')

sns.scatterplot(ax=axes[0, 0], data=df, x='weather', y='precipitation')
sns.scatterplot(ax=axes[0, 1], data=df, x='weather', y='temp_max')
sns.scatterplot(ax=axes[1, 0], data=df, x='weather', y='temp_min')
sns.scatterplot(ax=axes[1, 1], data=df, x='weather', y='wind')
plt.show()

def LABEL_ENCODING(c1):
    from sklearn import preprocessing
    label_encoder = preprocessing.LabelEncoder() # convert categorical data into numerical labels.
    df[c1]= label_encoder.fit_transform(df[c1])
    df[c1].unique() #unique numerical labels in the column after encoding
LABEL_ENCODING("weather")

df

df = df.drop('date',axis=1) #remove date column and no. of columns to drop

df

x = df.drop('weather',axis=1)
print(x)
y = df['weather']

df

inertias = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42,  n_init=10)
    kmeans.fit(df)
    inertias.append(kmeans.inertia_)

plt.figure(figsize=(8, 6))
plt.plot(range(1, 11), inertias, marker='o')
plt.xlabel('Cluster')
plt.ylabel('Inersia')
plt.title('Elbow Method')
plt.show()

scaler = StandardScaler()
scaled_features = scaler.fit_transform(df)

n_clusters = 5

kmeans = KMeans(n_clusters=n_clusters, random_state=42,  n_init=10)
df['cluster'] = kmeans.fit_predict(scaled_features)

df.to_csv('data_iit.csv', index=False)

df_clean = pd.read_csv("data_iit.csv")
df_clean.head(100)

print(df)
X = df.drop(['cluster'], axis=1)
print(X)
y = df['cluster']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)

import time
start_time = time.time()

knn = KNeighborsClassifier()

param_grid = {'n_neighbors': [3, 5, 7, 9], 'weights': ['uniform', 'distance'], 'metric': ['euclidean', 'manhattan']}
grid_search = GridSearchCV(knn, param_grid, cv=4)
grid_search.fit(X_train, y_train)

print("Best Parameter", grid_search.best_params_)

best_knn = grid_search.best_estimator_

best_knn.fit(X_train, y_train)
y_pred = best_knn.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

precision = precision_score(y_test, y_pred, average='weighted')
print("Precicion:", precision)

recall = recall_score(y_test, y_pred, average='weighted')
print("Recall:", recall)

f1 = f1_score(y_test, y_pred, average='weighted')
print("F1 Score:", f1)

end_time = time.time()

process_time = end_time - start_time

print(f"Time run: {process_time} second")