# 函数

## 把函数视作对象
Python 函数是对象
```py
def fun():
  pass

type(fun)
>>> <class 'function'>
```
## 匿名函数
使用 lambda 表达式

## 可调用对象
Python 数据模型文档列出了7种可调用对象
1. 用户定义的函数
   使用 def 或 lambda 表达式创建
2. 内置函数
   使用C语言（CPython）实现的函数，如 len 或 time.strftime
3. 内置方法
   使用C语言实现的方法，如 dict.get
4. 方法
   在类的定义中定义的方法
5. 类
   调用类时会运行类的`__new__`方法创建一个实例，然后运行`__init__`方法初始化实例，最后把实例返回给调用方
6. 类的实例
   如果类定义了`__call__`方法，那么他的实例也可作为函数调用
7. 生成器函数
   使用 yield 关键字的函数或方法，调用生成器函数返回的是生成器对象

## 用户定义的可调用类型
不仅 Python 函数是对象，任何Python对象都可以表现得像函数，只需要实现实例方法`__call__`
```py
import random

class BingoCage:
  def __init__(self, items):
    self._items = list(items)
    readom.shuffle(self._items)

  def pick(self):
    try:
      return self._items.pop()
    except IndexError:
      raise LookupError('empty')
  
  def __call__(self):
    return self.pick()
```


## 函数内省
除了 __doc__，函数对象还有很多属性。使用 dir 函数可以探知 factorial 具有下述属性：
```py
['__annotations__', '__call__', '__class__', '__closure__', '__code__',
'__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__',
'__format__', '__ge__', '__get__', '__getattribute__', '__globals__',
'__gt__', '__hash__', '__init__', '__kwdefaults__', '__le__', '__lt__',
'__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__',
'__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__','__subclasshook__']
```
其中大部分是Python 对象共有的

`__dict__`：函数使用`__dict__`属性存储赋予他的用户属性

函数专有而用户定义的一般对象没有的属性：
```py
class C:
  pass

obj = C()

def fun():
  pass

sorted(set(dir(fun)) - set(dir(obj)))

['__annotations__', '__call__', '__closure__', '__code__', '__defaults__',
'__get__', '__globals__', '__kwdefaults__', '__name__', '__qualname__']
```
|名称|类型|说明|
|-|-|-|
|`__annotations__`|dict|参数和返回值的注解|
|`__call__`|method-wrapper|实现`()`运算符|
|`__closure__`|tuple|函数闭包，即自由变量的绑定|
|`__code__`|code|编译成字节码的函数元数据和函数定义体|
|`__defaults__`|tuple|形式参数的默认值|
|`__get__`|method-wrapper|实现只读描述符协议|
|`__globals__`|dict|函数所在模块中的全局变量|
|`__kwdefaults__`|dict|仅限关键字形式参数的默认值|
|`__name__`|str|函数名称|
|`__qualname__`|str|函数的限定名称，如`Random.choice`|



## 定位参数到仅限关键字参数
使用`* **`展开可迭代对象，映射到单个参数


## 获取关于参数的信息
```py
# 定义一个函数
def fun(name, age=10):
  pass


fun.__defaults__ # (10,)

fun.__code__ # <code object fun at 0x...>

fun.__code__.co_varnames # ('name', 'age', ...)

fun.__code__.co_argcount # 2
```
参数名称在`fun.__code__.co_varnames`中，是其中的前`__code__.co_argcount`个，其他的是函数中定义的局部变量
其中不包括`* **`定义的变长参数
默认值在`fun.__defaults__`，顺序是从后往前

上面这种方法太过麻烦，更好的方式是使用`inspect`模块
```py
from inspect import signature

def fun(name, age=10):
  pass


sig = signature(fun)
str(sig)  # '(name, age=10)'

for name, param in sig.parameters.items():
  print(param.kind, ':', name, '=', param.default)

# POSITIONAL_OR_KEYWORD : name = <class 'inspect._empty'> 
# POSITIONAL_OR_KEYWORD : age = 10 

```


