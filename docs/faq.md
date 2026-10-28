# FAQ 常见问题
> 基于 mini_code_agent v0.1，汇总开发、运行阶段高频报错与解决方案，作为快速排错手册。

## 1. 我用到的代码
### 标准启动命令（bash）
```bash
python -m src.code_agent "你的问题"
```

### .env 读取代码片段
```python
load_dotenv()
self.client = OpenAI(api_key=os.getenv("LLM_API_KEY"), base_url=os.getenv("LLM_BASE_URL"))
```

### Pydantic校验捕获
```python
try:
    result = BaseAnswer.model_validate_json(result_text)
except ValidationError as e:
    raise RuntimeError(f"大模型返回格式不符合要求: {e}")
```

## 2. 我的理解
1. **FAQ定位**
    FAQ 和 dev-log、notes 不同，它不记录学习过程，只沉淀可复用的故障现象、原因、处理步骤，以后再踩相同坑直接查阅，不用重新复盘。
2. **高频问题归类**
    主要分为四类：包导入启动问题、Typer命令行问题、环境变量密钥问题、大模型返回校验问题，覆盖 v0.1 全部阻塞性报错。
3. **预防思路**
    很多报错根源是启动方式不规范、配置文件管理不规范、对框架隐式特性（Typer单命令模式）不了解。
4. **迭代规则**
    后续 v0.2、v0.3 遇到新报错，直接追加到这份文档，保持一份统一排错清单。

## 3. 踩坑
### 坑1：相对导入报错
#### 报错信息
```text
ImportError: attempted relative import with no known parent package
```
#### 现象
直接运行 cli.py，或者在非项目根目录执行启动命令。
#### 原因
Python 无法识别包层级，`.` 相对导入没有父包上下文。
#### 解决
必须在项目根目录，使用 `python -m src.code_agent` 方式启动，禁止直接 `python src/code_agent/cli.py`。

### 坑2：Typer单命令模式传参报错
#### 报错信息
```text
Usage: python -m src.code_agent [OPTIONS] {question}
Try 'python -m src.code_agent --help' for help.

Error: Got unexpected extra argument(s) (xxx)
```
#### 现象
输入 `python -m src.code_agent ask "xxx"` 报错。
#### 原因
只注册一条命令触发Typer单命令模式，ask不再是子命令。
#### 解决
临时：去掉 ask，直接传问题；长期（v0.2）新增一条子命令，退出单命令模式。

### 坑3：API Key 不生效，提示缺少密钥
#### 报错信息
```text
RuntimeError: 调用大模型失败: You didn't provide an API key.
```
#### 现象
程序正常启动，调用接口时报认证失败。
#### 原因
只改了 `.env.example`、`.env` 文件不存在、变量名大小写不一致、等号两侧带空格、文件不在根目录。
#### 解决
复制 `.env.example` → `.env`，填入真实密钥；核对变量名；等号左右不要空格。

### 坑4：Pydantic格式校验失败
#### 报错信息
```text
1 validation error for BaseAnswer
content
  Field required [type=missing, input_value={'summary': 'xxx'}, input_type=dict]
```
#### 现象
大模型返回内容缺少字段，或者返回多余说明文字，不是纯净JSON。
#### 原因
模型随机性高，没有严格遵守JSON输出要求。
#### 解决
prompt强制要求只输出JSON；调用时开启 `response_format={"type":"json_object"}`；降低 temperature。

### 坑5：ValidationError导入拼写错误
#### 报错信息
```text
ImportError: cannot import name 'ValiadationError' from 'pydantic'
Did you mean: 'ValidationError'?
```
#### 现象
导入异常类时报导入失败。
#### 原因
手写拼写错误。
#### 解决
修正为 `from pydantic import ValidationError`。

## 4. 参考
- Typer 官方文档：[https://typer.tiangolo.com/](https://typer.tiangolo.com/)
- Pydantic 官方文档：[https://docs.pydantic.dev/](https://docs.pydantic.dev/)
- python-dotenv 官方文档：[https://pypi.org/project/python-dotenv/](https://pypi.org/project/python-dotenv/)
- 项目内参考：`dev-log/v0.1.md`、`notes/` 下各笔记文档