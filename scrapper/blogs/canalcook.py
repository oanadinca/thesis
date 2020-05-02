from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import datetime
from blogposts import Post, Comment


def main():
    source = requests.get('https://canalcook.wordpress.com/').text
    soup = BeautifulSoup(source, 'lxml')

    posts = []

    articles = soup.find_all('article')

    for article in articles:
        headline = article.header.h1.text

        summaryList = article.find('div', class_='entry-content').find_all('p')
        summary = ""
        for s in summaryList:
            summary = summary + " " + s.text

        try:
            commentSource = requests.get(article.find('span', class_='comments-link').a['href']).text
            commentSoup = BeautifulSoup(commentSource, 'lxml')
            comments = commentSoup.find('ol', class_='commentlist').find_all('li')
        except Exception as e:
            comments = []

        id = 0

        commList = []

        anonymous = 1

        for comment in comments:
            id = id + 1

            refid = 1

            user = comment.find('div', class_='comment-author vcard').cite.text
            if user == 'Unknown' or user == 'Anonymous':
                user = 'Anonymous_user_' + str(anonymous)
                anonymous = anonymous + 1

            date = comment.find('time').text
            parsed_date = parse(date)
            timestamp = datetime.datetime.timestamp(parsed_date)

            msg = comment.find('div', class_='comment-content').text

            comm = Comment(id, refid, timestamp, user, msg)
            commList.append(comm)

            fail_condition = True
            while fail_condition:
                try:
                    replies = comment.find('ul', class_='children').find_all('li')

                    refid = id

                    for reply in replies:
                        id = id + 1

                        user = reply.find('div', class_='comment-author vcard').cite.text
                        if user == 'Unknown' or user == 'Anonymous':
                            user = 'Anonymous_user_' + str(anonymous)
                            anonymous = anonymous + 1

                        date = reply.find('time').text
                        parsed_date = parse(date)
                        timestamp = datetime.datetime.timestamp(parsed_date)

                        msg = reply.find('div', class_='comment-content').text

                        comm = Comment(id, refid, timestamp, user, msg)
                        commList.append(comm)

                    fail_condition = False
                except Exception as e:
                    fail_condition = False

        posts.append(Post(headline, summary, commList))

    for post in posts:
        print(post)