## 函数装饰器和闭包
装饰器是可调用的对象，其参数是另一个函数（被装饰的函数）。装饰器可能会处理被装饰的函数，然后把它返回，或者将其替换成另一个函数或可调用对象

装饰器的一个关键特性是，它们在被装饰的函数定义之后立即运行。这通常是在导入时（即 Python 加载模块时）

函数装饰器在导入模块时立即执行，而被装饰的函数只在明确调用时运行。这突出了 Python 程序员所说的导入时和运行时之间的区别。


## 变量作用域规则
```py
b = 1

def fun(num):
  print(num)
  print(b)
  b = 10

fun(1)
```
这会报错，`UnboundLocalError: local variable 'b' referenced before assignment`

## 闭包
```py
class Averager():
  def __init__(self):
    self.series = []
  def __call__(self, new_value):
    self.series.append(new_value)
    total = sum(self.series)
    return total/len(self.series)

def make_averager():
  series = []

  def averager(new_value):
    series.append(new_value)
    total = sum(series)
    return total/len(series)

  return averager
```

`series` 是 `make_averager` 函数的局部变量，因为那个函数的定义体中初始化了`series：series = []`。可是，调用 `avg(10)` 时，`make_averager` 函数已经返回了，而它的本地作用域也一去不复返了。
在 `averager` 函数中，`series` 是自由变量（`free variable`）。这是一个技术术语，指未在本地作用域中绑定的变量
审查返回的 `averager` 对象，我们发现 Python 在 `__code__` 属性（表示编译后的函数定义体）中保存局部变量和自由变量的名称
```py
avg.__code__.co_varname
# ('new_value', 'total')

avg.__code__.co_freevars
# ('series',)
```

`series` 的绑定在返回的 `avg` 函数的 `__closure__` 属性中
`avg.__closure__` 中的各个元素对应于 `avg.__code__.co_freevars` 中的一个名称。这些元素是 `cell` 对象，有个 `cell_contents` 属性，保存着真正的值
```py
avg.__closure__
#(<cell at 0x3123213: list object at 0x1231231,)
avg.__closure__[0].cell_contents
# [10, 11, 12]
```

综上，闭包是一种函数，它会保留定义函数时存在的自由变量的绑定，这样调用函数时，虽然定义作用域不可用了，但是仍能使用那些绑定。
注意，只有嵌套在其他函数中的函数才可能需要处理不在全局作用域中的外部变量。


## nonlocal 声明
上例中平均值计算的实现有缺陷，改进一下：
```py
def make_averager():
  const = 0
  total = 0

  def averager(new_value):
    count += 1
    total += new_value
    return total/count
  
  return averager
```
但是在运行时会报错：`UnboundLocalError: local variable 'count' referenced before assignment`
当`count`是任何不可变类型时，`count += 1`就和`count = count + 1`一样，因此，在`averager`中的定义会把`count`变成局部变量
对数字、字符串、元组等不可变类型来说，只能读取，不能更新。如果尝试重新绑定，例如 `count = count + 1`，其实会隐式创建局部变量 `count`。
这样的话就不是自由变量了，闭包也就失效了

为了解决这个问题，Python 3 引入了 `nonlocal` 声明。它的作用是把变量标记为自由变量，即使在函数中为变量赋予新值了，也会变成自由变量。如果为 nonlocal 声明的变量赋予新值，闭包中保存的绑定会更新
```py
def make_averager():
  count = 0
  total = 0

  def averager(new_value):
    nonlocal count, total
    total += new_value
    count += 1
    return total/count
  
  return averager
```

## 标准库中的装饰器
Python 中内置了3个用于装饰方法的函数：`property`, `classmethod`, `staticmethod`
其他：`functools.wraps`, `lru_cache`, `singledispatch`

