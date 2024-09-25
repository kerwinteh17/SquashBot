from requests_html import HTMLSession
import tweepy
import os
import random

session = HTMLSession()
url = 'https://clublocker.com/teams/33722/results'
r = session.get(url)
print(r)
r.html.render(sleep=3, keep_page=True, scrolldown=1)
print(r.html.text)


def authenticate():
    all_keys = open('twitterBot/twitterkeys', 'r', ).read().splitlines()
    api_key = all_keys[0]
    api_key_secret = all_keys[1]
    access_token = all_keys[2]
    access_token_secret = all_keys[3]

    authenticator = tweepy.OAuthHandler(api_key, api_key_secret)
    authenticator.set_access_token(access_token, access_token_secret)

    api = tweepy.API(authenticator, wait_on_rate_limit=True)
    return api

def get_team_score():
    team_score = r.html.find('.match-container')
    score_text = team_score[0].text
    score_text = score_text.splitlines()
    winner = score_text[0][8:-6]
    score = score_text[0][-5:]
    teams = r.html.find('.name')
    home_team = teams[2].text[:-3]
    away_team = teams[3].text[4:]
    if winner == home_team:
        loser = away_team
    else:
        loser = home_team

    result = winner + ' ' + score + ' ' + loser
    return result

def randomImage():
    os.chdir('twitterBot/pics')
    dir_list = os.listdir('.')
    image = random.choice(dir_list)
    size_bytes = os.stat(image).st_size
    size_mbytes = size_bytes / (1024 * 1024)
    while image == '.DS_Store' or size_mbytes > 3.0:
        image = random.choice(dir_list)
        size_bytes = os.stat(image).st_size
        size_mbytes = size_bytes / (1024 * 1024)
    return image

def tweet(api):
    actual_result = 'RESULT:\n' + get_team_score()
    image = randomImage()
    api.update_status_with_media(actual_result, image)
    os.remove(image)

if __name__ == "__main__":
    tweet(authenticate())

