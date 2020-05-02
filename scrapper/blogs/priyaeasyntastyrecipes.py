from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import datetime
from blogposts import Post, Comment


def main():
    source = requests.get('http://priyaeasyntastyrecipes.blogspot.com/').text
    soup = BeautifulSoup(source, 'lxml')

    posts = []

    articles = soup.find('div', class_='widget Blog').find_all('div', class_='post hentry')

    for article in articles:
        headline = article.h3.text

        summarySource = requests.get(article.h3.a['href']).text
        summarySoup = BeautifulSoup(summarySource, 'lxml')
        summary = summarySoup.find('div', class_='post-body entry-content').text

        try:
            comments = summarySoup.find('dl', id='comments-block')
            comm = comments.find('dt')
            if comm is None:
                comments = []
        except Exception as e:
            comments = []


        id = 0

        commList = []

        anonymous = 1

        for i in range(len(comments)):
            id = id + 1

            refid = 1

            print(comments.get(i))
            # user = comment.find('dt', class_='comment-author').text
            # if user == 'Unknown' or user == 'Anonymous':
            #     user = 'Anonymous_user_' + str(anonymous)
            #     anonymous = anonymous + 1
            #
            # date = comment.find('span', class_='comment-timestamp').text
            # parsed_date = parse(date)
            # timestamp = datetime.datetime.timestamp(parsed_date)
            #
            # msg = comment.find('dd', class_='comment-body').p.text
            #
            # comm = Comment(id, refid, timestamp, user, msg)
            # commList.append(comm)
            #
            # fail_condition = True
            # while fail_condition:
            #     try:
            #         replies = comment.find('div', class_='comment-replies').find_all('li')
            #
            #         refid = id
            #
            #         for reply in replies:
            #             id = id + 1
            #
            #             user = reply.find('div', class_='comment-header').cite.text
            #             if user == 'Unknown' or user == 'Anonymous':
            #                 user = 'Anonymous_user_' + str(anonymous)
            #                 anonymous = anonymous + 1
            #
            #             date = reply.find('span', class_='datetime secondary-text').text
            #             parsed_date = parse(date)
            #             timestamp = datetime.datetime.timestamp(parsed_date)
            #
            #             msg = reply.find('p', class_='comment-content').text
            #
            #             comm = Comment(id, refid, timestamp, user, msg)
            #             commList.append(comm)
            #
            #         fail_condition = False
            #     except Exception as e:
            #         fail_condition = False

    #     posts.append(Post(headline, summary, commList))
    #
    # for post in posts:
    #     print(post)