### 使用 functools.lru_cache 做备忘
`functools.lru_cache`实现了备忘功能，这是一项优化技术，把耗时函数的结果存储起来，避免相同入参的重复计算
斐波那契的例子：
```py
import functools

@functools.lru_cache()
def fibonacci(n):
  if n < 2:
    return n
  return fibonacci(n-2) + fibonacci(n-1)
```

### 单分派泛函数
`functools.singledispatch` 装饰器可以把整体方案拆分成多个模块

```py
from functools import singledispatch
from collections import abc
import numbers
import html

@singledispatch 
def htmlize(obj):
  content = html.escape(repr(obj))
  return '<pre>{}</pre>'.format(content)

@htmlize.register(str) 
def _(text): 
  content = html.escape(text).replace('\n', '<br>\n')
  return '<p>{0}</p>'.format(content)
  
@htmlize.register(numbers.Integral) 
def _(n):
  return '<pre>{0} (0x{0:x})</pre>'.format(n)

@htmlize.register(tuple) 
@htmlize.register(abc.MutableSequence)
def _(seq):
  inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
  return '<ul>\n<li>' + inner + '</li>\n</ul>'
```

# 面向对象

## 标识、相等性和别名
绑定相同对象的变量互为别名
每个变量都有标识、类型和值，对象一旦创建，他的标识绝不会变，可以把标识理解为内存地址
`is`运算符比较两个对象的标识，`id()`返回对象标识的整数表示

对象 ID 真正意义在不同实现中有所不同，在 CPython 中 id() 返回对象内存地址，但是在其他 Python 解释其中可能是其他值，关键是 ID 一定是唯一的数值标注，在对象的生命周期中绝不会变

## == 与 is
`==`比较两个对象的值，`is`比较对象标识
在变量和单例值之间比较时，应该使用 is
```py
x is None
x is not None
```

is 比 == 快，因为它不能重载，`a == b` 等同于`a.__eq__(b)`

## 默认浅复制
复制可变对象时默认浅复制，可以使用`copy.deepcpoy`深复制

## 函数参数作为引用时
Python 唯一支持的参数传递模式是 共享传参，函数内部的形参是实参的别名

## 避免使用可变类型作为参数默认值
```py
class Tmp:
  def __init__(list = []):
    self.list = list
  def append(item):
    self.list.append(item)


t1 = Tmp([1, 2, 3])
t1. append(4)
t1.list # [1, 2, 3 ,4]

t2 = Tmp()
t2.append(2)
t2.list # [2]

t3 = Tmp()
t3.list # [2]
```

默认值在函数定义时计算（通常在加载模块时），因此默认值变成了函数对象的属性，如果默认值对象是可变的，修改他后所有的函数调用都会受到影响
可变默认值导致的这个问题说明了为什么通常使用 `None` 作为接收可变值的参数的默认值

## 防御可变参数
```py
class Bus:
  def __init__(self, passengers = None):
    if passengrts is None:
      self.passengers = []
    else:
      # 使用副本
      self.passengers = list(passengers)

  def __append__(self, name):
    self.passengers.append(name)

team = [1, 2, 3]

bus = Bus(team)
bus.append(4)

team # [1,2,3] 因为使用了副本，副作用不会体现到外部
```

## del 和垃圾回收
`del`语句删除名称，而不是对象，`del`语句可能会导致对象被当作垃圾回收，但是仅当删除的变量保存的是对象的最后一个引用，或者无法得到对象时。重新绑定也可能会导致对象的引用数量归零，导致对象被销毁

在 CPython 中，垃圾回收使用的主要算法是引用计数。实际上，每个对象都会统计有多少引用指向自己，当引用计数归零时，对象立即就被销毁，CPython 会在对象上调用`__del__`方法，然后释放分配给对象的内存，CPython 2.0 增加了分代垃圾回收

