import os
from typing import Optional, Dict
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from data.dao.base import UsageRecordDAO
from utils.logger_handler import logger
from utils.config_handler import agent_config

class MongoUsageRecordDAO(UsageRecordDAO):
    """
    基于 MongoDB 的使用记录数据访问实现
    """

    def __init__(self):
        """
        初始化 MongoDB DAO
        """
        self.mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
        self.db_name = agent_config.get("mongo", {}).get("db_name", "smart_cleaner")
        self.collection_name = agent_config.get("mongo", {}).get("collection_name", "usage_records")
        
        try:
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=2000)
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            # 尝试连接，确保服务可用
            self.client.admin.command('ping')
            logger.info(f"[MongoUsageRecordDAO] 成功连接到 MongoDB: {self.db_name}.{self.collection_name}")
        except Exception as e:
            logger.error(f"[MongoUsageRecordDAO] 连接 MongoDB 失败: {str(e)}")
            # 在生产环境中，这里可能需要抛出异常或降级处理
            self.collection = None

    def get_record(self, user_id: str, month: str) -> Optional[Dict]:
        """
        根据用户ID和月份获取使用记录
        
        期望的 MongoDB 文档结构:
        {
            "user_id": "1001",
            "time": "2025-01",
            "feature": "清洁能力强",
            "efficiency": "高",
            "consumables": "低",
            "comparison": "优于竞品"
        }
        """
        if self.collection is None:
            logger.error("[MongoUsageRecordDAO] 数据库连接不可用，无法查询")
            return None

        try:
            query = {"user_id": user_id, "time": month}
            doc = self.collection.find_one(query)
            
            if doc:
                # 转换为业务需要的字典格式
                return {
                    "特征": doc.get("feature", ""),
                    "效率": doc.get("efficiency", ""),
                    "耗材": doc.get("consumables", ""),
                    "对比": doc.get("comparison", ""),
                }
            return None
        except PyMongoError as e:
            logger.error(f"[MongoUsageRecordDAO] 查询失败: {str(e)}")
            return None
