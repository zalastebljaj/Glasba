import re
import orodja
import time

vzorec = re.compile(
    r'name="\d*"><b>(?P<rank>\d+\.)</b></a><br.*?'
    r'album\."\shref="thechart.php\?a=\d*">(?P<naslov>.*?)</a>.*?'
    r'href="thechart.php\?b=\d*">(?P<avtor>.*?)</a></t.*?'
    r'Year of Release:.*?>(?P<leto>\d{4})</td><td width.*?'
    r'&nbsp;(?P<ocena>\d+)/100 \((?P<st_ocen>.+?) votes\).*?'
    r'alt="">\s(?P<st_komentarjev>\d+)\scomment',
    re.DOTALL
)


def pocisti_podatke(ujemanje_filma):
    podatki = ujemanje_filma.groupdict()
    podatki['leto'] = int(podatki['leto'])
    podatki['ocena'] = int(podatki['ocena'])
    podatki['st_ocen'] = int(podatki['st_ocen'].replace(',', ''))
    podatki['st_komentarjev'] = int(podatki['st_komentarjev'])
    return podatki

#for i in range(1, 251):
 #   url = ('https://www.besteveralbums.com/topratedstats.php?rs='
  #         '&o=album&d=0&y=0&r=10&ur=0&l=0&cp=1&orderby=Rank&sortdir=asc'
   #        '&page={}'
    #).format(i)
    #orodja.shrani_spletno_stran(url, 'glasba-{}.html'.format(i))
    #time.sleep(1)

podatki_filmov = []
for i in range(1, 101):
    vsebina = orodja.vsebina_datoteke('glasba_strani/glasba-{}.html'.format(i))
    for ujemanje_filma in vzorec.finditer(vsebina):
        podatki_filmov.append(pocisti_podatke(ujemanje_filma))
        #print(pocisti_podatke(ujemanje_filma))
orodja.zapisi_csv(
    podatki_filmov,
    ['rank', 'naslov', 'avtor', 'leto', 'ocena', 'st_ocen', 'st_komentarjev'],
    'albumi.csv'
    )
orodja.zapisi_json(podatki_filmov, 'albumi.json')