## 弱引用
弱引用不会增加对象的引用数量，弱引用不会妨碍所指的对象被当作垃圾回收
```py
import weakref

a_set = {0, 1}
wref = weakref.ref(a_set)
wref # <weakref at 0x1321331; to 'set' at 0x6877778>

wref() # {0, 1}
a_set = {2, 3, 4}
wref() # {0, 1}

wref() is None # False

wref() is None # True
```

# 控制流程

## 可迭代对象、迭代器和生成器
所有的生成器都是迭代器，因为生成器完全实现了迭代器的接口
迭代器用于从集合中取出元素，而生成器用于“凭空”生成元素

现在，内置的`range`函数也返回一个类似生成器的对象，以前则返回完整的列表。如果一定要`range`返回列表，那么必须明确指明，例如`list(range(10))`

在 Python 中，所有的集合都可以迭代，迭代器用于支持：
- for 循环
- 构建和扩展集合类型
- 逐行遍历文本文件
- 列表推导、字典推导和集合推导
- 元组拆包
- 调用函数时，使用 * 拆包实参

序列可以迭代，因为实现了`iter`函数
解释器需要迭代对象x时，会自动调用`iter()`
内置的 iter 函数有以下作用：
1. 检查对象是否实现了`__iter__`方法，如果实现了就调用他，获取一个迭代器
2. 如果没有实现`__iter__`，但是实现了`__getitem__`，Python会自动创建一个迭代器尝试按顺序获取元素
3. 如果尝试失败，抛出`TypeError`异常

任何 Python 序列都可迭代的原因是，他们都实现了`__getitem__`方法


从 Python3.4 开始，检查对象 x 能否迭代，最标准的做法是：调用`iter(x)`函数，如果不可迭代，再处理`TypeError`

### 可迭代对象与迭代器的对比
可迭代对象：使用`iter`函数可以获取迭代器的对象。如果对象实现了能返回迭代器的`__iter__`方法，那么对象就是可迭代的。序列都可以迭代。实现了`__getitem__`方法，而且其参数是从 0 开始的索引，这种对象也可以迭代。
Python 从可迭代对象获取迭代器

```py
s = 'abc'

for i in s:
  print(i)

it = iter(s)

while True:
  try:
    print(next(it))
  except StopIteration:
    del it
    break
```
`StopIteration`异常表示迭代器到头了

标准的迭代器接口有两个方法：
- `__next__`：返回下一个可用元素，如果没有元素了，抛出`StopIteration`异常
- `__iter__`：返回 self ，以便在应该使用可迭代对象的地方使用迭代器，例如在 for 循环中

### 典型迭代器
```py
import re
import reprlib

RE_WORD = re.compile('\w+')

class Sentence:

  def __init__(self, text):
    self.text = text
    self.words = RE_WORD.findall(text)

  def __repr__(self):
    return 'Sentence(%s)' % reprlib.repr(self.text)

  def __iter__(self):
    return SentenceIterator(self.words)


class SentenceIterator:

  def __init__(self, words):
    self.words = words
    self.index = 0

  def __next__(self):
    try:
      word = self.words[self.index]
    except IndexError:
      raise StopIteration()
    self.index += 1
    return word

  def __iter__(self):
    return self

```

在这个例子中，其实没必要在`SentenceIterator`中实现`__iter__`，不过这么做是对的，因为迭代器应该实现`__iter__ __next__`两个方法

用生成器实现：
```py
import re
import reprlib

RE_WORD = re.compile('\w+')

class Sentence:

  def __init__(self, text):
    self.text = text
    self.words = RE_WORD.findall(text)
  
  def __repr__(self):
    return 'Sentence(%s)' % reprlib.repr(self.text)

  def __iter__(self):
    for word in words:
      yield word
    return
```

### 生成器函数工作原理
只要 Python 函数的定义中出现了 yield 关键字，该函数就是生成器函数
调用生成器函数时会返回一个生成器对象，也就是说，生成器函数是生成器工厂

