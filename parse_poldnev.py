"""
Script that parsing poldnev.ru, checking students factors
using Emotion API and creating 'visits.csv'.

@author: Seva Zhidkov
@license: MIT
"""

import csv
import json
import re
import requests
import lxml.html

POLDNEV_BASE_URL = 'http://poldnev.ru/lksh/id{}'
STUDENT_IMAGE_REGEX = re.compile(r'href=\\"https?://img-fotki.yandex.ru/get/.*_XXL')

print('Starting analysing data from poldnev.ru')
visits_file = open('visits.csv', 'w')
visits_writer = csv.writer(visits_file)
# First student id
student_id = 1
while True:
    student_page = requests.get(POLDNEV_BASE_URL.format(student_id)).text
    student_html = lxml.html.document_fromstring(student_page)
    student_name = student_html.find_class('header-center').pop().text_content()
    if 'Ошибка' in student_name:
        break
    student_photos = []
    for photo in re.findall(STUDENT_IMAGE_REGEX, student_page):
        # Delete a beginning ('href="') of the string
        student_photos.append(photo[7:])
    print(student_id, student_name, student_photos)
    student_id += 1

visits_file.close()
