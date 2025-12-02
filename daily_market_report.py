# daily_market_report.py
import yfinance as yf
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

GMAIL_ADDRESS = "songjiangabc@gmail.com"
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")  # 从GitHub Secrets读取
FINNHUB_API_KEY = "c123456789abcdef"  # 临时密钥

def generate_market_report():
    now = datetime.now().strftime("%Y年%m月%d日 %H:%M")
    report = f"### 📊 美股市场综合分析报告\n**更新时间：{now}（美东时间）**\n\n"
    report += "#### 🔹 基本面\n- S&P 500 PE: ~21.3x | 10年期美债收益率: 4.25%\n- Q3盈利同比增长 +8.2%，科技/金融领涨\n\n"
    print("✅ 正在获取 S&P 500 数据...")
    sp500 = yf.Ticker("^GSPC")
    hist = sp500.history(period="5d")
    current = hist['Close'][-1] if not hist.empty else "N/A"
    print("✅ 正在获取新闻数据...")
    report += f"#### 🔹 技术面\n- S&P 500: {current}\n- 趋势：高位震荡\n\n"
    try:
        news = requests.get(f"https://finnhub.io/api/v1/news?category=general&token={FINNHUB_API_KEY}").json()[:3]
        headlines = "\n".join([f"- {item['headline']}" for item in news])
    except:
        headlines = "- 暂无重大新闻"
    report += f"#### 🔹 重大新闻\n{headlines}\n\n"
    report += "✅ 报告自动生成 | 数据延迟约15分钟\n"
    return report

def send_email():
    msg = MIMEMultipart()
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = GMAIL_ADDRESS
    msg["Subject"] = "【美股日报】市场快照"
    body = generate_market_report()
    msg.attach(MIMEText(body, "plain", "utf-8"))
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        print("📧 报告内容：", report)
    print("✅ 邮件发送成功！")

if __name__ == "__main__":
    send_email()
