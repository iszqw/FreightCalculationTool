"""
工具函数模块

本模块提供Excel文件的读取和导出功能
"""

import pandas as pd
import io

try:
    import openpyxl
except ImportError:
    raise ImportError("缺少必要的依赖库 openpyxl，请运行 `pip install openpyxl` 后重试。")

def read_excel_file(uploaded_file):
    """
    读取上传的Excel文件
    
    参数:
        uploaded_file: UploadedFile - Streamlit上传的文件对象
    
    返回:
        pandas.DataFrame - 读取的数据
    
    异常:
        Exception - 当文件读取失败时
    """
    try:
        df = pd.read_excel(uploaded_file)
        return df
    except Exception as e:
        raise Exception(f"读取Excel文件失败: {str(e)}")

def export_excel_file(df):
    """
    导出数据到Excel文件
    
    参数:
        df: pandas.DataFrame - 要导出的数据
    
    返回:
        bytes - Excel文件的二进制数据
    
    异常:
        Exception - 当文件导出失败时
    """
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="计算结果")
        processed_data = output.getvalue()
        return processed_data
    except Exception as e:
        raise Exception(f"导出Excel文件失败: {str(e)}")
