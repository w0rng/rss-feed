import requests
from bs4 import BeautifulSoup


def summary(url: str) -> tuple[str, list[str]]:
    summary_url = requests.post(
        'https://300.ya.ru/api/sharing-url',
        json={
            'article_url': url,
        },
        headers={'Authorization': 'OAuth y0_AgAAAAAiGsYSAAoX4wAAAAD2JILXvjT80r0mS1S08Bjaw6P2yuINkBg'}
    ).json()['sharing_url']

    page = requests.get(summary_url)
    text = page.text.encode('latin-1').decode('utf-8')
    soup = BeautifulSoup(text, 'html.parser')
    title = soup.find('h1', class_='title').text.strip()
    paragraphs = [p.text.replace('• ', '').strip() for p in soup.find_all('span', class_='text-wrapper')]
    return title, paragraphs
