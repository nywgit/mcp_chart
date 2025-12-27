#!/usr/bin/env python3

from typing import List
from fastmcp import FastMCP
import argparse
from chart_src.mcp_server import generate_charts_server
from chart_src.mcp_server.generate_charts_server import DataPoint

# ----------------------------
# FastMCP 应用
# ----------------------------
app = FastMCP(
    name="图表生成MCP",
    instructions="生成折线图、柱状图和饼状图，返回图表图片的URL或者base64。",
    version="1.0.0"
)

@app.tool(
    name="generate_charts",
    description="生成折线图、柱状图和饼状图图表并返回图片链接或base64。"
)
def generate_charts(chart_type: str,
                    title: str,
                    x_label: str,
                    y_label: str,
                    y_label_list: List[str],
                    data_list: List[DataPoint]) -> dict:
    """
    :param chart_type:图表类型 折线图：line_chart 柱状图：bar_chart 饼状图：pie_chart
    :param title:标题
    :param x_label:X轴标签
    :param y_label:Y轴标签
    :param y_label_list:曲线/柱子的标签集合
    :param data_list:图表数据
    :return:
    """
    print("MCP 输入:", chart_type, title, x_label, y_label, y_label_list, data_list)

    return generate_charts_server.generate_charts( chart_type, title, x_label, y_label, y_label_list, data_list)


# ----------------------------
# 启动
# ----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    app.run(transport="streamable-http", host=args.host, port=args.port, path="/mcp")
