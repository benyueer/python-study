"""
https://myapollo.com.tw/zh-tw/begin-to-asyncio/
"""

"""
coroutine

Event Loop

Awaitable

Tasks

Future
"""

import asyncio
from time import time
import unittest
import aiohttp
import requests

class TestAsyncio(unittest.TestCase):
    def test_asyncio(self):
        # 同时发送多个请求获取响应结果
        def do_requests():
            resp = requests.get('https://baidu.com')
            print(f'get -> {resp.status_code}')

        def run():
            """
            所有的请求是串行发送的，一个请求结束才能发送下一个，比较耗时
            """
            start = time()
            for _ in range(10):
                do_requests()
            print(f'tine: {time() - start} s')  # tine: 2.4070541858673096 s

        # run()

        def do_requests_asyncio(session):
            return session.get('https://baidu.com')

        async def run_asyncio():
            start = time()
            async with aiohttp.ClientSession() as session:
                tasks = []
                for _ in range(10):
                    tasks.append(do_requests_asyncio(session))

                results = await asyncio.gather(*tasks)
                for r in results:
                    print(f'get  {r.status}')
            print(f'end: {time() - start} s')  # end: 0.3408191204071045 s


        """
        async 修饰的函数成为 coroutine 对象，要使用 asyncio.run 运行
        """
        asyncio.run(run_asyncio())