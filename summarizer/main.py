from os import environ

import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def main(url: str) -> dict[str, str | list[str]]:
    summary_url = requests.post(
        "https://300.ya.ru/api/sharing-url",
        json={
            "article_url": url,
        },
        headers={"Authorization": f'OAuth {environ["YANDEX_300_TOKEN"]}'},
    ).json().get("sharing_url")

    if not summary_url:
        return {"error": "яндекс не смог перевести"}

    page = requests.get(summary_url)
    text = page.text.encode("latin-1").decode("utf-8")
    soup = BeautifulSoup(text, "html.parser")
    title = soup.find("h1", class_="title").text.strip()
    paragraphs = [p.text.replace("• ", "").strip() for p in soup.find_all("span", class_="text-wrapper")]
    return {"title": title, "paragraphs": paragraphs}
