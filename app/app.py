#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 19:15:32 2021

@author: vishwas
"""

from flask import Flask, render_template, request
from app import model

model = model.Model()
app = Flask(__name__)


@app.route("/")
def home():
    suggestions = model.get_suggestions()
    print("Got suggestions : {}".format(len(suggestions)))
    return render_template('home.html', suggestions=suggestions)


@app.route("/recommend", methods=["POST"])
def recommend():
    # 1. Get user from payload
    user = request.get_data().decode('utf-8')  # get user name from the URL
    if user is not None:
        user = user.split('=')[1]

    # 2. Get top 5 recommendations
    product_recommendations = model.get_recommendations(user)
    if isinstance(product_recommendations, str):  # no such user found in the database
        suggestions = model.get_suggestions()
        print("Got suggestions : {}".format((suggestions)))
        return render_template('home.html', user_not_found=True, suggestions=suggestions)
    else:
        product_cards = []
        product_added = set()
        for i in range(len(product_recommendations)):
            if product_recommendations.Product.iloc[i] not in product_added:
                product_added.add(product_recommendations.Product.iloc[i])
                product_reviews = model.get_reviews(product_recommendations.Product.iloc[i])
                product_reviews_vector = model.vectorizer.transform(product_reviews)
                pred = model.xgboost_model.predict(product_reviews_vector)
                print(pred)
                reviews_status = ('Good' if 1 in pred else 'Bad')
                product_card = {
                    'product_name': product_recommendations.Product.iloc[i],
                    'manufacturer': product_recommendations.Manufacturer.iloc[i],
                    'brand': product_recommendations.Brand.iloc[i],
                    'sentiment': reviews_status
                    }
                product_cards.append(product_card)

        product_cards = product_cards[0:6]
        return render_template('recommend.html', product_cards=product_cards)
