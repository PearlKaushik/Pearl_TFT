# -*- coding: utf-8 -*-
"""WeatherPrediction_LSTM.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vlmM4QF1Gw9fXhvHin9bs08bA6SAXRHC
"""

import pandas as pd #Used for data manipulation and analysis.
import numpy as np #numerical computations and array manipulation
import matplotlib.pyplot as plt #creating visualizations like line plots, bar plots, scatter plots
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, MinMaxScaler #Scaled Value= (Value−Min)/(Max−Min)
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential #allows you to build neural networks layer by layer
from tensorflow.keras.layers import LSTM, Dense, Dropout #Dense layer (fully connected layer) ,Dropout layer (used to prevent overfitting)
from tensorflow.keras.callbacks import EarlyStopping #stops training when the model stops improving

df=pd.read_csv("/content/seattle-weather.csv")

df

print("Column names:")
print(df.columns)

print("\nData statistics:")
print(df.describe())

print("\nMissing values:")
print(df.isnull().sum())

df['date'] = pd.to_datetime(df['date'])
df

label_encoder = LabelEncoder() # categorical to numeric values (weather is encoded)
df['weather_encoded'] = label_encoder.fit_transform(df['weather'])
df

df = df.drop(['weather', 'date'], axis=1)
df

scaler = MinMaxScaler()  #scaled = (x−min)/(max−min)
scaled_data = scaler.fit_transform(df) #scales the values in df to a range of 0 to 1
print(scaled_data)
print(scaled_data.shape)

sequence_length = 30  # Use the past 30 days to predict the next value
X = []
y = []
print(len(scaled_data))
print(type(scaled_data))
print(scaled_data.shape)

for i in range(sequence_length,len(scaled_data)): #30 to 1461
    X.append(scaled_data[i-sequence_length:i])  # Past 30 days
    #print(len(X))
    y.append(scaled_data[i, -1])      # Target is the last column (weather_encoded)
print(len(X))
print(len(y))

X, y = np.array(X), np.array(y) #converts list x and y into numpy
print(X.shape)
print(y.shape)
print(scaled_data)

#random_state- produces the same result each time I run the code
# and test and train data will be same
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print(type(scaled_data))
print(scaled_data.shape)
print(X_train.shape)
model = Sequential([
    #50 neurons, return_seq-The LSTM returns o/p at each step
    LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
    Dropout(0.2),# randomly sets 20% of the input units to 0 during training to prevent overfitting
    LSTM(50, return_sequences=False), #LSTM returns final o/p not at each step
    Dropout(0.2),
    Dense(25, activation='relu'),
    Dense(1, activation='linear')
])

# Adam(Adaptive Moment Estimation)-
# adjusts the learning rate based on the gradients and helping the model converge faster
model.compile(optimizer='adam', loss='mse') #smaller the mse,better the performance of model

early_stopping = EarlyStopping(
    monitor='val_loss', #Checks the model's error on validation data
    patience=10, #stops training if model performance doesnot improve for 10 consecutive epochs
    restore_best_weights=True)#Saves the best model result

# Train
history = model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=32,
    validation_data=(X_test, y_test), #evaluate model's performance
    callbacks=[early_stopping], #training will stop early if the model's performance doesn't improve
    verbose=1 #shows progress during training, including details like the loss value after each epoch
)

# Evaluate the model
loss = model.evaluate(X_test, y_test,
                      verbose=0)# no data to be visible
print(f"Test Loss: {loss:.4f}")

# Plot training history
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.title('Training and Validation Loss')
plt.show()

# Make predictions
predictions = model.predict(X_test)

# Inverse transform the scaled data for interpretation
predictions = scaler.inverse_transform(np.hstack((np.zeros((predictions.shape[0], df.shape[1]-1)), predictions.reshape(-1, 1))))[:, -1]
y_test_actual = scaler.inverse_transform(np.hstack((np.zeros((y_test.shape[0], df.shape[1]-1)), y_test.reshape(-1, 1))))[:, -1]

# Plot the predictions vs actual values
plt.figure(figsize=(10, 6))
plt.plot(y_test_actual, label='Actual')
plt.plot(predictions, label='Predicted')
plt.legend()
plt.title('Predictions vs Actual Values')
plt.show()