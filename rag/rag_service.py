"""
RAG服务[总结服务类]:用户提问，搜索参看资料，将提问和参考资料提交给模型，模型返回总结结果
"""

from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from model.factory import chat_model
from rag.vector_store import VectoreStoreService
from utils.prompt_loader import load_rag_prompts


def print_promot(prompt: str):
    """
    打印提示词
    :param prompt: 提示词字符串
    :return: prompt
    """
    logger.info("=" * 20)
    logger.info(prompt.to_string())
    logger.info("=" * 20)
    return prompt


class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectoreStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self.__init_chain()

    def __init_chain(self):
        """
        初始化链
        :return: 链实例
        """
        return self.prompt_template | print_promot | self.model | StrOutputParser()

    def retriever_docs(self, query: str) -> list[Document]:
        """
        检索文档
        :param query: 查询字符串
        :return: 检索到的文档列表
        """
        return self.retriever.invoke(query)

    def rag_summarize(self, query: str) -> str:
        """
        RAG总结
        :param query: 查询字符串
        :return: 总结结果字符串
        """
        try:
            dcontext_docs = self.retriever_docs(query)

            context = ""
            counter = 0
            for doc in dcontext_docs:
                counter += 1
                context += f"[参考资料{counter}]:参考资料:{doc.page_content}|参考元数据:{doc.metadata}\n"

            logger.info(f"[rag_summarize]检索到{counter}条参考资料")

            return self.chain.invoke(
                {
                    "input": query,
                    "context": context,
                }
            )
        except Exception as e:
            logger.error(f"[rag_summarize]执行失败: {str(e)}", exc_info=True)
            return "抱歉，知识库总结服务暂时不可用。"


if __name__ == "__main__":
    rag = RagSummarizeService()
    print(rag.rag_summarize("小户型适合哪些扫地机器人"))
