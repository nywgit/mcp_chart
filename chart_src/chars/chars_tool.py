import pandas as pd
import matplotlib.pyplot as plt
from chart_src.chars import BarChart
from chart_src.chars import LineChart
from chart_src.chars import PieChart

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
    plt.rcParams['font.sans-serif'] = [
        # === Windows 原生简体中文字体 ===
        'SimHei',                # 黑体（无衬线）
        'Microsoft YaHei',       # 微软雅黑（无衬线）
        'DengXian',              # 等线（无衬线）
        'YouYuan',               # 幼圆（无衬线，圆体）
        'SimSun',                # 宋体（有衬线，但广泛兼容）
        'FangSong',              # 仿宋（有衬线）
        'KaiTi',                 # 楷体（手写风格）
        'LiSu',                  # 隶书（书法体）

        # === 华文字体系列（Windows/macOS 常见）===
        'STXihei',               # 华文细黑（无衬线）
        'STSong',                # 华文宋体
        'STFangsong',            # 华文仿宋
        'STKaiti',               # 华文楷体
        'STLiti',                # 华文隶书
        'STXingkai',             # 华文行楷
        'STXinwei',              # 华文新魏
        'STCaiyun',              # 华文彩云（装饰体）
        'STHupo',                # 华文琥珀（装饰体）
        'STZhongsong',           # 华文中宋

        # === 开源/跨平台高质量简体中文字体 ===
        'Noto Sans SC',          # 思源黑体（Google/Adobe，无衬线，开源）
        'Noto Serif SC',         # 思源宋体（衬线，开源）
        'Source Han Serif SC',   # 同 Noto Serif SC（Adobe 命名）
        'Source Han Sans SC',    # 同 Noto Sans SC（Adobe 命名）
        'WenQuanYi Micro Hei',   # 文泉驿微米黑（Linux 常用开源黑体）
        'WenQuanYi Zen Hei',     # 文泉驿正黑

        # === 兜底英文字体（防止完全回退失败）===
        'DejaVu Sans'
    ]
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
