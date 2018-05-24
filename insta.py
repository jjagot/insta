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


@post('/pic')  # or @route('/login', method='POST')
def pic_redirector():
    page_url = request.forms.get('url')
    pic_url = get_pic_url(page_url)
    redirect(pic_url)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # threading.Timer(1.25, lambda: webbrowser.open('http://localhost:5000/pic')).start()
    # run(host="0.0.0.0", port=port, debug=True, reloader=False, workers=1)
    run(host="0.0.0.0", port=port)

app = bottle.default_app()
