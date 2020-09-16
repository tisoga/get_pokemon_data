import requests
from bs4 import BeautifulSoup

url = 'https://pokemondb.net/pokedex/national'
page = requests.get(url)
poke_name = []
soup = BeautifulSoup(page.content, 'html.parser')

def welcome():
    print('----------Pokedex Information Data---------------')
    status = True
    while status:
        gen = input('Sedang mencari informasi generasi ke berapa (1 - 8)? ')
        if gen.isdigit():
            if int(gen) >= 1 and int(gen) <= 8:
                status = False
            else:
                print('Kesalahan, Silahkan Masukan ')
                status = True
        else:
            print('Kesalahan, Silahkan Masukan ')
            status = True
    search_information(int(gen) - 1)

def search_information(gen):
    rs = soup.find_all('div', class_='infocard-list infocard-list-pkmn-lg')
    sections = rs[gen].find_all(class_='infocard')
    for section in sections:
        data = {}
        tipe = []
        name = section.find(class_='ent-name')
        type_poke = section.find_all('a', 'itype')
        for x in type_poke:
            tipe.append(x.text)
        data['name'] = name.text
        data['type'] = tipe
        poke_name.append(data)
    hasil(gen + 1)

def hasil(gen):
    status = True
    print('Jumlah Pokemon di generasi ke {} adalah {}'.format(gen, len(poke_name)))
    while status:
        qs = input('Apakah Anda Ingin Melihat Semua Pokemon di generasi ke {} (Y/N) ? '.format(gen))
        if qs.upper() == 'Y':
            check_pokemon()
            print('')  
        qs = input('Apakah Anda Ingin Mencari Informasi lagi (Y/N) ? ')
        if qs.upper() == 'Y':
            print('')
            poke_name.clear()
            welcome()
            status = False
        elif qs.upper() == 'N':
            status = False
        else:
            print('Kesalahan, Silahkan Pilih Kembali')
            status = True

def check_pokemon():
    for pokemon in poke_name:
        print('Name : ' + pokemon['name'])
        if len(pokemon['type']) == 1:            
            print('Type : ' + pokemon['type'][0])
        else:
            print('Type : ' + pokemon['type'][0] + ' , ' + pokemon['type'][1])
        print('')
welcome()
