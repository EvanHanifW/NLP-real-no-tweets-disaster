# -*- coding: utf-8 -*-
"""Project 1 - Evan Hanif Widiatama.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DIPhqQxq4fWOMtVJyQ875lIPt4jkcIGd
"""

import pandas as pd
df = pd.read_csv('tweets.csv')
df.info()

df.head() #Deskripsi dataset

df = df.drop(columns=['id', 'keyword', 'location'], axis=1) #menghapus kolom id, keyword, dan location karena tidak digunakan untuk analisis

text = df['text'].values #menggunakan kolom teks untuk atribut lalu mengubahnya ke np array
label = df['target'].values #menggunakan kolom target untuk label lalu mengubahnya ke np array

import re

df['text'] = df['text'].map(lambda x: re.sub(r'\W+', ' ', x)) #menghapus special karakter

from sklearn.model_selection import train_test_split

text_train, text_test, label_train, label_test = train_test_split(text, label, test_size=0.2) #split train dan test sebanyak 0.2 untuk test data

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

tokenizer = Tokenizer(num_words=5000, oov_token='x')
tokenizer.fit_on_texts(text_train)
tokenizer.fit_on_texts(text_test)

sekuens_train = tokenizer.texts_to_sequences(text_train)
sekuens_test = tokenizer.texts_to_sequences(text_test)
 
padded_train = pad_sequences(sekuens_train) 
padded_test = pad_sequences(sekuens_test)

import tensorflow as tf
from tensorflow.keras.layers import LSTM,Dense,Embedding,Dropout
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=5000, output_dim=16),
    tf.keras.layers.LSTM(64),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    Dropout(0.5),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy')>0.98 and logs.get('val_accuracy')>0.98):
      print("\nAkurasi train dan validasi didapat telah mencapai nilai > 98%!")
      self.model.stop_training = True
callbacks = myCallback() #membuat callback

num_epochs = 30
history = model.fit(padded_train, label_train, epochs=num_epochs, validation_data=(padded_test, label_test), verbose=2, callbacks=[callbacks])

import matplotlib.pyplot as plt

# Plot Accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Akurasi Model')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# Plot Loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Loss Model')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()