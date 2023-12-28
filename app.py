from datetime import datetime
from random import choices
from string import ascii_letters, digits

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
    articles_raw = Article.select().where(Article.id.not_in(read)).order_by(
        Article.created_at.desc()).limit(100)
    tag = request.args.get('tag')
    articles = []
    for article in articles_raw:
        article.paragraphs = article.paragraphs.split('__')
        article.tags = article.tags.split('__')
        if tag and tag not in article.tags:
            continue
        articles.append(article)
    resp = make_response(render_template('index.html', articles=articles))
    resp.set_cookie('userID', user, max_age=60*60*24*365*2)
    return resp


@app.route('/article/<int:article_id>')
def article(article_id: int):
    article = Article.get(id=article_id)
    article.paragraphs = article.paragraphs.split('__')
    article.tags = article.tags.split('__')
    article.count_read = Read.select().where(Read.article == article).count()
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


@app.route('/feeds')
def feeds():
    return render_template('feeds.html', feeds=Feed.select())


@app.route('/feeds/create', methods=['post'])
def new_feed():
    url = request.form.get('url')
    if url:
        Feed.create(url=url)
    return render_template('feeds.html', feeds=Feed.select())


@app.route('/feeds/<int:feed_id>/delete', methods=['post'])
def delete_feed(feed_id: int):
    Article.delete().where(Article.feed == feed_id).execute()
    Feed.get(id=feed_id).delete_instance()
    return render_template('feeds.html', feeds=Feed.select())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
