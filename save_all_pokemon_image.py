import requests
import shutil
import os
from bs4 import BeautifulSoup

url = 'https://pokemondb.net/pokedex/national'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
count = 0
generations = soup.find_all(
    'div', class_='infocard-list infocard-list-pkmn-lg')

if not os.path.exists('pokedex'):
    os.makedirs('pokedex')

for gen in generations:
    count += 1
    gen_name = 'Generations {}'.format(count)
    pokemons = gen.find_all('span', class_='infocard-lg-data text-muted')
    images = gen.find_all('span', class_='infocard-lg-img')
    print(gen_name)
    if not os.path.exists('pokedex/{}'.format(gen_name)):
        os.makedirs('pokedex/{}'.format(gen_name))
    for pokemon, img in zip(pokemons, images):
        id = pokemon.find('small')
        name = pokemon.find('a', class_='ent-name')
        if os.path.exists('pokedex/{}/{}.png'.format(gen_name, id.text+' '+name.text)):
            continue
        image = img.find('span', class_='img-fixed img-sprite')
        req = requests.get(image['data-src'], stream=True)
        if req.status_code == 200:
            with open('pokedex/{}/{}.png'.format(gen_name, id.text+' '+name.text), 'wb') as f:
                req.raw.decode_content = True
                shutil.copyfileobj(req.raw, f)
    print('{} Completed'.format(gen_name))