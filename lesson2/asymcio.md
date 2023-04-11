# asyncio
asyncio 模块提供了使用协程构建并发应用的工具。他使用单线程单进程的方式实现并发，应用的各个部分彼此合作，可以显式的切换任务，一般会在程序阻塞IO操作时发生上下文切换，如等待文件读写、网络请求等。同时asyncio也支持调度代码在将来的某个特定事件运行，从而支持一个协程等待另一个协程完成，以处理系统信号和识别其他的一些事件

## 异步并发概念
对于其他的并发模型大多采取线性的方式编写，并且依赖于语言运行时系统或操作系统的底层线程或进程来适当的改变上下文，而基于 asyncio 的应用要求应用代码显式的处理上下文切换
asyncio 提供的框架以事件循环（event loop）为中心，程序开启一个无限的循环，程序会把一些函数注册到事件循环上，当满足的事件发生的时候，调用相应的协程函数

## 事件循环
事件循环是一种处理多并发量的有效方式，我们可以定义事件循环来简化使用轮询方法来监控事件。
事件循环利用 poller 对象，使得程序员不用控制任务的添加、删除和事件的控制。事件循环使用回调方法来知道事件的发生。
支持以下操作：
- 注册、执行和取消延迟调用（超时）
- 创建可用于多种类型的通信的服务器和客户端的 Transports
- 启动进程以及相关的和外部通信程序的 Transports
- 将耗时函数调用委托给一个线程池
- 单线程（进程）的架构也避免多线程（进程）修改可变状态锁的问题

与事件循环交互的应用要显式的注册将运行的代码，让事件循环在资源可用时向应用代码发出必要的调用

## Future
future 是一个数据结构，表示还未完成的工作结果。事件循环可以监听 Future 对象是否完成，从而允许应用的一部分等待另一部分完成工作

## Task
Task 是 Future 的一个子类，他知道如何包装和管理一个协程的运行。任务需要的资源可用时，事件循环会调度任务允许，并返回一个结果，从而由其他协程消费

## 异步方法
使用 asyncio 意味着你要写异步方法
标准的同步方法：
```py
def regular_double(x):
  return 2*x
```
而一个异步方法：
```py
async def async_double(x):
  return 2*x
```

异步方法多了个 async
要调用异步方法，必须使用 await 关键字，但是不能在普通函数里使用 await 


## 协程
### 启动一个协程
一般异步方法被称之为协程，asyncio 事件循环可以通过多种不同的方法启动一个协程。一般对于入口函数，最简单的方法就是使用`run_until_complete()`，并将协程直接传入这个方法
```py
import asyncio

async def foo():
  print('this is a coroutine')


if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  try:
    print('coroutine begin')
    coro = foo()
    print('into event loop')
    loop.run_until_complete(coro)
  finally:
    print('close event loop')
    loop.close()

"""
输出：
coroutine begin
into event loop
this is a coroutine
close event loop
"""
```

这就是最简单的用 asyncio 调度协程的例子

### 从协程返回值
```py
import asyncio

async def foo():
  print('this is a coroutine')
  return 12

if __name__ == '__main__':
  loop = async.get_event_loop()
  try:
    print('coroutine begin')
    coro = foo()
    print('into event loop')
    res = loop.run_until_complete(coro)
    print(f"result is: {res}")
  finally:
    print('close event loop')
    loop.close()
```

### 协程调用协程
```py
import asyncio

async def main():
  res1 = await result1()
  res2 = await result2()
  return (res1, res2)

async def result1():
  return 1

async def result2():
  return 2

if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  try:
    result = loop.run_until_complete(main())
  finally:
    loop.close()

```

### 协程中调用普通函数
asyncio 的事件循环提供了三个方法调用普通函数：
1. call_soon：立即返会
   ```py
   loop.call_soon(callback, *args, context=None)


   import asyncio

   def foo(num):
    return num

   async def main(loop):
    loop.call_soon(foo, 1)


   if __name__ == '__main__':
      loop = async.get_event_loop()
      try:
        loop.run_until_complete(main(loop))
      finally:
        loop.close()
   ```
2. call_later：事件循环在延迟指定时间后调用函数
   ```py
   loop.call_later(delay, callback, *args, context=None)

   import asyncio

   def foo(num):
    return num

   async def main(loop):
    loop.run_later(1, foo, 1)


   if __name__ == '__main__':
      loop = asyncio.get_event_loop()
      try:
        loop.run_until_complete(main(loop))
      finally:
        loop.close()
   ```
