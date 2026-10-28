# Python 包机制学习笔记

> 
> 基于 mini_code_agent v0.1 项目，记录 Python 包结构、`__main__.py` 入口、`-m` 启动方式与相对导入的原理和踩坑经验。

## 1. 我用到的代码

### 包启动入口 **main**.py

```
from .cli import app

if __name__ == "__main__":
    app()
```

### 包内相对导入（cli.py 示例）

```
import typer
from rich.console import Console
from .llm import LLMClient
```

### 正确启动命令（bash）

```
# 项目根目录下执行，以模块方式启动
python -m src.code_agent "解释Pydantic的作用"
```

### 错误启动方式（直接运行文件）

```
# 会触发相对导入报错
python src/code_agent/cli.py
```

## 2. 我的理解

1. **`__main__.py` 的作用**
 它是 Python 包的入口文件。当使用 `python -m 包名` 启动时，Python 会自动在包内查找 `__main__.py` 并执行其中的代码，相当于整个包的“主函数”。
2. **`-m` 参数的意义**
 `-m` 代表 module，告诉 Python 以**模块/包模式**运行目标。此时 Python 会把当前目录加入搜索路径，识别包的层级结构，相对导入才能正常工作。
3. **相对导入依赖包模式**
 `from .llm import LLMClient` 里的 `.` 表示“当前包内”，只有 Python 知道当前文件属于哪个包时，才能解析这个点号。直接单独运行 py 文件时，文件被视为独立脚本，没有包上下文，相对导入就会失效。
4. **`__init__.py` 的作用**
 空的 `__init__.py` 用来标记文件夹是一个 Python 包。没有这个文件时，Python 不会把文件夹识别为可导入的包，包内的模块导入和 `-m` 启动都会受影响。

## 3. 踩坑

### 报错信息

```
Traceback (most recent call last):
  File "src/code_agent/__main__.py", line 1, in <module>
    from .cli import app
ImportError: attempted relative import with no known parent package
```

### 现象

直接右键运行 py 文件，或者用 `python xxx.py` 执行单个文件时，报相对导入错误。

### 原因

直接运行单个文件时，Python 把它当作独立脚本处理，无法识别它所属的包层级，`.` 相对导入没有父包上下文，因此失效。

### 解决

- 统一使用 `python -m src.code_agent` 的模块方式启动，始终在项目根目录下执行命令
- 不要直接双击或单独运行包内的单个 py 文件
- 确保 `src/code_agent/__init__.py` 文件存在，标记该目录为 Python 包

## 4. 参考

- Python 官方文档：模块与包
- 项目内参考：`src/code_agent/__main__.py`、`src/code_agent/__init__.py`、`src/code_agent/cli.py`