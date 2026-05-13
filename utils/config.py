"""
配置模块

本模块存储应用的配置设置
"""

# 页面配置
PAGE_CONFIG = {
    "page_title": "运费计算器",
    "layout": "centered",
    "page_icon": "📦"
}

# 应用配置
APP_CONFIG = {
    "app_name": "运费计算工具",
    "version": "1.0.0",
    "author": "System",
    "description": "用于计算运费的工具应用"
}

# 计算默认值
CALCULATION_DEFAULTS = {
    "unit_price": 5.0,  # 默认单价
    "fixed_fee": 0.0     # 默认固定费用
}