3. call_at：使用事件循环内部时间
   ```py
   loop.call_at(when, callback, *args, context=None)

   import asyncio

   def foo(num):
    return num

   async def main(loop):
    now = loop.time()
    loop.run_at(now + 2, foo, 2)


   if __name__ == "__main__":
      loop = asyncio.get_event_loop()
      try:
        loop.run_until_complete(main(loop))
      finally:
        loop.close()
   ```

### 获取 Future 里的结果
future 表示未完成的工作结果，有以下状态
- Pending
- Running
- Done
- Cancelled

创建 future 的时候，task 为 Pending
事件循环调用执行的时候是 Running
调用完毕 Done
取消的 task 为 Cancel

```py
import asyncio

def foo(future, result):
  future.set_result(result)

if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  try:
    all_done = asyncio.Future()
    loop.call_soon(foo, all_done, 'done')
    result = loop.run_until_complete(all_done)
  finally:
    loop.close()
```

### Future 对象使用 await
```py
import asyncio

def foo(future, result):
  future.set_result(result)

async def main(loop):
  all_done = asyncio.Future()
  loop.call_soon(foo, all_done, 'done')
  res = await all_done

if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  try:
    loop.run_until_complete(main(loop))
  finally:
    loop.close()
```

### Future 回调


### 并发的执行任务
```py
import asyncio

async def child():
  return 1

async def main(loop):
  task = loop.create_task(child())
  task.cancel()

  try:
    await task
  except asyncio.CancelledError:
    print('task cancelled')
  else:
    print("res: ", task.result())


if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  try:
    loop.run_until_complete(main(loop))
  finally:
    loop.close()

```

### 等待多个协程
```py
import asyncio

async def num(n):
  try:
    await asyncio.sleep(n*0.1)
    return n
  except asyncio.CancelledError:
    print(f"{n} cancelled")
    raise


async def main():
  tasks = [num(i) for i in range(10)]
  complete, pendding = await asyncio.wait(tasks, timeout = 0.5)
  for i in complete:
    print(f"{i.result()}")
  if pendding:
    for p in pendding:
      p.cancel()

if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  try:
    loop.run_until_complete(main())
  finally:
    loop.close()

```

### 使用 gather 
gather 和 wait 的不同：
1. gather 无法取消
2. 返回值是一个结果列表
3. 传入传出顺序相同

```py
import asyncio

async def num(n):
  try:
    await asyncio.sleep(n*0.1)
  except asyncio.CancelledError:
    print(f"{n} cancelled")
    raise

async def main():
  tasks = [num(i) for i in range(10)]
  complete = await asyncio.gather(*tasks)
  for i in complete:
    print(i)


if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  try:
    loop.run_until_complete(main())
  finally:
    loop.close()


```

# 常用 API
- asyncio.run
- asyncio.get_event_loop()
- asyncio.wait
- asyncio.gather
- asyncio.sleep
- asyncio.wait_for
- asyncio.to_thread
- asyncio.ensure_future
- asyncio.as_completed
- asyncio.shield
- loop.create_task
- loop.run_until_complete
- loop.create_future
- loop.run_in_executor
- loop.call_soon
- loop.call_later
- loop.call_at
- loop.time
- task.cancel
- future.result
- future.set_result
- future.add_done_callback
- async with
- async for


## gather 与 wait 的区别
他们都可以让多个协程并发执行
- gather：意思是“收集”，他会收集协程的结果，按照输入协程的顺序保存对应执行结果
  - 封装的Task全程黑盒，只告诉你执行结果
- wait：返回值有两项，第一项表示已完成任务列表，第二项为等待的任务列表，每个任务都是Task实例
  - 会返回封装的 Task，结果要`.result()`获取


## asyncio.create_task  loop.create_task  asyncio.ensure_future
创建一个 Task 有这3中方法
`asyncio.create_task`基于`loop.create_task`，接受一个协程作为参数
`asyncio.ensure_future`除了接受协程，还可以是 Future 对象或 awaitable 对象：
1. 如果参数是协程，会调用`loop.create_task`，返回 Task
2. 如果是 Future 直接返回
3. 如果是一个 awaitable 对象，会 await 这个对象的 __await__ 方法，再执行一次 ensure_future，最后返回 Task 或 Future


## shield

```py
import asyncio

async def num(n);
  return n*2



async def main():
  task1 = asyncio.shield(num(1))
  task2 = asyncio.create_task(num(2))

  ts = asyncio.gather(task1, task2, return_exceptions=True)

  taks1.cancel()

  await ts

  """
   输出:
   [concurrent.futures._base.CancelledError(), 4]

  """

if __name__ == '__main__':
  asyncio.run(main())

```

使用步骤：
1. 创建 GatherFuture 对象
2. 取消任务
3. await gather



## asynccontextmanager
