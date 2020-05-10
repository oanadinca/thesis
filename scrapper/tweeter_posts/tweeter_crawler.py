import sys
import requests
import requests_oauthlib
import json
import csv

# Replace the values below with yours
ACCESS_TOKEN = '1244562342920302593-yE96kjC9iSrZaMBLoJ9DMIuuC0p9ri'
ACCESS_SECRET = '8Vhjnd5woJVwYhYVvASyqLaWp2kmIosUHgpeyelE4pmI8'
CONSUMER_KEY = 'opTgnFRoHDEIZdRXIYEyOPgXa'
CONSUMER_SECRET = '956jIdpPfhFMcEjZvHhQLPjfTEMuJJa4s5OHMioHncppouD4cd'
my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)


def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        #trebuie sa verific ce am in list_of_elem si aici sa modific ce printez ca am un json si mna
        csv_writer.writerow(list_of_elem)


def get_tweets():
    url = 'https://stream.twitter.com/1.1/statuses/filter.json'
    # query_data = [('language', 'en'), ('locations', '-130,-20,100,50'),('track','#')]
    query_data = [('language', 'en'), ('track', 'coronavirus')]
    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    response = requests.get(query_url, auth=my_auth, stream=True)
    print(query_url, response)
    return response


def send_tweets_to_db(http_resp, file_name):
    num_tweets = 0
    for line in http_resp.iter_lines():
        try:
            full_tweet = json.loads(line)
            print(full_tweet['retweeted_status'])
            append_list_as_row(file_name, full_tweet)
            num_tweets += 1
            if num_tweets > 10:
                break
        except:
            e = sys.exc_info()[0]
            print("Error: %s" % e)


def main():
    file_name = 'tweeter_posts/tweeter_crawler.csv'
    resp = get_tweets()
    send_tweets_to_db(resp, file_name)


