import requests
import csv
from bs4 import BeautifulSoup

with open('pokemon_list.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'Pokemon', 'Type 1', 'Type 2','Generations'])

url = 'https://pokemondb.net/pokedex/national'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')


def write_new(id, name, tipe, generations):
    with open('pokemon_list.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if len(tipe) == 1:
            writer.writerow([id, name, tipe[0].text, '', generations])
        else:
            writer.writerow([id, name, tipe[0].text, tipe[1].text, generations])


gens = soup.find_all('div', class_='infocard-list infocard-list-pkmn-lg')
generations = 0
for gen in gens:
    generations += 1
    pokemons = gen.find_all('span', class_='infocard-lg-data text-muted')
    for pokemon in pokemons:
        id = pokemon.find('small')
        name = pokemon.find(class_='ent-name')
        tipe = pokemon.find_all('a', class_='itype')
        write_new(id.text, name.text, tipe, generations)
