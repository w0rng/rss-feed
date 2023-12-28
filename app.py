from datetime import datetime
from random import choices
from string import ascii_letters, digits

import requests
import urllib3
from feedparser import parse
from flask import Flask, render_template, make_response, request
from turbo_flask import Turbo

from models import db, Article, Feed, Read

app = Flask(__name__)
turbo = Turbo(app)
db.connect()
db.create_tables([Article, Feed, Read])


@app.route('/')
def feed():
    user = request.cookies.get('userID')
    if not user:
        user = ''.join(choices(ascii_letters + digits, k=16))

    read = Read.select().where(Read.user == user)
    read = [read.article.id for read in read]
    articles = Article.select().where(Article.id.not_in(read)).order_by(
        Article.created_at.desc())
    for article in articles:
        article.paragraphs = article.paragraphs.split('__')
        article.tags = article.tags.split('__')
    resp = make_response(render_template('index.html', articles=articles))
    resp.set_cookie('userID', user)
    return resp


@app.route('/article/<int:article_id>')
def article(article_id: int):
    article = Article.get(id=article_id)
    article.paragraphs = article.paragraphs.split('__')
    article.tags = article.tags.split('__')
    return render_template('article.html', article=article)


@app.route('/article/<int:article_id>/read')
def read_article(article_id: int):
    user = request.cookies.get('userID')
    if not user:
        user = ''.join(choices(ascii_letters + digits, k=16))
    try:
        article = Article.get(id=article_id)
        Read.create(article=article, user=user, created_at=datetime.now())
    except Article.DoesNotExist:
        pass
    return 'OK'


def new_article(url: str, feed: int):
    domain = urllib3.util.parse_url(url).host
    summery = requests.get(f'https://functions.yandexcloud.net/d4et1vtk7puk3hij7th2?url={url}').json()
    newspaper = requests.get(f'https://functions.yandexcloud.net/d4e09pp7rcsn53mvf23j?url={url}').json()
    tags = [domain]
    paragraphs = '__'.join(summery['paragraphs'])
    tags = '__'.join(tags)
    return Article.create(url=url, title=summery['title'], paragraphs=paragraphs, image=newspaper['image'],
                          tags=tags, feed=feed, created_at=datetime.now())


@app.route('/feed/<int:feed>/update')
def update_feed(feed: int):
    feed = Feed.get(id=feed)
    articles = parse(feed.url)['entries']
    for article in articles:
        try:
            Article.get(url=article.link)
        except Article.DoesNotExist:
            new_article(article.link, feed.id)
    return 'OK'


@app.route('/feed/add', methods=['POST'])
def add_feed():
    url = request.json['url']
    feed = Feed.create(url=url)
    update_feed(feed.id)
    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
