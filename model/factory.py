from abc import ABC, abstractmethod
from typing import Optional

from utils.config_handler import agent_config
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import BaseChatModel, ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings


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
        return ChatTongyi(model=agent_config["chat_model_name"])


class EmbeddingsModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings]:
        """
        生成嵌入模型实例
        :return: 嵌入模型实例
        """
        return DashScopeEmbeddings(model=agent_config["embeddings_model_name"])


chat_model = ChatModelFactory().generator()
embeddings_model = EmbeddingsModelFactory().generator()
