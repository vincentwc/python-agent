# 系统架构设计文档 (Architecture Design)

本文档旨在帮助开发人员快速理解 **智扫通 (Smart Cleaner Agent)** 的核心架构、数据流转及关键模块设计。

## 1. 系统分层架构 (Layered Architecture)

系统整体采用典型的 **分层架构**，自上而下分为四层：

```mermaid
graph TD
    User((User)) --> UI[前端展示层 (Streamlit UI)]
    UI --> AgentCore[智能体核心层 (ReactAgent)]
    
    subgraph AgentCore
        Router{路由/规划}
        Middleware[中间件 (Log/Monitor)]
        PromptEngine[提示词引擎]
    end
    
    AgentCore --> Tools[工具服务层 (Tools & RAG)]
    
    subgraph Tools
        Weather[天气服务]
        Location[位置服务]
        RAG[RAG 知识库服务]
        External[外部数据源]
    end
    
    Tools --> Infra[基础设施层 (Infrastructure)]
    
    subgraph Infra
        LLM[DashScope LLM]
        VectorDB[ChromaDB]
        FileSystem[本地文件/CSV]
    end
```

### 1.1 前端展示层 (Frontend)
*   **文件**: `app.py`
*   **职责**: 
    *   处理用户交互（输入/输出）。
    *   维护会话状态 (`st.session_state`)。
    *   流式渲染回复。
    *   **商业化要点**: 这里的代码应当只负责"显示"，不包含任何业务逻辑。

### 1.2 智能体核心层 (Agent Core)
*   **文件**: `agent/react_agent.py`, `agent/tools/middleware.py`
*   **职责**:
    *   **大脑**: 基于 ReAct (Reasoning + Acting) 模式，决定是直接回答用户，还是调用工具。
    *   **中间件**: 实现了类似 Web 框架的拦截器机制（日志记录、动态提示词切换、工具调用监控）。
    *   **状态管理**: 维护对话上下文 (`messages`)。

### 1.3 工具服务层 (Tools Service)
*   **文件**: `agent/tools/agent_tools.py`, `rag/rag_service.py`
*   **职责**:
    *   **RAG**: 封装了文档检索、切片、向量化逻辑。
    *   **原子能力**: 提供具体的功能函数（如查天气、查ID）。
    *   **隔离性**: 每个工具都是独立的，互不依赖。

### 1.4 基础设施层 (Infrastructure)
*   **文件**: `model/factory.py`, `rag/vector_store.py`, `utils/`
*   **职责**:
    *   模型工厂：统一管理 LLM 和 Embedding 模型的初始化。
    *   向量数据库：管理 ChromaDB 的连接和持久化。
    *   配置管理：加载 YAML 和 环境变量。

---

## 2. 核心请求链路 (Request Lifecycle)

当用户输入 "北京今天天气怎么样？" 时，数据流转如下：

1.  **用户输入**: `app.py` 接收文本。
2.  **任务分发**: 调用 `ReactAgent.execute_stream("北京今天天气怎么样？")`。
3.  **模型思考 (Thought)**: 
    *   LLM 接收提示词 + 用户问题。
    *   LLM 判断需要外部信息，输出 "Call Tool: get_weather('北京')"。
4.  **工具执行 (Action)**:
    *   `monitor_tool` 中间件拦截调用，记录日志。
    *   执行 `get_weather('北京')`，返回 "北京天气晴..."。
5.  **结果生成 (Observation)**:
    *   工具结果回传给 LLM。
    *   LLM 结合工具结果，生成最终自然语言回复。
6.  **流式响应**: `app.py` 逐字渲染结果给用户。

---

## 3. 关键设计模式 (Design Patterns)

*   **工厂模式 (Factory Pattern)**: `model/factory.py` 用于创建不同配置的模型实例，方便未来切换模型供应商（如切换到 OpenAI 或 DeepSeek）。
*   **装饰器模式 (Decorator Pattern)**: `middleware.py` 使用装饰器 (`@wrap_tool_call`) 实现了 AOP (面向切面编程)，将日志和监控逻辑与业务逻辑解耦。
*   **单例模式 (Singleton Pattern)**: (隐式) Streamlit 的 `st.session_state` 实际上充当了会话级别的单例容器。

## 4. 商业化改进方向 (Roadmap)

为了从 Demo 走向 Product，我们需要关注：

1.  **稳定性**: 引入重试机制 (Retries) 和断路器 (Circuit Breaker)。
2.  **可观测性**: 接入 Prometheus/Grafana 或 LangSmith 进行链路追踪。
3.  **多租户**: 区分不同用户的知识库和对话历史。
4.  **异步化**: 将耗时的 RAG 操作改为异步 (`async/await`) 提高并发能力。
