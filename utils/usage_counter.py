"""
打开次数计数器模块

本模块用于记录应用打开次数,当达到指定次数时显示弹框提示
"""

import os
import random
from datetime import datetime

# 内存中的配置
config = {
    "open_count": 0,
    "popups": [
        {
            "type": "fixed_count",
            "target_count": 1,
            "title": "初次见面",
            "message": "🎈 欢迎第一次打开！这个页面有点害羞,但很高兴认识你～",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 2,
            "title": "再次光临",
            "message": "👋 第 2 次了！看来我们之间有点小默契了。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 3,
            "title": "三顾茅庐",
            "message": "🍀 3 次访问！幸运数字,今天一定有好运相伴。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 4,
            "title": "四方来财",
            "message": "📈 4 次了！每次打开都是在给自己加 buff 呢。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 6,
            "title": "六六大顺",
            "message": "🧧 6 次访问！顺顺顺,今天的工作也会顺滑如丝。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 7,
            "title": "幸运七",
            "message": "🎰 7 次！老虎机都该中奖了 —— 奖励你一个虚拟的「今日免加班」券。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 8,
            "title": "发发发",
            "message": "💰 8 次！发发发,老板看了都想给你加鸡腿。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 9,
            "title": "长长久久",
            "message": "🎂 9 次,像生日蜡烛一样圆满。许个愿吧：希望代码永远没 bug。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 11,
            "title": "光棍节特供",
            "message": "🦯 11 次 —— 两根棍子！敲敲桌子,提醒自己该站起来活动啦。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 13,
            "title": "面包师的一打",
            "message": "🍞 13 次！面包师的一打,多给你一份精神食粮。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 14,
            "title": "一心一意",
            "message": "💖 14 次,谐音「一世」—— 这个页面愿陪你度过漫长工作日。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 15,
            "title": "月圆之夜",
            "message": "🌕 15 次,每月十五月儿圆。奖励你一个虚拟月饼 🥮（五仁的,不喜勿拍）。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 16,
            "title": "六六大顺 plus",
            "message": "🎵 16 = 4x4,四平八稳！今天的工作节奏稳如老狗。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 17,
            "title": "一起走",
            "message": "🤝 17 次,谐音「一起」—— 页面和你一起并肩作战。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 18,
            "title": "十八般武艺",
            "message": "⚔️ 18 次！你已经练就十八般武艺,什么问题都难不倒你。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 19,
            "title": "依旧长久",
            "message": "🔟9 次,离 20 只差一步！坚持就是胜利,先给你一朵小红花 🌺。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 21,
            "title": "二十一世纪",
            "message": "📡 21 次！进入 21 世纪新纪元 —— 奖励你一个虚拟 WiFi 信号满格 📶。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 23,
            "title": "乔丹时刻",
            "message": "🏀 23 次！像乔丹一样传奇 —— 今天你就是工位上的 MVP。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 24,
            "title": "一天二十四小时",
            "message": "⏰ 24 次！刚好凑满一天的小时数,奖励你一次准时下班的机会（意念版）。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 25,
            "title": "银牌 quarter",
            "message": "🎓 25 次！四分之一个一百,银牌成就达成。继续冲金！",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 30,
            "title": "三十而立",
            "message": "🎂 30 次！而立之年,页面已经成熟到能帮你自动点咖啡了（假的）。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 33,
            "title": "三三不尽",
            "message": "♾️ 33 次！三三不尽,好运绵绵。奖励一个精神上的泡泡糖 🫧。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 40,
            "title": "不惑之年",
            "message": "🧘 40 次！不惑了 —— 你已经对摸鱼和加班的平衡了然于心。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 42,
            "title": "生命宇宙答案",
            "message": "🌌 42 次！《银河系漫游指南》说这是终极答案 —— 你的终极答案是：再摸五分钟。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 50,
            "title": "半百勇士",
            "message": "⚡ 50 次！半百成就 —— 授予你「闪电侠」称号,手速+50%。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 60,
            "title": "一甲子",
            "message": "📆 60 次！一甲子的轮回,页面和你已经算是老熟人啦。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 66,
            "title": "六六大顺·改",
            "message": "🎲 66 次！双倍六六大顺,今天你可以在心里哼着歌工作。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 70,
            "title": "古稀之年",
            "message": "🎻 70 次！页面已经「古稀」,但对你依然充满热情。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 75,
            "title": "钻石进度的 3/4",
            "message": "💎 75 次！四分之三的钻石之路,离一百就差一小段啦。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 77,
            "title": "双喜临门",
            "message": "🎉🎉 77 次！两个 lucky 7 叠在一起,今天中奖绝缘体都能中个「再来一杯」。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 80,
            "title": "八十不坏",
            "message": "🛡️ 80 次！页面依旧坚挺,就像你面对周一早会的心态。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 90,
            "title": "九十冲刺",
            "message": "🏃 90 次！离一百就差最后 10 步,冲刺阶段给你加个虚拟氮气加速。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 99,
            "title": "差一点圆满",
            "message": "🧩 99 次！就差 1 次就能召唤百次成就,今晚加个班？（开玩笑的）",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 101,
            "title": "百尺竿头",
            "message": "🚀 101 次！百次之后更进一步,你已经超越了普通的用户。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 111,
            "title": "三根棍子",
            "message": "🚶🚶🚶 111 次！三根棍子排排走,像三个好朋友 —— 你、页面和咖啡。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 125,
            "title": "八分之一千",
            "message": "📊 125 次！八分之一的一千,数学上很工整,工作上很顺心。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 150,
            "title": "一百五十分",
            "message": "🏅🏅 150 次！金牌用户的平方,授予你「铂金手指」称号。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 175,
            "title": "青铜圣斗士",
            "message": "🛡️ 175 次！你已经燃烧了小宇宙,距离雅典娜（下班）更近一步。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 199,
            "title": "差一丢丢",
            "message": "⏳ 199 次！再打开一次就是 200 勇士,现在的你就像等待发令枪的运动员。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 250,
            "title": "二百五·特别版",
            "message": "🤪 250 次！这数字有点调皮,但你是认真的「二百五勇士」—— 奖励你一个虚拟的搞笑眼镜👓。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 300,
            "title": "斯巴达三百",
            "message": "🛡️⚔️ 300 次！这就是斯巴达！今天你的工作效率像列奥尼达一样勇猛。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 365,
            "title": "一年之约",
            "message": "📅 365 次！刚好一年（按每天一次算）,页面给你发了个虚拟年假。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 400,
            "title": "四百年",
            "message": "🏰 400 次！像一座古老的城堡,你和页面的友谊已经坚不可摧。",
            "enabled": True,
            "shown": False
        },
        {
            "type": "fixed_count",
            "target_count": 500,
            "title": "半千荣耀",
            "message": "🏆🏆🏆 500 次！半千荣耀,授予你「终身首席操作员」称号,附带虚拟红毯走秀一次。",
            "enabled": True,
            "shown": False
        }
    ],
    "date_popups": [
        {
            "type": "date",
            "target_date": "2026-04-03",
            "title": "活动通知",
            "message": "今天是我的生日补药再工作啦！！！",
            "enabled": True,
            "last_shown_date": None
        }
    ],
    "random_popups": [
        {
            "type": "random",
            "probability": 0.1,  # 10%的概率
            "title": "随机提示",
            "message": "这是一个随机弹出的提示！",
            "enabled": True
        }
    ],
    "weekly_popups": [
        {
            "type": "weekly",
            "weekday": 3,  # 0-6,3表示周四
            "probability": 0.02,  # 50%的概率
            "title": "周四提示",
            "message": "有没有要找工作的 会开车天天载我跟我爸妈上山下乡玩就行,前六个月试用期8000 转正26000 一年后给你发一台车一套房 有意者私聊 并先交50块押金 我吃完肯德基 给你办入职",
            "enabled": True,
            "last_shown_weekday": None
        }
    ],
    "enabled": True,  # 是否启用此功能
    "last_open_time": None
}


