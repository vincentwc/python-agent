import os
import random
from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
from utils.config_handler import agent_config
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

arg = RagSummarizeService()

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

external_data = {}


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


def generate_external_data():
    """
    {
      "user_id": {
        "month": {"特征": "xxx","效率":"xxx"}
        "month": {"特征": "xxx","效率":"xxx"}
        "month": {"特征": "xxx","效率":"xxx"}
      },
      "user_id": {
        "month": {"特征": "xxx","效率":"xxx"}
        "month": {"特征": "xxx","效率":"xxx"}
        "month": {"特征": "xxx","效率":"xxx"}
      },
      "user_id": {
        "month": {"特征": "xxx","效率":"xxx"}
        "month": {"特征": "xxx","效率":"xxx"}
        "month": {"特征": "xxx","效率":"xxx"}
      }
    }
    """
    if not external_data:
        external_data_path = get_abs_path(agent_config["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件{external_data_path}不存在")

        with open(external_data_path, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:  # 跳过表头
                arr: list[str] = line.strip().split(",")
                user_id: str = arr[0].replace('"', "")
                feature: str = arr[1].replace('"', "")
                efficiency: str = arr[2].replace('"', "")
                consumables: str = arr[3].replace('"', "")
                comparison: str = arr[4].replace('"', "")
                time: str = arr[5].replace('"', "")
                if user_id not in external_data:
                    external_data[user_id] = {}
                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison,
                }


@tool(
    "fetch_external_data",
    description="从外部系统中获取用户在指定月份的使用记录，以纯字符串的形式返回，如果未检测到返回空字符串",
)
def fetch_external_data(user_id: str, month: str) -> str:
    """
    从外部系统中获取用户在指定月份的使用记录，以纯字符串的形式返回
    """
    generate_external_data()
    try:
        return external_data[user_id][month]
    except KeyError:
        logger.warning(
            f"[fetch_external_data]未能获取用户{user_id}在{month}的使用记录数据"
        )
        return ""


@tool("fill_context_for_report", description="无入参，无返回值，调用后出发中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
  return "fill_context_for_report已调用"

# if __name__ == "__main__":
    # print(fetch_external_data("1005", "2025-06"))
