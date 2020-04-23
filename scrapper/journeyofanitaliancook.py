from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import datetime
from blogposts import Post, Comment


def main():
    source = requests.get('http://journeyofanitaliancook.blogspot.com/').text
    soup = BeautifulSoup(source, 'lxml')

    posts = []

    articles = soup.find_all('div', class_='post hentry')

    for article in articles:
        headline = article.h3.text
        summary = article.find('div', class_='post-body entry-content').text

        commentLink = article.find('span', class_='post-comment-link').a['href']

        commentSource = requests.get(commentLink).text
        commentSoup = BeautifulSoup(commentSource, 'lxml')

        comments = commentSoup.find_all('dl', id='comments-block')

        id = 0

        commList = []

        for comment in comments:
            id = id + 1

            refid = 1

            user = comment.dt.span.text

            date = comment.find('p', class_='comment-timestamp').text
            parsed_date = parse(date)
            timestamp = datetime.datetime.timestamp(parsed_date)

            msg = comment.dd.p.text

            comm = Comment(id, refid, timestamp, user, msg)
            commList.append(comm)

        posts.append(Post(headline, summary, commList))

    for post in posts:
        print(post)
