# Typer 学习笔记
> 基于 mini_code_agent v0.1 项目，记录 Typer 命令行框架的实际用法、单命令模式特性与异常退出方式。

## 1. 我用到的代码
### 命令注册与应用初始化
```python
import typer
from rich.console import Console

app = typer.Typer(help="Mini Code Agent - 本地AI编程助手")
console = Console()

@app.command()
def ask(question: str = typer.Argument(..., help="发给AI的提问内容")):
    ...
```

### 异常退出控制
```python
except RuntimeError as e:
    console.print(f"[bold red]错误：[/bold red] {e}", err=True)
    raise typer.Exit(code=1)
```

### 程序入口启动
```python
def main():
    app()

if __name__ == "__main__":
    main()
```

## 2. 我的理解
1. **@app.command() 装饰器**
    作用是把普通 Python 函数注册为一条终端命令，函数名默认就是命令名，函数参数会自动映射为命令的入参，不需要手写参数解析逻辑。
2. **typer.Argument 位置参数**
    用来声明必填的位置参数，`...` 代表参数必填，`help` 字段会自动生成到命令的帮助文档里；配合 `Annotated` 写法是当前官方推荐的规范。
3. **单命令模式**
    当 Typer 应用内只注册了唯一一个命令时，会自动进入单命令模式：命令名会被隐去，参数直接挂在根命令下，调用时不需要输入命令名称。
4. **typer.Exit 退出码**
    用来主动终止程序并返回指定退出码，`code=1` 代表异常退出，`code=0` 代表正常退出，符合命令行工具的通用约定，方便外部脚本判断执行结果。

## 3. 踩坑
### 报错信息
```text
Usage: python -m src.code_agent [OPTIONS] {question}
Try 'python -m src.code_agent --help' for help.

Error: Got unexpected extra argument(s) (解释Pydantic的作用)
```

### 现象
执行 `python -m src.code_agent ask "解释Pydantic的作用"` 时报错，提示存在多余的位置参数。

### 原因
v0.1 版本只注册了 `ask` 一个命令，触发了 Typer 的单命令模式。此时 `ask` 不会被识别为子命令，而是被当作 `question` 参数的值，后续输入的问题文本就变成了多余参数。

### 解决
- 临时方案：去掉命令名，直接执行 `python -m src.code_agent "解释Pydantic的作用"`
- 长期方案：新增第二条子命令（如 `version`），Typer 会自动退出单命令模式，恢复 `ask` 子命令用法。

## 4. 参考
- Typer 官方文档：[https://typer.tiangolo.com/](https://typer.tiangolo.com/)
- 项目内参考：`src/code_agent/cli.py`