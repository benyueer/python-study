import asyncio
import random
import time
from typing import Callable
import unittest


"""
协程：又称微线程，纤程。英文名Coroutine。
"""


class TestAsync(unittest.TestCase):
    def test_async(self):
        # 异步函数
        async def async_fun():
            return 1

        # 直接调用异步函数不会返回结果，而是返回一个coroutine对象：
        print(async_fun())


        # 协程需要通过其他方式来驱动，因此可以使用这个协程对象的send方法给协程发送一个值：
        # print(async_fun().send(None))  # 但是这样会报错：StopIteration: 1

        # 因为生成器/协程在正常返回退出时会抛出一个StopIteration异常，而原来的返回值会存放在StopIteration对象的value属性中，通过以下捕获可以获取协程真正的返回值：
        try:
            async_fun().send(None)
        except StopIteration as e:
            print(e.value)  # 1

        # 定义一个 run 函数驱动协程
        def run(coroutine):
            try:
                coroutine.send(None)
            except StopIteration as e: 
                return e.value

        # 在协程函数中可以通过await挂起自身协程，并等待另一个协程返回：
        async def await_coroutine():
            result = await async_fun()   # await 只能出现在async函数中
            print(result)

        run(await_coroutine())  # 1

        # await 只能出现在async函数中
        # await 后的对象需要是一个Awaitable，或实现了相关协议
        # 查看Awaitable抽象类的代码，表明了只要一个类实现了__await__方法，那么通过它构造出来的实例就是一个Awaitable：
        """
        class Awaitable(metaclass=ABCMeta):
            __slots__ = ()

            @abstractmethod
            def __await__(self):
                yield

            @classmethod
            def __subclasshook__(cls, C):
                if cls is Awaitable:
                    return _check_methods(C, "__await__")
                return NotImplemented
        """
        # 而且可以看到，Coroutine类也继承了Awaitable，而且实现了send，throw和close方法。所以await一个调用异步函数返回的协程对象是合法的。
        """
        class Coroutine(Awaitable):
            __slots__ = ()

            @abstractmethod
            def send(self, value):
                ...

            @abstractmethod
            def throw(self, typ, val=None, tb=None):
                ...

            def close(self):
                ...
                
            @classmethod
            def __subclasshook__(cls, C):
                if cls is Coroutine:
                    return _check_methods(C, '__await__', 'send', 'throw', 'close')
                return NotImplemented
        """


    def test_generator(self):
        class Potato:
            @classmethod
            def make(cls, num, *args, **kes):
                potatos = []
                for i in range(num):
                    potatos.append(cls.__new__(cls, *args, **kes))
                return potatos

        all_potatos = Potato.make(5)

        async def take_potatos(num):
            count = 0
            while True:
                if len(all_potatos) == 0:
                    await ask_for_potato()
                potato = all_potatos.pop()
                yield potato
                count += 1
                if count == num:
                    break


        async def ask_for_potato():
            await asyncio.sleep(random.random())
            all_potatos.extend(Potato.make(random.randint(1, 10)))

        async def buy_potatos(name: str):
            bucket = []
            async for p in take_potatos(50):
                bucket.append(p)
                print(f'got {name} {id(p)}')

        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(asyncio.wait([buy_potatos('potato'), buy_potatos('tomato')]))
        loop.close()

    def test_asyncio(self):

        def dosomething(index: int):
            print(f'start {index}')
            time.sleep(1)
            print(f'end {index}')

        def run(fun: Callable):
            start = time.time()

            for i in range(5):
                fun(i)
            
            print(f'time: {time.time() - start} s')

        run(dosomething) # 用了5s

        async def dosomethis_asyncio_sleep(index):
            print(f'start {index}')
            await asyncio.sleep(1)
            print(f'end {index}')

        def run_asyncio():
            start = time.time()

            tasks = [dosomethis_asyncio_sleep(i) for i in range(5)]
            asyncio.run(asyncio.wait(tasks))
            
            print(f'time: {time.time() - start} s')

        run_asyncio()  # 用了1s
        """
        start 0
        start 1
        start 2
        start 3
        start 4
        end 0
        end 1
        end 2
        end 3
        end 4
        time: 1.0056591033935547 s  
        """





