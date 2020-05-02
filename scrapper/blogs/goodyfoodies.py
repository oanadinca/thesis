from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import datetime
from blogposts import Post, Comment


def main():
    source = requests.get('http://goodyfoodies.blogspot.com').text
    soup = BeautifulSoup(source, 'lxml')

    posts = []

    articles = soup.find_all('div', class_='post hentry uncustomized-post-template')

    for article in articles:
        headline = article.h3.text
        summary = article.find('div', class_='post-body entry-content').text

        commentLink = article.find('span', class_='post-comment-link').a['href']

        commentSource = requests.get(commentLink).text
        commentSoup = BeautifulSoup(commentSource, 'lxml')

        comments = commentSoup.find_all('div', class_='comment-block')

        id = 0

        commList = []

        for comment in comments:
            id = id + 1

            refid = 1

            user = comment.div.cite.text

            date = comment.find('span', class_='datetime secondary-text').a.text
            parsed_date = parse(date)
            # print('Date:', parsed_date.date())
            # print('time:', parsed_date.time())
            timestamp = datetime.datetime.timestamp(parsed_date)
            # print(timestamp)

            msg = comment.p.text

            comm = Comment(id, refid, timestamp, user, msg)
            commList.append(comm)

        posts.append(Post(headline, summary, commList))

    for post in posts:
        print(post)
