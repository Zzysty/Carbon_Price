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


def fill_null_with_average(records):
    """
    对返回的记录中的null值进行前后值平均处理
    """
    filled_records = []
    for i, record in enumerate(records):
        date, price = record
        if price is None:
            # 查找前一个和后一个非null的值
            prev_price = next((records[j][1] for j in range(i - 1, -1, -1) if records[j][1] is not None), None)
            next_price = next((records[j][1] for j in range(i + 1, len(records)) if records[j][1] is not None), None)

            # 如果前后都存在值，计算平均值
            if prev_price is not None and next_price is not None:
                price = (prev_price + next_price) / 2
            elif prev_price is not None:
                price = prev_price
            elif next_price is not None:
                price = next_price

        filled_records.append((date, price))

    return filled_records
