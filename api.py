from flask import Flask, jsonify, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

movies_df = pd.read_csv('IMDB_movies.csv')
netflix_df = pd.read_csv('netflix_data.csv')

app = Flask(__name__)

tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(movies_df['Description'])

tfidf_vectorizer1 = TfidfVectorizer(stop_words='english')
tfidf_matrix1 = tfidf_vectorizer1.fit_transform(netflix_df['description'])

@app.route('/top_movies', methods=['GET'])
def get_top_movies():
    top_movies = movies_df.nlargest(10, 'Rating')[['Title', 'Rating']].to_dict(orient='records')
    return jsonify(top_movies)

@app.route('/recommend_by_genre', methods=['GET'])
def recommend_by_genre():
    genre = request.args.get('genre')
    genre_movies = movies_df[movies_df['Genre'].str.contains(genre, case=False, na=False)]
    top_genre_movies = genre_movies.nlargest(10, 'Rating')[['Title', 'Rating']].to_dict(orient='records')
    return jsonify(top_genre_movies)

@app.route('/recommend_by_content', methods=['GET'])
def recommend_by_content():
    title = request.args.get('title')
    movie_index = netflix_df[netflix_df['title'].str.lower() == title.lower()].index
    if movie_index.empty:
        return jsonify({"error": "Movie not found"}), 404
    cosine_sim = cosine_similarity(tfidf_matrix1[movie_index[0]], tfidf_matrix1).flatten()
    similar_indices = cosine_sim.argsort()[-11:-1][::-1]
    recommended_movies = netflix_df.iloc[similar_indices][['title', 'description', 'listed_in']].to_dict(orient='records')
    return jsonify(recommended_movies)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
