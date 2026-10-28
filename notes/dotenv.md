# python-dotenv 学习笔记
> 基于 mini_code_agent v0.1 项目，记录环境变量加载、密钥隔离规范与配置文件分离的实践方法。

## 1. 我用到的代码
### .env 配置文件（本地私有）
```text
LLM_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
LLM_BASE_URL=[https://api.deepseek.com/v1](https://api.deepseek.com/v1)
LLM_MODEL=deepseek-chat
```

### .env.example 配置模板（公开提交）
```text
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=[https://api.deepseek.com/v1](https://api.deepseek.com/v1)
LLM_MODEL=deepseek-chat
```

### 代码中加载与读取
```python
import os
from dotenv import load_dotenv

load_dotenv()

self.client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL")
)
self.model = os.getenv("LLM_MODEL", "deepseek-chat")
```

## 2. 我的理解
1. **配置与代码分离**
    把 API 密钥、接口地址等敏感配置从 Python 代码中抽离到独立文件，避免密钥硬编码在源码里，降低泄露风险。
2. **.env 与 .env.example 的分工**
    - `.env` 存放真实密钥，被 `.gitignore` 排除，不提交到代码仓库
    - `.env.example` 只保留变量名和占位符，公开提交，告诉使用者项目需要哪些配置项
3. **load_dotenv() 的作用**
    自动读取项目根目录下的 `.env` 文件，把里面的键值对加载到系统环境变量中，后续通过 `os.getenv()` 即可读取。
4. **os.getenv 带默认值**
    `os.getenv("LLM_MODEL", "deepseek-chat")` 第二个参数是兜底默认值，当 `.env` 中没有对应配置时，使用默认值，提高程序健壮性。

## 3. 踩坑
### 报错信息
```text
RuntimeError: 调用大模型失败: 
You didn't provide an API key. You need to provide your API key in an Authorization header.
```

### 现象
程序启动后调用大模型时报认证错误，提示缺少 API Key。

### 常见原因
- 只修改了 `.env.example`，没有复制生成 `.env` 文件
- `.env` 文件不在项目根目录，`load_dotenv()` 找不到
- 变量名拼写错误、大小写不匹配（`llm_api_key` ≠ `LLM_API_KEY`）
- 等号前后有多余空格，导致读取到的值带空格

### 解决
- 复制 `.env.example` 为 `.env`，填入真实密钥
- 确认 `.env` 位于项目根目录
- 核对变量名大小写与代码中 `os.getenv()` 的参数完全一致
- 等号两侧不要加空格

## 4. 参考
- python-dotenv 官方文档：[https://pypi.org/project/python-dotenv/](https://pypi.org/project/python-dotenv/)
- 项目内参考：`src/code_agent/llm.py`、`.env.example`