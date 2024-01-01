from fastapi import FastAPI
from newspaper import Article

app = FastAPI()


@app.get("/")
def main(url: str) -> dict[str, str | list[str]]:
    article = Article(url)
    article.download()
    article.parse()
    return {
        "image": article.top_image,
    }
