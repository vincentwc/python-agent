import os
import hashlib
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader


def get_file_md5_hex(file_path: str):
    """
    获取文件的MD5值,返回16进制字符串
    :param file_path: 文件路径
    :return: 文件的MD5值,16进制字符串
    """
    if not os.path.exists(file_path):
        logger.error(f"[md5计算]文件{file_path}不存在")
        return None
    if not os.path.isfile(file_path):
        logger.error(f"[md5计算]文件{file_path}不是文件")
        return None
    md5_obj = hashlib.md5()
    chunk_size = 4096  # 4KB分片，避免文件过大爆内存

    try:
        with open(file_path, "rb") as f:  # 以二进制只读模式打开文件
            while chunk := f.read(chunk_size):  # 每次读取4KB数据
                md5_obj.update(chunk)  # 更新MD5值
                md5_hex = md5_obj.hexdigest()  # 每次读取后立即计算MD5值
                return md5_hex  # 每次读取后返回MD5值
    except Exception as e:
        logger.error(f"[md5计算]文件{file_path}md5失败,{str(e)}")
        return None


def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):
    """
    列出目录下所有的文件列表(允许的文件后缀)
    :param path: 目录路径或文件路径
    :param allowed_types: 允许的文件类型列表
    :return: 目录下所有允许的文件路径列表
    """
    files = []
    if not os.path.exists(path):
        logger.error(f"[listdir_with_allowed_type]目录{path}不存在")
        return allowed_types
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]路径{path}不是文件夹")
        return allowed_types

    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path, f))

    return tuple(files)


def pdf_loader(file_path: str, passwd=None) -> list[Document]:
    """
    加载PDF文件
    :param file_path: PDF文件路径
    :return: PDF文档对象
    """
    return PyPDFLoader(file_path, password=passwd).load()


def txt_loader(file_path: str) -> list[Document]:
    """
    加载txt文件
    :param file_path: txt文件路径
    :return: txt文档对象
    """
    return TextLoader(file_path, encoding="utf-8").load()
