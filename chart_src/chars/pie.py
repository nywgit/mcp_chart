import io
import base64


class PieChart:
    def __init__(self, plt, title, x_label, y_label, y_label_list):
        """
        :param plt: matplotlib.pyplot 对象
        :param title: 图表标题
        :param x_label: X轴标签
        :param y_label: Y轴标签
        :param y_label_list: 曲线/柱子的集合
        """
        self.plt = plt
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.y_label_list = y_label_list

    def get_chart_image(self, df, storage_tool):
        """
        生成饼状图并返回结果
        :param df: DataFrame，包含 x、y1、y2 列
        :param storage_tool: 存储工具对象，用于将图片保存到存储空间
        :return: 结果字典，包含饼状图 URL 或 Base64 字符串
        """
        sizes = [df[f'y{i}'].sum() for i, item_y_label in enumerate(self.y_label_list)]  # 根据列名获取对应的值
        y_columns = [item_y_label for item_y_label in self.y_label_list]  # 提取实际的列名
        self.plt.figure(figsize=(7, 7))
        self.plt.pie(sizes, labels=y_columns, autopct='%1.1f%%', startangle=90)
        self.plt.title(self.title)
        self.plt.axis('equal')

        buf = io.BytesIO()
        self.plt.savefig(buf, format='png')
        buf.seek(0)
        img_bytes = buf.read()
        buf.close()
        self.plt.close()

        results = {}
        if storage_tool is not None:
            # ✅ 将 bytes 转为 URL
            results["type"] = "url"
            results["bar_chart_url"] = storage_tool.upload_from_memory(img_bytes)
        else:
            # ✅ 将 bytes 转为 Base64 字符串
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            results["type"] = "base64"
            results["bar_chart_base64"] = f"![](data:image/png;base64,{img_base64})"
        return results
