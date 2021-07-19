import pandas as pd
import pickle
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app import app_constants


class Model:

    def __init__(self):
        self.xgboost_model = pickle.load(open(app_constants.MODEL_PICKLE_FILE, 'rb'))
        self.vectorizer = pickle.load(open(app_constants.VECTORIZER_FILE, 'rb'))
        self.data = pd.read_csv(app_constants.DATA_FILE)
        self.data = self.data[~(self.data['clean_text'].isnull())]
        self.cosine_similarity = Model.create_similarity(self.data)

    @staticmethod
    def create_similarity(data):
        # creating a count matrix
        cv = TfidfVectorizer(stop_words='english')
        count_matrix = cv.fit_transform(data['clean_text'])
        cos_similarity = cosine_similarity(count_matrix)
        return cos_similarity

    def get_suggestions(self):
        users = set(self.data['reviews_username'])
        return json.dumps(list(users))

    def get_reviews(self, product_name):
        reviews = self.data[self.data['name'] == product_name]['reviews_text']
        return reviews

    def get_recommendations(self, user_name):
        if user_name not in self.data['reviews_username'].unique():
            return (
                'Sorry! The user you searched is not in our database. Please check the spelling or try with some other user')
        else:
            idx = self.data.loc[self.data['reviews_username'] == user_name].index[0]
            sim_scores = list(enumerate(self.cosine_similarity[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            product_indices = [i[0] for i in sim_scores]
            products_name = self.data['name'].iloc[product_indices]
            products_brand = self.data['brand'].iloc[product_indices]
            manufacturers = self.data['manufacturer'].iloc[product_indices]
            return_df = pd.DataFrame(columns=['Product', 'Brand', 'Manufacturer'])
            return_df['Product'] = products_name
            return_df['Brand'] = products_brand
            return_df['Manufacturer'] = manufacturers
            return return_df
