"""
运费计算模块

本模块负责处理运费计算的核心逻辑，包括阶梯价格计算
"""

import pandas as pd


def calculate_freight(df, weight_col, region_col, pricing_rules=None):
    """
    计算运费
    
    参数:
        df: pandas.DataFrame - 包含重量和地区数据的DataFrame
        weight_col: str - 重量列的列名
        region_col: str - 地区列的列名
        pricing_rules: dict - 计费规则字典（可选，默认使用内置规则）
    
    返回:
        pandas.DataFrame - 包含运费计算结果的DataFrame
    
    异常:
        ValueError - 当重量列或地区列不存在或无效时
    """
    # 检查重量列是否存在
    if weight_col not in df.columns:
        raise ValueError(f"重量列 '{weight_col}' 不存在于数据中")
    
    # 检查地区列是否存在
    if region_col not in df.columns:
        raise ValueError(f"地区列 '{region_col}' 不存在于数据中")
    
    # 检查重量列是否有有效数据
    if df[weight_col].isnull().all():
        raise ValueError(f"重量列 '{weight_col}' 中没有有效数据")
    
    # 使用计费规则
    if pricing_rules is None:
        pricing_rules = {}
    
    def clean_region_name(region):
        """清理地区名称，移除后缀和民族名称"""
        region_clean = str(region).strip()
        
        # 统一处理异体字"內"为标准字"内"
        region_clean = region_clean.replace('內', '内')
        
        # 移除空格
        region_clean = region_clean.replace(' ', '')
        
        # 特殊处理：内蒙古相关
        if '内蒙古' in region_clean:
            return '内蒙'
        
        # 移除民族名称（如：回族、壮族、维吾尔族等）
        region_clean = region_clean.replace('回族', '').replace('壮族', '').replace('维吾尔族', '').replace('藏族', '').strip()
        
        # 移除后缀
        region_clean = region_clean.replace('省', '').replace('市', '').replace('自治区', '').replace('特别行政区', '').strip()
        
        return region_clean
    
    # 定义计算函数
    def calculate_single_freight(row):
        weight = row[weight_col]
        region = row[region_col]
        
        print(f"[DEBUG] 开始计算运费 - 重量: {weight}, 地区: {region}")
        
        # 检查重量是否为有效数值
        if pd.isna(weight):
            print(f"[DEBUG] 重量无效: {weight}")
            return 0
        
        # 检查重量是否为数值类型
        if not isinstance(weight, (int, float)):
            try:
                weight = float(weight)
                print(f"[DEBUG] 重量转换成功: {weight}")
            except:
                print(f"[ERROR] 重量转换失败: {weight}")
                return 0
        
        # 检查重量是否大于0
        if weight <= 0:
            print(f"[DEBUG] 重量无效: {weight}")
            return 0
        
        if pd.isna(region):
            print(f"[DEBUG] 地区无效: {region}")
            return 0
        
        # 检查地区是否在规则中
        matched_region = None
        if region not in pricing_rules:
            # 尝试模糊匹配
            region_clean = clean_region_name(region)
            print(f"[DEBUG] 地区不在规则中，尝试模糊匹配 - 原始: {region}, 清理后: {region_clean}")
            
            # 尝试精确匹配清理后的地区名
            if region_clean in pricing_rules:
                matched_region = region_clean
                print(f"[DEBUG] 精确匹配成功: {matched_region}")
            else:
                # 尝试子字符串匹配
                for rule_region in pricing_rules:
                    rule_clean = clean_region_name(rule_region)
                    if rule_clean in region_clean or region_clean in rule_clean:
                        matched_region = rule_region
                        print(f"[DEBUG] 子字符串匹配成功: {matched_region}")
                        break
            
            # 额外尝试：直接匹配清理后的地区名（处理异体字问题）
            if not matched_region:
                for rule_region in pricing_rules:
                    if clean_region_name(rule_region) == region_clean:
                        matched_region = rule_region
                        print(f"[DEBUG] 异体字匹配成功: {matched_region}")
                        break
            
            # 额外尝试：大小写不敏感匹配
            if not matched_region:
                region_clean_lower = region_clean.lower()
                for rule_region in pricing_rules:
                    if clean_region_name(rule_region).lower() == region_clean_lower:
                        matched_region = rule_region
                        print(f"[DEBUG] 大小写不敏感匹配成功: {matched_region}")
                        break
            
            if not matched_region:
                # 只打印报错日志，并打印所有可用的地区名
                print(f"[ERROR] 地区匹配失败: {region} (清理后: {region_clean})")
                print(f"[ERROR] 可用的地区名: {list(pricing_rules.keys())}")
                return 0
            region = matched_region
        
        # 向上取整到整数
        weight = int(weight) if weight == int(weight) else int(weight) + 1
        print(f"[DEBUG] 向上取整后的重量: {weight}")
        
        # 限制重量范围，防止异常值
        if weight > 1000:
            print(f"[ERROR] 重量超过1000: {weight}")
            return 0
        
        # 获取当前地区的价格规则
        region_rules = pricing_rules[region]
        print(f"[DEBUG] 地区规则: {region_rules}")
        
        # 检查计费规则格式，支持不同的重量段
        # 李海洋格式：0-1KG、1.01-3KG、3KG以上首重1KG/2KG/3KG、3KG以上续重1KG
        if '1.01-3KG' in region_rules:
            print(f"[DEBUG] 使用格式（李海洋）：0-1KG、1.01-3KG、3KG以上")
            if weight <= 1:
                result = region_rules.get('0-1KG', 0)
                print(f"[DEBUG] 重量{weight}kg，使用0-1KG价格: {result}")
                return result
            elif weight <= 3:
                result = region_rules.get('1.01-3KG', region_rules.get('0-1KG', 0))
                print(f"[DEBUG] 重量{weight}kg，使用1.01-3KG价格: {result}")
                return result
            else:
                # 支持多种首重格式：1KG、2KG、3KG
                first_weight_price = region_rules.get('3KG以上首重3KG', region_rules.get('3KG以上首重2KG', region_rules.get('3KG以上首重1KG', 0)))
                additional_weight_price = region_rules.get('3KG以上续重1KG', 0)
                # 根据首重类型确定计算方式
                if '3KG以上首重3KG' in region_rules:
                    result = first_weight_price + additional_weight_price * (weight - 3)
                    print(f"[DEBUG] 重量{weight}kg，使用首重3KG续重计算: 首重{first_weight_price} + 续重{additional_weight_price} × {weight-3} = {result}")
                elif '3KG以上首重2KG' in region_rules:
                    result = first_weight_price + additional_weight_price * (weight - 2)
                    print(f"[DEBUG] 重量{weight}kg，使用首重2KG续重计算: 首重{first_weight_price} + 续重{additional_weight_price} × {weight-2} = {result}")
                else:
                    result = first_weight_price + additional_weight_price * (weight - 1)
                    print(f"[DEBUG] 重量{weight}kg，使用首重1KG续重计算: 首重{first_weight_price} + 续重{additional_weight_price} × {weight-1} = {result}")
                return result
        # 久久金属格式：0-1KG、1.01-2KG、2.01-3KG、3KG以上首重1KG、3KG以上续重1KG
        elif '1.01-2KG' in region_rules:
            print(f"[DEBUG] 使用格式（久久金属）：0-1KG、1.01-2KG、2.01-3KG、3KG以上")
            if weight <= 1:
                result = region_rules.get('0-1KG', 0)
                print(f"[DEBUG] 重量{weight}kg，使用0-1KG价格: {result}")
                return result
            elif weight <= 2:
                result = region_rules.get('1.01-2KG', region_rules.get('0-1KG', 0))
                print(f"[DEBUG] 重量{weight}kg，使用1.01-2KG价格: {result}")
                return result
            elif weight <= 3:
                result = region_rules.get('2.01-3KG', region_rules.get('1.01-2KG', 0))
                print(f"[DEBUG] 重量{weight}kg，使用2.01-3KG价格: {result}")
                return result
            else:
                first_weight_price = region_rules.get('3KG以上首重1KG', 0)
                additional_weight_price = region_rules.get('3KG以上续重1KG', 0)
                result = first_weight_price + additional_weight_price * (weight - 1)
                print(f"[DEBUG] 重量{weight}kg，使用首重续重计算: 首重{first_weight_price} + 续重{additional_weight_price} × {weight-1} = {result}")
                return result
        # 郭亚军格式：0-3KG、3KG以上首重2KG、3KG以上续重1KG
        elif '0-3KG' in region_rules:
            print(f"[DEBUG] 使用格式（郭亚军）：0-3KG、3KG以上")
            if weight <= 3:
                result = region_rules.get('0-3KG', 0)
                print(f"[DEBUG] 重量{weight}kg，使用0-3KG价格: {result}")
                return result
            else:
                # 检查首重是1KG还是2KG
                first_weight_price = region_rules.get('3KG以上首重2KG', region_rules.get('3KG以上首重1KG', 0))
                additional_weight_price = region_rules.get('3KG以上续重1KG', 0)
                # 如果是首重2KG，计算方式为：首重价格 + 续重价格 × (重量 - 2)
                if '3KG以上首重2KG' in region_rules:
                    result = first_weight_price + additional_weight_price * (weight - 2)
                    print(f"[DEBUG] 重量{weight}kg，使用首重2KG续重计算: 首重{first_weight_price} + 续重{additional_weight_price} × {weight-2} = {result}")
                else:
                    result = first_weight_price + additional_weight_price * (weight - 1)
                    print(f"[DEBUG] 重量{weight}kg，使用首重1KG续重计算: 首重{first_weight_price} + 续重{additional_weight_price} × {weight-1} = {result}")
                return result
        # 其他格式
        else:
            # 尝试直接使用首重和续重规则
            print(f"[DEBUG] 尝试使用首重和续重规则")
            first_weight_price = region_rules.get('3KG以上首重2KG', region_rules.get('3KG以上首重1KG', region_rules.get('首重1KG', region_rules.get('首重', 0))))
            additional_weight_price = region_rules.get('3KG以上续重1KG', region_rules.get('续重1KG', region_rules.get('续重', 0)))
            print(f"[DEBUG] 首重价格: {first_weight_price}, 续重价格: {additional_weight_price}")
            
            if first_weight_price > 0:
                # 检查是否是首重2KG的情况
                if '3KG以上首重2KG' in region_rules:
                    if weight <= 2:
                        result = first_weight_price
                        print(f"[DEBUG] 重量{weight}kg，使用首重2KG价格: {result}")
                        return result
                    else:
                        result = first_weight_price + additional_weight_price * (weight - 2)
                        print(f"[DEBUG] 重量{weight}kg，使用首重2KG续重计算: 首重{first_weight_price} + 续重{additional_weight_price} × {weight-2} = {result}")
                        return result
                else:
                    if weight <= 1:
                        result = first_weight_price
                        print(f"[DEBUG] 重量{weight}kg，使用首重1KG价格: {result}")
                        return result
                    else:
                        result = first_weight_price + additional_weight_price * (weight - 1)
                        print(f"[DEBUG] 重量{weight}kg，使用首重1KG续重计算: 首重{first_weight_price} + 续重{additional_weight_price} × {weight-1} = {result}")
                        return result
            
            # 尝试使用其他可能的重量段
            if '0-1KG' in region_rules:
                if weight <= 1:
                    result = region_rules.get('0-1KG', 0)
                    print(f"[DEBUG] 重量{weight}kg，使用0-1KG价格: {result}")
                    return result
            
            print(f"[ERROR] 未找到匹配的重量段格式，地区: {region}")
            return 0
    
    # 应用计算函数到每一行
    df["运费"] = df.apply(calculate_single_freight, axis=1)
    
    return df
