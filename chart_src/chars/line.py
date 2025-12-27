import io
import base64
import numpy as np

class LineChart:
    def __init__(self, plt, title, x_label, y_label, y_label_list):
        """
        :param plt: matplotlib.pyplot 对象
        :param title: 图表标题
        :param x_label: X轴标签
        :param y_label: Y轴标签
        :param y_label_list: 曲线/柱子的标签集合
        """
        self.plt = plt
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.y_label_list = y_label_list

    def get_chart_image(self, df, storage_tool):
        """
        生成折线图并返回结果
        :param df: DataFrame，包含 x、y1、y2 列
        :param storage_tool: 存储工具对象，用于将图片保存到存储空间
        :return: 结果字典，包含折线图 URL 或 Base64 字符串
        """
        self.plt.figure(figsize=(10, 6))
        # 根据y_label_list中的标签数量绘制多条线
        for i, item_y_label in enumerate(self.y_label_list):
            y_col_name = f'y{i}'  # 对应y1, y2, y3等列
            self.plt.plot(df['x'], df[y_col_name], marker='o', label=item_y_label)

        self.plt.title(self.title)
        self.plt.xlabel(self.x_label)
        self.plt.ylabel(self.y_label)
        self.plt.legend()
        self.plt.grid(True, linestyle='--', alpha=0.6)
        self.plt.xticks(df['x'])
        # ✅ 正确做法：只对数值列求最大值
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) == 0:
            raise ValueError("数据中没有数值列")
        y_max = df[numeric_columns].max().max()
        y_ticks = np.arange(0, y_max, y_max / 5)
        self.plt.yticks(y_ticks, [str(y) for y in y_ticks])
        self.plt.tight_layout()


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
            results["line_chart_url"] = storage_tool.upload_from_memory(img_bytes)
        else:
            # ✅ 将 bytes 转为 Base64 字符串
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            results["type"] = "base64"
            results["line_chart_base64"] = f"![](data:image/png;base64,{img_base64})"
        return results
