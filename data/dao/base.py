from abc import ABC, abstractmethod
from typing import Optional, Dict

class UsageRecordDAO(ABC):
    """
    数据访问对象 (DAO) 抽象基类，用于访问用户使用记录。
    支持不同的数据源实现（如 CSV, MySQL, MongoDB 等）。
    """

    @abstractmethod
    def get_record(self, user_id: str, month: str) -> Optional[Dict]:
        """
        根据用户ID和月份获取使用记录
        
        :param user_id: 用户ID
        :param month: 月份 (格式: YYYY-MM)
        :return: 包含记录信息的字典，如果未找到则返回 None
        """
        pass
