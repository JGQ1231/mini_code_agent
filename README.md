# mini_code_agent

本地 AI 编程助手命令行工具。通过命令行输入问题，调用大模型（DeepSeek）回答，返回「总结 + 详细内容」结构化结果，终端彩色输出。

> 当前版本：v0.1（基础可运行版本）
> 定位：学习 Python CLI 工程化 + 大模型应用开发的练手项目，适合作为 AI 应用开发方向的作品集。

---

## ✨ 功能特性

- 命令行输入问题，调用 DeepSeek 大模型接口
- 返回结构化结果：**一句话总结 + 详细回答正文**
- 彩色终端输出，可读性好
- 配置与代码分离，API 密钥通过 `.env` 管理，避免泄露
- Pydantic 强制校验大模型返回格式，防止脏数据导致程序崩溃
- 分层架构设计，便于后续扩展（多轮对话、多模型、RAG）

---

## 🛠️ 技术栈

| 技术 | 用途 |
|---|---|
| Python 3.10+ | 主体开发语言 |
| Typer | 命令行框架（命令注册、参数解析） |
| Rich | 终端彩色输出 |
| Pydantic | 数据模型定义与格式校验 |
| python-dotenv | 读取 `.env` 环境变量配置 |
| OpenAI SDK | 调用 DeepSeek 兼容接口 |

---

## 📈 版本进度

- [x] v0.1 基础命令行框架 + LLM 调用 + 结构化返回（已完成）
- [ ] v0.2 退出单命令模式，新增子命令与日志
- [ ] v0.3 多轮对话历史
- [ ] v0.4 多模型切换
- [ ] v0.5 RAG 检索增强回答
- [ ] v0.6 单元测试与打包分发

---

## 📁 项目结构

```
mini_code_agent/
├── src/code_agent/          # 源码包
│   ├── __init__.py          # 包标记文件
│   ├── __main__.py          # 包启动入口
│   ├── cli.py               # 命令行入口、ask命令、彩色输出
│   ├── llm.py               # 大模型调用封装、配置读取、异常处理
│   └── schemas.py           # Pydantic 数据模型定义
├── dev-log/                 # 版本开发日志（按版本留痕）
│   └── v0.1.md
├── docs/                    # 项目文档
│   ├── architecture.md      # 架构设计说明
│   ├── faq.md               # 排错手册
│   └── screenshots/         # 运行截图
├── notes/                   # 配套学习笔记
│   ├── typer.md
│   ├── pydantic.md
│   ├── dotenv.md
│   └── python-package.md
├── .env                     # 本地私有密钥配置（不提交）
├── .env.example             # 配置模板（提交）
├── .gitignore               # Git 忽略规则
├── CHANGELOG.md             # 版本变更记录
├── README.md
└── requirements.txt         # Python 依赖清单
```

---

## 🚀 环境部署

### 1. 创建虚拟环境

```bash
# 在项目根目录执行
python -m venv venv

# Windows PowerShell 激活
venv\Scripts\activate

# Linux / macOS 激活
source venv/bin/activate
```

激活成功后，命令提示符前会出现 `(venv)`。

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

> 依赖有新增时，用 `pip freeze > requirements.txt` 重新导出依赖清单，保持清单和实际安装一致。

### 3. 配置密钥

复制模板生成 `.env`：

```bash
cp .env.example .env
```

编辑 `.env`，填入你的 API 密钥：

```text
LLM_API_KEY=sk-你的密钥
LLM_BASE_URL=[https://api.deepseek.com/v1](https://api.deepseek.com/v1)
LLM_MODEL=deepseek-chat
```

> ⚠️ `.env` 已加入 `.gitignore`，不会提交，密钥切勿泄露。

### 4. 运行

```bash
python -m src.code_agent "你的问题"
```

示例：

```bash
python -m src.code_agent "解释Pydantic的作用"
```

---

## 📸 运行截图

![v0.1 运行截图](docs/screenshots/v0.1.png)

> 截图待补充：放置 v0.1 实际运行输出效果图。

---

## ⚠️ 已知限制（v0.1）

- **Typer 单命令模式**：当前只注册了 `ask` 一个命令，调用时**不能带 `ask` 子命令**，需直接传参数。
- 无多轮对话能力，每次提问均为独立会话。
- 无日志系统，异常统一以通用错误提示展示。

---

## 📌 后续计划

- v0.2：新增第二条子命令退出单命令模式，补充日志输出
- v0.3：多轮对话历史
- v0.4：多模型切换
- v0.5：RAG 检索增强
- v0.6：单元测试与打包分发

详见 [CHANGELOG.md](CHANGELOG.md) 与 `dev-log/`。

---

## 📚 相关文档

- [架构设计](docs/architecture.md)
- [常见问题 FAQ](docs/faq.md)
- [开发日志 v0.1](dev-log/v0.1.md)
- [学习笔记](notes/)

---

## 🔒 安全提示

- API 密钥只存在 `.env`，绝不提交到 Git。
- 不要将密钥发送给他人，密钥泄露请立即在平台删除并重新创建。

---

## 📄 协议

本项目为个人学习用途，遵循 MIT 协议（待补充）。

---

文档全部输出完毕。README 直接复制覆盖项目根目录的 `README.md` 即可。需要我把这份 README 一起落到本地并教你按之前约定的顺序做 Git 首次提交吗？