# 安装

# 使用 anaconda-navigator 创建环境

# 常用命令
```shell
# 创建环境
conda create -n name python=version

# 查看所有环境
conda env list

# 激活环境
activate name

# 退出环境
conda deactivate name 

# 删除环境
conda remove -n name --all

# 安装指定包 -c 为源
conda install numpy=1.19.2 -c conda-forge

# 更新指定的包或所有的包  --all 所有包
conda update numpy

# 卸载指定的包
conda remove numpy

# 列出当前环境中已安装的包
conda list

# 搜索指定的包
conda search pandas

# 清理Anaconda的缓存和不需要的包
conda clean --all
```