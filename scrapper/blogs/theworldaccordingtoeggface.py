from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import datetime
from blogposts import Post, Comment


def main():
    source = requests.get('http://theworldaccordingtoeggface.blogspot.com/').text
    soup = BeautifulSoup(source, 'lxml')

    posts = []

    articles = soup.find_all('div', class_='post hentry')

    for article in articles:
        headline = article.h3.text
        summary = article.find('div', class_='post-body entry-content').text

        commentLink = article.h3.a['href'] #este link-ul din headline pentru ca nu exista nicio referinta la comentarii in pagina home

        commentSource = requests.get(commentLink).text
        commentSoup = BeautifulSoup(commentSource, 'lxml')

        # comments = commentSoup.find('div', class_='comments')
# nu exista niciun comentariu pe acest blog

        posts.append(Post(headline, summary, ""))

    for post in posts:
        print(post)
