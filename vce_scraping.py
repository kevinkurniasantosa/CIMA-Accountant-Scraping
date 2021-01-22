import requests
import csv
import copy
import datetime
import time
import random
from threading import Thread
import smtplib
import mimetypes
import string
import os
import os.path
import traceback
import pprint
from bs4 import BeautifulSoup
import math
import calendar
import time
import logging
import pandas as pd
from itertools import islice
from pathlib import Path
from datetime import datetime
import json
import urllib
from bs4 import NavigableString as nav
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

print('import success')
print('--------------------------')

def clean_string(x):
    try:
        x=x.replace('\"','\'\'').replace('\r',' ').replace('\n',' ')
        x=unicodedata.normalize('NFKD', x).encode('ascii', 'ignore')
        x=x.decode('ascii')
    except:
        x='?'

    return x
    
def vce_scraping(data, file):
    main_url = 'https://vceguide.com/comptia/sy0-501-comptia-security-v2/'
    res = requests.get(main_url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.text, 'html.parser')

    wrapper = soup.find('div', class_='wrap_page')
    list_ul = wrapper.find_all('ul')

    for ul in list_ul:
        print('----------------------------')
        list_li = ul.find_all('li')
        
        for i, li in enumerate(list_li):
            ## Get question number
            question_num_str = li.a.text.strip()
            print(str(question_num_str))
            x = re.match("Question (\d+)", str(question_num_str))
            question_num = x.group(1)

            ## Get each question link
            question_url = li.find('a', href=True)['href']
            print('URL: ' + str(question_url))
            
            ## Request for each question link
            res_url = requests.get(question_url, headers={'User-Agent': 'Mozilla/5.0'})
            soup_url = BeautifulSoup(res_url.text, 'html.parser')

            ## ID
            if int(question_num) < 10:
                # id = "{0:03}".format(int(question_num)) 
                id = "00{}".format(int(question_num))
            elif int(question_num) >= 10 and int(question_num) < 100:
                id = "0{}".format(int(question_num)) 
            else:
                id = "{}".format(int(question_num)) 
            print('ID: ' + str(id))

            content = soup_url.find('div', class_='entry-content')
            ## Question
            try:
                question = content.find('p').text.strip()
                question = question.replace('\n', ' ')
                x = re.match("(.+) A\.", str(question))
                question = x.group(1)
            except:
                question = ""

            print('Question: ' + str(question))

            ## ANSWERS CHOICES
            answer_choices = content.find_all('p')[0].find_all('strong')

            ## A
            try:
                a_choice = answer_choices[0].text.strip()
                x = re.match("A. (.+)", str(a_choice))
                a_choice = x.group(1)
            except:
                a_choice = ""
            print('A: ' + str(a_choice))

            ## B
            try:
                b_choice = answer_choices[1].text.strip()
                x = re.match("B. (.+)", str(b_choice))
                b_choice = x.group(1)
            except:
                b_choice = ""
            print('B: ' + str(b_choice))

            ## C
            try:
                c_choice = answer_choices[2].text.strip()
                x = re.match("C. (.+)", str(c_choice))
                c_choice = x.group(1)
            except:
                c_choice = ""
            print('C: ' + str(c_choice))

            ## D
            try:
                d_choice = answer_choices[3].text.strip()
                if 'Correct Answer' in d_choice:
                    d_choice = ""
                else:
                    x = re.match("D. (.+)", str(d_choice))
                    d_choice = x.group(1)
            except:
                d_choice = ""
            print('D: ' + str(d_choice))

            ## E
            try:
                try:
                    e_choice = answer_choices[4].text.strip()
                    if 'Correct Answer' in e_choice:
                        e_choice = ""
                    else:
                        x = re.match("E. (.+)", str(e_choice))
                        e_choice = x.group(1)
                except:
                    e_choice = ""
                    pass
            except:
                e_choice = ""
            print('E: ' + str(e_choice))

            ## F
            try:
                try:
                    f_choice = answer_choices[5].text.strip()
                    if 'Correct Answer' in f_choice:
                        f_choice = ""
                    else:
                        x = re.match("F. (.+)", str(f_choice))
                        f_choice = x.group(1)
                except:
                    f_choice = ""
                    pass
            except:
                f_choice = ""
            print('F: ' + str(f_choice))

            ## G
            try:
                try:
                    g_choice = answer_choices[6].text.strip()
                    if 'Correct Answer' in g_choice:
                        g_choice = ""
                    else:
                        x = re.match("G. ()", str(g_choice))
                        g_choice = x.group(1)
                except:
                    g_choice = ""
                    pass
            except:
                g_choice = ""
            print('G: ' + str(g_choice))

            ## Answer
            try:
                answer = content.find('div', class_='sh-content').span.text.strip()
                y = re.match("Correct Answer: (.+)", str(answer))
                answer = y.group(1)
            except:
                answer = '-'
            print('Answer: ' + str(answer))

            dict_result = {
                "id": id,
                "version": "",
                "question": question,
                "media": "",
                "A": a_choice,
                "B": b_choice,
                "C": c_choice,
                "D": d_choice,
                "E": e_choice,
                "F": f_choice,
                "G": g_choice,
                "answer": answer,
                "explanation": ""
            }

            data.append(dict_result) 
            print('updated')

        print('=== DIFFERENT PAGE ===')

    json.dump(data, file, indent=2, sort_keys=False)

def main():
    with open("questions_answers_vce_comp_security.json", "r+") as file:
        data = json.load(file)
        vce_scraping(data, file)
        # data.update(dict_result)
        # file.seek(0)
        # json.dump(data, file)

if __name__ == '__main__':
    main()
    

