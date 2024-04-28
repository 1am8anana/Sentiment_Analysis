# -*- coding: utf-8 -*-
"""Preprocess.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MxEVB9A5HZmfGwzDU7eDNkKyR7ZKidkP

**Import Library for preprocessing**
"""

import pandas as pd
import numpy as np

"""**Load the Dataset that i just prepared**"""

tcas = pd.read_csv('C:/Users/tarza\OneDrive/Desktop/Sentiment_Analysis/Dataset/tcas_prepared.csv')
shopping = pd.read_csv('C:/Users/tarza\OneDrive/Desktop/Sentiment_Analysis/Dataset/shopping_prepared.csv')
general = pd.read_csv('C:/Users/tarza\OneDrive/Desktop/Sentiment_Analysis/Dataset/general_prepared.csv')

"""# **Data Preprocessing**"""

sentiment_label = {'neg': 0, 'pos': 1}
tcas['sentiment'] = tcas['label'].map(sentiment_label)
shopping['sentiment'] = shopping['label'].map(sentiment_label)
general['sentiment'] = general['label'].map(sentiment_label)

"""Combine 3 dataframes for model experiment (after this process)"""

combined_df = pd.concat([tcas, shopping, general], ignore_index=True)
len(combined_df['sentence'])

"""Import PyThaiNLP for preprocessing Thai Dataset"""

from pythainlp.corpus.common import thai_stopwords
from pythainlp import word_tokenize
import string

"""Instantiate Stopwords(thai) and punctuation"""

stopwords_thai = list(thai_stopwords())
pun = string.punctuation+'ๆ'+'ฯ'

def process_sentence(sentence):
    sentence_clean = "".join(u for u in sentence if u not in pun)
    sentence_clean = word_tokenize(sentence_clean)
    sentence_clean = " ".join(word for word in sentence_clean)
    sentence_clean = " ".join(word for word in sentence_clean.split() if word.lower not in stopwords_thai)
    return sentence_clean

tcas['text_tokens'] = tcas['sentence'].apply(process_sentence)
combined_df['text_tokens'] = combined_df['sentence'].apply(process_sentence)

"""Split each data for:

    * train set = 80
    * validation set = 20
"""

# features and target of tcas dataset
Xtcas = tcas[['text_tokens']]
ytcas = tcas['sentiment']

# features and target of combined dataset
Xdf = combined_df[['text_tokens']]
ydf = combined_df['sentiment']

from sklearn.model_selection import cross_val_score, train_test_split

Xtcas_train, Xtcas_test, ytcas_train, ytcas_test = train_test_split(Xtcas, ytcas, test_size=0.2, random_state=42)
Xdf_train, Xdf_test, ydf_train, ydf_test = train_test_split(Xdf, ydf, test_size=0.2, random_state=42)

"""Import CountVectorizer for counting my vectors"""

from sklearn.feature_extraction.text import CountVectorizer

cvec_tcas = CountVectorizer(analyzer=lambda x:x.split(' '))
cvec_tcas.fit_transform(Xtcas_train['text_tokens'])

cvec_df = CountVectorizer(analyzer=lambda x:x.split(' '))
cvec_df.fit_transform(Xdf_train['text_tokens'])

cvec_df.vocabulary_

BOWtcas_train = cvec_tcas.transform(Xtcas_train['text_tokens'])
BOWtcas_test = cvec_tcas.transform(Xtcas_test['text_tokens'])
BOWdf_train = cvec_df.transform(Xdf_train['text_tokens'])
BOWdf_test = cvec_df.transform(Xdf_test['text_tokens'])

def n1_process(sentence):
    # Tokens
    clean = process_sentence(sentence)
    if not isinstance(clean, str):
        raise ValueError("Processed sentence is not a string.")
    # BOW
    BOW_sentence = cvec_tcas.transform([clean])
    return BOW_sentence

def n2_process(sentence):
    # Tokens
    clean = process_sentence(sentence)
    if not isinstance(clean, str):
        raise ValueError("Processed sentence is not a string.")
    
    # BOW
    BOW_sentence = cvec_df.transform([clean])  # Pass the processed sentence as a list
    return BOW_sentence

print(n1_process("สวัสดีครับ"))