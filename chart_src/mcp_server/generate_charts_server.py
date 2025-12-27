import json
from typing import List
from pydantic import BaseModel
from typing import Union
from chart_src.chars import chars_tool
from chart_src.storage import QiniuTool, oss_tool

def is_not_empty(value):
    return value is not None and isinstance(value, str) and value.strip() != ""


class DataPoint(BaseModel):
    x: Union[str, int, float]
    y_list: List[Union[str, int, float]]

def generate_charts(chart_type: str,
                    title: str,
                    x_label: str,
                    y_label: str,
                    y_label_list: List[str],
                    data_list: List[DataPoint]) -> dict:

    # 对每个入参都判空
    for k in ["chart_type", "title", "x_label", "y_label", "y_label_list", "data_list"]:
        if not k in locals() or locals()[k] is None:
            raise ValueError(f"缺少必要字段: {k}")

    # 校验 data_list
    if not isinstance(data_list, list) or len(data_list) == 0:
        raise ValueError("data 必须是非空列表")

    # 对data_list的每个值判空
    for i, item in enumerate(data_list):
        for k in ["x", "y_list"]:
            value = getattr(item, k, None)
            if value is None:
                raise ValueError(f"data[{i}][{k}] 不能为空")

    # 将 DataPoint 列表转为字典列表
    temp_data_list = []
    for item in data_list:
        obj = {"x": item.x}
        for i, label in enumerate(y_label_list):
            obj["y" + str(i)] = item.y_list[i]
        temp_data_list.append(obj)
    # 将 data_dict_list 列表转为字典列表
    data_dict_list = [dict(item) for item in temp_data_list]
    print("data_dict_list:", data_dict_list)

    chart_config = {
        "chart_type": chart_type,
        "title": title,
        "x_label": x_label,
        "y_label": y_label,
        "y_label_list": y_label_list,
        "data_dict_list": data_dict_list
    }

    # 获取对象存储工具
    storage_tool = oss_tool.get_oss_tool()
    print("storage_tool:", storage_tool)

    # 获取图表图片
    results = chars_tool.get_chart_image(chart_config, storage_tool)
    # === 返回结果 ===
    print("MCP 输出:", results)
    return {
        "content": [
            {
                "type": results["type"],
                "text": json.dumps(results, ensure_ascii=False, indent=2)
            }
        ]
    }

