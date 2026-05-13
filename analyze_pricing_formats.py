"""
分析所有计费规则的重量段格式
"""

import pandas as pd

# 读取所有sheet
xl = pd.ExcelFile('计费规则.xlsx')
sheets = xl.sheet_names

print(f"总共 {len(sheets)} 个计费规则sheet")
print("=" * 50)

# 存储不同的列名格式
column_formats = {}

for sheet in sheets:
    df = pd.read_excel('计费规则.xlsx', sheet_name=sheet)
    columns = df.columns.tolist()
    
    # 提取重量段相关的列名
    weight_columns = [col for col in columns if 'KG' in str(col) or '公斤' in str(col)]
    
    # 记录列名格式
    format_key = tuple(sorted(weight_columns))
    if format_key not in column_formats:
        column_formats[format_key] = []
    column_formats[format_key].append(sheet)
    
    print(f"\n=== {sheet} ===")
    print(f"列名: {columns}")
    print(f"重量段列: {weight_columns}")

print("\n" + "=" * 50)
print("发现的计费规则格式:")
print("=" * 50)

for i, (format_key, sheets_list) in enumerate(column_formats.items(), 1):
    print(f"\n格式 {i}:")
    print(f"重量段列: {format_key}")
    print(f"使用此格式的sheet: {', '.join(sheets_list)}")
    print(f"共 {len(sheets_list)} 个sheet")
