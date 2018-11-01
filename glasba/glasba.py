import csv
import re
import os
import requests

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
    r'Year of Release:.*?>(?P<leto>\d+)<.*?'
    r'&nbsp;(?P<ocena>\d+)/100 \((?P<št_ocen>.+?) votes\).*?'
    r'alt=""> (?P<št_komentarjev>\d+) comments</a>',
    re.DOTALL
)

# for ujemanje in vzorec.finditer(vsebina):
#     print(ujemanje,group(1))

# with open('albumi1.csv', 'w') as dat:
#     print('naslov', file=dat)
#     for ujemanje in re.finditer(vzorec, vsebina, re.DOTALL):
#         print('{}'.format(ujemanje.group(1)), file=dat)

with open('albumi.csv', 'w', encoding='utf8') as datoteka:
    writer = csv.writer(datoteka)
    writer.writerow(
            ('rank',
             'naslov',
             'avtor',
             'leto',
             'ocena',
             'št_ocen',
             'št_komentarjev')
    )
    for ujemanje in vzorec.finditer(vsebina):
        print(ujemanje.groupdict())
        writer.writerow(
                (ujemanje.group(1),
                 ujemanje.group(2),
                 ujemanje.group(3),
                 ujemanje.group(4),
                 ujemanje.group(5),
                 ujemanje.group(6),
                 ujemanje.group(7))
        )


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
