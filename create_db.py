# перебираем xml по указанному пути
# из каждого файла вытаскиваем данные в list(namedtuple)
# собранные данные токенизируем, нормализуем, делаем морфологический анализ
# результат каждой обработки записываем в свой list(namedtuple)
# все листы записываем в БД

import glob
import os
import subprocess
import sh
from tqdm import tqdm
from xml.dom import minidom
from collections import namedtuple
from sacremoses import MosesPunctNormalizer
from sacremoses import MosesTokenizer

# получаем список файлов *.xml с новостями на казахском
dir_with_xml = "/media/zhake/Data/Projects/kaz-parallel-corpora/akorda_kz/xml/"
xml_files = glob.glob(dir_with_xml + "*kaz.xml")

news_item = namedtuple("news_item", "url section title date_time text")
news_items = []

# из каждого файла вытаскиваем данные в list(namedtuple)
for xml_file in tqdm(xml_files):
    # open a file
    kaz_xml_data = minidom.parse(xml_file)
    kaz_xml_data.normalize()
    # extract urls
    if len(kaz_xml_data.getElementsByTagName("url")[0].childNodes) == 0:
        kaz_url = ""
    else:
        kaz_url = kaz_xml_data.getElementsByTagName("url")[0].childNodes[0].nodeValue
    # extract sections
    if len(kaz_xml_data.getElementsByTagName("section")[0].childNodes) == 0:
        kaz_section = ""
    else:
        kaz_section = (
            kaz_xml_data.getElementsByTagName("section")[0].childNodes[0].nodeValue
        )
    # extract titles
    if len(kaz_xml_data.getElementsByTagName("title")[0].childNodes) == 0:
        kaz_title = ""
    else:
        kaz_title = (
            kaz_xml_data.getElementsByTagName("title")[0].childNodes[0].nodeValue
        )
    # extract date_times
    if len(kaz_xml_data.getElementsByTagName("date_time")[0].childNodes) == 0:
        kaz_date_time = ""
    else:
        kaz_date_time = (
            kaz_xml_data.getElementsByTagName("date_time")[0].childNodes[0].nodeValue
        )
    # extract text
    if len(kaz_xml_data.getElementsByTagName("text")[0].childNodes) == 0:
        kaz_text = ""
    else:
        kaz_text = kaz_xml_data.getElementsByTagName("text")[0].childNodes[0].nodeValue

    kaz_title = kaz_title.replace('"', "")
    kaz_text = kaz_text.replace('"', "")

    tmp_data = news_item(
        url=kaz_url,
        section=kaz_section,
        title=kaz_title,
        date_time=kaz_date_time,
        text=kaz_text,
    )

    news_items.append(tmp_data)

# собранные данные токенизируем, нормализуем, делаем морфологический анализ
# результат каждой обработки записываем в свой list(namedtuple)

# токенизация
tokenized_news_items = []
mpn = MosesPunctNormalizer()
mtok = MosesTokenizer()

for item in tqdm(news_items):
    tokenized_text = mpn.normalize(text=item.text)
    tokenized_text = mtok.tokenize(text=tokenized_text, return_str=True)

    tmp_data = news_item(
        url=item.url,
        section=item.section,
        title=item.title,
        date_time=item.date_time,
        text=tokenized_text,
    )

    tokenized_news_items.append(tmp_data)

# нормализация
# normalized_news_items = []
# APERTIUM_KAZ_PATH = "/home/zhake/Source/apertium-kaz/"

# for item in news_items:
#     tmp_out = sh.echo(item.text)
#     tmp_out = sh.apertium(tmp_out, "-d", APERTIUM_KAZ_PATH, "kaz-morph")
#     tmp_out = sh.sed(tmp_out, "-e", "s/\$\W*\^/$\\n^/g")
#     tmp_out = sh.cut(tmp_out, "-f2", "-d", "/")
#     tmp_out = sh.cut(tmp_out, "-f1", "-d", "<")

#     normalized_text = tmp_out

#     tmp_data = news_item(
#         url=item.url,
#         section=item.section,
#         title=item.title,
#         date_time=item.date_time,
#         text=normalized_text
#     )

#     normalized_news_items.append(tmp_data)

# print(normalized_news_items[55])


# все листы записываем в БД
import sqlite3

conn = sqlite3.connect("db/akorda.sqlite")

cursor = conn.cursor()

for item in tqdm(news_items):
    sql = "insert into data (url, section, title, date_time, text) values("
    sql += (
        '"' + item.url + '"'
        + ", "
        + '"' + item.section + '"'
        + ", "
        + '"' + item.title + '"'
        + ", "
        + '"' + item.date_time + '"'
        + ", "
        + '"' + item.text + '"'
        + ");"
    )
    cursor.execute(sql)
conn.commit()

for item in tqdm(tokenized_news_items):
    sql = "insert into tokenized_data (url, section, title, date_time, text) values("
    sql += (
        '"' + item.url + '"'
        + ", "
        + '"' + item.section + '"'
        + ", "
        + '"' + item.title + '"'
        + ", "
        + '"' + item.date_time + '"'
        + ", "
        + '"' + item.text + '"'
        + ");"
    )
    cursor.execute(sql)
conn.commit()

