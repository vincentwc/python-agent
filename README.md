# 智扫通机器人客服 (Smart Cleaner Agent)

这是一个基于 Python 的智能客服机器人项目，使用了 LangChain 框架和通义千问大模型（DashScope），结合 RAG（检索增强生成）技术，为用户提供关于扫地机器人的问答服务。

## 📋 功能特点

*   **智能问答**：基于大模型回答用户的自然语言问题。
*   **知识库检索 (RAG)**：自动检索本地文档（PDF, TXT），提供准确的产品知识。
*   **流式响应**：打字机效果的流畅对话体验。
*   **多工具支持**：集成天气查询、位置查询、使用记录查询等工具。
*   **友好的 UI**：基于 Streamlit 构建的现代化 Web 界面。

## 🛠️ 技术栈

*   **Python**: 3.10+
*   **LangChain**: 智能体编排
*   **Streamlit**: Web 界面
*   **ChromaDB**: 向量数据库
*   **DashScope (通义千问)**: LLM 和 Embeddings

## 🚀 快速开始

### 1. 环境准备

确保你已经安装了 Python 3.10 或更高版本。

```bash
git clone <repository_url>
cd python-agent
```

### 2. 安装依赖

建议使用虚拟环境：

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

安装项目依赖：

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

⚠️ **安全提示**：API Key 属于敏感信息，请确保不要将包含真实 Key 的 `.env` 文件提交到代码仓库。

1. **复制配置文件模板**：
   `.env.example` 是公开的配置模板，仅包含配置项名称。
   ```bash
   cp .env.example .env
   ```

2. **编辑 `.env` 文件**：
   `.env` 是本地私有配置文件（已被 `.gitignore` 忽略）。
   打开 `.env` 文件，填入你的阿里云 DashScope API Key：
   ```properties
   DASHSCOPE_API_KEY=sk-your_real_api_key_here
   ```

### 4. 运行应用

```bash
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`。

## 📂 项目结构

```
.
├── agent/              # 智能体核心逻辑
│   ├── tools/          # 自定义工具
│   └── react_agent.py  # React 智能体实现
├── config/             # 配置文件 (YAML)
├── data/               # 知识库数据和外部数据
├── model/              # 模型工厂
├── prompts/            # 提示词模板
├── rag/                # RAG 服务 (向量检索)
├── utils/              # 通用工具函数
├── app.py              # Streamlit 启动入口
├── requirements.txt    # 项目依赖
└── .env                # 环境变量 (不要提交到版本控制)
```

## 📝 开发指南

*   **添加新工具**: 在 `agent/tools/` 下创建新工具函数，并在 `agent/react_agent.py` 中注册。
*   **修改提示词**: 编辑 `prompts/` 下的文本文件或 `config/prompts.yaml`。
*   **更新知识库**: 将 PDF 或 TXT 文件放入 `data/` 目录，重启应用会自动加载（注意：目前逻辑是启动时加载，大量文件建议优化为离线脚本）。

## 📄 许可证

MIT License
