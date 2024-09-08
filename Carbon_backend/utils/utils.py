import pandas as pd


def format_date(df: pd.DataFrame, date_column: str):
    """处理日期字段并转换为 "YY-MM-DD" 格式"""
    df[date_column] = pd.to_datetime(df[date_column]).dt.strftime('%Y-%m-%d')


def clean_numeric_column(df: pd.DataFrame, columns: list):
    """
    清理 DataFrame 中指定的列，处理空白字符串、空值、"-" 和 "--"，将其替换为 None。
    去掉百分号、逗号等非数值字符，并将其转换为浮点数或整数。
    """
    for column in columns:
        # 移除非数值字符（如逗号、百分号等），并将其转换为浮点数
        df[column] = df[column].replace(r'[^\d.-]', '', regex=True)

        # 将空白字符串、空格、"-"、"--" 直接替换为 pd.NA (适用于 Pandas 的缺失值)
        df[column] = df[column].replace(["", " ", "-", "--"], pd.NA)

        # 使用 pd.to_numeric 将非数值转换为 NaN（可以导入到数据库时存为 NULL）
        df[column] = pd.to_numeric(df[column], errors='coerce')

    return df
