import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from django.conf import settings
from book.models import Author, Book, Publisher, ExtraInfo
from bucket import bucket


def _is_english(item):
    language_obj = item.find('div', class_='property_language')
    if language_obj and 'english' in language_obj.text:
        return True
    return False


def _is_pdf(item):
    type_obj = item.find('div', class_='property__file')
    if type_obj and 'PDF' in type_obj.text:
        return True
    return False


def _get_title(item):
    title_and_sub = item.find('h3', {'itemprop': 'name'}).text.split(":")
    return title_and_sub[0].strip()


def _get_subtitle(item):
    title_and_sub = item.find('h3', {'itemprop': 'name'}).text.split(":")
    return title_and_sub[1].strip() if len(title_and_sub) > 1 else ''


def _get_publisher(item):
    publisher_obj = item.find('a', {'title': 'Publisher'})
    return '' if publisher_obj is None else publisher_obj.text


def _get_authors(item):
    authors = []
    for author in item.find('div', class_='authors').findAll('a'):
        authors.append(author.text)
    return authors


def _get_year(item):
    year_obj = item.find('div', class_='property_year')
    return '' if year_obj is None else year_obj.find('div', class_='property_value').text


def _get_size(item):
    return item.find('div', class_='property__file').find('div', class_='property_value').text.split(',')[1].split('MB')[0].strip()


def _get_id(item):
    return item.find('td', class_='itemCover').find('div').get('data-book_id')


def _get_isbn(item):
    return item.find('td', class_='itemCover').find('div').get('data-isbn')


def _get_link(item):
    return item.find('td', class_='itemCover').find('a').get('href')


def _get_content(url):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    result = session.get(url, headers={
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
    })
    return BeautifulSoup(result.text, 'html.parser')


def _scrap_books(page=1):
    url = f'....?page={page}'
    content = _get_content(url)
    box = content.find('div', {'id': 'searchResultBox'})
    result = []
    for item in box.find_all('div', class_='resItemBox'):
        if _is_english(item) and _is_pdf(item):
            result.append({
                'title': _get_title(item),
                'sub_title': _get_subtitle(item),
                'publisher': _get_publisher(item),
                'authors': _get_authors(item),
                'year': _get_year(item),
                'size': _get_size(item),
                'slug': _get_id(item),
                'isbn': _get_isbn(item),
                'link': _get_link(item),
            })
    return result


def _scrap_remind_fields_book(url):
    content = _get_content(url)
    image_link = content.find('div', class_='details-book-cover-content').find('a').get('href')
    description_obj = content.find('div', {'id': 'bookDescriptionBox'})
    description = " " if description_obj is None else description_obj.text.strip()
    file_link_obj = content.find('a', class_='addDownloadedBook')
    if file_link_obj is None:
        return False
    file_link = content.find('a', class_='addDownloadedBook').get('href').strip()
    return image_link, description, file_link


def save_book_in_db(dict_book):
    authors = []
    for author in dict_book['authors']:
        author_obj = Author.objects.get_or_create(name=author)[0]
        authors.append(author_obj.id)
    publisher_id = Publisher.objects.get_or_create(name=dict_book['publisher'])[0]
    book_obj = Book.objects.create(
        title=dict_book['title'], sub_title=dict_book['sub_title'],
        publisher=publisher_id, published=2100 if dict_book['year'] == '' else dict_book['year'],
        size=dict_book['size'], slug=dict_book['slug'], isbn=dict_book['isbn'], link=dict_book['link'],
    )
    for author in authors:
        book_obj.authors.add(author)



def main_page_scrap_and_save_db():
    page_number_scraped = ExtraInfo.objects.filter(key='page_number_scraped').first()
    books = _scrap_books(page_number_scraped.value + 1)
    for dict_book in books:
        save_book_in_db(dict_book)
    page_number_scraped.value += 1
    page_number_scraped.save()


def book_scrap():
    queryset = Book.objects.filter(image_link='')
    if queryset.exists():
        book_obj = queryset.first()
        result = _scrap_remind_fields_book(book_obj.link)
        if not result:
            book_obj.delete()
        else:
            book_obj.image_link = result[0]
            book_obj.description = result[1]
            book_obj.file_link = result[2]
            book_obj.save()


def image_upload_s3():
    queryset = Book.objects.filter(image_link__startswith='htt',image__exact='1.jpg')
    if queryset.exists():
        book_obj = queryset.first()
        bucket.upload_object(book_obj.image_link, book_obj.slug)
        book_obj.image = f'{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{book_obj.slug}.jpg'
        book_obj.save()
