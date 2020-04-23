from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import datetime
from blogposts import Post, Comment


def main():
    source = requests.get('http://warnewsupdates.blogspot.com/').text
    soup = BeautifulSoup(source, 'lxml')

    posts = []

    articles = soup.find('div', class_='widget Blog').find_all('div', class_='post hentry')

    for article in articles:
        headline = article.h3.a.text

        summarySource = requests.get(article.h3.a['href']).text
        summarySoup = BeautifulSoup(summarySource, 'lxml')

        summary = summarySoup.find('div', class_='post-body entry-content').text
        summary = summary.replace('\n', "")
        # print(summary)

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

            user = comment.find('div', class_='comment-author vcard').cite.text
            if user == 'Unknown' or user == 'Anonymous':
                user = 'Anonymous_user_' + str(anonymous)
                anonymous = anonymous + 1

            date = comment.find('div', class_='comment-meta commentmetadata').a.text
            parsed_date = parse(date)
            timestamp = datetime.datetime.timestamp(parsed_date)

            msg = ""
            msgList = comment.find('div', class_='comment-body').find_all('p')
            for m in msgList:
                if 'Like' not in m.text:
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

                        user = reply.find('div', class_='comment-author vcard').cite.text
                        if user == 'Unknown' or user == 'Anonymous':
                            user = 'Anonymous_user_' + str(anonymous)
                            anonymous = anonymous + 1

                        date = reply.find('div', class_='comment-meta commentmetadata').a.text
                        parsed_date = parse(date)
                        timestamp = datetime.datetime.timestamp(parsed_date)

                        msg = ""
                        msgList = reply.find('div', class_='comment-body').find_all('p')
                        for m in msgList:
                            if m.text != 'Like':
                                if 'Like' not in m.text:
                                    msg = msg + m.text + " "

                        comm = Comment(id, refid, timestamp, user, msg)
                        commList.append(comm)

                    fail_condition = False
                except Exception as e:
                    fail_condition = False

        posts.append(Post(headline, summary, commList))

    for post in posts:
        print(post)
