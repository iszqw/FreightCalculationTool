"""
运费计算工具主应用

本文件负责页面布局和用户交互
"""

import streamlit as st
import pandas as pd
import time
import hashlib
from utils.calculator import calculate_freight
from utils.excel_utils import read_excel_file, export_excel_file
from utils.config import PAGE_CONFIG
# from utils.usage_counter import increment_open_count, get_active_popup

# 设置页面配置
st.set_page_config(**PAGE_CONFIG)

# 初始化会话状态
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = True

# 增加打开次数并检查是否显示弹框（暂时禁用）
# config = increment_open_count()
# active_popup = get_active_popup()
# if active_popup:
#     st.warning(f"**{active_popup['title']}**\n\n{active_popup['message']}")

# 自定义CSS样式
st.markdown("""
<style>
    /* 全局布局 */
    .stApp {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }
    
    /* 主要内容区域 */
    .main {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        max-width: 800px;
        margin: 0 auto;
        flex: 1;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1.5rem;
        font-family: 'Arial', sans-serif;
    }
    .info-box {
        background-color: #e8f4f8;
        border-left: 4px solid #3498db;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 4px;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 4px;
    }
    /* 页脚样式 */
    .footer {
        text-align: center;
        padding: 1rem;
        background-color: #f8f9fa;
        border-top: 1px solid #e9ecef;
        width: 100%;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 100;
    }
    
    /* 为页脚留出空间 */
    .main-content {
        padding-bottom: 80px;
    }
    /* 隐藏右上角菜单 */
    .stActionButton {
        display: none !important;
    }
    /* 隐藏 Deploy 按钮 */
    .stDeployButton {
        display: none !important;
    }
    
    /* 按钮样式 */
    .stButton > button[kind="primary"] {
        background-color: #4CAF50 !important;
        color: white !important;
    }
    
    .stButton > button[kind="secondary"] {
        background-color: #F44336 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 主要内容区域
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# 页面标题
st.title("运费计算工具")

# 初始化会话状态
if "pricing_rules" not in st.session_state:
    st.session_state["pricing_rules"] = None
if "pricing_file_uploaded" not in st.session_state:
    st.session_state["pricing_file_uploaded"] = False
if "freight_file_uploaded" not in st.session_state:
    st.session_state["freight_file_uploaded"] = False
if "selected_sheet" not in st.session_state:
    st.session_state["selected_sheet"] = None
if "sheet_names" not in st.session_state:
    st.session_state["sheet_names"] = None
if "pricing_file" not in st.session_state:
    st.session_state["pricing_file"] = None
if "result_df" not in st.session_state:
    st.session_state["result_df"] = None

# 上传计费规则文件
st.header("计费规则")

# 上传计费规则文件（仅当未上传时显示）
if not st.session_state["pricing_file_uploaded"]:
    pricing_file = st.file_uploader("上传计费规则 Excel 文件", type=["xlsx", "xls"])

    # 读取计费规则
    if pricing_file is not None:
        try:
            # 显示上传中状态
            with st.spinner("正在上传并解析文件..."):
                time.sleep(0.5)  # 模拟处理时间
                # 读取Excel文件的所有sheet
                xls = pd.ExcelFile(pricing_file)
                sheet_names = xls.sheet_names
                
                if not sheet_names:
                    st.error("未读取到工作表，请检查文件格式")
                else:
                    # 保存sheet名称和文件对象到会话状态
                    st.session_state["sheet_names"] = sheet_names
                    st.session_state["pricing_file"] = pricing_file
                    st.session_state["pricing_file_uploaded"] = True
                    st.session_state["selected_sheet"] = None  # 初始状态为空
                    st.success("计费规则文件上传成功！")
                    # 强制重新渲染页面，确保选择框显示
                    st.rerun()
            
        except Exception as e:
            st.error(f"加载计费规则文件失败：{e}")
else:
    # 独立的计费规则选择组件
    st.subheader("选择计费规则表格")
    # 确保sheet_names存在且不为空
    if "sheet_names" in st.session_state and st.session_state["sheet_names"]:
        # 让用户选择sheet，初始状态为空
        selected_sheet = st.selectbox(
            "请选择要使用的计费规则表格", 
            [""] + st.session_state["sheet_names"], 
            index=0
        )
        
        # 当用户选择了有效的表格时，加载计费规则
        if selected_sheet and selected_sheet != st.session_state.get("selected_sheet"):
            try:
                # 显示加载状态
                with st.spinner("正在加载计费规则..."):
                    time.sleep(0.5)  # 模拟处理时间
                    # 重新读取选择的sheet
                    xls = pd.ExcelFile(st.session_state["pricing_file"])
                    df_pricing = pd.read_excel(xls, sheet_name=selected_sheet)
                    
                    # 提取计费规则
                    pricing_rules = {}
                    for _, row in df_pricing.iterrows():
                        region = str(row.iloc[0]).strip()
                        if pd.isna(region) or region == '':
                            continue
                        # 为每个地区创建一个包含所有重量段价格的字典
                        region_rules = {}
                        for col in df_pricing.columns[1:]:
                            if not pd.isna(row[col]):
                                region_rules[col] = row[col]
                        if region_rules:
                            pricing_rules[region] = region_rules
                    
                    if not pricing_rules:
                        st.error("未读取到有效计费规则，请检查表格格式")
                    else:
                        # 保存sheet名称和对应的计费规则
                        st.session_state["pricing_rules"] = pricing_rules
                        st.session_state["selected_sheet"] = selected_sheet
                        st.success(f"计费规则加载成功！(表格：{selected_sheet})")
                        st.write(f"共 {len(pricing_rules)} 个地区的计费规则")
                
            except Exception as e:
                st.error(f"加载计费规则失败：{e}")
    else:
        # 如果sheet_names不存在，尝试重新读取
        if "pricing_file" in st.session_state and st.session_state["pricing_file"]:
            try:
                xls = pd.ExcelFile(st.session_state["pricing_file"])
                st.session_state["sheet_names"] = xls.sheet_names
                st.rerun()
            except Exception as e:
                st.error(f"读取工作表失败：{e}")
        else:
            st.info("请先上传计费规则文件")

# 删除计费规则文件按钮（放在上传文件下方）
if st.session_state["pricing_file_uploaded"]:
    if st.button("删除计费规则文件", type="secondary"):
        st.session_state["pricing_rules"] = None
        st.session_state["pricing_file_uploaded"] = False
        st.session_state["selected_sheet"] = None
        st.session_state["sheet_names"] = None
        st.session_state["pricing_file"] = None
        st.success("计费规则文件已删除")
        st.rerun()

# 上传需要计算运费的文件（仅当选择了计费规则后显示）
if st.session_state["pricing_file_uploaded"] and st.session_state.get("selected_sheet") and st.session_state.get("pricing_rules"):
    st.header("计算运费")
    
    # 上传运费计算文件（仅当未上传时显示）
    if not st.session_state["freight_file_uploaded"]:
        freight_file = st.file_uploader("上传需要计算运费的 Excel 文件", type=["xlsx", "xls"])

        # 计算运费
        if freight_file is not None:
            try:
                # 显示 Loading 状态
                with st.spinner("正在处理文件..."):
                    time.sleep(0.5)  # 模拟处理时间
                    df_freight = read_excel_file(freight_file)
                    
                    if st.session_state["pricing_rules"] is not None:
                        # 识别计费重量字段
                        weight_col = None
                        for col in df_freight.columns:
                            if "计费重量" in str(col):
                                weight_col = col
                                break
                        if not weight_col:
                            # 尝试其他可能的字段
                            weight_col_candidates = [col for col in df_freight.columns if any(keyword in str(col).lower() for keyword in ['重量', 'weight', 'kg', 'kgs'])]
                            weight_col = weight_col_candidates[0] if weight_col_candidates else df_freight.columns[0]
                        
                        # 识别结算目的地省份字段
                        region_col = None
                        for col in df_freight.columns:
                            if "结算目的地省份（中转费）" in str(col):
                                region_col = col
                                break
                        if not region_col:
                            # 尝试其他可能的字段
                            region_col_candidates = [col for col in df_freight.columns if any(keyword in str(col).lower() for keyword in ['省份', '地区', '目的地', '省份（中转费）', '结算目的地', 'province', 'region', 'destination'])]
                            region_col = region_col_candidates[0] if region_col_candidates else df_freight.columns[1] if len(df_freight.columns) > 1 else df_freight.columns[0]
                        
                        # 计算运费
                        result_df = calculate_freight(df_freight, weight_col, region_col, st.session_state["pricing_rules"])
                        
                        # 保存结果到会话状态
                        st.session_state["result_df"] = result_df
                        st.session_state["freight_file_uploaded"] = True
                        st.success("计算完成")
                        # 强制重新渲染页面，确保导出和删除按钮显示
                        st.rerun()
                    else:
                        st.error("请先上传计费规则文件")
            except Exception as e:
                st.error(f"计算失败：{e}")
    else:
        # 导出结果
        if "result_df" in st.session_state:
            output = export_excel_file(st.session_state["result_df"])
            st.download_button(
                label="导出结果",
                data=output,
                file_name="运费计算结果.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary"
            )
        
        # 删除计算文件按钮（放在导出按钮下方）
        if st.button("删除计算文件", type="secondary"):
            st.session_state["freight_file_uploaded"] = False
            st.session_state["result_df"] = None
            st.success("计算文件已删除")
            st.rerun()
else:
    if st.session_state["pricing_file_uploaded"]:
        if not st.session_state.get("selected_sheet"):
            st.info("请选择计费规则表格")
        else:
            st.info("请等待计费规则加载完成")
    else:
        st.info("请先上传计费规则文件")

# 关闭主要内容区域
st.markdown('</div>', unsafe_allow_html=True)

# 页脚
st.markdown("""
<div class="footer">
    <p>© 2026 运费计算工具</p>
</div>
""", unsafe_allow_html=True)
