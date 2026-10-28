# Pydantic 学习笔记
> 基于 mini_code_agent v0.1 项目，记录数据模型定义、JSON 格式校验与异常捕获的实际用法，用于约束大模型返回结构。

## 1. 我用到的代码
### 数据模型定义（schemas.py）
```python
from pydantic import BaseModel, Field

class BaseAnswer(BaseModel):
    summary: str = Field(description="一句话总结回答内容")
    content: str = Field(description="详细回答正文")
```

### JSON 解析与校验（llm.py）
```python
from pydantic import ValidationError
from .schemas import BaseAnswer

result_text = response.choices[0].message.content
result = BaseAnswer.model_validate_json(result_text)

except ValidationError as e:
    raise RuntimeError(f"大模型返回格式不符合要求: {e}")
```

## 2. 我的理解
1. **BaseModel 基础模型类**
    继承 `BaseModel` 后，类就具备了数据校验、类型转换、JSON 解析的能力，相当于定义了一份强制遵守的数据“合同”。
2. **字段类型注解**
    通过 `summary: str` 这种类型注解声明字段类型，Pydantic 会严格校验输入值的类型，不符合就抛出异常，从源头避免脏数据。
3. **model_validate_json 方法**
    可以直接把 JSON 字符串解析成模型对象，同时完成格式校验和字段检查，非常适合处理大模型返回的 JSON 结果。
4. **项目里的必要性**
    大模型的输出是不可控的，有可能返回多余文字、缺字段、格式错乱。用 Pydantic 做一层校验，能把格式问题拦截在底层，不会导致上层业务代码崩溃。

## 3. 踩坑
### 坑 1：ValidationError 拼写错误
#### 报错信息
```text
ImportError: cannot import name 'ValiadationError' from 'pydantic'
Did you mean: 'ValidationError'?
```
#### 现象
导入异常类时报错，提示找不到该名称。
#### 原因
手动输入时字母顺序写错，把 `ValidationError` 拼成了 `ValiadationError`（多插入了一个字母 i）。
#### 解决
修正拼写为 `ValidationError`；导入类名时优先参考官方文档，避免凭印象手写。

### 坑 2：大模型返回格式不合法导致校验失败
#### 报错信息
```text
1 validation error for BaseAnswer
content
  Field required [type=missing, input_value={'summary': 'xxx'}, input_type=dict]
```
#### 现象
大模型返回的 JSON 缺少字段，或附带了额外的解释文字，导致解析失败。
#### 原因
模型温度过高，没有严格遵守 JSON 输出要求；未开启 `response_format={"type": "json_object"}` 强制参数。
#### 解决
- 调用接口时开启 `response_format={"type": "json_object"}`
- 调低 `temperature` 到 0.1 左右，降低输出随机性
- 在 system prompt 中明确强调只返回 JSON，不要多余文字

## 4. 参考
- Pydantic 官方文档：[https://docs.pydantic.dev/](https://docs.pydantic.dev/)
- 项目内参考：`src/code_agent/schemas.py`、`src/code_agent/llm.py`