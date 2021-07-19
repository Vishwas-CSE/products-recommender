from os import path

def get_abs_path(*paths):
    abs_path = path.abspath(path.join(*paths))
    return abs_path


MODEL_PICKLE_FILE = get_abs_path('app/data/product_sentiment_model.pkl')
VECTORIZER_FILE = get_abs_path('app/data/tfidf_vectorizer.pkl')
DATA_FILE = get_abs_path('app/data/final_data.csv')
