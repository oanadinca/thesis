from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import datetime
from blogposts import Post, Comment


def main():
    source = requests.get('http://warnewsupdates.blogspot.com/').text
    soup = BeautifulSoup(source, 'lxml')

    posts = []

    articles = soup.find('div', id='content-container')
    print(articles)
    #     .find_all('h2', class_='entry-title')
    #
    # for article in articles:
    #     headline = article.a.text
    #
    #     summarySource = requests.get(article.a['href']).text
    #     summarySoup = BeautifulSoup(summarySource, 'lxml')
    #
    #     summaryList = summarySoup.find('div', class_='entry-content').find_all('p')
    #     for s in summaryList:
    #         summary = summary + s.text.replace('\n', "")
    #
    #     try:
    #         comments = summarySoup.find('ol', class_='commentlist').find_all('li')
    #         comments.pop(0) #primul element nu este un comentariu real
    #     except Exception as e:
    #         comments = []
    #
    #     id = 0
    #
    #     commList = []
    #
    #     anonymous = 1
    #
    #     for comment in comments:
    #         id = id + 1
    #
    #         refid = 1
    #
    #         user = comment.find('div', class_='comment-author vcard').cite.text
    #         if user == 'Unknown' or user == 'Anonymous':
    #             user = 'Anonymous_user_' + str(anonymous)
    #             anonymous = anonymous + 1
    #
    #         date = comment.find('span', class_='comment-meta commentmetadata').a.text
    #         parsed_date = parse(date)
    #         timestamp = datetime.datetime.timestamp(parsed_date)
    #
    #         msg = ""
    #         msgList = comment.find('div', class_='comment-body').find_all('p')
    #         for m in msgList:
    #             msg = msg + m.text + " "
    #
    #         comm = Comment(id, refid, timestamp, user, msg)
    #         commList.append(comm)
    #
    #         fail_condition = True
    #         while fail_condition:
    #             try:
    #                 replies = comment.find('ul', class_='children').find_all('li')
    #                 del replies[-1]
    #
    #                 refid = id
    #
    #                 for reply in replies:
    #                     id = id + 1
    #
    #                     user = reply.find('div', class_='comment-author vcard').cite.text
    #                     if user == 'Unknown' or user == 'Anonymous':
    #                         user = 'Anonymous_user_' + str(anonymous)
    #                         anonymous = anonymous + 1
    #
    #                     date = reply.find('span', class_='comment-meta commentmetadata').a.text
    #                     parsed_date = parse(date)
    #                     timestamp = datetime.datetime.timestamp(parsed_date)
    #
    #                     msg = ""
    #                     msgList = reply.find('div', class_='comment-body').find_all('p')
    #                     for m in msgList:
    #                         msg = msg + m.text + " "
    #
    #                     comm = Comment(id, refid, timestamp, user, msg)
    #                     commList.append(comm)
    #
    #                 fail_condition = False
    #             except Exception as e:
    #                 fail_condition = False
    #
    #     posts.append(Post(headline, summary, commList))
    #
    # for post in posts:
    #     print(post)
