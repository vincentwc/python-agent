import os
from abc import ABC, abstractmethod
from typing import Optional
from langchain_community.chat_models.tongyi import BaseChatModel, ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.embeddings import Embeddings
from utils.config_handler import agent_config


def check_api_key():
    """
    检查环境变量中是否存在DASHSCOPE_API_KEY
    """
    if not os.environ.get("DASHSCOPE_API_KEY"):
        raise ValueError(
            "未检测到 DASHSCOPE_API_KEY 环境变量！\n"
            "请在项目根目录下创建 .env 文件，并配置 DASHSCOPE_API_KEY=sk-xxx\n"
            "或者参考 .env.example 文件。"
        )


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[BaseChatModel | Embeddings]:
        """
        生成模型实例
        :return: 模型实例
        """


class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[BaseChatModel]:
        """
        生成聊天模型实例
        :return: 聊天模型实例
        """
        check_api_key()
        return ChatTongyi(model=agent_config["chat_model_name"])


class EmbeddingsModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings]:
        """
        生成嵌入模型实例
        :return: 嵌入模型实例
        """
        check_api_key()
        return DashScopeEmbeddings(model=agent_config["embeddings_model_name"])


chat_model = ChatModelFactory().generator()
embeddings_model = EmbeddingsModelFactory().generator()
