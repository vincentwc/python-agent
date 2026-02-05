import os
from utils.logger_handler import logger
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from model.factory import embeddings_model
from utils.config_handler import chroma_config
from utils.file_handler import (
    get_file_md5_hex,
    listdir_with_allowed_type,
    pdf_loader,
    txt_loader,
)
from utils.path_tool import get_abs_path


class VectoreStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_config["collection_name"],
            embedding_function=embeddings_model,
            persist_directory=chroma_config["persist_directory"],
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_config["chunk_size"],
            chunk_overlap=chroma_config["chunk_overlap"],
            separators=chroma_config["separators"],
            length_function=len,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_config["k"]})

    def load_documents(self):
        """
        从数据文件夹内读取文件，转为向量存入到向量存储，要计算md5值去重
        :param documents: 文档列表
        """

        def check_md5_hex(md5_for_sheck: str):
            """
            检查md5文件是否存在
            :param md5_for_sheck: md5值
            :return: 是否存在
            """
            if not os.path.exists(
                get_abs_path(chroma_config["md5_hex_store"])
            ):  # 检查md5文件是否存在
                open(
                    get_abs_path(chroma_config["md5_hex_store"]), "w", encoding="utf-8"
                ).close()  # 创建空文件
                return False  # md5没处理
            with open(
                get_abs_path(chroma_config["md5_hex_store"]), "r", encoding="utf-8"
            ) as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_sheck:
                        return True  # md5已处理
                return False  # md5没处理

        def save_md5_hex(md5_for_check: str):
            """
            保存md5值到文件
            :param md5_for_check: md5值
            """
            with open(
                get_abs_path(chroma_config["md5_hex_store"]), "a", encoding="utf-8"
            ) as f:
                f.write(md5_for_check + "\n")

        def get_file_documents(read_path: str):
            """
            读取文档
            :param read_path: 文件路径
            :return: 文档列表
            """
            if read_path.endswith(".pdf"):
                return pdf_loader(read_path)
            elif read_path.endswith(".txt"):
                return txt_loader(read_path)
            return []

        allowed_file_path = listdir_with_allowed_type(
            get_abs_path(chroma_config["data_path"]),
            tuple(chroma_config["allowed_file_type"]),
        )

        for path in allowed_file_path:
            # 获取文件的md5
            md5_hex = get_file_md5_hex(path)

            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]文件{path}的内容已经在知识库内，跳过")
                continue  # md5已处理，跳过
            try:
                documents: list[Document] = get_file_documents(path)
                if not documents:
                    logger.error(f"[加载知识库]文件{path}的内容为空，跳过")
                    continue  # 内容为空，跳过
                # 对文档进行切分
                split_documents: list[Document] = self.spliter.split_documents(
                    documents
                )
                if not split_documents:
                    logger.error(f"[加载知识库]文件{path}的内容切分后为空，跳过")
                    continue  # 切分后为空，跳过
                # 为文档添加元数据
                # for doc in split_documents:
                #     doc.metadata["source"] = path

                self.vector_store.add_documents(split_documents)  # 向向量存储添加文档

                save_md5_hex(md5_hex)  # 保存md5值

                logger.info(f"[加载知识库]文件{path}的内容加载成功")
            except Exception as e:
                # exc_info为true会记录详情的堆栈，为false仅记录错误本身
                logger.error(
                    f"[加载知识库]文件{path}的内容加载失败,{str(e)}", exc_info=True
                )

# if __name__ == "__main__":
#     vs = VectoreStoreService()
#     vs.load_documents()

#     retriever = vs.get_retriever()

#     res = retriever.invoke("迷路")

#     for r in res:
#         print(r.page_content)
#         print("=" * 20)
