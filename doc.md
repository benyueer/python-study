## pyenv
> pyenv是一个forked自ruby社区的简单、低调、遵循UNIX哲学的Python环境管理工具, 它可以轻松切换全局解释器版本, 同时结合vitualenv插件可以方便的管理对应的包源.

只要控制PATH变量就能够做到python版本的切换, pyenv通过在PATH头部插入shims路径来实现对python版本的控制.

### 安装
```shell
brew install pyenv 
```
配置环境变量

安装后要把你之前安装的python环境变量删除

### 使用
```shell
# 查看当前版本
pyenv version

# 查看所有版本
pyenv versions

# 查看所有可安装的版本
pyenv install --list

# 安装指定版本
pyenv install 3.6.5
# 安装新版本后rehash一下
pyenv rehash

# 删除指定版本
pyenv uninstall 3.5.2

# 指定全局版本
pyenv global 3.6.5

# 指定多个全局版本, 3版本优先
pyenv global 3.6.5 2.7.14

# 实际上当你切换版本后, 相应的pip和包仓库都是会自动切换过去的

```

* 在VSCode中使用





## poetry
> Poetry 和 Pipenv 类似，是一个 Python 虚拟环境和依赖管理工具，另外它还提供了包管理功能，比如打包和发布。你可以把它看做是 Pipenv 和 Flit 这些工具的超集。它可以让你用 Poetry 来同时管理 Python 库和 Python 程序。

### 安装
```shell
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```

### 使用
```shell

# 创建虚拟环境
poetry env use python  # 创建了名为python的虚拟环境

# 激活环境
poetry shell
  # 或使用 run 
  poetry run python main

# 退出环境
exit

# 删除环境
poetry env remove python  # 删除了名为python的环境

```

* 在VS Code 中使用
创建并激活环境后`which python`找到环境地址，设置interpreter
