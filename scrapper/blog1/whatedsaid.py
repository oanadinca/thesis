from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import datetime
from data_model.blogposts import Post, Comment
import csv


def get_last_post_id_from_file(file_name):
    with open(file_name, 'r') as reader_obj:
        csv_reader = csv.reader(reader_obj)

        for row in reversed(list(csv_reader)):
            return int(row[0])

    return -1


# TODO: how to append per post all the comments?
def append_posts_to_file(file_name, posts):
    for post in posts:
        if len(post.comments) == 0:
            append_list_as_row(file_name, [post.id, post.headline.encode('utf-8'), post.summary.encode('utf-8'),
                                           post.url,
                                           '', '', '', '', '', ''])
        else:
            for comment in post.comments:
                append_list_as_row(file_name, [post.id, post.headline.encode('utf-8'), post.summary.encode('utf-8'),
                                               post.url, comment.id, comment.ref_id, comment.timestamp,
                                               comment.username.encode('utf-8'), comment.replied_to.encode('utf-8'),
                                               comment.msg.encode('utf-8')])


def append_post_to_file(file_name, post):
    if len(post.comments) == 0:
        append_list_as_row(file_name, [post.id, post.headline.encode('utf-8'), post.summary.encode('utf-8'),
                                       post.url,
                                       '', '', '', '', '', ''])
    else:
        for comment in post.comments:
            append_list_as_row(file_name, [post.id, post.headline.encode('utf-8'), post.summary.encode('utf-8'),
                                           post.url, comment.id, comment.ref_id, comment.timestamp,
                                           comment.username.encode('utf-8'), comment.replied_to.encode('utf-8'),
                                           comment.msg.encode('utf-8')])


def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


def first_open_csv(file_name, fieldnames):
    with open(file_name, 'w') as writer_file:
        csv_writer = csv.writer(writer_file)
        csv_writer.writerow(fieldnames)


def main():
    post_id = 0
    posts = []
    file_name = 'blog1/whatedsaid_scrape.csv'
    fieldnames = ['post_id', "post_headline", "post_summary", "post_url", "comment_id", "comment_ref_id",
                  "comment_timestamp", "comment_username", "comment_replied_to", "comment_message"]
    try:
        post_id = get_last_post_id_from_file(file_name)
    except Exception as e:
        first_open_csv(file_name, fieldnames)

    source = requests.get('https://whatedsaid.wordpress.com').text
    soup = BeautifulSoup(source, 'lxml')

    archive_list = soup.find('select', id='archives-dropdown-5').find_all('option')
    archive_list.pop(0)  # select month phrase with no link to use

    for i in range(0, 2):
        selection = archive_list[i]
        page_link = selection['value']
        # print(page_link)
        article_source = requests.get(page_link).text
        article_soup = BeautifulSoup(article_source, 'lxml')

        articles = article_soup.find_all('article')
        for article in articles:
            post_id = post_id + 1
            post_headline = article.header.h1.a.text
            post_url = article.header.h1.a['href']

            summary_source = requests.get(post_url).text
            # print(headline)
            summary_soup = BeautifulSoup(summary_source, 'lxml')
            summary_list = summary_soup.find('div', class_='entry-content').find_all('p')
            post_summary = ""
            for s in summary_list:
                post_summary = post_summary + " " + s.text.replace('\n', '').replace('\t', '')\
                    # .replace('\U0001f642', ':)').replace('मुलांचे हक्क', '')
            # print(post_summary)
            try:
                comments = summary_soup.find('ol', class_='comment-list').find_all('li')
            except Exception as e:
                comments = []

            comment_id = 0
            comm_list = []
            anonymous = 1

            for comment in comments:
                comment_id = comment_id + 1
                comment_ref_id = 0
                try:
                    user = comment.find('div', class_='comment-author vcard').b.a.text.replace('\n', '').replace(
                        '\t',
                        '')
                except Exception as e:
                    try:
                        user = comment.find('div', class_='comment-author vcard').b.text.replace('\n', '').replace(
                            '\t',
                            '')
                    except Exception as e:
                        user = ''

                if user == 'Unknown' or user == 'Anonymous':
                    user = 'Anonymous_user_' + str(anonymous)
                    anonymous = anonymous + 1

                try:
                    date = comment.find('div', class_='comment-metadata').a.time.text.replace('\n', '').replace(
                        '\t', '')
                    parsed_date = parse(date)
                    timestamp = datetime.datetime.timestamp(parsed_date)
                except Exception as e:
                    timestamp = ''

                msg = ""
                try:
                    msg_list = comment.find('div', class_='comment-content').find_all('p')
                    like_buttons = comment.find('div', class_='comment-content').find('p',
                                                                                      class_='comment-likes comment-not-liked')
                    if like_buttons in msg_list:
                        msg_list.remove(like_buttons)
                    for m in msg_list:
                        msg = msg + m.text.replace('\n', '').replace('\t', '')\
                            # .replace('\U0001f642', ':)')
                except Exception as e:
                    msg = ''

                if not (user == '' and msg == '' and timestamp == ''):
                    comm = Comment(comment_id, comment_ref_id, timestamp, user, "", msg)
                    comm_list.append(comm)
                else:
                    comment_id = comment_id - 1

                fail_condition = True
                while fail_condition:
                    try:
                        replies = comment.find('ol', class_='children').find_all('li')
                        comment_ref_id = comment_id
                        replied_to = user
                        print(user)

                        for reply in replies:
                            print('ok')
                            comment_id = comment_id + 1
                            try:
                                user = reply.find('div', class_='comment-author vcard').b.a.text.replace('\n',
                                                                                                         '').replace(
                                    '\t', '')
                            except Exception as e:
                                try:
                                    if user == '':
                                        user = reply.find('div', class_='comment-author vcard').b.text.replace('\n',
                                                                                                               '').replace(
                                            '\t', '')
                                except Exception as e:
                                    user = ''

                            if user == 'Unknown' or user == 'Anonymous':
                                user = 'Anonymous_user_' + str(anonymous)
                                anonymous = anonymous + 1

                            try:
                                date = reply.find('div', class_='comment-metadata').a.time.text.replace('\n',
                                                                                                        '').replace(
                                    '\t', '')
                                parsed_date = parse(date)
                                timestamp = datetime.datetime.timestamp(parsed_date)
                            except Exception as e:
                                timestamp = ''

                            msg = ""
                            try:
                                msg_list = reply.find('div', class_='comment-content').find_all('p')
                                like_buttons = comment.find('div', class_='comment-content').find('p',
                                                                                                  class_='comment-likes comment-not-liked')
                                if like_buttons in msg_list:
                                    msg_list.remove(like_buttons)
                                for m in msg_list:
                                    msg = msg + m.text.replace('\n', '').replace('\t', '')\
                                        # .replace('\U0001f642', ':)')  # smiley face
                            except Exception as e:
                                msg = ''

                            if not (user == '' and msg == '' and timestamp == ''):
                                comm = Comment(comment_id, comment_ref_id, timestamp, user, replied_to, msg)
                                comm_list.append(comm)
                            else:
                                comment_id = comment_id - 1

                        fail_condition = False
                    except Exception as e:
                        fail_condition = False

            posts.append(Post(post_id, post_headline, post_summary, post_url, comm_list))

    # append_posts_to_file(file_name, posts)
    # print(post.id, post.comments)

    index = 0  # trebuie modificat cu primul index din range-ul de parcurgere
    for post in posts:
        post_file_name = "blog1/post_" + str(index)
        append_post_to_file(post_file_name, post)
        index = index + 1

