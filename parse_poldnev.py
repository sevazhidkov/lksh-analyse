"""
Script that parsing poldnev.ru, checking students factors
using Emotion API and creating 'visits.csv'.

@author: Seva Zhidkov
@license: MIT
"""

import os
import time
import csv
import json
import re
import requests
import lxml.html

POLDNEV_BASE_URL = 'http://poldnev.ru/lksh/id{}'
LAST_STUDENT_ID = 3024
STUDENT_IMAGE_REGEX = re.compile(r'href=\\"https?://img-fotki.yandex.ru/get/.*_XXL')
OCP_API_KEY = os.environ['OCP_API_KEY']
EMOTION_API_URL = 'https://api.projectoxford.ai/emotion/v1.0/recognize'


def detect_emotions(photo_url):
    # Emotion API limits
    time.sleep(2.5)
    response = requests.post(EMOTION_API_URL, headers={
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': OCP_API_KEY
    }, data=json.dumps({'url': photo_url}))
    faces = json.loads(response.text)
    if not faces:
        return None
    # If there are few faces, sort it by square of face rectangle
    faces.sort(
        key=lambda x: x['faceRectangle']['width'] * x['faceRectangle']['height'],
        reverse=True
    )
    return list(faces[0]['scores'].values())

print('Starting analysing data from poldnev.ru')
visits_file = open('visits.csv', 'a')
visits_writer = csv.writer(visits_file)
# First student id
student_id = 1
while student_id <= LAST_STUDENT_ID:
    student_page = requests.get(POLDNEV_BASE_URL.format(student_id)).text
    student_html = lxml.html.document_fromstring(student_page)
    student_name = str(student_html.find_class('header-center').pop().text_content())
    if 'Ошибка' in student_name:
        student_id += 1
        continue
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
        if 'class' not in row.attrib and not len(student_photos) == 1:
            continue
        try:
            emotions = detect_emotions(student_photos[photo_num])
        except IndexError:
            break
        if not emotions:
            photo_num += 1
            continue
        visits_writer.writerow(
            [student_id, student_name, visit_date,
             visit_position] + emotions
        )
        print(student_id, student_name, visit_date,
              visit_position, emotions, sep='|')
        photo_num += 1
    student_id += 1

visits_file.close()
