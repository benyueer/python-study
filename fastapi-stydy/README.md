## alembic

### 安装
```shell
pip install alembic
```

### 配置
修改`alembic.ini`的`sqlalchemy.url`为数据库地址
修改`env.py`的`target_metadata`为`Base`的`metadata`

### 操作
1. 生成版本
   ```
   alembic revision --autogenerate -m "message" 将当前模型中的状态生成迁移文件
   ```
2. 更新数据库
   ```
   alembic upgrade head   将生成的迁移文件执行到数据库中
   alembic downgrade head   降级
   ```
3. 命令
   ```
    init：创建一个 alembic 仓库。
    revision：创建一个新的版本文件。
    --autogenerate：自动将当前模型的修改，生成迁移脚本。
    -m：本次迁移做了哪些修改，用户可以指定这个参数，方便回顾。
    upgrade：将指定版本的迁移文件映射到数据库中，会执行版本文件中的 upgrade 函数。如果有多个迁移脚本没有被映射到数据库中，那么会执行多个迁移脚本。
    [head]：代表最新的迁移脚本的版本号。
    downgrade：会执行指定版本的迁移文件中的 downgrade 函数。
    heads：展示head指向的脚本文件版本号。
    history：列出所有的迁移版本及其信息。
    current：展示当前数据库中的版本号。另外，在你第一次执行 upgrade 的时候，就会在数据库中创建一个名叫 alembic_version 表，这个表只会有一条数据，记录当前数据库映射的是哪个版本的迁移文件。
   ```
