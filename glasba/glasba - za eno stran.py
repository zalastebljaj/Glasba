import csv
import re
import os
import requests
import json

BEA_url = 'https://www.besteveralbums.com/topratedstats.php?o=album'
BEA_directory = 'glasba_strani'
BEA_dat = 'glasba.html'
BEA_csv = 'glasba.csv'


with open('glasba_strani/glasba.html') as datoteka:
    vsebina = datoteka.read()

vzorec = re.compile(
    r'name="\d*"><b>(?P<rank>\d+\.)</b></a><br.*?'
    r'album\."\shref="thechart.php\?a=\d*">(?P<naslov>.*?)</a>.*?'
    r'href="thechart.php\?b=\d*">(?P<avtor>.*?)</a></t.*?'
    r'Year of Release:.*?>(?P<leto>\d{4})<.*?'
    r'&nbsp;(?P<ocena>\d+)/100 \((?P<st_ocen>.+?) votes\).*?'
    r'alt=""> (?P<st_komentarjev>\d+) comments</a>',
    re.DOTALL
)

# for ujemanje in vzorec.finditer(vsebina):
#     print(ujemanje,group(1))

# with open('albumi1.csv', 'w') as dat:
#     print('naslov', file=dat)
#     for ujemanje in re.finditer(vzorec, vsebina, re.DOTALL):
#         print('{}'.format(ujemanje.group(1)), file=dat)


def pocisti_podatke(podatki):
    podatki['leto'] = int(podatki['leto'])
    podatki['ocena'] = int(podatki['ocena'])
    podatki['st_ocen'] = int(podatki['st_ocen'].replace(',', ''))
    podatki['st_komentarjev'] = int(podatki['st_komentarjev'])
    return podatki

podatki_filmov = []
with open('albumi.csv', 'w', encoding='utf8') as csv_datoteka:
    writer = csv.DictWriter(
        csv_datoteka,
        ['rank', 'naslov', 'avtor', 'leto',
         'ocena', 'st_ocen', 'st_komentarjev']
    )
    writer.writeheader()
    for ujemanje in vzorec.finditer(vsebina):
        podatki_filma = pocisti_podatke(ujemanje.groupdict())
        writer.writerow(podatki_filma)
        podatki_filmov.append(podatki_filma)
with open('albumi.json', 'w') as json_datoteka:
    json.dump(podatki_filmov, json_datoteka, indent=4, ensure_ascii=False)


def url_to_string(url):
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('Stran ne obstaja!')
        return None
    else:
        return r.text


def save_string_to_file(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf8') as file_out:
        file_out.write(text)
    return None


def shrani_stran(url):
    text = url_to_string(BEA_url)
    return save_string_to_file(text, BEA_directory, BEA_dat)
