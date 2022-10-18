import unittest

"""
在Python中，一边循环一边计算的机制，称为生成器：generator。

与普通函数不同，generator 在遇到 yield时将值返回，函数中断，后面的代码不再执行，当再次调用 next 时，从上一次 中断的位置继续执行，碰到 yield 继续中断

生成器的 return 返回值 不能在循环中获取，必须捕获 StopIteration 错误，值在错误的 value 中
"""

class TestGenerator(unittest.TestCase):
    def test_generator(self):
        # 创建一个generator
        # 使用生成式
        g = (x for x in range(10))
        print(g)  # <generator object TestGenerator.test_generator.<locals>.<genexpr> at 0x10b673eb0>
        for n in g:
            print(n)

        # yield
        def fib(num):
            n, a, b = 0, 0, 1
            while n < num:
                yield b
                a, b = b, b + a
                n = n + 1
            return 'done'

        for i in fib(10):
            print(i)
