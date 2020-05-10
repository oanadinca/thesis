from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import datetime
from data_model.blogposts import Post, Comment
import csv

# TODO: need to refactor as whatedsaid


def get_last_post_id_from_file(file_name):
    with open(file_name, 'r') as reader_obj:
        csv_reader = csv.reader(reader_obj)

        for row in reversed(list(csv_reader)):
            return int(row[0])

    return -1


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


# TODO: how to append per post all the comments?
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
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(list_of_elem)


def first_open_csv(file_name, fieldnames):
    with open(file_name, 'w') as writer_file:
        csv_writer = csv.writer(writer_file)
        csv_writer.writerow(fieldnames)


def get_soup(url):
    try:
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        return soup
    except Exception as e:
        return e


def get_headline(article):
    return article.header.h2.a.text


def get_summary(soup):
    summary_list = soup.find('div', class_='entry-content').find_all('p')
    post_summary = ""
    for s in summary_list:
        post_summary = post_summary + " " + s.text.replace('\n', '').replace('\t', '')
    # print(post_summary)
    return post_summary


def get_comments(soup):
    try:
        comments = soup.find('ol', class_='comment-list').find_all('li')
    except Exception as e:
        comments = []
    return comments


def get_username(comment):
    try:
        username = comment.find('div', class_='comment-author vcard').b.a.text.replace('\n', '').replace('\t', '')
    except Exception as e:
        try:
            username = comment.find('div', class_='comment-author vcard').b.text.replace('\n', '').replace('\t', '')
        except Exception as e:
            username = ''
    return username


def get_timestamp(comment):
    try:
        date = comment.find('div', class_='comment-metadata').a.time.text.replace('\n', '').replace('\t', '')
        parsed_date = parse(date)
        timestamp = datetime.datetime.timestamp(parsed_date)
    except Exception as e:
        timestamp = ''
    return timestamp


def get_message(comment):
    msg = ""
    try:
        msg_list = comment.find('div', class_='comment-content').find_all('p')
        for m in msg_list:
            msg = msg + m.text.replace('\n', '').replace('\t', '')
    except Exception as e:
        msg = ''
    return msg


def main(args):
    post_id = 0
    posts = []

    file_name = 'blog3/chiasuanchong_scrape.csv'
    fieldnames = ['post_id', "post_headline", "post_summary", "post_url", "comment_id", "comment_ref_id",
                  "comment_timestamp", "comment_username", "comment_replied_to", "comment_message"]
    try:
        post_id = get_last_post_id_from_file(file_name)
    except Exception as e:
        first_open_csv(file_name, fieldnames)

    page_soup = get_soup(args.url)
    if isinstance(page_soup, Exception):
        return

    archive_list = page_soup.find('section', id='archives-2').find_all('li')

    for i in range(0, 2):  # 20 is the last page
        selection = archive_list[i]
        page_url = selection.a['href']
        # print(page_url)
        article_soup = get_soup(page_url)
        if isinstance(article_soup, Exception):
            break

        articles = article_soup.find_all('article')
        for article in articles:
            post_id = post_id + 1
            post_headline = get_headline(article)
            post_url = article.header.h2.a['href']
            summary_soup = get_soup(post_url)
            if isinstance(summary_soup, Exception):
                return
            post_summary = get_summary(summary_soup)

            comments = get_comments(summary_soup)
            comment_id = 0
            comments_final_list = []
            anonymous = 1
            for comment in comments:
                comment_id = comment_id + 1
                comment_ref_id = 0
                username = get_username(comment)
                if username == 'Unknown' or username == 'Anonymous':
                    username = 'Anonymous_user_' + str(anonymous)
                    anonymous = anonymous + 1
                timestamp = get_timestamp(comment)
                msg = get_message(comment)

                if not (username == '' and msg == '' and timestamp == ''):
                    comm = Comment(comment_id, comment_ref_id, timestamp, username, "", msg)
                    comments_final_list.append(comm)
                else:
                    comment_id = comment_id - 1

                fail_condition = True
                while fail_condition:
                    try:
                        replies = comment.find('ol', class_='children').find_all('li')
                        comment_ref_id = comment_id
                        replied_to = username
                        # print(user)

                        for reply in replies:
                            comment_id = comment_id + 1
                            username = get_username(reply)
                            if username == 'Unknown' or username == 'Anonymous':
                                username = 'Anonymous_user_' + str(anonymous)
                                anonymous = anonymous + 1
                            timestamp = get_timestamp(reply)
                            msg = get_message(reply)

                            if not (username == '' and msg == '' and timestamp == ''):
                                comm = Comment(comment_id, comment_ref_id, timestamp, username, replied_to, msg)
                                comments_final_list.append(comm)
                            else:
                                comment_id = comment_id - 1

                        fail_condition = False
                    except Exception as e:
                        fail_condition = False

            posts.append(Post(post_id, post_headline, post_summary, post_url, comments_final_list))

    append_posts_to_file(file_name, posts)
    # print(post.id, post.comments)

    for post in posts:
        post_file_name = "blog3/post_" + str(post.id)
        append_post_to_file(post_file_name, post)

