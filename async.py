import sys
import aiohttp
import asyncio
from datetime import datetime, date


def create_data(number):
    url_prefix = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='
    data = datetime.today().date()
    user_input = int(number)
    if user_input > 10:
        user_input = 10
    lst_urls = []
    for i in range(user_input):
        new_data = date(year=data.year, month=data.month, day=data.day - i)
        lst_urls.append(url_prefix + new_data.strftime("%d.%m.%Y"))
    return lst_urls


async def get_result(result, value=None):
    new_dct = {}
    dct = {}
    valute = ['EUR', 'USD']
    if value:
        valute.append(value.upper())
    for i in result['exchangeRate']:
        for cur, val in i.items():
            if val in valute:
                new_dct[i.get('currency')] = f"sale: {i.get('saleRate')}, purchase: {i.get('purchaseRate')}"
    dct[result.get('date')] = new_dct
    return dct


async def func_to_api(url, value=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print("status:", response.status)
            if response.status == 200:
                result = await response.json()
                if value:
                    return await get_result(result, value)
                return await get_result(result)
            elif 400 <= response.status < 500:
                return f'Server error'
            elif response.status >= 500:
                return f'Client error'


async def main(day, value=None):
    urls = create_data(day)
    result = []
    for i in urls:
        if value:
            result.append(func_to_api(str(i), value))
        else:
            result.append(func_to_api(str(i)))
    finish = await asyncio.gather(*result)
    return finish


if __name__ == '__main__':
    path = sys.argv
    if len(path) == 3:
        r = asyncio.run(main(path[1], path[2]))
        print(f'Result{r}')
    else:
        r = asyncio.run(main(path[1]))
        print(f'Result{r}')