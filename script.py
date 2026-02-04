import requests

DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=bd1e007f5e46bafdc99021191b24da07fc0599cb270586d6442add65574b3b68"


def get_fund_net_worth(fund_code: str):
    url = f'https://m.dayfund.cn/ajs/ajaxdata.shtml?showtype=getfundvalue&fundcode={fund_code}'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    res.encoding = "gb2312"
    fund_info = res.text.split('|')

    def format_value(value):
        try:
            if '-' in value:
                return f'<font color="#00FF00">{value}</font>'  # 绿色：下跌
            else:
                return f'<font color="#FF0000">{value}</font>'  # 红色：上涨
        except:
            return value

    fund_name = get_fund_name(fund_code)
    net_worth_time = fund_info[0] if len(fund_info) > 0 else "未知时间"
    intraday_time = f"{fund_info[9]} {fund_info[10]}" if len(fund_info) > 10 else "未知时间"

    data = f"""
    ### 【{fund_code}】{fund_name}
    > **净值更新时间**：{net_worth_time}
    > **最新净值**：{fund_info[1] if len(fund_info) > 1 else "暂无"}
    > **涨跌金额**：{format_value(fund_info[3] if len(fund_info) > 3 else "暂无")}
    > **涨跌幅度**：{format_value(fund_info[4] if len(fund_info) > 4 else "暂无")}

    > **盘中更新时间**：{intraday_time}
    > **盘中预估净值**：{fund_info[7] if len(fund_info) > 7 else "暂无"}
    > **盘中涨跌金额**：{format_value(fund_info[6] if len(fund_info) > 6 else "暂无")}
    > **盘中涨跌幅度**：{format_value(fund_info[5] if len(fund_info) > 5 else "暂无")}
    ---
    """
    return data


def get_fund_name(fund_code: str):
    url = f"https://www.dayfund.cn/fundpre/{fund_code}.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
    }
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    try:
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
    response = requests.post(DINGTALK_WEBHOOK, json=data, headers=headers)
    if response.json().get("errcode") == 0:
        print("钉钉通知发送成功！")
    else:
        print(f"钉钉通知发送失败：{response.text}")


if __name__ == '__main__':
    fund_codes = ['018463', '011782', '025491', '025209', '161725', '015790', '023567', '002207']
    total_content = "# 📊 基金净值实时更新\n"
    total_content += "> 数据来源：天天基金网 | 盘中估值仅供参考\n\n"

    for code in fund_codes:
        total_content += get_fund_net_worth(code)

    send_to_dingtalk(total_content)
    print(total_content)
