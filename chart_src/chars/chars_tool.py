import matplotlib.pyplot as plt
import pandas as pd

from chart_src.chars.bar import BarChart
from chart_src.chars.line import LineChart
from chart_src.chars.pie import PieChart


def get_chart_image(chart_config, storage_tool):
    """
    :param chart_config: chart相关数据
    :param storage_tool: 存储对象工具
    :return:
    """
    # 解析配置参数
    chart_type = chart_config.get("chart_type")
    title = chart_config.get("title")
    x_label = chart_config.get("x_label")
    y_label = chart_config.get("y_label")
    y_label_list = chart_config.get("y_label_list", [])
    data_dict_list = chart_config.get("data_dict_list", [])

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    # 创建DataFrame
    df = pd.DataFrame(data_dict_list)
    df = df.sort_values("x").reset_index(drop=True)

    # 根据图表类型生成图表
    if "line" in chart_type or "折线图" in chart_type:
        line_chart = LineChart(plt, title, x_label, y_label, y_label_list)
        return line_chart.get_chart_image(df, storage_tool)
    elif "bar" in chart_type or "柱状图" in chart_type:
        bar_chart = BarChart(plt, title, x_label, y_label, y_label_list)
        return bar_chart.get_chart_image(df, storage_tool)
    else:
        pie_chart = PieChart(plt, title, x_label, y_label, y_label_list)
        return pie_chart.get_chart_image(df, storage_tool)
