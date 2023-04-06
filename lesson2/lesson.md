# 字面量
在代码中，被写下来的固定的值称为字面量

## 值类型
Python 中常用的有6种值类型
- 数字    Number
- 字符串  String
- 列表    List
- 元组    Tuple
- 集合    Set
- 字典    Dictionary

# 注释
单行注释：Python 中使用井号（#）注释
多行注释：使用 """

# 变量
变量名 = 变量值

# 数据类型
使用`type()`查看变量数据类型

# 数据类型转换
```py
int(x)
float(x)
str(x)
```

# if 语句
```py
if exp:
  do
elif exp:
  do
else:
  do
```

# while
```py
while exp:
  do
```

# for
```py
for i in list:
  do
```

## range
for 循环语句，本质上是遍历序列类型
range 可以生成xulie
```py
# 生成0-num 的序列
range(num)

# 生成 a-b 的序列
range(a, b)

# 生成 a-b，步长s的序列
range(a, b, s)
```

## for 中变量作用域
```py
for 临时变量 in 序列:
  do

print(临时变量)
```
遍历时，将序列中的值赋值给 临时变量，在规范中只能在循环内访问，但实际上在外部也能访问到


## 列表推导式
```py
# 语法
out_list = [表达式 for 变量 in 列表 条件判断语句等]

# 示例
out_list = [i**2 for i in range(5)]

out_list = [i**2 for i in range(5) if i % 2 == 0]
```


# 函数
```py
def fun():
  pass
```
## 传参

1. 位置参数
   调用函数时实参与形参位置上一一对应
   ```py
   def info(name, age):
      print(name, age)
   ```
2. 默认参数
   给形参一个默认值
   ```py
    def info(name, age, level=INFO):
        pass

    info('mical', 16)
   ```
3. 可变参数
   ```py
    def calc(*muns):
        pass

    nums = [1,2,3]
    calc(*nums)
   ```
4. 关键字参数
   ```py
    def info(name, age, **kw):
      pass

    info('Mical', 17, level='info')
   ```
5. 命名关键字参数
   ```py
    # 使用 * 分隔，* 后是命名关键字参数
    def info(name, age, *, type):
      pass

    info('Mical', 16, type="qwe")

   ```

## 匿名函数
lambda 关键字声明匿名函数
```py
lambda 入参: 函数体

lambda x, y: x + y
```

## 变量作用域
全局作用域与局部作用域

函数内定义的变量自在函数内生效


# List 列表
列表定义
```py
l = [1, 'hello', Obj]

ll = [[1, 2, 3], [3, 4, 5]]
```

# 元组
不可以修改元组内容
```py
t = ((1, 2), 'q')

t[0][1] # 2
```

# 切片
```py
l = [1, 2, 3, 4, 5] # 字符串 元组 同样适用
r = l[1:4]
r1 = l[:]
r2 = l[1:4:2]
r3 = l[4:1:-1]
```

# 集合
```py
# 定义
s1 = {1, 2 ,3 ,4 ,5}
s_empty = set()

# 添加元素
s1.add(7)

# 移除
s1.remove(7)
s1.pop()


```


# 字典
```py
# 定义
d = {key: value}
d1 = dict()
```


# 异常
```py
# 基础语法
try:
  exp
except:
  pass


# 捕获指定异常
try:
  exp
except NameError as e:
  pass


# 捕获多个异常
try:
  exp
except (NameError, RuntimeError) as e:
  pass

# 捕获所有异常
try:
  exp
except Exception as e:
  pass

# else
try:
  exp
except Exception as e:
  pass
else:
  pass

# finally

try:
  exp
except Exception as e:
  pass
finally:
  pass
```


# 对象
```py
# Python3中类基本都会继承于object类
class Circle(object):
  # pi 是类属性
  pi = 3.14
  def __init__(self, r):
    # r 是实例属性
    slef.r = r
```