```py
def gen_123():
  yield 1
  yield 2
  yield 3

gen1 = gen_123()

for i in gen1:
  print(i)

# 1, 2, 3

gen2 = gen_123()

next(gen2)  # 1
next(gen2)  # 2
next(gen2)  # 3

```

把生成器函数传递给`next()`时，生成器函数会向前，执行函数体中的下一个`yield`，返回产出的值，并在函数定义的当前位置暂停，最终，函数返回时，抛出`StopIteration`异常，这一点与迭代器一致

惰性实现：
```py
import re

RE_WORD = re.compile('\w+')

class Sentence:
  def __init__(self, text):
    self.text = text

  def __iter__(self):
    for match in RE_WORD.findall(self.text):
      yield match.group()
```

### 生成器表达式
简单的生成器函数，可以替换成生成器表达式
生成器表达式可以理解成列表推导的惰性版本：不会急迫地去构建列表，而是返回一个生成器，按需惰性生成元素
```py
def gen_AB():
  print('start')
  yield A
  print('continue')
  yield B
  print('end')

res1 = [x*3 for x in gen_AB()]
# start
# continue
# end

for i in res1:
  print(i)
# AAA
# BBB


# 这里返回一个生成器，但没有调用，因此不会输出 start
res2 = (x*3 for x in gen_AB())

# 此时才会执行生成器
for i in res2:
  print(i)

```

改进 Sentence： 
```py
import re

RE_WORD = re.compile('\w+')

class Sentence:
  # ...
  def __iter__(self):
    return (match.group() for match in RE_WORD.findall(self.text))
```
这里不再是生成器函数了，而是使用了生成器表达式构建生成器，然后将其返回



## 上下文管理器和 else 块
else 子句不仅能在 if 中使用，还能在 for while 和 try 中使用

上下文管理器对象存在的目的是管理 with 语句，就像迭代器对象存在是为了管理 for 语句一样

with 语句的目的是为了简化 try/finally 模式
这种模式用于保证一段代码运行完毕后执行某项操作，如释放资源

上下文管理器协议包含`__enter__`和`__exit__`两个方法，with 语句开始运行时，会在上下文管理器对象上调用 __enter__ 方法，with 语句运行结束后，会调用 __exit__ 方法，以此扮演 finally 子句的角色

```py
with open('text.txt') as fp:
  s = fp.read(100)

len(s) # 100

```
在 with 块的末尾关闭了文件，因此不能执行 I/O 操作

```py
class LookingGlass:
  def __enter__(self):
    import sys
    self.original_write = sys.stdout.write
    sys.stdout.write = self.reverse_write
    return 'AFASFL'
  
  def reverse_write(self, text):
    self.orononal_write(text[::-1])

  def __exit__(self, exc_type, exc_value, traceback):
    import sys
    sys.stdout.write = self.original_write
    if exc_type is ZeroDivisionError:
        print('place do not  divide by zero')
        return True


with LookingGlass() as what:
  print(what)

# LFSAFA

# 在 with 块结束后，打印不是反向了
what
# AFASFL
```

### contextlib模块中的实用工具

- closing
  如果对象提供了 close 方法，但没有实现 \__enter__/\__exit__ 协议，那么可以使用这个函数构建上下文管理器
- suppress
  构建临时忽略指定异常的上下文管理器
- @contextmanager
  这个装饰器把简单的生成器函数变成上下文管理器，这样就不用创建类去实现管理器协议了
- ContextDecorator
  这是个基类，用于定义基于类的上下文管理器
- ExitStack
  这个上下文管理器能够进入多个上下文管理器，with 块结束时，ExitStack 按照后进先出的顺序调用栈中各个上下文管理器的 \__exit__ 方法


### 使用 @contextmanager
```py
import contextlib

@contextlib.contextmanager
def looking_glass():
  import sys
  original_write = sys.stdout.write

  def reverse_write(text):
    original_write(text[::-1])

  sys.stdout.write = reverse_write
  yield 'FADASD'
  sys.stdout.write = original_write
```


