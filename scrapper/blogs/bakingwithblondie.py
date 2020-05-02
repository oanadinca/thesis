from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import datetime
from blogposts import Post, Comment


def main():
    source = requests.get('https://bakingwithblondie.blogspot.com/').text
    soup = BeautifulSoup(source, 'lxml')

    posts = []

    articles = soup.find('div', class_='widget Blog').find_all('article')

    for article in articles:
        headline = article.div.div.h3.text

        summarySource = requests.get(article.div.a['href']).text
        summarySoup = BeautifulSoup(summarySource, 'lxml')
        summaryList = summarySoup.find_all('div', class_='separator')
        summary = ""
        for s in summaryList:
            summary = summary + s.text

        try:
            comments = summarySoup.find('div', class_='comments-content').find_all('li')
        except Exception as e:
            comments = []

        id = 0

        commList = []

        anonymous = 1

        for comment in comments:
            id = id + 1

            refid = 1

            user = comment.find('div', class_='comment-header').cite.text
            if user == 'Unknown' or user == 'Anonymous':
                user = 'Anonymous_user_' + str(anonymous)
                anonymous = anonymous + 1

            date = comment.find('span', class_='datetime secondary-text').text
            parsed_date = parse(date)
            timestamp = datetime.datetime.timestamp(parsed_date)

            msg = comment.find('p', class_='comment-content').text

            comm = Comment(id, refid, timestamp, user, msg)
            commList.append(comm)

            fail_condition = True
            while fail_condition:
                try:
                    replies = comment.find('div', class_='comment-replies').find_all('li')

                    refid = id

                    for reply in replies:
                        id = id + 1

                        user = reply.find('div', class_='comment-header').cite.text
                        if user == 'Unknown' or user == 'Anonymous':
                            user = 'Anonymous_user_' + str(anonymous)
                            anonymous = anonymous + 1

                        date = reply.find('span', class_='datetime secondary-text').text
                        parsed_date = parse(date)
                        timestamp = datetime.datetime.timestamp(parsed_date)

                        msg = reply.find('p', class_='comment-content').text

                        comm = Comment(id, refid, timestamp, user, msg)
                        commList.append(comm)

                    fail_condition = False
                except Exception as e:
                    fail_condition = False

        posts.append(Post(headline, summary, commList))

    for post in posts:
        print(post)