def increment_open_count():
    """
    增加打开次数
    
    返回:
        dict - 更新后的配置字典
    """
    global config
    config["open_count"] += 1
    config["last_open_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return config


def get_today_date():
    """
    获取今天的日期，格式为 YYYY-MM-DD
    
    返回:
        str - 今天的日期
    """
    return datetime.now().strftime("%Y-%m-%d")


def get_today_weekday():
    """
    获取今天是周几，0-6，0表示周一，6表示周日
    
    返回:
        int - 今天是周几
    """
    return datetime.now().weekday()


def get_active_popup():
    """
    获取当前应该显示的弹框（按优先级）
    
    优先级：固定次数 > 指定日期 > 纯随机 > 周四弹框
    
    返回:
        dict or None - 应该显示的弹框，如果没有则返回None
    """
    global config
    
    # 如果功能被禁用，不显示弹框
    if not config.get("enabled", True):
        return None
    
    current_count = config.get("open_count", 0)
    today_date = get_today_date()
    today_weekday = get_today_weekday()
    
    # 1. 检查固定次数弹框（优先级最高）
    for popup in config.get("popups", []):
        if (popup.get("enabled", True) and 
            not popup.get("shown", False) and 
            current_count >= popup.get("target_count", 0)):
            # 标记为已显示
            popup["shown"] = True
            return popup
    
    # 2. 检查指定日期弹框
    for popup in config.get("date_popups", []):
        if (popup.get("enabled", True) and 
            popup.get("target_date") == today_date and 
            popup.get("last_shown_date") != today_date):  # 确保今天只显示一次
            # 标记为今天已显示
            popup["last_shown_date"] = today_date
            return popup
    
    # 3. 检查纯随机弹框
    for popup in config.get("random_popups", []):
        if popup.get("enabled", True):
            probability = popup.get("probability", 0.1)
            if random.random() < probability:
                return popup
    
    # 4. 检查每周四弹框
    for popup in config.get("weekly_popups", []):
        if (popup.get("enabled", True) and 
            popup.get("weekday") == today_weekday and 
            popup.get("last_shown_weekday") != today_weekday):  # 确保今天只显示一次
            probability = popup.get("probability", 0.5)
            if random.random() < probability:
                # 标记为今天已显示
                popup["last_shown_weekday"] = today_weekday
                return popup
    
    return None


def reset_counter():
    """
    重置计数器和所有弹框的显示状态
    """
    global config
    config["open_count"] = 0
    
    # 重置所有弹框的显示状态
    for popup in config.get("popups", []):
        popup["shown"] = False
    for popup in config.get("date_popups", []):
        popup["last_shown_date"] = None
    for popup in config.get("weekly_popups", []):
        popup["last_shown_weekday"] = None


def add_fixed_count_popup(target_count, title, message, enabled=True):
    """
    添加固定次数弹框
    
    参数:
        target_count: int - 目标打开次数
        title: str - 弹框标题
        message: str - 弹框内容
        enabled: bool - 是否启用
    """
    global config
    new_popup = {
        "type": "fixed_count",
        "target_count": target_count,
        "title": title,
        "message": message,
        "enabled": enabled,
        "shown": False
    }
    config["popups"].append(new_popup)
    # 按目标次数排序
    config["popups"].sort(key=lambda x: x["target_count"])


def add_date_popup(target_date, title, message, enabled=True):
    """
    添加指定日期弹框
    
    参数:
        target_date: str - 目标日期，格式为 YYYY-MM-DD
        title: str - 弹框标题
        message: str - 弹框内容
        enabled: bool - 是否启用
    """
    global config
    new_popup = {
        "type": "date",
        "target_date": target_date,
        "title": title,
        "message": message,
        "enabled": enabled,
        "last_shown_date": None
    }
    config["date_popups"].append(new_popup)


def add_random_popup(probability, title, message, enabled=True):
    """
    添加纯随机弹框
    
    参数:
        probability: float - 弹出概率，0-1之间
        title: str - 弹框标题
        message: str - 弹框内容
        enabled: bool - 是否启用
    """
    global config
    new_popup = {
        "type": "random",
        "probability": probability,
        "title": title,
        "message": message,
        "enabled": enabled
    }
    config["random_popups"].append(new_popup)


def add_weekly_popup(weekday, probability, title, message, enabled=True):
    """
    添加每周固定日弹框
    
    参数:
        weekday: int - 周几，0-6，0表示周一，6表示周日
        probability: float - 弹出概率，0-1之间
        title: str - 弹框标题
        message: str - 弹框内容
        enabled: bool - 是否启用
    """
    global config
    new_popup = {
        "type": "weekly",
        "weekday": weekday,
        "probability": probability,
        "title": title,
        "message": message,
        "enabled": enabled,
        "last_shown_weekday": None
    }
    config["weekly_popups"].append(new_popup)


def update_popup_content(popup_type, index, **kwargs):
    """
    更新弹窗内容
    
    参数:
        popup_type: str - 弹窗类型：fixed_count, date, random, weekly
        index: int - 弹窗索引
        **kwargs: 要更新的属性
    """
    global config
    
    if popup_type == "fixed_count":
        popups = config.get("popups", [])
    elif popup_type == "date":
        popups = config.get("date_popups", [])
    elif popup_type == "random":
        popups = config.get("random_popups", [])
    elif popup_type == "weekly":
        popups = config.get("weekly_popups", [])
    else:
        return
    
    if 0 <= index < len(popups):
        for key, value in kwargs.items():
            popups[index][key] = value
        
        # 如果是固定次数弹框，重新排序
        if popup_type == "fixed_count":
            popups.sort(key=lambda x: x["target_count"])


def remove_popup(popup_type, index):
    """
    删除弹窗
    
    参数:
        popup_type: str - 弹窗类型：fixed_count, date, random, weekly
        index: int - 弹窗索引
    """
    global config
    
    if popup_type == "fixed_count":
        popups = config.get("popups", [])
    elif popup_type == "date":
        popups = config.get("date_popups", [])
    elif popup_type == "random":
        popups = config.get("random_popups", [])
    elif popup_type == "weekly":
        popups = config.get("weekly_popups", [])
    else:
        return
    
    if 0 <= index < len(popups):
        popups.pop(index)


def update_config(new_config):
    """
    更新整个配置
    
    参数:
        new_config: dict - 新的配置字典
    """
    global config
    config.update(new_config)


def get_config():
    """
    获取当前配置
    
    返回:
        dict - 当前配置字典
    """
    return config


# 使用示例
if __name__ == "__main__":
    # 测试功能
    config = increment_open_count()
    print(f"当前打开次数: {config['open_count']}")
    print(f"今天日期: {get_today_date()}")
    print(f"今天是周几: {get_today_weekday()}")
    
    active_popup = get_active_popup()
    if active_popup:
        print(f"应该显示的弹框:")
        print(f"类型: {active_popup['type']}")
        print(f"标题: {active_popup['title']}")
        print(f"内容: {active_popup['message']}")
    else:
        print("没有应该显示的弹框")
