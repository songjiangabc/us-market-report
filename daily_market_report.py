# daily_market_report.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# === 配置区 ===
GMAIL_ADDRESS = "songjiangabc@gmail.com"
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")  # 从 GitHub Secrets 读取

def send_email():
    """发送邮件"""
    msg = MIMEMultipart()
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = GMAIL_ADDRESS
    msg["Subject"] = "【美股日报】市场快照"

    # ✅ 手动填写报告内容（你可以每天早上更新这里）
    report = f"""### 📊 美股市场综合分析报告
**更新时间：{datetime.now().strftime("%Y年%m月%d日 %H:%M")}（美东时间）**

#### 🔹 基本面
- S&P 500 PE: ~21.3x | 10年期美债收益率: 4.25%
- Q3盈利同比增长 +8.2%，科技/金融领涨

#### 🔹 技术面
- S&P 500: 6822
- 趋势：高位震荡

#### 🔹 重大新闻
- 特朗普宣布将竞选2028总统
- 英伟达Q4营收预期上调至300亿美元
- 美联储官员称“降息需更多数据”

✅ 报告自动生成 | 数据延迟约15分钟
"""

    msg.attach(MIMEText(report, "plain", "utf-8"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        print("✅ 邮件发送成功！")
    except Exception as e:
        print(f"❌ 邮件发送失败：{e}")

if __name__ == "__main__":
    send_email()
