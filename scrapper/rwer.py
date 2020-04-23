from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import datetime
from blogposts import Post, Comment


def main():
    source = requests.get('https://rwer.wordpress.com/').text
    soup = BeautifulSoup(source, 'lxml')

    posts = []

    articles = soup.find('div', id='main').find_all('h2')

    for article in articles:
        headline = article.a.text

        summarySource = requests.get(article.a['href']).text
        summarySoup = BeautifulSoup(summarySource, 'lxml')
        summaryList = summarySoup.find('div', id='main').find('div', class_='content').find_all('p')
        summaryList.pop(0)
        summary = ""
        for s in summaryList:
            summary = summary + " " + s.text

        try:
            comments = summarySoup.find('ol', id='thecomments').find_all('li')
        except Exception as e:
            comments = []

        id = 0
        commList = []
        anonymous = 1

        for comment in comments:
            id = id + 1

            refid = 1

            try:
                user = comment.find('div', class_='author').find('div', class_='name').text.replace('\t', '').replace('\n', '')
                if user == 'Unknown' or user == 'Anonymous':
                    user = 'Anonymous_user_' + str(anonymous)
                    anonymous = anonymous + 1

                date = comment.find('div', class_='date').text
                parsed_date = parse(date)
                timestamp = datetime.datetime.timestamp(parsed_date)

                msg = ''
                msgList = comment.find('div', class_='content').find_all('p')
                for m in msgList:
                    msg = msg + m.text.replace('\n', ' ') + " "

                comm = Comment(id, refid, timestamp, user, msg)
                commList.append(comm)
            except Exception as e:
                comm = None

            fail_condition = True
            while fail_condition:
                try:
                    replies = comment.find('ul', class_='children').find_all('li')

                    refid = id

                    for reply in replies:
                        id = id + 1

                        try:
                            user = reply.find('div', class_='author').find('div', class_='name').text.replace('\t', '').replace('\n', '')
                            if user == 'Unknown' or user == 'Anonymous':
                                user = 'Anonymous_user_' + str(anonymous)
                                anonymous = anonymous + 1

                            date = reply.find('div', class_='date').text
                            parsed_date = parse(date)
                            timestamp = datetime.datetime.timestamp(parsed_date)

                            msg = ''
                            msgList = reply.find('div', class_='content').find_all('p')
                            for m in msgList:
                                msg = msg + m.text.replace('\n', '') + " "

                            comm = Comment(id, refid, timestamp, user, msg)
                            commList.append(comm)
                        except Exception as e:
                            comm = None

                    fail_condition = False
                except Exception as e:
                    fail_condition = False

        posts.append(Post(headline, summary, commList))

    for post in posts:
        print(post)
