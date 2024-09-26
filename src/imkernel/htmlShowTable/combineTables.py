from pandas import DataFrame
import ipywidgets as widgets


def generate_table(headers, data):
    """
    根据表头和数据生成带灰色背景的HTML表格字符串
    """
    # 给表头增加灰色背景色
    header_row = "".join([f"<th style='background-color: gray;'>{col}</th>" for col in headers])
    # 添加表格行
    data_rows = "".join([f"<tr>{''.join([f'<td>{cell}</td>' for cell in row])}</tr>" for row in data])
    return f"<tr>{header_row}</tr>{data_rows}"


def combine_tables(tables):
    """
    动态合并多个表格
    :param tables: 一个包含多个表格数据的列表，每个表格数据是一个包含表头和数据的字典
    :return: 生成的HTML字符串
    """
    html_parts = ['<table style="border-collapse: collapse; width: 100%;" border="1px solid black;">']
    for table in tables:
        html_parts.append(generate_table(table["headers"], table["data"]))
    html_parts.append("</table>")
    return "".join(html_parts)


def show_html_table(table_html: str):
    return widgets.HTML(value=table_html)


# 从 DataFrame 提取表头和数据
def df_to_table(df: DataFrame):
    headers = df.columns.tolist()  # 提取表头
    data = df.values.tolist()  # 提取数据
    return {"headers": headers, "data": data}
