"""
Script that parsing poldnev.ru, checking students factors
using Emotion API and creating 'visits.csv'.

@author: Seva Zhidkov
@license: MIT
"""

import csv
import json
import requests
import lxml.html

POLDNEV_BASE_URL = 'http://poldnev.ru/lksh/id{}'


print('Starting analysing data from poldnev.ru')
visits_file = open('visits.csv', 'w')
visits_writer = csv.writer(visits_file)
# First student id
student_id = 1
while True:
    student_page = lxml.html.parse(POLDNEV_BASE_URL.format(student_id)).getroot()
    student_id += 1

visits_file.close()
