# 运费计算工具

基于 Streamlit 的运费计算工具，支持多种计费规则格式的运费自动计算。

## 功能特性

- 📦 支持多种计费规则格式
- 📊 自动识别 Excel 文件中的重量和地区字段
- 🔄 支持地区名称模糊匹配和异体字处理
- 📤 一键导出计算结果到 Excel 文件
- 🎨 简洁美观的 Web 界面

## 技术栈

- Python 3.8+
- Streamlit 1.40+
- Pandas 2.0+
- OpenPyXL

## 项目结构

```
Freight calculation tool/
├── app.py                     # 主应用入口
├── requirements.txt           # 依赖配置
├── README.md                  # 项目说明文档
├── utils/                     # 工具模块
│   ├── __init__.py            # 模块导出
│   ├── calculator.py          # 运费计算核心逻辑
│   ├── config.py              # 应用配置
│   ├── excel_utils.py         # Excel 文件读写
│   └── usage_counter.py       # 打开次数计数器
└── TestFile/                  # 测试数据目录
```

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动应用

```bash
python -m streamlit run app.py
```

### 访问地址

- 本地地址：http://localhost:8501

## 使用说明

1. **上传计费规则文件**：选择包含计费规则的 Excel 文件
2. **选择计费规则表格**：从文件中选择要使用的工作表
3. **上传运费计算文件**：选择包含重量和地区信息的 Excel 文件
4. **查看计算结果**：系统自动计算运费并展示结果
5. **导出结果**：点击"导出结果"按钮下载计算结果

## 计费规则格式

支持以下几种常见的计费规则格式：

- **格式**：0-1KG、1.01-3KG、3KG以上首重1KG/2KG/3KG、3KG以上续重1KG
- **格式**：0-1KG、1.01-2KG、2.01-3KG、3KG以上首重1KG、3KG以上续重1KG
- **格式**：0-3KG、3KG以上首重2KG、3KG以上续重1KG

## 开发

### 代码规范

- 遵循 PEP8 规范（4 空格缩进、双引号字符串）
- 注释与文档字符串使用中文
- 变量、函数、类命名采用英文 snake_case 风格

### 日志规范

- 统一使用 `logging` 模块
- 日志分级：INFO（关键流程）、WARNING（潜在问题）、ERROR（异常）

## 许可证

MIT License