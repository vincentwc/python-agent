from agent.tools.agent_tools import get_weather, get_user_location, get_current_month


def test_get_weather():
    result = get_weather("北京")
    assert isinstance(result, str)
    assert "北京" in result
    assert "天气" in result


def test_get_user_location():
    result = get_user_location()
    assert isinstance(result, str)
    assert result in ["北京", "上海", "广州", "深圳"]


def test_get_current_month():
    result = get_current_month()
    assert isinstance(result, str)
    assert result.startswith("2025-")
