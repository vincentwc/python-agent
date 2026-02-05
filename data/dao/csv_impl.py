import os
import csv
from typing import Optional, Dict
from data.dao.base import UsageRecordDAO
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

class CSVUsageRecordDAO(UsageRecordDAO):
    """
    基于 CSV 文件的使用记录数据访问实现
    """

    def __init__(self, file_path: str):
        """
        初始化 CSV DAO
        
        :param file_path: CSV 文件路径（相对路径或绝对路径）
        """
        self.file_path = get_abs_path(file_path)
        self._cache = {}
        self._load_data()

    def _load_data(self):
        """
        加载 CSV 数据到内存缓存中
        """
        if not os.path.exists(self.file_path):
            logger.error(f"[CSVUsageRecordDAO] 文件不存在: {self.file_path}")
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    user_id = row.get("user_id")
                    time = row.get("time")
                    
                    if not user_id or not time:
                        continue

                    if user_id not in self._cache:
                        self._cache[user_id] = {}
                    
                    # 映射 CSV 列名到业务字段
                    self._cache[user_id][time] = {
                        "特征": row.get("feature", ""),
                        "效率": row.get("efficiency", ""),
                        "耗材": row.get("consumables", ""),
                        "对比": row.get("comparison", ""),
                    }
            logger.info(f"[CSVUsageRecordDAO] 成功加载数据，共 {len(self._cache)} 个用户")
        except Exception as e:
            logger.error(f"[CSVUsageRecordDAO] 加载数据失败: {str(e)}", exc_info=True)

    def get_record(self, user_id: str, month: str) -> Optional[Dict]:
        """
        根据用户ID和月份获取使用记录
        """
        return self._cache.get(user_id, {}).get(month)
