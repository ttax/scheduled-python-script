import requests
import os  
DINGTALK_WEBHOOK = os.getenv("DINGTALK_WEBHOOK", "")
# 校验环境变量是否存在
if not DINGTALK_WEBHOOK:
    raise ValueError("环境变量 DINGTALK_WEBHOOK 未配置，请检查GitHub Secrets")

def read_fund_codes_from_file(file_path: str = None):
    """
    从文件中读取基金代码，优先使用环境变量指定的路径
    """
    # 优先读取环境变量中的文件路径，否则用默认值
    file_path = file_path or os.getenv("FUND_CODES_FILE", "fund_codes.txt")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            codes = [line.strip() for line in f if line.strip()]
            unique_codes = list(dict.fromkeys(codes))
            print(f"成功从文件读取 {len(unique_codes)} 个基金代码")
            return unique_codes
    except FileNotFoundError:
        print(f"错误：未找到文件 {file_path}，请确保文件存在")
        return []
    except Exception as e:
        print(f"读取文件失败: {e}")
        return []

def get_fund_net_worth(fund_code: str):
    url = f'https://m.dayfund.cn/ajs/ajaxdata.shtml?showtype=getfundvalue&fundcode={fund_code}'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.encoding = "gb2312"
        fund_info = res.text.split('|')
    except Exception as e:
        print(f"获取基金 {fund_code} 数据失败: {e}")
        return f"### 【{fund_code}】获取数据失败\n---\n"

    def format_value(value):
        try:
            if '-' in str(value):
                return f'<font color="#00FF00">{value}</font>'  # 绿色：下跌
            else:
                return f'<font color="#FF0000">{value}</font>'  # 红色：上涨
        except:
            return value

    fund_name = get_fund_name(fund_code)
    
    # 安全获取数据
    net_worth_time = fund_info[0] if len(fund_info) > 0 else "未知时间"
    intraday_time = f"{fund_info[9]} {fund_info[10]}" if len(fund_info) > 10 else "未知时间"
    latest_net = fund_info[1] if len(fund_info) > 1 else "暂无"
    change_amount = fund_info[3] if len(fund_info) > 3 else "暂无"
    change_percent = fund_info[4] if len(fund_info) > 4 else "暂无"
    estimate_net = fund_info[7] if len(fund_info) > 7 else "暂无"
    estimate_change = fund_info[6] if len(fund_info) > 6 else "暂无"
    estimate_percent = fund_info[5] if len(fund_info) > 5 else "暂无"

    data = f"""
### 【{fund_code}】{fund_name}
> **净值更新时间**：{net_worth_time}
> **最新净值**：{latest_net}
> **涨跌金额**：{format_value(change_amount)}
> **涨跌幅度**：{format_value(change_percent)}

> **盘中更新时间**：{intraday_time}
> **盘中预估净值**：{estimate_net}
> **盘中涨跌金额**：{format_value(estimate_change)}
> **盘中涨跌幅度**：{format_value(estimate_percent)}
---
"""
    return data

def get_fund_name(fund_code: str):
    url = f"https://www.dayfund.cn/fundpre/{fund_code}.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.encoding = "utf-8"
        return res.text.split('<title>')[1].split('</title>')[0].split("(")[0].strip()
    except:
        return "未知名称"

def send_to_dingtalk(content):
    headers = {"Content-Type": "application/json;charset=utf-8"}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "来财来财啦",
            "text": content
        }
    }
    try:
        response = requests.post(DINGTALK_WEBHOOK, json=data, headers=headers, timeout=15)
        if response.json().get("errcode") == 0:
            print("钉钉通知发送成功！")
        else:
            print(f"钉钉通知发送失败：{response.text}")
    except Exception as e:
        print(f"发送钉钉消息失败: {e}")

def read_fund_codes_from_file(file_path: str = "fund_codes.txt"):
    """
    从文件中读取基金代码
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # 读取所有行，去除空格和空行
            codes = [line.strip() for line in f if line.strip()]
            # 去重并保持顺序
            unique_codes = list(dict.fromkeys(codes))
            print(f"成功从文件读取 {len(unique_codes)} 个基金代码")
            return unique_codes
    except FileNotFoundError:
        print(f"错误：未找到文件 {file_path}，请确保文件存在")
        return []
    except Exception as e:
        print(f"读取文件失败: {e}")
        return []

if __name__ == '__main__':
    # 从文件读取基金代码
    fund_codes = read_fund_codes_from_file()
    
    if not fund_codes:
        print("未读取到有效的基金代码，程序退出")
        exit()

    total_content = "# 📊 基金净值实时更新\n"
    total_content += "> 数据来源：天天基金网 | 盘中估值仅供参考\n\n"

    for code in fund_codes:
        total_content += get_fund_net_worth(code)

    send_to_dingtalk(total_content)
    # print(total_content) # 调试用，正式运行可注释
