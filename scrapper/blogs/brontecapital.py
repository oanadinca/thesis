from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import datetime
from blogposts import Post, Comment


def main():
    source = requests.get('http://brontecapital.blogspot.com/').text
    soup = BeautifulSoup(source, 'lxml')

    posts = []

    articles = soup.find_all('div', class_='post hentry uncustomized-post-template')

    for article in articles:
        headline = article.h3.a.text

        summarySource = requests.get(article.h3.a['href']).text
        summarySoup = BeautifulSoup(summarySource, 'lxml')
        summaryList = summarySoup.find('div', class_='post-body entry-content').find_all('span', lang='EN-US')
        summary = ""
        for s in summaryList:
            try:
                summary = summary + " " + s.text
            except Exception as e:
                summary = summary + ''

        if summary == "":
            summaryList = summarySoup.find('div', class_='post-body entry-content').find_all('div')
            for s in summaryList:
                try:
                    summary = summary + " " + s.text.replace('\n', '')
                except Exception as e:
                    summary = summary + ''

        if summary == "":
            summaryList = summarySoup.find('div', class_='post-body entry-content').find_all('b')
            summary = ""
            for s in summaryList:
                try:
                    summary = summary + " " + s.text.replace('\n', '')
                except Exception as e:
                    summary = summary + ''

        else:
            summary = summarySoup.find('div', class_='post-body entry-content').text.replace('\n', '')

        try:
            commentUsers = summarySoup.find('div', id='comments').find_all('dt', class_='comment-author')
            commentBodies = summarySoup.find('div', id='comments').find_all('dd', class_='comment-body')
            commentFooters = summarySoup.find('div', id='comments').find_all('dd', class_='comment-footer')

        except Exception as e:
            comments = []

        id = 0

        commList = []

        anonymous = 1

        for comment in commentBodies:
            id = id + 1

            refid = 1

            commentUser = commentUsers.pop(0)
            user = commentUser.text.replace('said...', '').replace('\n', '')
            if user == 'Unknown' or user == 'Anonymous':
                user = 'Anonymous_user_' + str(anonymous)
                anonymous = anonymous + 1

            commentFooter = commentFooters.pop(0)

            date = commentFooter.find('span', class_='comment-timestamp').a.text
            parsed_date = parse(date)
            timestamp = datetime.datetime.timestamp(parsed_date)

            try:
                msg = comment.find('p').text.replace('\n', ' ')
            except Exception as e:
                msg = ''

            comm = Comment(id, refid, timestamp, user, msg)
            commList.append(comm)

        posts.append(Post(headline, summary, commList))

    for post in posts:
        print(post)
