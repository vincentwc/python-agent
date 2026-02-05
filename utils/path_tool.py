"""
为整个工程提供统一的绝对路径
"""

import os


def get_project_path() -> str:
    """
    获取工程根目录绝对路径
    :return: 工程根目录绝对路径字符串
    """
    ocurrent_fiel = os.path.abspath(__file__)  # 当前文件绝对路径
    current_dir = os.path.dirname(ocurrent_fiel)  # 当前文件所在目录绝对路径
    return os.path.dirname(current_dir)  # 工程根目录绝对路径
  
def get_abs_path(relative_path: str) -> str:
    """
    获取相对路径对应的绝对路径
    :param relative_path: 相对路径字符串
    :return: 绝对路径字符串
    """
    return os.path.join(get_project_path(), relative_path)
  
# if __name__ == "__main__":
#     print(get_project_path())
#     print(get_abs_path("config/config.txt"))
