import os
import random

from langchain_core.tools import tool

from data.dao.csv_impl import CSVUsageRecordDAO
from data.dao.mongo_impl import MongoUsageRecordDAO
from rag.rag_service import RagSummarizeService
from utils.config_handler import agent_config
from utils.logger_handler import logger

arg = RagSummarizeService()

# ---------------- 数据源切换 ----------------
# 商业化改造：使用 MongoDB 替换 CSV
# 如果您想切回 CSV，只需注释掉 Mongo 行，解开 CSV 行即可
# usage_dao = CSVUsageRecordDAO(agent_config["external_data_path"])
usage_dao = MongoUsageRecordDAO()
# -------------------------------------------

user_ids = [
    "1001",
    "1002",
    "1003",
    "1004",
    "1005",
    "1006",
    "1007",
    "1008",
    "1009",
    "1010",
]

month_arr = [
    "2025-01",
    "2025-02",
    "2025-03",
    "2025-04",
    "2025-05",
    "2025-06",
    "2025-07",
    "2025-08",
    "2025-09",
    "2025-10",
    "2025-11",
    "2025-12",
]


@tool("rag_summarize", description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    """
    从向量存储中检索参考资料
    """
    return arg.rag_summarize(query)


@tool("get_weather", description="获取城市天气,以纯字符串的形式返回")
def get_weather(city: str) -> str:
    """
    获取城市天气
    """
    return f"{city}的天气为晴朗,温度为25摄氏度,湿度为50%,风速为3米/秒,气压为1013hPa,能见度为10公里"


@tool("get_user_location", description="获取用户位置,以纯字符串的形式返回")
def get_user_location() -> str:
    """
    获取用户位置
    """
    return random.choice(["北京", "上海", "广州", "深圳"])


@tool("get_user_id", description="获取用户ID,以纯字符串的形式返回")
def get_user_id() -> str:
    """
    获取用户ID
    """
    return random.choice(user_ids)


@tool("get_current_month", description="获取当前月份,以纯字符串的形式返回")
def get_current_month() -> str:
    """
    获取当前月份,以字符串的形式返回
    """
    return random.choice(month_arr)


@tool(
    "fetch_external_data",
    description="从外部系统中获取用户在指定月份的使用记录，以纯字符串的形式返回，如果未检测到返回空字符串",
)
def fetch_external_data(user_id: str, month: str) -> str:
    """
    从外部系统中获取用户在指定月份的使用记录，以纯字符串的形式返回
    """
    record = usage_dao.get_record(user_id, month)
    if record:
        return str(record)

    logger.warning(f"[fetch_external_data]未能获取用户{user_id}在{month}的使用记录数据")
    return ""


@tool(
    "fill_context_for_report",
    description="无入参，无返回值，调用后出发中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息",
)
def fill_context_for_report():
    return "fill_context_for_report已调用"


# if __name__ == "__main__":
# print(fetch_external_data("1005", "2025-06"))
