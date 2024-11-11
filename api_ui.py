import streamlit as st
import requests

API_BASE_URL = "http://172.17.131.56:5000"

st.title("Рекомендации фильмов")
st.write("Это приложение позволяет запрашивать рекомендации фильмов через API.")

option = st.sidebar.selectbox(
    "Выберите действие",
    ["Справка", "Топ-10 популярных фильмов", "Рекомендации по жанру", "Рекомендации по контенту"]
)

if option == "Справка":
    st.subheader("Справка")
    st.write("""
    Это приложение поддерживает следующие команды:

    1. **Топ-10 популярных фильмов**: Возвращает список из 10 фильмов с наивысшим рейтингом.
    - Путь: `/top_movies`
    - Метод: `GET`

    2. **Рекомендации по жанру**: Позволяет получить топ-10 фильмов для указанного жанра.
    - Путь: `/recommend_by_genre`
    - Метод: `GET`
    - Параметр: `genre` (например, `genre=Action`)

    3. **Рекомендации по контенту**: Находит фильмы, похожие на указанный фильм по его описанию.
    - Путь: `/recommend_by_content`
    - Метод: `GET`
    - Параметр: `title` (например, `title=Guardians of the Galaxy`)
    """)

elif option == "Топ-10 популярных фильмов":
    st.subheader("Топ-10 популярных фильмов")
    response = requests.get(f"{API_BASE_URL}/top_movies")
    if response.status_code == 200:
        top_movies = response.json()
        for movie in top_movies:
            st.write(f"**{movie['Title']}** - Рейтинг: {movie['Rating']}")
    else:
        st.error("Ошибка при получении данных")

elif option == "Рекомендации по жанру":
    st.subheader("Рекомендации по жанру")
    genre = st.text_input("Введите жанр (например, Action):")
    if genre:
        response = requests.get(f"{API_BASE_URL}/recommend_by_genre", params={"genre": genre})
        if response.status_code == 200:
            genre_movies = response.json()
            for movie in genre_movies:
                st.write(f"**{movie['Title']}** - Рейтинг: {movie['Rating']}")
        else:
            st.error("Ошибка при получении данных")

elif option == "Рекомендации по контенту":
    st.subheader("Рекомендации по контенту")
    title = st.text_input("Введите название фильма:")
    if title:
        response = requests.get(f"{API_BASE_URL}/recommend_by_content", params={"title": title})
        if response.status_code == 200:
            content_movies = response.json()
            for movie in content_movies:
                st.markdown(f"<span style='color: green; font-weight: bold;'>{movie['title']}</span>",
                            unsafe_allow_html=True)
                st.write(f"**Описание:** {movie['description']}")
                st.write(f"**Жанры:** {movie['listed_in']}")
                st.write("-----------------------------------------------------------------------")
        else:
            st.error("Ошибка при получении данных")

# Run this file with Streamlit by calling:
# streamlit run api_ui.py
