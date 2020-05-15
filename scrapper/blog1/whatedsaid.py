from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import datetime
from data_model.blogposts import Post, Comment, Contribution
import csv


def get_last_post_id_from_file(file_name):
    with open(file_name, 'r') as reader_obj:
        csv_reader = csv.reader(reader_obj)

        for row in reversed(list(csv_reader)):
            return int(row[0])

    return -1


def append_posts_to_file(file_name, posts):
    for post in posts:
        if len(post.comments) == 0:
            append_list_as_row(file_name, [post.id, post.headline, post.summary,
                                           post.timestamp, post.author, post.url,
                                           '', '', '', '', '', ''])
        else:
            for comment in post.comments:
                append_list_as_row(file_name, [post.id, post.headline, post.summary,
                                               post.timestamp, post.author, post.url,
                                               comment.genid, comment.ref, comment.time,
                                               comment.nickname,
                                               comment.text])


def append_post_to_file(file_name, post):
    # if len(post.comments) == 0:
    #     append_list_as_row(file_name, [post.id, post.headline, post.summary,
    #                                    post.timestamp, post.author, post.url,
    #                                    '', '', '', '', '', ''])
    # else:
    for comment in post.comments:
        append_list_as_row(file_name, [
                                        # post.id, post.headline, post.summary,
                                        # post.timestamp, post.author, post.url,
                                        comment.genid, comment.ref, comment.time,
                                        comment.nickname,
                                        comment.text])


def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'a+', newline='', encoding='utf8') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(list_of_elem)


def first_open_csv(file_name, fieldnames):
    with open(file_name, 'w', encoding='utf8') as writer_file:
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
    return article.header.h1.a.text


def get_summary(soup):
    summary_list = soup.find('div', class_='entry-content').find_all('p')
    post_summary = ""
    for s in summary_list:
        post_summary = post_summary + " " + s.text.replace('\n', '').replace('\t', '') \
            # .replace('\U0001f642', ':)').replace('मुलांचे हक्क', '')
    # print(post_summary)
    return post_summary


def get_post_timestamp(soup):
    try:
        date = soup.find('span', class_='posted-on').a.time.text.replace('\n', '').replace('\t', '')
        parsed_date = parse(date)
        timestamp = datetime.datetime.timestamp(parsed_date)
    except Exception as e:
        timestamp = ''
    return timestamp


def get_post_username(soup):
    try:
        username = soup.find('span', class_='author vcard').a.text
    except Exception as e:
        username = ''

    return username


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
        like_buttons = comment.find('div', class_='comment-content').find('p',
                                                                          class_='comment-likes comment-not-liked')
        if like_buttons in msg_list:
            msg_list.remove(like_buttons)
        for m in msg_list:
            msg = msg + m.text.replace('\n', '').replace('\t', '') \
                # .replace('\U0001f642', ':)')
    except Exception as e:
        msg = ''
    return msg


def main(args):
    post_id = 0
    posts = []
    postsJSON = []

    file_name = 'blog1/whatedsaid_scrape.csv'
    fieldnames = ['post_id', "post_headline", "post_summary", "post_timestamp", "post_author", "post_url",
                  "comment_id", "comment_ref_id",
                  "comment_timestamp", "comment_username", "comment_replied_to", "comment_message"]
    try:
        post_id = get_last_post_id_from_file(file_name)
    except Exception as e:
        first_open_csv(file_name, fieldnames)

    page_soup = get_soup(args.url)
    if isinstance(page_soup, Exception):
        return

    archive_list = page_soup.find('select', id='archives-dropdown-5').find_all('option')
    archive_list.pop(0)  # select month phrase with no url to use

    for i in range(0, 2):
        selection = archive_list[i]
        page_url = selection['value']
        # print(page_url)
        article_soup = get_soup(page_url)
        if isinstance(article_soup, Exception):
            break

        articles = article_soup.find_all('article')
        for article in articles:
            post_id = post_id + 1
            post_headline = get_headline(article)
            post_url = article.header.h1.a['href']
            summary_soup = get_soup(post_url)
            if isinstance(summary_soup, Exception):
                return
            post_summary = get_summary(summary_soup)
            post_timestamp = get_post_timestamp(summary_soup)
            post_author = get_post_username(summary_soup)

            comments = get_comments(summary_soup)
            comment_id = 0
            comments_final_list = [Comment(0, 0, post_timestamp, post_author, "", post_summary)]
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
                    comm = Comment(comment_id, comment_ref_id, timestamp, username, post_author, msg)
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

            post = Post(post_id, post_headline, post_summary, post_timestamp, post_author,
                        post_url, comments_final_list)
            posts.append(post)

            # ElasticSearch model
            contribution = Contribution(post_id, comments_final_list)
            postsJSON.append(contribution)

    append_posts_to_file(file_name, posts)

    for post in posts:
        post_file_name = "blog1/post_" + str(post.id)
        append_post_to_file(post_file_name, post)

    return postsJSON
