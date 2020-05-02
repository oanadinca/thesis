from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import datetime
from blogposts import Post, Comment


def main():
    source = requests.get('http://inspiringscience.net').text
    soup = BeautifulSoup(source, 'lxml')

    posts = []

    articles = soup.find('div', id='content').find_all('article')

    for article in articles:
        headline = article.header.h1.a.text

        summarySource = requests.get(article.header.h1.a['href']).text
        summarySoup = BeautifulSoup(summarySource, 'lxml')
        summaryList = summarySoup.find('div', class_='post-entry').find_all('p')
        summary = ""
        for s in summaryList:
            summary = summary + " " + s.text

        try:
            comments = summarySoup.find('ol', class_='commentlist').find_all('li')
        except Exception as e:
            comments = []

        id = 0

        commList = []

        anonymous = 1

        for comment in comments:
            id = id + 1

            refid = 1

            user = comment.find('p', class_='comment-author').span.text
            if user == 'Unknown' or user == 'Anonymous':
                user = 'Anonymous_user_' + str(anonymous)
                anonymous = anonymous + 1

            date = comment.find('p', class_='comment-date').a.time.text
            parsed_date = parse(date)
            timestamp = datetime.datetime.timestamp(parsed_date)

            msg = ''
            msgList = comment.find('div', class_='comment-text').find_all('p')
            del msgList[-1]
            for m in msgList:
                msg = msg + m.text + " "

            comm = Comment(id, refid, timestamp, user, msg)
            commList.append(comm)

            fail_condition = True
            while fail_condition:
                try:
                    replies = comment.find('ul', class_='children').find_all('li')

                    refid = id

                    for reply in replies:
                        id = id + 1

                        user = reply.find('p', class_='comment-author').span.text
                        if user == 'Unknown' or user == 'Anonymous':
                            user = 'Anonymous_user_' + str(anonymous)
                            anonymous = anonymous + 1

                        date = reply.find('p', class_='comment-date').a.time.text
                        parsed_date = parse(date)
                        timestamp = datetime.datetime.timestamp(parsed_date)

                        msg = ''
                        msgList = reply.find('div', class_='comment-text').find_all('p')
                        del msgList[-1]
                        for m in msgList:
                            msg = msg + m.text + " "

                        comm = Comment(id, refid, timestamp, user, msg)
                        commList.append(comm)

                    fail_condition = False
                except Exception as e:
                    fail_condition = False

        posts.append(Post(headline, summary, commList))

    for post in posts:
        print(post)
