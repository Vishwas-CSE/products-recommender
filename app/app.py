#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 19:15:32 2021

@author: vishwas
"""
import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import json

# load the nlp model and tfidf vectorizer from disk
filename = 'data/product_sentiment_model.pkl'
clf = pickle.load(open(filename, 'rb'))
vectorizer = pickle.load(open('data/tfidf_vectorizer.pkl', 'rb'))

def get_data():
    data = pd.read_csv('data/final_data.csv')
    return data


def create_sim():
    data = get_data()
    # creating a count matrix
    cv = CountVectorizer()
    print(data['clean_text'])
    data = data[~(data['clean_text'].isnull())]
    print(data['clean_text'].isna().sum())
    count_matrix = cv.fit_transform(data['clean_text'])
    # creating a similarity score matrix
    sim = cosine_similarity(count_matrix)
    return data, sim


def get_reviews(product_name):
    data = get_data()
    reviews = data[data['name'] == product_name]['reviews_text']
    return reviews


def get_recommendations(user_name):
    # user_name = user_name.lower()
    data = get_data()
    try:
        data, sim = create_sim()
        data.head()
        sim.shape
    except Exception as ex:
        print("Exception occured")
        raise ex

    if user_name not in data['reviews_username'].unique():
        return (
            'Sorry! The user you searched is not in our database. Please check the spelling or try with some other user')
    else:
        i = data.loc[data['reviews_username'] == user_name].index[0]
        lst = list(enumerate(sim[i]))
        lst = sorted(lst, key=lambda x: x[1], reverse=True)
        lst = lst[1:11]
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['name'][a])
        return l


def get_suggestions():
    data = get_data()
    users = set(data['reviews_username'])
    return json.dumps(list(users))

app = Flask(__name__)

@app.route("/")
def home():
    suggestions = get_suggestions()
    print("Got suggestions : {}".format(len(suggestions)))
    return render_template('home.html', suggestions=suggestions)


@app.route("/recommend", methods=["POST"])
def recommend():
    # 1. Get user from payload
    user = request.get_data().decode('utf-8')  # get user name from the URL
    if user is not None:
        user = user.split('=')[1]

    # user = user.upper()
    # 2. Get top 5 recommendations
    product_recommendations = get_recommendations(user)
    print(product_recommendations)
    print(type(product_recommendations))
    if isinstance(product_recommendations, str):  # no such user found in the database
        suggestions = get_suggestions()
        print("Got suggestions : {}".format((suggestions)))
        return render_template('home.html', user_not_found=True, suggestions=suggestions)
    else:

        data = get_data()
        product_cards = []
        product_recommendations = set(product_recommendations)
        for product in product_recommendations:
            print(product)
            name = product
            # manufacturer = data[data['name'] == product['name']]['manufacturer']
            # brand = data[data['name'] == product['name']]['brand']

            product_card = {'product_name': name, 'manufacturer': "dummy", 'brand': "dummy"}
            product_cards.append(product_card)

        # get user names for auto completion
        suggestions = get_suggestions()

        return render_template('recommend.html', product_cards=product_cards)

#
# if __name__ == '__main__':
#     app.run(debug=True)
