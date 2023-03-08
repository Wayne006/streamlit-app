import random
import requests
import bs4
import streamlit as st
from PIL import Image

css = '''
header {
    visibility: hidden
}

footer {
    visibility: hidden
}

.center {
    text-align: center
}

strong, a {
    display: block
}

hr {
    background-color: blue
}

a, a:hover {
    text-decoration: none
}

a:hover {
    color: SlateBlue
}

a:active {
    color: Violet
}
'''

st.set_page_config('電影推薦app', Image.open('popcorn.png'))
st.write(f'<style>{css}</style>', unsafe_allow_html=True)

response = requests.get('https://www.imdb.com/chart/top/')
soup = bs4.BeautifulSoup(response.text, 'lxml')

rows = soup.find('tbody').find_all('tr')
movies = []
years = []
for row in rows:
    title = row.find(class_='titleColumn').find('a').text
    year = row.find(class_='titleColumn').find('span').text.replace('(', '').replace(')', '')
    rating = float(row.find('strong').text)
    url = 'https://www.imdb.com/' + row.find('a').get('href')

    years.append(year)
    movies.append([title, year, rating, url])

min_rating, max_rating = movies[-1][2], movies[0][2]
years = sorted(set(years))

st.write('<h1 class="center">電影推薦app</h1>', unsafe_allow_html=True)
st.info('''
本支app會從IMDB的評分在前250名的所有電影當中隨機為您挑選出一部電影。

您還可以在側邊欄依照指示選擇電影要符合的條件，app會根據您選擇的條件來篩選電影。
''', icon='ℹ️')
st.write('<hr>', unsafe_allow_html=True)

with st.sidebar:
    st.write('<h1 class="center">條件設定</h1>', unsafe_allow_html=True)
    input_rating = st.number_input('您想要評分至少是幾分的電影？', min_rating, max_rating, step=0.1, format='%.1f')
    input_year = st.selectbox('您希望電影的年份至少要在幾年以後？', years)

filtered_movies = []
for movie in movies:
    if movie[2] >= input_rating and movie[1] >= input_year:
        filtered_movies.append(movie)
if filtered_movies:
    selected_movie = random.choice(filtered_movies)

    st.write(f'''
    <strong class="center">以下是app為您挑選的電影：</strong>
    
    <a href="{selected_movie[3]}" class="center">
        {selected_movie[0]}（年份：{selected_movie[1]}、評分：{selected_movie[2]}）
    </a>
    ''', unsafe_allow_html=True)
else:
    st.warning('找不到符合條件的電影', icon='⚠️')
