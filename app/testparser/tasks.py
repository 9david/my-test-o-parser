from celery import shared_task
from bs4 import BeautifulSoup
import re


@shared_task
def task_parser(html_content, num):
    data_list = []

    soup = BeautifulSoup(html_content, 'html.parser')

    # НАХОДИМ ВСЕ ЭЛЕМЕНТЫ С КЛАССОМ "... ... tile-root"
    pattern = re.compile(r'\b\w*\d\w*\b\s+\b\w*\d\w*\b\s+tile-root\b')
    divs = soup.find_all('div', class_=pattern)

    if not len(divs):
        raise 'Видимо поменялись теги, проверь!'

    for div in divs[:num]:
        data_dict = {'name':'', 'price':0, 'discount':'', 'image_url':'', 'description':''}
        # NAME, PRICE AND DISCOUNT
        # Находим текст внутри тега <span class="tsBody500Medium">
        name = div.find('span', class_='tsBody500Medium').text
        # print(name)
        data_dict['name'] = name

        # Находим текст внутри тега <span class="c305-a1 tsHeadline500Medium c305-c0">
        price = div.find('span', class_='c305-a1 tsHeadline500Medium c305-c0').text
        # print(price)
        data_dict['price'] = int(price.replace('\u2009', '').replace('₽', ''))

        # Находим текст внутри тега <span class="tsBodyControl400Small c305-a2 c305-a7 c305-b1">
        discount = div.find('span', class_='tsBodyControl400Small c305-a2 c305-a7 c305-b1').get_text()
        # print(discount)
        data_dict['discount'] = discount

        # IMAGE_URL AND DESCRIPTION_URL
        # Находим атрибут src внутри тега <div class="...">
        pattern = re.compile(r'\b\w*\d\w*\b\s+\b\w*\d\w*\b')
        image_url = div.find('img', class_=pattern)['src']
        # print(image_url)
        data_dict['image_url'] = image_url

        # Находим href внутри тега <a class="tile-hover-target ... ...">
        pattern = re.compile(r'\btile-hover-target\b\s+\b\w*\d\w*\b\s+\b\w*\d\w*\b')
        description = div.find('a', class_=pattern).get('href')
        # print(description)
        data_dict['description'] = 'https://www.ozon.ru' + description

        data_list.append(data_dict)

        if not name or not price or not discount or not image_url or not description:
            raise('Проверь данные, где-то сохранилось пустое значение. Возможно где-то поменялся тег!')

    return data_list

