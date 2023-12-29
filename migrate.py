from asyncio import run

from tortoise import Tortoise

from models import Feed, Article, Read, Bookmark
from models_old import Feed as FeedOld, Article as ArticleOld, Read as ReadOld, Save as SaveOld


async def init():
    await Tortoise.init(
        db_url='postgres://postgres:postgres@db:5432/postgres',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()


async def main():
    await init()
    for feed in FeedOld.select():
        if await Feed.filter(id=feed.id).exists():
            continue
        await Feed(url=feed.url, id=feed.id).save()
    for article in ArticleOld.select():
        if await Article.filter(id=article.id).exists():
            continue
        await Article(url=article.url, title=article.title, paragraphs=article.paragraphs.split('__'),
                      image=article.image,
                      tags=article.tags.split('__'), feed_id=article.feed.id, created_at=article.created_at,
                      id=article.id).save()
    for read in ReadOld.select():
        if await Read.filter(id=read.id).exists():
            continue
        await Read(article_id=read.article.id, user=read.user, created_at=read.created_at, id=read.id).save()
    for save in SaveOld.select():
        if await Bookmark(id=save.id).exists():
            continue
        await Bookmark(article_id=save.article.id, user=save.user, created_at=save.created_at, id=save.id).save()


if __name__ == '__main__':
    run(main())
