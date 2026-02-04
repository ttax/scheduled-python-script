import requests
import os  # 新增：导入os模块读取环境变量

# 从环境变量读取钉钉Webhook（替代硬编码）
DINGTALK_WEBHOOK = os.getenv("DINGTALK_WEBHOOK", "")
# 校验环境变量是否存在
if not DINGTALK_WEBHOOK:
    raise ValueError("环境变量 DINGTALK_WEBHOOK 未配置，请检查GitHub Secrets")

# 其余代码不变（read_fund_codes_from_file 函数可适配环境变量）
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

# 其余函数（get_fund_net_worth/get_fund_name/send_to_dingtalk）不变
