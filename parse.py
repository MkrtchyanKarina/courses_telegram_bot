import requests


def get_category():
    url = 'https://stepik.org/api/catalog-blocks?platform=web'
    res = requests.get(url=url).json()['catalog-blocks'][0]['content']
    categories_and_courses = []
    for i in range(5):
        r = res[i]
        title = r['title']
        courses = r['courses'][:5]
        categories_and_courses.append([title, courses])
    return categories_and_courses


def request_id(id):
    url = f'https://stepik.org/api/courses/{id}'
    res = requests.get(url=url).json()
    title = res['courses'][0]['title']
    return title


