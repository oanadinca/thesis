from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import datetime
from blogposts import Post, Comment


def main():
    source = requests.get('https://www.honeywerehome.com/').text
    soup = BeautifulSoup(source, 'lxml')

    posts = []

    articles = soup.find_all('div', class_='entry-summary')

    for article in articles:
        headline = article.div.a['title']

        summaryList = article.find_all('p')
        summary = ""
        for s in summaryList:
            summary = summary + " " + s.text

        commentLink = article.a['href']

        commentSource = requests.get(commentLink).text
        commentSoup = BeautifulSoup(commentSource, 'lxml')

        comments = commentSoup.find('ol', class_='comment-list').find_all('li')

        id = 0

        commList = []

        for comment in comments:
            id = id + 1

            refid = 1

            user = comment.find('div', class_='comment-author').cite.text

            date = comment.find('span', class_='comment-date').text
            parsed_date = parse(date)
            timestamp = datetime.datetime.timestamp(parsed_date)

            msg = comment.find('div', class_='comment-content').p.text

            comm = Comment(id, refid, timestamp, user, msg)
            commList.append(comm)

            fail_condition = True
            while fail_condition:
                try:
                    replies = comment.find('ul', class_='children').find_all('li')

                    refid = id

                    for reply in replies:
                        id = id + 1

                        user = reply.find('div', class_='comment-author').cite.text

                        date = reply.find('span', class_='comment-date').text
                        parsed_date = parse(date)
                        timestamp = datetime.datetime.timestamp(parsed_date)

                        msg = reply.find('div', class_='comment-content').p.text

                        print(user)

                        comm = Comment(id, refid, timestamp, user, msg)
                        commList.append(comm)

                    fail_condition = False
                except Exception as e:
                    fail_condition = False

        posts.append(Post(headline, summary, commList))

    for post in posts:
        print(post)
