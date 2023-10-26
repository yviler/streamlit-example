import streamlit as st
import os
import pandas as pd
import numpy as np
import nltk
import re
from nltk.corpus import stopwords
from gensim.models import Word2Vec
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.metrics import cohen_kappa_score
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import random
import multiprocessing
#%matplotlib widget
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

import time
import torch
import transformers as ppb
import warnings
import pandas as pd
from keras.models import load_model
from model import model_load

import sqlite3

def test_prediction(fileAddress, modelAddress, set, lang):

    dataset_path = fileAddress
    string_jawaban = pd.read_csv(dataset_path, sep="\t", encoding="ISO-8859-1")
    if lang==1:
      model_class, tokenizer_class, pretrained_weights = (ppb.BertModel, ppb.BertTokenizer, 'bert-base-uncased')
    else:
      model_class, tokenizer_class, pretrained_weights = (ppb.BertModel, ppb.BertTokenizer, 'cahya/bert-base-indonesian-1.5G')
    tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
    model = model_class.from_pretrained(pretrained_weights)
    cuda = torch.device('cuda')

    tokenisasi = string_jawaban['essay']

    sentences = []
    tokenize_sentences = []
    train_bert_embeddings = []


    tokenized_test = tokenisasi.apply((lambda x: tokenizer.encode(x, add_special_tokens=True ,max_length=512, truncation=True)))

    max_len = 0
    for i in tokenized_test.values:
        if len(i) > max_len:
            max_len = len(i)
    padded_test = np.array([i + [0]*(max_len-len(i)) for i in tokenized_test.values])
    attention_mask_test = np.where(padded_test != 0, 1, 0)
    test_input_ids = torch.tensor(padded_test)
    test_attention_mask = torch.tensor(attention_mask_test)

    with torch.no_grad():
        last_hidden_states_test = model(test_input_ids, attention_mask=test_attention_mask)
    test_features = last_hidden_states_test[0][:,0,:].numpy()

    test_x,test_y = test_features.shape

    testDataVectors = np.reshape(test_features,(test_x,1,test_y))


    #lstm_model = get_model(bidirectional=True)
    #modelAddress="aes_model_"+nama_model+set_problem+".h5"
    #st.write("ADDRESS:",modelAddress)
    
    bilstm_model = load_model(modelAddress)
    bilstm_model.load_weights(modelAddress)
    preds = bilstm_model.predict(testDataVectors)

    prediction_value = int(np.around(preds))

    return prediction_value

#execute program
#if __name__ == '__main__':

def scoring(conn, jawaban_student, selected_course, selected_task, selected_problem, language):
  model_address = model_load(conn, selected_course, selected_task, selected_problem)
    
  warnings.filterwarnings('ignore')
  set_count = 1
  all_sets_score = []

  # creating some sample data
  sample = {
          'set': ['1'],
          'essay': [jawaban_student]
          }

  # print (jawaban_student)
  # creating the DataFrame
  df = pd.DataFrame(sample)


  # displaying the DataFrame

  df.to_csv('test_answer.csv', sep="\t")
  #modelAddress='/content/gdrive/MyDrive/Asset/aesindo-bert-bilstm1_1.h5'
  test_address='test_answer.csv'

  predscore = test_prediction(test_address,model_address, 1, language)
  #st.write("\nJawaban Mahasiswa:", jawaban_student)
  #st.write("\nPredictions Score:", predscore)

  # creating some sample data
  sample2 = {
          'set': ['1'],
          'score': [predscore]
          }
  df2 = pd.DataFrame(sample2)
  df2.to_csv('prediction_score.csv', sep="\t")
  #st.write('Skor sudah tersimpan ke dalam bentuk csv')
  return predscore
