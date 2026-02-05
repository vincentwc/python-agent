import os
import sys

# 将项目根目录添加到 sys.path，解决模块导入问题
# 这样即使在 scripts 目录下直接运行脚本，也能找到 utils 模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv

from dotenv import load_dotenv
from pymongo import MongoClient

from utils.config_handler import agent_config
from utils.path_tool import get_abs_path

# 确保能加载环境变量
load_dotenv()


def migrate_csv_to_mongo():
    """
    将 CSV 中的数据迁移到 MongoDB
    """
    csv_path = get_abs_path(agent_config["external_data_path"])
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
    db_name = agent_config.get("mongo", {}).get(
        "db_name", "smart_cleaner"
    )  # 从配置文件获取数据库名
    collection_name = agent_config.get("mongo", {}).get(
        "collection_name", "usage_records"
    )

    print(f"🚀 开始迁移数据...")
    print(f"源文件: {csv_path}")
    print(f"目标 MongoDB: {mongo_uri} -> {db_name}.{collection_name}")

    if not os.path.exists(csv_path):
        print(f"❌ CSV 文件不存在: {csv_path}")
        return

    try:
        # 连接 MongoDB
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        db = client[db_name]
        collection = db[collection_name]

        # 清空旧数据 (可选，防止重复)
        delete_result = collection.delete_many({})
        print(f"🧹 已清理旧数据: {delete_result.deleted_count} 条")

        records = []
        with open(csv_path, "r", encoding="utf-8") as f:
            # CSV 文件包含表头，DictReader 会自动读取第一行作为 key
            # 表头为: "用户ID","特征","清洁效率","耗材","对比","时间"
            reader = csv.DictReader(f)
            for row in reader:
                # 第一行为csv的标题，跳过
                if row["用户ID"] == "用户ID":
                    continue
                # 构造符合 MongoDB 规范的文档
                # 使用中文 Key 从 CSV 读取，映射到 MongoDB 的英文 Key
                doc = {
                    "user_id": row.get("用户ID"),
                    "time": row.get("时间"),
                    "feature": row.get("特征"),
                    "efficiency": row.get("清洁效率"),
                    "consumables": row.get("耗材"),
                    "comparison": row.get("对比"),
                }

                # 简单的数据清洗：去除可能存在的首尾空白
                for k, v in doc.items():
                    if isinstance(v, str):  
                        doc[k] = v.strip()

                # 确保关键字段存在才添加
                if doc["user_id"]:  
                    records.append(doc)

        if records:
            result = collection.insert_many(records)
            print(f"✅ 成功迁移 {len(result.inserted_ids)} 条记录！")
        else:
            print("⚠️ CSV 文件为空，未迁移任何数据。")

    except Exception as e:
        if "requires authentication" in str(e):
            print(
                f"❌ 迁移失败: MongoDB 需要身份验证。请在 .env 文件中配置正确的 MONGO_URI (格式: mongodb://user:pass@host:port/)"
            )
        else:
            print(f"❌ 迁移失败: {str(e)}")


if __name__ == "__main__":
    migrate_csv_to_mongo()
