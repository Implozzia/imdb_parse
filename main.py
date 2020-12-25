import requests
import csv
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    else:
        print(r.status_code)


def split_cast(string):
    c = string.split('Stars:')[1]
    c = c.replace('\n', '')
    return c


def split_details(string):
    d = string.replace('\n', '')
    d = d.replace('Edit', '')
    d = d.replace('See more', '')
    d = d.replace('»', '')
    d = d.replace('See more', '')
    d = d.replace('on IMDbPro', '')
    d = d.replace('Details', 'Details:\n')
    d = d.replace('See full technical specs', '')
    return d


def write_csv(data):
    with open('films.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((
            data['name'],
            data['genre'],
            data['rate'],
            data['cast'],
            data['details']
        ))


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    titles = soup.find_all('div', class_='lister-item-content')
    for title in titles:
        try:
            name = title.find('a').text.strip()
        except:
            name = ''
        try:
            genre = title.find('span', class_='genre').text.strip()
        except:
            genre = ''
        try:
            rate = title.find('strong').text.strip()
        except:
            rate: ''
        try:
            c = title.find('p', class_='').text.strip()
            cast = split_cast(c)
        except:
            cast = ''

        try:
            detailsContent = get_html('https://www.imdb.com' + title.find('a').get('href'))
            soup = BeautifulSoup(detailsContent, 'lxml')
            d = soup.find('div', id='titleDetails').text.strip()
            details = split_details(d)
        except:
            details = ''

        data = {'name': name,
                'genre': genre,
                'rate': rate,
                'cast': cast,
                'details': details
                }
        write_csv(data)


def main():
    pattern = 'https://www.imdb.com/search/title/?title_type=feature&release_date=2000-02-25,2020-05-28&user_rating=4.0,10.0&genres=comedy&countries=us&start=1&ref_=adv_nxt'

    for i in range(1, 202, 50):
        url = pattern.format(str(i))
    get_data(get_html(pattern))


if __name__ == '__main__':
    main()
