import os
from bottle import route, run, request, post, get, redirect
import datetime
# import threading
import webbrowser
import html
import re
from bs4 import BeautifulSoup
import requests
import json


def get_pic_url(page_url):
    headers = {
        'Accept-Language': r'en-US,en;q=0.5',
        'Upgrade-Insecure-Requests': '1',
        'Accept-Encoding': r'gzip, deflate, br',
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Accept': r'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    r = requests.get(page_url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    script = soup.find('script', text=re.compile('window\._sharedData'))

    json_text = re.search(r'^\s*window\._sharedData\s*=\s*({.*?})\s*;\s*$', script.string, flags=re.DOTALL | re.MULTILINE).group(1)
    data = json.loads(json_text)
    return data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['display_url']


def get_user_image_links(profile_url):
    headers = {
        'Accept-Language': r'en-US,en;q=0.5',
        'Upgrade-Insecure-Requests': '1',
        'Accept-Encoding': r'gzip, deflate, br',
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Accept': r'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    r = requests.get(profile_url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    script = soup.find('script', text=re.compile('window\._sharedData'))
    json_text = re.search(r'^\s*window\._sharedData\s*=\s*({.*?})\s*;\s*$', script.string, flags=re.DOTALL | re.MULTILINE).group(1)
    data = json.loads(json_text)
    pics = [x['node'] for x in data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']]

    # return {x['display_url']: x['thumbnail_resources'][0]['src'] for x in pics}
    # return [{x['display_url']: x['thumbnail_resources'][0]['src']} for x in pics]
    return [(x['display_url'], x['thumbnail_resources'][0]['src']) for x in pics]


@get('/pic')  # or @route('/login')
def pic_form():
    return '''
        <!DOCTYPE html>
        <html>
            <head>
            <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
            <style>
            label{
                display: inline-block;
                float: left;
                clear: left;
                width: 125px;
                text-align: right;
            }
            input {
                display: inline-block;
                float: left;
            }
            </style>
            </head>
            <body>
                <form action="/pic" method="post">
                    <label>Picture URL: </label><input name="url" type="text" size="75" />
                    <label><input value="Submit" type="submit" />
                </form>
            </body>
        </html>
    '''


@get('/user')  # or @route('/login')
def user_form():
    return '''
        <!DOCTYPE html>
        <html>
            <head>
            <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
            <style>
            label{
                display: inline-block;
                float: left;
                clear: left;
                width: 125px;
                text-align: right;
            }
            input {
                display: inline-block;
                float: left;
            }
            </style>
            </head>
            <body>
                <form action="/user" method="post">
                    <label>User URL: </label><input name="url" type="text" size="75" />
                    <label><input value="Submit" type="submit" />
                </form>
            </body>
        </html>
        '''


@post('/pic')  # or @route('/login', method='POST')
def pic_redirector():
    page_url = request.forms.get('url')
    pic_url = get_pic_url(page_url)
    redirect(pic_url)


@post('/user')  # or @route('/login', method='POST')
def user_redirector():
    page_url = request.forms.get('url')
    user_images = get_user_image_links(page_url)
    image_divs = ''
    x = 1
    for pic in user_images:
        if x == 1:
            image_divs += r'<div>'
        image_divs += r'<a href="{0}"><img src="{1}" alt=""  /></a>'.format(pic[0], pic[1])
        if x % 3 == 0 and x != len(user_images):
            image_divs += r'</div><div>'

        x += 1
    image_divs += r'</div>'

    return '''
        <!DOCTYPE html>
        <html>
            <head>
            <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
            <style>
                div {{
                    text-align: justify;
                }}
                div img {{
                    display: inline-block;
                    width: 150px;
                    height: 150px;
                }}
                div:after {{
                    content: '';
                    display: inline-block;
                    width: 100%;
                }}
            </style>
            </head>
            <body>
            {0}
            </body>
        </html>
        '''.format(image_divs)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # threading.Timer(1.25, lambda: webbrowser.open('http://localhost:5000/pic')).start()
    run(host="0.0.0.0")

app = bottle.default_app()
