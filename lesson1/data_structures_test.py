from email.policy import default
import unittest


class TestDataStructures(unittest.TestCase):

    def test_list(self):
        fruits = ['orange', 'apple', 'pear',
                  'banana', 'kiwi', 'apple', 'banana']
        # append
        fruits.append('apple')

        # extend
        # insert

        # remove
        # pop
        # clear
        # index
        print(fruits.index('banana'))

        # count
        print(fruits.count('apple'))
        # sort
        fruits.sort()
        print(fruits)
        # reverse
        fruits.reverse()
        print(fruits)

        # copy
        fruits_copy = fruits.copy()
        print(fruits_copy, fruits, sep='\n')

    def test_list_stack(self):
        # pop append
        stack = [1, 2, 3]
        stack.append(4)
        stack.pop()

    def test_list_queue(self):
        # append popleft
        from collections import deque
        queue = deque([1, 2, 3])
        queue.append(4)
        queue.popleft()

    def test_del(self):
        a = [1, 2, 3, 4, 5, 6]
        del a[0]
        print(a)
        del a[2:4]
        print(a)
        del a[:]
        print(a)

    def test_tuple(self):
        t = 123, 456, 1231
        u = *t, 222, 5454
        print(u)

    def test_set(self):
        # 创建集合可以用{} 或 set
        set1 = {1, 2, 3, 1}
        print(set1)  # 1, 2, 3 重复的1被删去

        print(1 in set1)  # True

        a = set('qwe')
        b = set('qert')
        print(a - b)  # w
        print(a | b)  # e r w q t
        print(a ^ b)  # r w t
        print(a & b)  # e q

        set2 = {1}
        # 添加元素
        set2.add(2)
        set2.update((4, 5))
        print(set2)
        # 删除元素
        set2.remove(1)
        set2.discard(1)
        set2.pop()

    def test_dict(self):
        # 创建
        d1 = {'name': 'ad', 'age': 123}
        d2 = dict([('name', 'asd')])
        # 访问
        print(d1['name'])
        # 修改
        d1['age'] = 20
        print(d1)
        # 删除
        del d1['age']
        print(d1)
        """
        内置方法
        """
        print(len(d1))
        print(str(d1))
        print(type(d1))

        # clear
        d2.clear()  # 清空所有元素
        print(d2)  # {}
        # copy 返回浅拷贝
        # fromkeys 创建新字典
        d3 = dict.fromkeys(('name', 'age'))  # {'name': None, 'age': None}
        d4 = dict.fromkeys(('name', 'age'), 10)  # {'name': 10, 'age': 10}
        print(d3, d4, sep='\n')
        # get(key, default=None)
        print(d3.get('name', 10))
        # items
        print(d4.items())
        # keys
        print(d4.keys())
        # setdefault
        d4.setdefault('time', 12)
        print(d4)
        # update
        d3.update(d4)
        print(d3)
        # values
        print(d4.values())
        # pop(key[, default])
        print(d4.pop('name', 1))
        # popitem
        print(d3.popitem())


