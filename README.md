# 基金净值钉钉通知

定时从天天基金网获取基金净值，推送到钉钉群机器人。

## 功能
- 从 `fund_codes.txt` 读取基金代码
- 每天9:50-15:50定时推送（GitHub Actions）
- 支持手动触发推送
- 涨跌金额/幅度自动标红（涨）/绿（跌）

## 快速开始
### 1. 环境准备
```bash
# 克隆仓库
git clone https://github.com/你的用户名/你的仓库名.git
cd 你的仓库名

# 安装依赖
pip install requests
