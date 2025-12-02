# daily_market_report.py
import yfinance as yf
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# === 配置区 ===
GMAIL_ADDRESS = "songjiangabc@gmail.com"
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")  # 从 GitHub Secrets 读取
FINNHUB_API_KEY = "c123456789abcdef"  # 临时密钥（每天限100次请求）

def generate_market_report():
    """生成美股市场综合分析报告"""
    now = datetime.now().strftime("%Y年%m月%d日 %H:%M")
    report = f"### 📊 美股市场综合分析报告\n**更新时间：{now}（美东时间）**\n\n"
    
    # --- 基本面（静态数据）---
    report += "#### 🔹 基本面\n- S&P 500 PE: ~21.3x | 10年期美债收益率: 4.25%\n- Q3盈利同比增长 +8.2%，科技/金融领涨\n\n"

    # --- 技术面（动态数据）---
    try:
        print("✅ 正在获取 S&P 500 数据...")
        sp500 = yf.Ticker("^GSPC")
        hist = sp500.history(period="5d")
        print("📊 S&P 500 历史数据：\n", hist.head())  # 调试信息
        
        if not hist.empty:
            current = hist['Close'].iloc[-1]
            report += f"#### 🔹 技术面\n- S&P 500: {current:.0f}\n- 趋势：高位震荡\n\n"
        else:
            report += "#### 🔹 技术面\n- S&P 500: N/A（无数据）\n\n"
    except Exception as e:
        print(f"⚠️ 获取 S&P 500 数据失败：{e}")
        report += "#### 🔹 技术面\n- S&P 500: 获取失败\n\n"

    # --- 重大新闻（动态数据）---
    try:
        print("✅ 正在获取新闻数据...")
        response = requests.get(
            f"https://finnhub.io/api/v1/news?category=general&token={FINNHUB_API_KEY}"
        )
        print("📡 新闻 API 响应状态码：", response.status_code)  # 调试信息
        response.raise_for_status()  # 检查 HTTP 错误
        news_items = response.json()[:3]
        if news_items:
            headlines = "\n".join([f"- {item['headline']}" for item in news_items])
            report += f"#### 🔹 重大新闻\n{headlines}\n\n"
        else:
            report += "#### 🔹 重大新闻\n- 新闻列表为空\n\n"
    except Exception as e:
        print(f"⚠️ 获取新闻失败：{e}")
        report += "#### 🔹 重大新闻\n- 暂无重大新闻\n\n"

    report += "✅ 报告自动生成 | 数据延迟约15分钟\n"
    return report

def send_email():
    """发送邮件"""
    msg = MIMEMultipart()
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = GMAIL_ADDRESS
    msg["Subject"] = "【美股日报】市场快照"
    
    body = generate_market_report()
    msg.attach(MIMEText(body, "plain", "utf-8"))
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        print("✅ 邮件发送成功！")
    except Exception as e:
        print(f"❌ 邮件发送失败：{e}")

if __name__ == "__main__":
    # 生成报告并打印内容（用于调试）
    report = generate_market_report()
    print("📧 报告内容：\n", report)
    # 发送邮件
    send_email()
