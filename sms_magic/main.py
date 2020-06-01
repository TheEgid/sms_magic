import asks
import trio
import os
import contextlib
from dotenv import load_dotenv
import asyncclick as click


async def fetch(url, params):
    my_response = await asks.get(url, params=params)
    my_response.raise_for_status()
    print(my_response.text)
    return my_response.text


@click.command(load_dotenv())
async def main(**args):
    url = 'https://smsc.ru/sys/send.php'
    params = {
        'login': os.getenv("LOGIN"),
        'psw': os.getenv("PASSWORD"),
        'phones': os.getenv("PHONES"),
        'mes': 'HOHOHO!'
    }
    async with trio.open_nursery() as nursery:
        nursery.start_soon(fetch, url, params)


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt):
        main(_anyio_backend="trio")
