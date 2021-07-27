import asyncio

import aiohttp as aiohttp
import requests
from database import async_main


SW_API = 'https://swapi.dev/api/people/'


async def get_person(url: str):
    async with aiohttp.client.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


def name_generator(url_list):
    try:
        for url in url_list:
            r = requests.get(url)
            yield r.json()['name']
    except KeyError:
        for url in url_list:
            r = requests.get(url)
            yield r.json()['title']


async def get_homeworld_name(url: str):
    async with aiohttp.client.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def get_sw_people():
    star_war_persons_list = list()
    persons_tasks = [get_person(f'{SW_API}/{i}') for i in range(1, 10)]
    persons_info = await asyncio.gather(*persons_tasks)
    for person in persons_info:
        data = dict()
        data['birth_year'] = person['birth_year']
        data['eye_color'] = person['eye_color']
        data['films'] = ', '.join(name_generator(person['films']))
        data['gender'] = person['gender']
        data['hair_color'] = person['hair_color']
        data['height'] = person['height']
        planet = await get_homeworld_name(person['homeworld'])
        data['homeworld'] = planet['name']
        data['mass'] = person['mass']
        data['name'] = person['name']
        data['skin_color'] = person['skin_color']
        data['species'] = ', '.join(name_generator(person['species']))
        data['starships'] = ', '.join(name_generator(person['starships']))
        data['vehicles'] = ', '.join(name_generator(person['vehicles']))

        star_war_persons_list.append(data)
    return list(star_war_persons_list)


async def main():
    sw_people_list = await get_sw_people()
    await async_main(sw_people_list)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())



