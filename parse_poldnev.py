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


def detect_emotions(photo_url):
    pass


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
    student_name = str(student_html.find_class('header-center').pop().text_content())
    if 'Ошибка' in student_name:
        break
    student_photos = []
    for photo in re.findall(STUDENT_IMAGE_REGEX, student_page):
        # Delete a beginning ('href="') of the string
        student_photos.append(photo[7:])
    # First row - names of columns
    visits_rows = student_html.get_element_by_id('person-table').getchildren()[1:]
    photo_num = 0
    for row in visits_rows:
        # row[1] - year and month, row[2] - position
        visit_date = row[1].text_content()
        visit_position = row[2].text_content()
        # If there is no photo for this visit - continue to next student visit
        if 'class' not in row.attrib:
            continue
        print(student_id, student_name, visit_date,
              visit_position, student_photos[photo_num])
        photo_num += 1
    student_id += 1

visits_file.close()