# 协程
协程是指一个过程，这个过程与调用方协作，产出由调用方提供的值

## 用作协程的生成器的基本行为
```py
def simple_coroutine():
  x = yield

my_coro = simple_coroutine()
next(ny_coro)

my_coro.send(12)

StopIteration
```

协程可以身处四个状态中的一个，当前状态可以用`inspect.getgeneratorstate()`获取
- GEN_CREATED
  等待开始执行
- GEN_RUNNING
  解释器正在执行
- GEN_SUSOENDE
  在 yield 表达式处暂停
- GEN_CLOSED
  执行结束

## 预激协程的装饰器
如果不预激，那么协程没什么用
为了简化协程用法，使用预激装饰器
```py
from functools import wraps

def coroutine(func):
  @wraps(func)
  def primer(*args, **kwargs):
    gen = func(*args, ** kwargs)
    next(gen)
    return gen
  
  return primer

# 用法
@coroutine
def averager():
  total = 0
  count = 0
  averager = None
  while True:
    term = yield averager
    total += term
    count += 1
    averager = total / count
```

## 终止协程和异常处理
协程中未处理的异常会向上冒泡，传递给 next 或 send 的调用方

从 Python 2.5 开始，客户代码可以在生成器对象上调用两个方法，显式地把异常发给协程，这两个方法是`throw close`
`generator.throw(exc_type[, exc_value[, trackback]]`：
使生成器在暂停的 yield 表达式处抛出异常，如果生成器处理了抛出的异常，代码会执行到下一个 yield，而产出的值会成为 throw 的返回值
`generator.close()`：
使生成器在暂停的 yield 表达式处抛出 GeneratorExit 异常，如果生成器没有处理这个异常，或者抛出 StopIterator 异常，调用方不会报错。

```py
class DemoException(Exception):
  """
    自定义异常类型
  """

def demo_exc_handling():
  while True:
    try:
      x = yield
    except DemoException:
      print('dome exception')
    else:
      print('recived {!r}'.format(x))
  raise RuntimeError('this line never run')

# close
exc_coro = demo_exc_handling()
next(exc_coro)
exc_coro.send(12)
# recived 12
exc_coro.send(22)
# recived 22
exc_coro.close()

inspect.getgeneratorstate(exc_coro) # GEN_CLOSED


# throw
exc_throw = demo_exc_handling()
next(exc_throw)
exc_throw(12)
# recived 12
exc_throw.throw(DomeException)
# dome exception
inspect.getgeneratorstate(exc_throw) # GEN_SUSPENDED


# throw 传入未处理异常
exc_no = demo_exc_handling()
next(exc_no)
exc_no.send(12)
# recived 12
exc_no.throw(ZeroDivisionError)

# 此处报错

inspect.getgeneratorstate(exc_no) # GEN_CLOSED

```

## 让协程返回值
```py
from collections import namedtuple

Result = namedtuple('Result', 'count average')

def averager():
  total = 0
  count = 0
  average = None
  while True:
    x = yield
    if x is None:
      break
    total += x
    count += 1
    average = total /count 
  return Result(count, average)


# 使用
avg = averager()
next(avg)
avg.send(12)

try:
  avg.send(None)
except StopIteration as exc:
  res = rdc.value

res # 12

```
为了返回值，协程必须正常终止，因此判断传入值终止循环


# 使用 yield from
yield from 是全新的语言结构，它的作用比 yield 多很多

```py
def chain(*iterables):
  for it in iterables:
    yield from it

s = 'abc'
l = tuple(range(3))
list(chain(s, t))
# [a, b, c, 0, 1, 2]
```

`yield from x`表达式对 x 对象做的第一件事是调用`iter(x)`，从中获取迭代器，因此 x 可以是任何可迭代对象
